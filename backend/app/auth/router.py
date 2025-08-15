from fastapi import APIRouter , status, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Annotated
import logging

from app.core import USER_REGISTRATION, EMAIL_VERIFICATIONS
from app.email import send_verification_email
from app.auth import LoginResponse, LoginRequest, get_current_user
from app.users import User, UserCreate, UserResponse, UserUpdate
from app.core import limiter, hash_password, get_db, verify_password, resend_verification_limiter, create_access_token
from app.email_verification import EmailVerificationService, RegistrationResponse, EmailVerificationCode, EmailVerificationResponse


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new user account and send verification"
)
@limiter.limit("5/minute")
async def register (
    request: Request,
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> RegistrationResponse :
    """
    Register a new account and send email verification

    Args:
        request: Request for rate limiting
        user_data: User registration data
        db: Database session

    Returns:
        RegistrationResponse: Success message and next step

    Raise:
        If user already exist or validation fails
    """

    try:

        logger.info(f"Attempting to register user: {user_data.email}")
        
        result = await db.execute(
            select(User).where(
                user_data.email == User.email
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.error(f"Registration failed - user {user_data.email} already exist")

            USER_REGISTRATION.labels(status="duplicate").inc()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exist"
            )
        
        hashed_password = hash_password(user_data.password)

        user = User(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hashed_password,
            full_name = user_data.full_name,
            is_active = False,
            is_email_verified = False,
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        #create a verification for this user
        verification = await EmailVerificationService.createVerification(
            user_id=user.id,
            email=user.email,
            db=db
        )

        email_sent = send_verification_email(
            to_email = user.email,
            verification_code=verification.code,
            user_name=user.username,
        )

        if not email_sent:
            logger.error(f"Failed to send verification code to {user.email}")

        logger.info(f"User registered successfully , verification send: {user.email}")

        USER_REGISTRATION.labels(status="success").inc()

        return RegistrationResponse(
            success=True,
            message="Registration successful! Please check your email to verify your account",
            user_id=user.id,
            next_step="Verify email"
        )
    
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Database Integrity error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Internal server error"
        ) 
    
@router.post(
    "/verify-email",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
    description="Verify email address with 6-digit code"
)
async def verify_email(
    request:Request,
    verification_data: EmailVerificationCode,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> EmailVerificationResponse:
    """
    Verify Email address using 6-digit code

    Activate the user account upon successfull veriifdcation

    Args:
        veriifcation_data: userId and code

    Returns:
        Success/failure message

    Raises:
        HTTPException: If verification fails
    """

    logger.info(f"Attempting to email verification for user: {verification_data.user_id}")

    try:
        success, message = await EmailVerificationService.verify_code(
            user_id=verification_data.user_id,
            code=verification_data.code,
            db=db,
        )

        if not success:
            logger.warning(f"Email verifcation failed for user:{verification_data.user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        else:
            logger.info(f"Email verification successful for user: {verification_data.user_id}")
            return EmailVerificationResponse(
                success=True,
                message=message,
                user_id=verification_data.user_id
            )

    except Exception as e:    
        logger.error(f"Error during email verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification code"
        )
    
@router.post(
    "/resend-verification",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
    description="Resend verification code in email"
)
@resend_verification_limiter #limit it to 5 per hour lol
async def resend_verification(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> EmailVerificationResponse:
    """
    Resend verification code to user's email

    Args:
        user_id: UserID of the user requesting resend
        db: Database session

    Returns:
        Success/Failed message

    Raises:
        HTTPException: if user not found or rate limited
    """

    logger.info(f"Resend verification requested for user {user_id}")

    try:
        user = await db.get(User, user_id)
        if not user:
            logger.error(f"User id {user_id} was not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User was not found"
            )
        
        if  user.is_email_verified:
            logger.info(f"Email was already verified")
            return EmailVerificationResponse(
                success=True,
                message="Email is already verified",
                user_id=user_id
            )
        
        verification = await EmailVerificationService.createVerification(
            user_id=user.id,
            email=user.email,
            db=db
        )

        email_sent = await send_verification_email(
            to_email=user.email,
            verification_code=verification.code,
            user_name=user.username,
        )

        if not email_sent:
            logger.error(f"Failed to resend verification email: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend verification email"
            )
        
        logger.info(f"Verification resent successfully for user: {user.email}")

        return EmailVerificationResponse(
            success=True,
            message="Verification code sent to your email",
            user_id=user.id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errror resending verification code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend verification"
        )
    
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description="Login User",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LoginResponse:
    """
    Login User account

    Args: login_data: user credential (email and password)

    Returns:
        LoginResponse: user_id and message

    Raises:
        validation fails
    
    """
    logger.info(f"Attempting to login")

    try:
        result = await db.execute(
            select(User).where(
                login_data.email == User.email
            )
        )

        exisiting_user = result.scalar_one_or_none()

        if not exisiting_user:
            logger.error(f"Login failed - user doesnt exist: {login_data.email}")
            raise HTTPException (
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(login_data.password, exisiting_user.hashed_password):
            logger.error("Login failed - Invalid password.")
            raise HTTPException (
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        if not exisiting_user.is_active:
            logger.error(f"Login Failed - Account not verified: {login_data.email}")
            raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account not verified. Please check your email and verify your account"
            )
        
        token = create_access_token({
            "sub": str(exisiting_user.id)
        })

        logger.info(f"User login successfully: {exisiting_user.email}")

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax"
        )

        return LoginResponse(
            user=UserResponse.model_validate(exisiting_user, from_attributes=True),
            message="Login succesfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Clear authentication cookie and logout user"
)
async def logout(response: Response):
    """
    Logout user by clearing the HTTP-only auth cookie

    Args:
        response: fastApi response object to modify cookies

    return:
        dict: success message
    """
    response.delete_cookie(
      key="access_token",
      httponly=True,
      secure=True,
      samesite="lax"
    )

    return {"message" : "Succussfully logged out"}

@router.get(
    "/me",
    response_model=UserResponse
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    
    """Get current user information"""
    return UserResponse.model_validate(current_user, from_attributes=True)

@router.put(
    "/me",
    response_model=UserResponse
)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """update current user - Protected route"""
    # Update logic here
    current_user.username = user_data.username
    current_user.full_name = user_data.full_name
    await db.commit()
    return UserResponse.model_validate(current_user, from_attributes=True)




        








    

