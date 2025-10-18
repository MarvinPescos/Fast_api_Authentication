import secrets
from fastapi import APIRouter, Query, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.auth.dependencies import get_auth_service
from app.core import settings, oauth_state_manager
from app.oauth import facebook_oauth_service, google_oauth_service
from app.auth import AuthService

router = APIRouter()

@router.get(
    "/facebook/login",
    status_code=status.HTTP_200_OK,
    description="Facebook login buton"
    )
async def facebook_login():
    """User click 'Login with Facebook ' button """

    state = await oauth_state_manager.create_state()

    auth_url = facebook_oauth_service.get_authorization_url(state)
    if not auth_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server Error"
        )
    return {"authorization_url": auth_url}

@router.get(
    "/facebook/callback",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Callback"
)
async def facebook_callback(
    code: str = Query(...),
    state: str = Query(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Facebook Redirects here after user authorizes"""

    if not await oauth_state_manager.validate_state(state):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired Oauth state"
        )

    token_data = await facebook_oauth_service.exchange_code_for_token(code)
    facebook_user = await facebook_oauth_service.get_user_info(token_data["access_token"])
    user, jwt_token = await facebook_oauth_service.authenticate_or_create_user(
        auth_service.db, facebook_user, token_data
    )
    
   
    redirect_response = RedirectResponse(
        url=f"{settings.FRONTEND_URL}/dashboard?login=success"
    )
    
  
    redirect_response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,  
        samesite="none", 
        max_age=3600 * 24,
        domain=None  
    )
    
    return redirect_response


@router.get(
    "/google/login",
    status_code=status.HTTP_200_OK,
    description="Google login button"
)
async def google_login():
    """User click 'Login with Google' button"""

    state = await oauth_state_manager.create_state()

    auth_url = google_oauth_service.get_authorization_url(state)
    if not auth_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server Error"
        )
    return {"authorization_url": auth_url}


@router.get(
    "/google/callback",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description="Callback"
)
async def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Google redirects here after user authorizes"""

    if not await oauth_state_manager.validate_state(state):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired Oauth state"
        )

    token_data = await google_oauth_service.exchange_code_for_token(code)
    google_user = await google_oauth_service.get_user_info(token_data["access_token"])
    user, jwt_token = await google_oauth_service.authenticate_or_create_user(
        auth_service.db, google_user, token_data
    )
    
    redirect_response = RedirectResponse(
        url=f"{settings.FRONTEND_URL}/dashboard?login=success"
    )
    
    redirect_response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,  
        samesite="none", 
        max_age=3600 * 24,
        domain=None  
    )
    
    return redirect_response
