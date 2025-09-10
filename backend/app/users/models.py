from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum
from typing import Optional, List
from sqlalchemy.sql import func
from datetime import datetime
from app.core import settings
import enum

class Base(DeclarativeBase):
    pass

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"
    FAILED = "failed"

class VerificationType(str, enum.Enum):
    EMAIL_REGISTRATION = "email_registration"
    EMAIL_CHANGE = "email_change"
    PASSWORD_RESET = "password_reset" 
    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), )
    full_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String(50), default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    email_verifications:Mapped[List["EmailVerification"]] = relationship(
        "EmailVerification",
        back_populates="user",
        order_by="EmailVerification.created_at.desc()"
    )

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    email: Mapped[str] = mapped_column(String(255))  # No unique constraint - allow multiple records
    
    # Industry standard: Separate columns for different security patterns
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

    user: Mapped[User] = relationship("User", back_populates="email_verifications")

    @property
    def current_code(self) -> Optional[str]:
        """Get the appropriate code/token based on verification type"""
        if self.verification_type == VerificationType.PASSWORD_RESET:
            return self.reset_token
        else:
            return self.email_code












