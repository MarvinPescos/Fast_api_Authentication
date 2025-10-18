from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.sql import func
from datetime import datetime
from app.core import Base
import enum

if (TYPE_CHECKING):
    from app.email_verification.models import EmailVerification
    from app.activities.cat_facts.models import CatFactSubscription

class OAuthProvider(str, enum.Enum):
    FACEBOOK = "facebook"
    GOOGLE = "google"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), )
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    role: Mapped[str] = mapped_column(String(50), default="user")
    
    # Two-Factor Authentication fields
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    two_factor_secret: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    email_verifications:Mapped[List["EmailVerification"]] = relationship(
        "EmailVerification",
        back_populates="user",
        order_by="EmailVerification.created_at.desc()"
    )

    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        "OAuthAccount",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    cat_fact_subscription: Mapped[Optional["CatFactSubscription"]] = relationship(
        "CatFactSubscription",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    provider: Mapped[OAuthProvider] = mapped_column(Enum(OAuthProvider))
    provider_user_id: Mapped[str] = mapped_column(String(255))  # Their ID on Facebook/Google

    # Tokens (you should encrypt these!)
    access_token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    provider_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="oauth_accounts")
