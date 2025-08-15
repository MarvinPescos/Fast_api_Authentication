from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class EmailVerifications(BaseModel):
    """Schema for requesting email verification"""
    email: EmailStr = Field (..., description="Email address to verify")

class EmailVerificationCode(BaseModel):
    """Schema for submiting verification code"""
    user_id: int = Field(..., description="User ID", gt=0)
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")

class ResendVerification(BaseModel):
    """Schema for resend verification"""
    user_id:int = Field(..., description="User ID" ,gt=0)

class EmailVerificationResponse(BaseModel):
    """Schema for verification response"""
    success: bool = Field(..., description="Whether the operation was successfull")
    message: str = Field(..., description="Response message")
    user_id: Optional[int] = Field(None, description="User ID if registration was successfull")

class RegistrationResponse(BaseModel):
    """Schema for registration response (no token, token only when verified)"""
    success: bool = Field(..., description="Whether the operation was successfull")
    message: str = Field(..., description="Response message")
    user_id: Optional[int] = Field(None, description="User ID if registration was successfull")
    next_step: str = Field(..., description="What the user should do next")
