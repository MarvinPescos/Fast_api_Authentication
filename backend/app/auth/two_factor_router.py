from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core import get_db
from app.auth.dependencies import get_current_user
from app.auth.two_factor import two_factor_service
from app.auth.two_factor_schemas import (
    TwoFactorSetupResponse,
    TwoFactorEnableRequest,
    TwoFactorEnableResponse,
    TwoFactorDisableRequest,
    TwoFactorStatusResponse
)
from app.users import User
from app.core.security import verify_password
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/2fa", tags=["Two-Factor Authentication"])


@router.get(
    "/status",
    response_model=TwoFactorStatusResponse,
    status_code=status.HTTP_200_OK,
    description="Check if 2FA is enabled for current user"
)
async def get_2fa_status(
    current_user: User = Depends(get_current_user)
):
    """Get 2FA status for the authenticated user"""
    return TwoFactorStatusResponse(enabled=current_user.two_factor_enabled)


@router.post(
    "/setup",
    response_model=TwoFactorSetupResponse,
    status_code=status.HTTP_200_OK,
    description="Initialize 2FA setup (generates QR code)"
)
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate QR code and secret for 2FA setup
    
    This endpoint generates a new TOTP secret and QR code.
    The user should scan the QR code with Google Authenticator
    and then call /enable with a generated code to confirm.
    """
    if current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is already enabled. Disable it first to set up again."
        )
    
    # Generate new secret
    secret = two_factor_service.generate_secret()
    
    # Generate QR code
    qr_code = two_factor_service.generate_qr_code(
        email=current_user.email,
        secret=secret
    )
    
    # Temporarily store secret (not enabled yet)
    stmt = update(User).where(User.id == current_user.id).values(
        two_factor_secret=secret
    )
    await db.execute(stmt)
    await db.commit()
    
    logger.info("2fa_setup_initiated", user_id=current_user.id)
    
    return TwoFactorSetupResponse(
        secret=secret,
        qr_code=qr_code,
        manual_entry_key=secret
    )


@router.post(
    "/enable",
    response_model=TwoFactorEnableResponse,
    status_code=status.HTTP_200_OK,
    description="Enable 2FA after verifying TOTP code"
)
async def enable_2fa(
    request: TwoFactorEnableRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Enable 2FA after user confirms they can generate valid codes
    
    Requires a valid TOTP code to confirm the setup
    """
    if current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is already enabled"
        )
    
    if not current_user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA setup not initiated. Call /setup first."
        )
    
    # Verify the token
    if not two_factor_service.verify_totp(current_user.two_factor_secret, request.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # Enable 2FA
    stmt = update(User).where(User.id == current_user.id).values(
        two_factor_enabled=True
    )
    await db.execute(stmt)
    await db.commit()
    
    logger.info("2fa_enabled", user_id=current_user.id)
    
    return TwoFactorEnableResponse(
        success=True,
        message="Two-factor authentication enabled successfully"
    )


@router.post(
    "/disable",
    status_code=status.HTTP_200_OK,
    description="Disable 2FA"
)
async def disable_2fa(
    request: TwoFactorDisableRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Disable 2FA
    
    Requires both password and current TOTP code for security
    """
    if not current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is not enabled"
        )
    
    # Verify password
    if not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Verify TOTP token
    if not two_factor_service.verify_totp(current_user.two_factor_secret, request.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # Disable 2FA and remove secret
    stmt = update(User).where(User.id == current_user.id).values(
        two_factor_enabled=False,
        two_factor_secret=None
    )
    await db.execute(stmt)
    await db.commit()
    
    logger.info("2fa_disabled", user_id=current_user.id)
    
    return {
        "success": True,
        "message": "Two-factor authentication disabled successfully"
    }

