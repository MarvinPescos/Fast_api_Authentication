from fastapi import APIRouter , status, Depends, HTTPException, Response, Request

from app.auth import LoginResponse, LoginRequest
from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.service import AuthService
from app.users import User, UserCreate, UserResponse, UserUpdate
from app.core import limiter, resend_verification_limiter
from app.email_verification import RegistrationResponse, EmailVerificationResponse, EmailVerificationCode
from app.auth.schemas import ForgetPasswordRequest, ResetPasswordRequest

router = APIRouter()

@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new user account and send verification"
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserCreate,  
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register new user"""
    return await auth_service.register_user(user_data)



@router.post(
    "/verify-email",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
    description="Verify email address with 6-digit code"
)
async def verify_email(
    request: Request,
    verification_data: EmailVerificationCode,
    auth_service: AuthService = Depends(get_auth_service)
):
    """verify email address using 6 digit code"""
    return await auth_service.verify_email(verification_data)



@router.post(
    "/resend-verification",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
    description="Resend verification code in email"
)
@resend_verification_limiter
async def resend_verification(
    request: Request,
    user_id: int,
    auth_service: AuthService = Depends(get_auth_service)
):
    """resend verification to email that requested"""
    return await auth_service.resend_verification(user_id)



@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description="Login user"
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login user account"""
    user, token = await auth_service.login(login_data)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return LoginResponse(
        user=UserResponse.model_validate(user, from_attributes=True),
        message="Login successful"
    )



@router.put(
    "/update-user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    description="Update users username or fullname"
)
async def user_update(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Update user data (username || fullname)"""
    updated_user = await auth_service.update_user(current_user, user_data)
    return UserResponse.model_validate(updated_user, from_attributes=True)



@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Logout user"
)
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {"message": "Successfully logout"}

@router.post(
    "/password/forget",
    status_code=status.HTTP_200_OK,
    description="Request password reset email"
)
@limiter.limit("5/minute")
async def forget_password(
    request: Request,
    payload: ForgetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):   
    """Request password reset email"""
    return await auth_service.forget_password(payload)


@router.post(
    "/password/reset",
    status_code=status.HTTP_200_OK,
    description="Reset password with verification code"
)
@limiter.limit("10/hour")
async def reset_password(
    request: Request,
    payload: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password using verification code"""
    return await auth_service.reset_password(payload)


