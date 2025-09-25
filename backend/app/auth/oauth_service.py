# import httpx
# import secrets
# import structlog
# from typing import Optional, Dict, Any
# from fastapi import HTTPException, status
# from urllib.parse import urlencode

# from app.core import settings
# from app.users import User, UserCreate
# # Removed circular import - AuthService will import this instead
# from app.core import create_access_token

# logger = structlog.get_logger(__name__)

# class FacebookOAuthService:
#     """
#         Facebook 2.0 implementation following Meta's official flow
#     """

#     def __init__(self):
#         self.client_id = settings.FACEBOOK_CLIENT_ID
#         self.client_secret = settings.FACEBOOK_CLIENT_SECRET
#         self.redirect_uri = settings.FACEBOOK_REDIRECT_URI

#         self.auth_url = "https://www.facebook.com/v18.0/dialog/oauth"
#         self.token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
#         self.user_info_url = "https://graph.facebook.com/v18.0/me"
    
#     def get_authorization_url(self, state: str = None) -> str:
#         """
#         Generate Facebook OAuth authorization URL

#         Args:
#             state: CSRF protection token 

#         Returns:
#             Authorization URL for redirect
#         """
#         params = {
#             "client_id": self.client_id,
#             "redirect_uri": self.redirect_uri,
#             "scope": "public_profile",  # Only public_profile is always available
#             "response_type": "code",
#             "state": state,  # CSRF protection
#         }

#         return f"{self.auth_url}?{urlencode(params)}"

#     async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
#         """
#         Exchange authorization code for access token
        
#         Args:
#             code: Authorization code from Facebook
            
#         Returns:
#             Token response from Facebook
            
#         Raises:
#             HTTPException: If token exchange fails
#         """
#         try:
#             async with httpx.AsyncClient() as client:
#                 response = await client.post(
#                     self.token_url,
#                     data={
#                         "client_id": self.client_id,
#                         "client_secret": self.client_secret,
#                         "redirect_uri": self.redirect_uri,
#                         "code": code,
#                     },
#                     headers={"Accept": "application/json"}
#                 )
                
#                 if response.status_code != 200:
#                     logger.error(f"Facebook token exchange failed: {response.text}")
#                     raise HTTPException(
#                         status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="Failed to exchange code for token"
#                     )
                
#                 return response.json()
                
#         except httpx.RequestError as e:
#             logger.error(f"Facebook API request failed: {str(e)}")
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Facebook service temporarily unavailable"
#             )
    
#     async def get_user_info(self, access_token: str) -> Dict[str, Any]:
#         """
#         Get user information from Facebook Graph API
        
#         Args:
#             access_token: Facebook access token
            
#         Returns:
#             User information from Facebook
#         """
#         try:
#             async with httpx.AsyncClient() as client:
#                 response = await client.get(
#                     self.user_info_url,
#                     params={
#                         "fields": "id,name,picture.type(large)",  # Removed email field
#                         "access_token": access_token,
#                     }
#                 )
                
#                 if response.status_code != 200:
#                     logger.error(f"Facebook user info request failed: {response.text}")
#                     raise HTTPException(
#                         status_code=status.HTTP_400_BAD_REQUEST,
#                         detail="Failed to get user information"
#                     )
                
#                 return response.json()
                
#         except httpx.RequestError as e:
#             logger.error(f"Facebook API request failed: {str(e)}")
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Facebook service temporarily unavailable"
#             )
    
#     async def authenticate_or_create_user(
#         self, 
#         facebook_user: Dict[str, Any], 
#         auth_service
#     ) -> tuple[User, str]:
#         """
#         Find existing user or create new one from Facebook data
        
#         Args:
#             facebook_user: User data from Facebook
#             auth_service: Auth service instance
            
#         Returns:
#             Tuple of (User, JWT token)
#         """
#         try:
#             email = facebook_user.get("email")  # May be None
#             facebook_id = facebook_user.get("id")
#             name = facebook_user.get("name", "")
            
#             # Try to find existing user by email (if available)
#             existing_user = None
#             if email:
#                 existing_user = await auth_service.user_repo.get_by_email(email)
            
#             if existing_user:
#                 # Update Facebook ID if not set
#                 if not hasattr(existing_user, 'facebook_id') or not existing_user.facebook_id:
#                     # You'd need to add facebook_id column to User model
#                     pass
                
#                 user = existing_user
#             else:
#                 # Create new user from Facebook data
#                 # Generate a secure random password since they're using OAuth
#                 import secrets
#                 random_password = secrets.token_urlsafe(32)
                
#                 # Use a placeholder email if not provided
#                 user_email = email or f"fb_{facebook_id}@facebook.local"
                
#                 user_data = UserCreate(
#                     username=f"fb_{facebook_id}",  # Unique username
#                     email=user_email,
#                     password=random_password,  # They won't use this
#                     full_name=name or f"Facebook User {facebook_id}"
#                 )
                
#                 # Create user but mark as verified since Facebook verified the identity
#                 from app.core import hash_password
#                 user = await auth_service.user_repo.create(
#                     username=user_data.username,
#                     email=user_data.email,
#                     hashed_password=hash_password(user_data.password),
#                     full_name=user_data.full_name,
#                     is_active=True,  # Facebook users are immediately active
#                     is_email_verified=bool(email),  # Only if we actually got email
#                     # facebook_id=facebook_id,  # Add this field to User model
#                 )
            
#             # Generate JWT token
#             token = create_access_token({"sub": str(user.id)})
            
#             logger.info(f"Facebook OAuth successful for user: {user.email}")
#             return user, token
            
#         except Exception as e:
#             logger.error(f"Facebook authentication failed: {str(e)}")
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Authentication failed"
#             )


# # Singleton instance
# facebook_oauth = FacebookOAuthService()