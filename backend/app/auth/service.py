from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status
import structlog

from app.users import User, UserCreate, UserResponse
from app.core import hash_password, verify_password, create_access_token
from app.email import send_verification_email
from app.email_verification import EmailVerificationService, RegistrationResponse, EmailVerificationCode
from app.core import USER_REGISTRATION

logger = structlog.get_logger(__name__)

class AuthService:
    """
        Service layer for authentication business logic
    """

    def __init__ (self, db: AsyncSession):
        self.db = db

    