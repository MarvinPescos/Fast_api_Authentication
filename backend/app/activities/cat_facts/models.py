from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Time
from typing import Optional, TYPE_CHECKING
from sqlalchemy.sql import func
from datetime import datetime, time
from app.core import Base

if TYPE_CHECKING:
    from app.users import User


class CatFactSubscription(Base):
    __tablename__ = "cat_fact_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Time preference in 24-hour format (e.g., "09:00:00")
    preferred_time: Mapped[time] = mapped_column(Time, default=time(9, 0, 0))

    # Timezone (e.g., "Asia/Manila", "UTC")
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")

    # Track when last email was sent
    last_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Track total emails sent
    total_sent: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to User
    user: Mapped["User"] = relationship("User", back_populates="cat_fact_subscription")
