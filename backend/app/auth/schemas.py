from pydantic import BaseModel, EmailStr, Field, validator
from app.users import UserResponse
import re


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user: UserResponse
    message: str

class ForgetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    code: str = Field(..., min_length=32, max_length=128, description="Password reset token from email")
    new_password: str = Field(..., min_length=8, description="New password")

    @validator('new_password')
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

