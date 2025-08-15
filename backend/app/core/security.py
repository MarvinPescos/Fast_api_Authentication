from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Union, Optional, Dict, Any
from app.core import settings
from app.errors import PasswordHashingError, InvalidTokenError
from fastapi import Request, HTTPException, status
import logging

logger = logging.getLogger(__name__)

Token=str
PasswordHash=str

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password: str) -> PasswordHash:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise PasswordHashingError("Failed to hash password")
    
def verify_password(plain_password: str, hashed_password) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        raise PasswordHashingError("Failed to verify password")

def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
) -> Token:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else: 
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encode_jwt
    except Exception as e:
        logger.error(f"Token creation failed: {str(e)}")
        raise InvalidTokenError("Failed to create token")
        
def verify_access_token(token: str) -> Union[Dict[str, Any], None]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token expired")
        raise InvalidTokenError("Token has expired")
    except jwt.JWTError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise InvalidTokenError("Invalid Token")
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise InvalidTokenError("Token verification failed")
    
def get_token_from_cookie(request: Request) -> str:
    token =  request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing auth token"
        )
    return token
