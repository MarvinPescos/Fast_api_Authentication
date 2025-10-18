from pydantic import BaseModel, Field


class TwoFactorSetupResponse(BaseModel):
    """Response for 2FA setup initiation"""
    secret: str = Field(..., description="TOTP secret (should be stored securely)")
    qr_code: str = Field(..., description="Base64 encoded QR code image")
    manual_entry_key: str = Field(..., description="Secret for manual entry")


class TwoFactorEnableRequest(BaseModel):
    """Request to enable 2FA"""
    token: str = Field(..., description="6-digit TOTP code", min_length=6, max_length=6)


class TwoFactorVerifyRequest(BaseModel):
    """Request to verify 2FA token during login"""
    email: str = Field(..., description="User email")
    token: str = Field(..., description="6-digit TOTP code", min_length=6, max_length=6)


class TwoFactorDisableRequest(BaseModel):
    """Request to disable 2FA"""
    password: str = Field(..., description="User's password for verification")
    token: str = Field(..., description="6-digit TOTP code", min_length=6, max_length=6)


class TwoFactorStatusResponse(BaseModel):
    """Response for 2FA status"""
    enabled: bool = Field(..., description="Whether 2FA is enabled")
    

class TwoFactorEnableResponse(BaseModel):
    """Response after successfully enabling 2FA"""
    success: bool
    message: str

