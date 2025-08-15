from pydantic import BaseModel
from app.users import UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user: UserResponse
    message: str