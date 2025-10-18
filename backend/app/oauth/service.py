from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from typing import Optional, Dict, Tuple, Any
from urllib.parse import urlencode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

from app.core import settings , create_access_token, hash_password
from app.users import User, OAuthAccount, OAuthProvider

import structlog
import secrets
import httpx


logger = structlog.get_logger(__name__)

class BaseOAuthService(ABC):
    
    @abstractmethod
    def __init__(self):
        """Initialize provider-specific configuration"""
        pass

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Generate OAuth authorization URL"""
        pass
    
    @abstractmethod
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from provider"""
        pass

    def get_provider_type(self) -> OAuthProvider:
        """Return the provider type pass"""

    # main entry point

    async def authenticate_or_create_user(self, db: AsyncSession, user_data: Dict[str, any], token_data: Dict[str, any]) -> Tuple [User, str]:
        """
        Find existing user or create new one from OAuth data
        
        Args:
            db: Database Session
            user_data: User data from Oauth Provider
            token_data: token response from provider

        return:
            Tuple of (User, JWT Token)
        """

        provider_user_id = user_data.get("id")
        email = user_data.get("email")
        name = user_data.get("name", " ")
        picture_url = self._extract_picture_url(user_data)


        #check if oauth acc exist
        result = await db.execute(
            select(OAuthAccount).where(
                OAuthAccount.provider == self.get_provider_type(),
               OAuthAccount.provider_user_id == provider_user_id 
            )
        )

        oauth_account = result.scalar_one_or_none()

        # if true oauth acc update tokens
        if oauth_account:
            await self._update_oauth_account(oauth_account, token_data)
            await db.commit()
            user = await db.get(User, oauth_account.user_id)
            logger.info(f"Existing {self.get_provider_type().value} user logged in: {user.email}")

        # link or create through oauth
        else:    
            user = None

            if email:
                result = await db.execute(select(User).where(
                    User.email == email
                  )
                )
                user = result.scalar_one_or_none()
            
            # existing user just link oauth
            if user:
                logger.info(f"Linking {self.get_provider_type().value} to existing user: {user.email}")
                oauth_account = await self._create_ouath_account(
                    db, user.id, provider_user_id, email, name, picture_url, token_data
                )
            
            else: 
                user = await self._create_user_with_oauth(
                    db, provider_user_id, email, name, picture_url, token_data
                )
                logger.info(f"New {self.get_provider_type().value} user created: {user.email}")
        
        access_token = create_access_token({"sub": str(user.id)})
        return user, access_token

    # Helper methods

    def _extract_picture_url(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Extract picture URL"""
        picture = user_data.get("picture")
        if isinstance(picture, dict):
            return picture.get("data", {}).get("url")
        return picture

    async def _generate_unique_name(self, db: AsyncSession, prefix: str, identifier: str) -> str:
        """Generate unique username"""
        base_username = f"{prefix}_{identifier}"
        username = base_username
        counter = 1

        while True:
            result = await db.execute(
                select(User).where(User.username == username)
            )

            if not result.scalar_one_or_none():
                return username
            username = f"{username}_{counter}"
            counter+=1

    async def _create_ouath_account(self, db: AsyncSession,
                                   user_id: int, 
                                   provider_user_id: str, 
                                   email: Optional[str], 
                                   name: str, 
                                   picture_url: Optional[str], 
                                   token_data: Dict[str, Any]
                                   ) -> OAuthAccount:
        """Create OAuth account record"""

        oauth_account = OAuthAccount(
            user_id = user_id,
            provider = self.get_provider_type(),
            provider_user_id = provider_user_id,
            access_token = token_data.get("access_token"),
            refresh_token = token_data.get("refresh_token"),
            provider_email = email,
            provider_name = name,
            profile_picture_url=picture_url
        )

        db.add(oauth_account)
        await db.commit()
        return oauth_account

    async def _update_oauth_account(self, oauth_account: OAuthAccount, token_data: Dict[str, Any]):
        """Update Oauth account data (access_token, refresh token, token_expires)"""
        expires_in = token_data.get("expires_in", 3600)

        oauth_account.access_token = token_data.get("access_token")
        oauth_account.refresh_token = token_data.get("refresh_token")
        oauth_account.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        oauth_account.updated_at = datetime.now(timezone.utc)

    async def _create_user_with_oauth(self, db: AsyncSession,
                                      provider_user_id: str, 
                                      email: Optional[str], 
                                      name: str, 
                                      picture_url: Optional[str], 
                                      token_data: Dict[str, Any]) -> User:
        """ Create new user with Oauth Account"""
        provider_prefix = f"{self.get_provider_type().value[:2]}"
        username = await self._generate_unique_name(db, provider_prefix, provider_user_id)
        user_email = email or f"{provider_prefix}_{provider_user_id}@oauth.local"
    
        user = User(
            username=username,
            email=user_email,
            hashed_password=hash_password(secrets.token_urlsafe(32)),
            full_name = name or f"{self.get_provider_type().value.title()} User",
            is_active = True,
            is_email_verified = bool(email)    
        )

        db.add(user)
        await db.flush()

        await self._create_ouath_account(
            db, user.id, provider_user_id, email, name, picture_url, token_data
        )

        await db.commit()
        await db.refresh(user)
        return user


class FacebookOauthService(BaseOAuthService):
    """Facebook Oauth Implementation"""

    def __init__(self):
        self.client_id = settings.FACEBOOK_APP_ID
        self.client_secret = settings.FACEBOOK_APP_SECRET
        self.redirect_uri = settings.FACEBOOK_REDIRECT_URI

        self.auth_url = "https://www.facebook.com/v18.0/dialog/oauth"
        self.token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        self.user_info_url = "https://graph.facebook.com/v18.0/me" 

    def get_provider_type(self) -> OAuthProvider:
        return OAuthProvider.FACEBOOK
    
    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "public_profile",
            "response_type": "code",
            "state": state
        }

        return f"{self.auth_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": self.redirect_uri,
                        "code": code,
                    },
                    headers={"Accept" : "application/json"}
                )
            
                if response.status_code != 200:
                    logger.error(f"Facebook token exchange failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to exchange code for token"
                    )

                return response.json()

        except httpx.RequestError as e:    
            logger.error(f"Facebook API request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Facebook service temporarily unavailable"
            )
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.user_info_url,
                    params={
                        "fields": "id,name,email,picture.type(large)",
                        "access_token": access_token,
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Facebook user info failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to get user information"
                    )
                
                return response.json()
                
        except httpx.RequestError as e:
            logger.error(f"Facebook API request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Facebook service temporarily unavailable"
            )

class GoogleOAuthService(BaseOAuthService):
    """Google OAuth Implementation"""

    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    def get_provider_type(self) -> OAuthProvider:
        return OAuthProvider.GOOGLE
    
    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }

        return f"{self.auth_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": self.redirect_uri,
                        "code": code,
                        "grant_type": "authorization_code"
                    },
                    headers={"Accept": "application/json"}
                )
            
                if response.status_code != 200:
                    logger.error(f"Google token exchange failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to exchange code for token"
                    )

                return response.json()

        except httpx.RequestError as e:    
            logger.error(f"Google API request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google service temporarily unavailable"
            )
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.user_info_url,
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Google user info failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to get user information"
                    )
                
                return response.json()
                
        except httpx.RequestError as e:
            logger.error(f"Google API request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google service temporarily unavailable"
            )


google_oauth_service = GoogleOAuthService()
facebook_oauth_service = FacebookOauthService()



