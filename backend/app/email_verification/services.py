from datetime import datetime, timedelta
from sqlalchemy import update, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import secrets
import string
import logging

from app.users import User
from app.email_verification.models import EmailVerification, VerificationStatus, VerificationType
from app.core import settings

logger = logging.getLogger(__name__)

class EmailVerificationService:
    """Service for handling email verification logic"""

    @staticmethod
    async def generate_reset_token() -> str:
         return secrets.token_urlsafe(32)

    @staticmethod
    async def generate_code() -> str:
        """Generate a 6-digit verification code"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))
    
    @staticmethod
    async def createVerification(
        user_id: int,
        email: str,
        db: AsyncSession,
        verification_type: VerificationType = VerificationType.EMAIL_REGISTRATION
    ) -> EmailVerification:
        """
            Create a new email verification request

            Args:
                user_id: User id of the user who requested
                email: Email address to verify
                db: Database Session
                verification_type: Type of verification (email registration, email change, etc)

            returns:
                EmailVerification: The created verification 
        """
        try:
            #Invalidate any existing pending for verification this user
            await db.execute(
                update(EmailVerification).where(
                    EmailVerification.user_id == user_id,
                    EmailVerification.status == VerificationStatus.PENDING
                ).values(status=VerificationStatus.EXPIRED)
            )

            logger.info("Attempting to create verification")

            # Create verification with appropriate field based on type
            if verification_type == VerificationType.PASSWORD_RESET:
                reset_token = await EmailVerificationService.generate_reset_token()
                verification = EmailVerification(
                    user_id=user_id,
                    email=email,
                    reset_token=reset_token,
                    verification_type=verification_type,
                    expires_at=datetime.utcnow() + timedelta(
                        minutes=settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
                    )
                )
            else:
                # Email verification (6-digit code)
                email_code = await EmailVerificationService.generate_code()
                verification = EmailVerification(
                    user_id=user_id,
                    email=email,
                    email_code=email_code,
                    verification_type=verification_type,
                    expires_at=datetime.utcnow() + timedelta(
                        minutes=settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
                    )
                )

            logger.info("Successfully created verification for this user")

            db.add(verification)
            await db.commit()
            await db.refresh(verification)
            
            return verification

        except Exception as e:
            logger.error(f"Failed to create verification for  user {user_id}: {str(e)}")
            await db.rollback()
            raise


    @staticmethod
    async def get_active_verification(
            user_id: int,
            db: AsyncSession,
        ) -> Optional[EmailVerification]:
            """ Get active (none-expired, pending) verification for user"""
            result = await db.execute(
                select(EmailVerification).where(
                    EmailVerification.user_id == user_id,
                    EmailVerification.expires_at > datetime.utcnow()
                ).order_by(EmailVerification.created_at.desc())
            )

            return result.scalar_one_or_none()
        
    @staticmethod
    async def verify_code(
            user_id: int,
            code: str,
            db: AsyncSession
        ) -> tuple[bool, str]:
            """ 
                Verify the provided code

                Return:
                    tuple: (success: bool, message: str)        
            """
            try:
                verification = await EmailVerificationService.get_active_verification(user_id, db)

                logger.info("Attempting to verify verification code input by user")

                if not verification:
                    return False, "No active verification found or expired code"
                
                # For email verification, check email_code
                if not verification.email_code or verification.email_code != code:
                    return False, "Invalid verification code"
                
                verification.status = VerificationStatus.VERIFIED
                verification.verified_at = datetime.utcnow()

                user = await db.get(User, user_id)
                if user:
                    user.is_active = True
                    user.is_email_verified = True

                await db.commit()
                logger.info(f"Email verification successful for user {user_id}")
                return True, "Email verified successfully"
            except Exception as e:
                 logger.error(f"Email verification failed for user {user_id}: {str(e)}")
                 await db.rollback()
                 return False, "Verification failed due to system error"
                 
    @staticmethod
    async def cleanup_expired_verifications(db:AsyncSession) -> dict :
         """Background task clean up expired verifications"""
         try:
            result = await db.execute(
                    update(EmailVerification).where(
                        EmailVerification.status == VerificationStatus.PENDING,
                        EmailVerification.expires_at < datetime.utcnow()
                    ).values(
                        status=VerificationStatus.EXPIRED,
                        updated_at=datetime.utcnow()
                    )
                    )
            
            await db.commit()
            count = result.rowcount

            logger.info(f"Cleaned up {count} expired email verification")

            return {
                "success": True,
                "cleaned_count": count,
                "timestamp": datetime.utcnow().isoformat()
            }
         except Exception as e:
              logger.error(f"Failed to cleanup expired verification {str(e)}")
              await db.rollback()
              return{
                "success": False,
                "error": {str(e)},
                "cleaned_count": 0,
              }
         
    
    @staticmethod
    async def verify_pasword_reset_code(user_id: int, code: str, db: AsyncSession) -> tuple[bool, str]:
         """
            Validatre a password reset code: Pending, not expired, matches.
            On success: mark VERIFIED and return (True, "OK").
         """
         try:
              verification = await EmailVerificationService.get_active_verification(user_id, db)
              if not verification:
                   return False, "No active reset found or expired"
              if verification.verification_type != VerificationType.PASSWORD_RESET:
                   return False, "Invalid verification type"
              # For password reset, check reset_token
              if not verification.reset_token or verification.reset_token != code:
                   return False, "Invalid reset code"
              
              verification.status = VerificationStatus.VERIFIED
              verification.verified_at = datetime.utcnow()

              await db.commit()
              return True, "OK"
         except Exception as e:
              await db.rollback()
              return False, "Reset verification failed"
              




