from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional


class CatFactSubscriptionCreate(BaseModel):
    """Schema for creating a cat fact subscription"""
    preferred_time: Optional[time] = Field(default=time(9, 0, 0), description="Preferred time for daily cat fact (24-hour format)")
    timezone: Optional[str] = Field(default="UTC", description="Timezone")


class CatFactSubscriptionUpdate(BaseModel):
    """Schema for updating subscription preferences"""
    is_active: Optional[bool] = None
    preferred_time: Optional[time] = None
    timezone: Optional[str] = None


class CatFactSubscriptionResponse(BaseModel):
    """Schema for subscription status response"""
    id: int
    user_id: int
    is_active: bool
    preferred_time: time
    timezone: str
    last_sent_at: Optional[datetime]
    total_sent: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class SubscriptionStatusResponse(BaseModel):
    """Schema for checking subscription status"""
    subscribed: bool
    subscription: Optional[CatFactSubscriptionResponse] = None
    message: str = Field(default="", description="Status message")


class SubscribeResponse(BaseModel):
    """Schema for subscribe action response"""
    success: bool
    message: str
    subscription: CatFactSubscriptionResponse
    next_send: Optional[str] = Field(default=None, description="Next scheduled send time")


class UnsubscribeResponse(BaseModel):
    """Schema for unsubscribe action response"""
    success: bool
    message: str
    unsubscribed_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of unsubscription")


class SendDailyRequest(BaseModel):
    """Schema for triggering daily send (GitHub Actions)"""
    api_key: str = Field(..., description="API key for authentication")


class SendDailyResponse(BaseModel):
    """Schema for daily send response"""
    success: bool
    message: str
    sent_count: int
    failed_count: int
    total_subscribers: int = Field(default=0, description="Total active subscribers")
    execution_time: Optional[str] = Field(default=None, description="Time taken to send emails")
    details: Optional[list] = None


class CatFactResponse(BaseModel):
    """Schema for a single cat fact"""
    fact: str
    source: str  # 'api' or 'fallback'
    length: int = Field(default=0, description="Length of the fact in characters")
    fetched_at: datetime = Field(default_factory=datetime.utcnow, description="When the fact was fetched")
