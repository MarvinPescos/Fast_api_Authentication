from pydantic import BaseModel, Field

class QRRequest(BaseModel):
    """Request Schema for QR"""
    text: str = Field(..., description="text to be encrypt")

class QRResponse(BaseModel):
    """Response Schema for QR"""
    qr_code_base64: str = Field(..., description="QR itself")