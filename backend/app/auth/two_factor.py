"""
Two-Factor Authentication Service using TOTP (Time-based One-Time Password)
"""
import pyotp
import qrcode
import io
import base64
from typing import Tuple
import structlog

logger = structlog.get_logger(__name__)


class TwoFactorService:
    """Service for handling two-factor authentication"""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(email: str, secret: str, issuer: str = "BalanceHub") -> str:
        """
        Generate QR code for Google Authenticator
        
        Args:
            email: User's email
            secret: TOTP secret
            issuer: Application name
            
        Returns:
            Base64 encoded QR code image
        """
        # Create provisioning URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=email,
            issuer_name=issuer
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """
        Verify TOTP token
        
        Args:
            secret: TOTP secret
            token: 6-digit code from authenticator app
            
        Returns:
            True if valid, False otherwise
        """
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)
        except Exception as e:
            logger.error("totp_verification_failed", error=str(e))
            return False
    


two_factor_service = TwoFactorService()

