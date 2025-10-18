from fastapi import APIRouter, Depends, status
from app.activities.qr_generator.schemas import QRRequest, QRResponse
from app.activities.qr_generator.service import qr_service
from app.users import User
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post(
    "/generate",
    response_model=QRResponse,
    status_code=status.HTTP_200_OK,
    description="Generate QR code from text input"
)
def generate_qr(
    payload: QRRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a QR code from the provided text.
    """
    return qr_service.generate_qr(payload)

