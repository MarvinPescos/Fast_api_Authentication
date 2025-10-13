from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List
import re

class Settings(BaseSettings):
    #Database Settings
    DB_USER: str = Field(..., description="Database username")
    DB_PASS: str = Field(..., min_length=1, description="Databse password")
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: str = Field(default="5432", pattern=r"\d+$", description="Database port")
    DB_NAME: str = Field(..., min_length=1, description="Datanse name")

    SECRET_KEY: str = Field(..., min_length=32, description="JWT secret key")
    ALGORITHM: str = Field(default="HS256", pattern=r"^(HS256|HS384|HS512)$")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1, le=1440)

    # App Settings
    APP_NAME: str = Field(default="Financial Tracker", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode" )
    FRONTEND_URL: str = Field(default="http://localhost:5173", description="Frontend application URL")

    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000", 
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173"
        ], 
        description="Allowed CORS origins"
    )

    EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES: int = Field(default=15, ge=5, le=60, description="Verification code expiry time")

    MAIL_FROM: str = Field(..., description="Your verified sender email address")
    MAIL_FROM_NAME: str = Field(default="Financial Tracker", description="Display name for sender")
    BREVO_API_KEY: str = Field(..., description="Brevo API key")

    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: str = Field(default="6379", description="Redis port")
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")

    # FACEBOOK_CLIENT_ID:str = Field(..., description="Facebook App ID")
    # FACEBOOK_CLIENT_SECRET: str = Field(..., description="Facebook App Secret")
    # FACEBOOK_REDIRECT_URI: str = Field(..., description="Facebook OAuth redirect uri")

    SENTRY_DSN: str = Field(..., description="Your Sentry_dsn key")

    @property
    def DATABASE_URL(self) -> str:
      """Get database URL for async operations"""
      return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get database URL for sync operations (migrations)"""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
 