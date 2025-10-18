from app.activities.qr_generator.schemas import QRRequest, QRResponse
from fastapi import HTTPException, status
import structlog
import qrcode
import io
import base64

logger = structlog.get_logger(__name__)


class QRGeneratorService:
    """Service for generating QR codes from text input."""
    
    @staticmethod
    def generate_qr(data: QRRequest) -> QRResponse:
        """
        Generate QR code from text input.
        
        Args:
            data: QRRequest containing text to encode
            
        Returns:
            QRResponse with base64-encoded QR code image
            
        Raises:
            HTTPException: If text is empty or QR generation fails
        """
        try:
            text = data.text
            if not text or not text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Text is required and cannot be empty"
                )
            
            qr = qrcode.QRCode(
                version=1,  
                error_correction=qrcode.constants.ERROR_CORRECT_L,  
                box_size=10,  
                border=4,  
            )
            
            
            qr.add_data(text)
            qr.make(fit=True)
            
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            
            qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.info("qr_generation_success", text_length=len(text))
            
            return QRResponse(qr_code_base64=qr_base64)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("qr_generation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate QR code"
            )



qr_service = QRGeneratorService()
