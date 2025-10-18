from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

class UserRole(str, Enum):
    USER="user"
    ADMIN="admin"
    MODERATOR="moderator"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="user username")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password")
    full_name: Optional[str] = Field(None, max_length=100,description="User fullname")

    @validator('username')
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
           raise ValueError("Username must be alphanumeric")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v
        
    @validator('password')
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password must have at least 1 number")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must have at least 1 uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must have at least 1 lowercase letter")
        return v
        
class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50 )
    email: EmailStr = None
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)

class ProfileUpdateRequest(BaseModel):
    """Schema for updating user profile - all fields optional"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username (alphanumeric only)")
    email: Optional[EmailStr] = Field(None, description="Email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    current_password: Optional[str] = Field(None, description="Current password (required for email/password change)")
    new_password: Optional[str] = Field(None, min_length=8, description="New password")
    
    @validator('username')
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.isalnum():
                raise ValueError("Username must be alphanumeric")
            if len(v) < 3:
                raise ValueError("Username must be at least 3 characters long")
        return v
        
    @validator('new_password')
    def validate_new_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not re.search(r"\d", v):
                raise ValueError("Password must have at least 1 number")
            if not re.search(r"[A-Z]", v):
                raise ValueError("Password must have at least 1 uppercase letter")
            if not re.search(r"[a-z]", v):
                raise ValueError("Password must have at least 1 lowercase letter")
        return v

class UserResponse(BaseModel):
    id: int = Field(..., description="User id")
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="user email address")
    full_name: Optional[str] = Field(None, description="user full name")
    is_active: bool = Field(..., description="User active status")
    role: str = Field(..., description="user role")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(None, description="Last update timestamp")

    class Config:
        from_attributes=True
        json_encoders= {
            datetime: lambda v: v.isoformat()
        }




