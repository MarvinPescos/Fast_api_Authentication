from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.sql import func
from datetime import datetime
from app.core import Base
import enum

if TYPE_CHECKING:
    from app.users.models import User

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"
    FAILED = "failed"

class VerificationType(str, enum.Enum):
    EMAIL_REGISTRATION = "email_registration"
    EMAIL_CHANGE = "email_change"
    PASSWORD_RESET = "password_reset"

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    email: Mapped[str] = mapped_column(String(255)) 
    email_code: Mapped[Optional[str]] = mapped_column(
        String(6), nullable=True, 
        comment="6-digit code for email verification"
    )
    reset_token: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, 
        comment="32+ char secure token for password reset"
    )
    
    verification_type: Mapped[VerificationType] = mapped_column(
        Enum(VerificationType),
        default=VerificationType.EMAIL_REGISTRATION
    )
    status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus),
        default=VerificationStatus.PENDING
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="email_verifications")

    @property
    def current_code(self) -> Optional[str]:
        """Get the appropriate code/token based on verification type"""
        if self.verification_type == VerificationType.PASSWORD_RESET:
            return self.reset_token
        else:
            return self.email_code