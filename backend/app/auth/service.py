from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
import structlog

from app.auth import LoginRequest, LoginResponse
from app.email import send_verification_email
from app.users import User, UserCreate, UserResponse, UserUpdate
from app.core import hash_password, verify_password, create_access_token
from app.email import send_verification_email
from app.email_verification import EmailVerificationService, RegistrationResponse, EmailVerificationResponse, EmailVerificationCode
from app.core import USER_REGISTRATION
from app.repositories import BaseRepository, UserRepository

logger = structlog.get_logger(__name__)

class AuthService:
    """
        Service layer for authentication business logic
    """

    def __init__ (self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register_user(self, user_data: UserCreate) -> RegistrationResponse:
        """ 
        Register a new user account and send verification email.
        
        Business logic:
        1. Check if user already exists
        2. Hash password
        3. Create user record
        4. Generate email verification
        5. Send verification email
        
        Args:
            user_data: User registration data
            
        Returns:
            RegistrationResponse: Success message and next steps
            
        Raises:
            HTTPException: If user already exists or system error

        """
        try:
            logger.info("user_registration_started", email=user_data.email)

            if await self.user_repo.exists(email=user_data.email):
                logger.error("Registration failed - user already exists", email=user_data.email)
                USER_REGISTRATION.labels(status="duplicate").inc()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists"
                )
            
            hashed_password = hash_password(user_data.password)

            user = await self.user_repo.create(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
                is_active=False,
                is_email_verified=False,
            )

            # Fallback check - ensure user creation was successful
            if not user:
                logger.error("user_creation_failed", email=user_data.email)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user account"
                )

            verification = await EmailVerificationService.createVerification(
                user_id=user.id,
                email=user.email,
                db=self.db
            )

            email_sent = await send_verification_email(
                to_email=user.email,
                verification_code=verification.code,
                user_name=user.username
            )
            

            if not email_sent:
                logger.warning(f"failed to send email verification to: {user.email}")    

            logger.info("user_registration_success - verification send",
                        user_id=user.id, email=user.email)
            USER_REGISTRATION.labels(status="success").inc()

            return RegistrationResponse(
                success=True,
                message="Registration successful! Please check your email to verify your account",
                user_id=user.id,
                next_step="Verify email"
            )

        except HTTPException:
            raise
        except IntegrityError as e:
            logger.error("registration_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Registration failed due to data conflict"
            )
        except Exception as e:
            logger.error("registration_unexpected_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed"
            )
            
    async def verify_email(self, verification_data: EmailVerificationCode) -> EmailVerificationResponse:
        """
        Verify user email with verification code.
        
        Args:
            user_id: ID of user to verify
            code: 6-digit verification code
            
        Returns:
            EmailVerificationResponse: Success/failure message
            
        """

        logger.info(f"Attempting email verification for user: {verification_data.user_id}")

        try:
            success, message = await EmailVerificationService.verify_code(
                user_id=verification_data.user_id,
                code=verification_data.code,
                db=self.db
            )
            
            if not success:
                logger.warning(f"Email verificaiton failed for user: {verification_data.user_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
            
            logger.info(f"Email Verification successful for user: {verification_data.user_id}")
            return EmailVerificationResponse(
                success=True,
                message=message,
                user_id=verification_data.user_id,
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during email verification: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Email verifcation failed"
            )
        
    async def resend_verification(self, user_id: int) -> EmailVerificationResponse:
        """
        Resend verification code to user's email.

        Args:
            user_id: ID of user requesting resend

        Returns: 
            EmailVerificationResponse: Success/Failure Message
        """
        logger.info(f"Resend verification requested for user {user_id}")

        try: 
            user = await self.db.get(User, user_id)

            if not user:
                logger.error(f"User {user_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User id not found"
                )

            if user.is_email_verified:
                logger.info(f"Email already verified for user {user_id}")
                return EmailVerificationResponse(
                    success=True,
                    message="Email is already verified",
                    user_id=user_id
                )

            verification = await EmailVerificationService.createVerification(
                user_id=user_id,
                email=user.email,
                db=self.db
            )             

            email_sent = await send_verification_email(
                to_email=user.email,
                verification_code=verification.code,
                user_name=user.user_name
            )

            if not email_sent:
                logger.warning(f"Failed to send email to: {user.email}")

            logger.info(f"Verification succesfully send to user: {user.email}")

            return EmailVerificationResponse(
                success=True,
                message="Verification code re sent to your email"
            )
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during resending email verification: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend email verification"
            )
        
    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """
            Login User account

            Args: login_data: user credential (email and password)

            Returns:
                LoginResponse: user_id and message

             Raises:
                validation fails
        """
        logger.info(f"Attempting to login user: {login_data.email}")

        try:
            existing_user = await self.user_repo.get_by_email(login_data.email)

            if not existing_user:
                logger.warning(f"Login Failed user doesn't exist: {login_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            if not verify_password(login_data.password, existing_user.hashed_password):
                logger.warning(f"Login failed - Invalid Password:  {login_data.password}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Password"
                )
            
            if not existing_user.is_active:
                logger.error(f"Login Failed - account not verified: {login_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is not verified. Please check you email"
                )
                 
            token = create_access_token({
                "sub" : str(existing_user.id)
            })

            logger.info(f"User login successfully: {existing_user.email}")
            return existing_user, token
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed due to system error"
            )

    async def update_user(self, user: User, user_data: UserUpdate) -> User:
        """
        Update user information.

        Args:
            user: Current user Object
            user_data: Updated user data

        Returns:
            User: Updated user object
        """
        try:
            # Update user fields
            user.username = user_data.username
            user.full_name = user_data.full_name

            await self.db.commit()
            await self.db.refresh(user)

            logger.info(f"User updated successfully: {user.email}")
            return user
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
    