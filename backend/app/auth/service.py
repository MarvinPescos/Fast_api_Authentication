from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from fastapi import HTTPException, status
import structlog
import os

from app.auth import LoginRequest, LoginResponse, ResetPasswordRequest, ForgetPasswordRequest
from app.email import send_verification_email
from app.users import User, UserCreate, UserResponse, UserUpdate
from app.core import hash_password, verify_password, create_access_token, PASSWORD_RESET
from app.email_verification import EmailVerification ,EmailVerificationService, RegistrationResponse, EmailVerificationResponse, EmailVerificationCode
from app.core import USER_REGISTRATION
from app.repositories import BaseRepository, UserRepository
from app.email.service import send_password_reset_email
from app.email_verification.models import VerificationStatus, VerificationType


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
                verification_code=verification.email_code,
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
                verification_code=verification.email_code,
                user_name=user.username
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
                logger.warning(f"Login failed - Invalid Password for user: {login_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            if not existing_user.is_active:
                logger.error(f"Login Failed - account not verified: {login_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is not verified. Please check you email"
                )
            
            # Check if 2FA is enabled
            if existing_user.two_factor_enabled:
                # Import here to avoid circular dependency
                from app.auth.two_factor import two_factor_service
                
                # If no TOTP code provided, indicate 2FA is required
                if not login_data.totp_code:
                    logger.info(f"2FA verification required for user: {login_data.email}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="2FA_REQUIRED"
                    )
                
                # Verify TOTP code
                if not two_factor_service.verify_totp(existing_user.two_factor_secret, login_data.totp_code):
                    logger.warning(f"Invalid 2FA code for user: {login_data.email}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid 2FA code"
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
    
    async def update_profile(self, user: User, profile_data) -> User:
        """
        Update user profile information including email and password.

        Args:
            user: Current user Object
            profile_data: ProfileUpdateRequest with optional fields

        Returns:
            User: Updated user object
            
        Raises:
            HTTPException: If validation fails or user already exists
        """
        try:
            # Track if we need to verify current password
            needs_password_verification = profile_data.email is not None or profile_data.new_password is not None
            
            # Verify current password if changing email or password
            if needs_password_verification:
                if not profile_data.current_password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Current password is required to change email or password"
                    )
                
                if not verify_password(profile_data.current_password, user.hashed_password):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Current password is incorrect"
                    )
            
            # Update username if provided
            if profile_data.username is not None and profile_data.username != user.username:
                # Check if username is already taken
                existing_user = await self.user_repo.get_user_by_username(profile_data.username)
                if existing_user and existing_user.id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )
                user.username = profile_data.username
            
            # Update email if provided
            if profile_data.email is not None and profile_data.email != user.email:
                # Check if email is already taken
                existing_user = await self.user_repo.get_user_by_email(profile_data.email)
                if existing_user and existing_user.id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already taken"
                    )
                user.email = profile_data.email
                user.is_email_verified = False  # Require re-verification
            
            # Update password if provided
            if profile_data.new_password is not None:
                user.hashed_password = hash_password(profile_data.new_password)
            
            # Update full name if provided
            if profile_data.full_name is not None:
                user.full_name = profile_data.full_name

            await self.db.commit()
            await self.db.refresh(user)

            logger.info(f"Profile updated successfully: {user.email}")
            return user
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity error updating profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )

    async def forget_password(self, payload: ForgetPasswordRequest):
        try:
            result = await self.db.execute(select(User).where(User.email == payload.email))
            user = result.scalar_one_or_none()

            if user:
                await self.db.execute(
                    update(EmailVerification).where(
                        EmailVerification.user_id == user.id,
                        EmailVerification.verification_type == VerificationType.PASSWORD_RESET,
                        EmailVerification.status == VerificationStatus.PENDING
                    ).values(status=VerificationStatus.EXPIRED)
                )

                await self.db.commit()

                verification = await EmailVerificationService.createVerification(
                    user_id = user.id,
                    email=user.email,
                    db=self.db,
                    verification_type=VerificationType.PASSWORD_RESET
                )

                frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
                reset_link = f"{frontend_url}/reset-password?code={verification.reset_token}"

                sent = await send_password_reset_email(
                    to_email=user.email,
                    reset_link=reset_link,
                    user_name=user.username,
                )

                if sent:
                    try:
                        PASSWORD_RESET.labels(status="issued").inc()
                    except NameError:
                        pass # (If you read this I got tired remove it if you want but if you want to make a custom error then go)

                return {"message": "If that email exist, we've sent a reset link"}

        except Exception as e:
            logger.error(f"Forget password error: {str(e)}")
            return {"message": "If that email exists, we've sent a reset link."}

    async def reset_password(self, payload: ResetPasswordRequest):
        try:
            
            result = await self.db.execute(
                select(EmailVerification).where(
                    EmailVerification.reset_token == payload.code,
                    EmailVerification.status == VerificationStatus.PENDING,
                    EmailVerification.verification_type == VerificationType.PASSWORD_RESET,
                    EmailVerification.expires_at > datetime.utcnow()
                )
            )

            verification = result.scalar_one_or_none()

            if not verification:
                try:
                    PASSWORD_RESET.labels(status="invalid").inc()
                except NameError:
                    ...
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset token"
                )
            
            user = await self.db.get(User, verification.user_id)

            if not user:
                try:
                    PASSWORD_RESET.labels(status="invalid").inc()
                except NameError:
                    ...
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user.hashed_password = hash_password(payload.new_password)

            verification.status = VerificationStatus.VERIFIED

            await self.db.commit()

            try:
                PASSWORD_RESET.labels(status="success").inc()
            except NameError:
                ...
            
            return {"message": "Successfully changed password"}

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to reset Password"
            )
    