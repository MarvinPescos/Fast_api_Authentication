from fastapi import APIRouter, Depends, status
from app.activities.joke_cipher_qr.schemas import JokeCipherQRRequest, JokeCipherQRResponse
from app.activities.joke_cipher_qr.service import joke_cipher_qr_service
from app.users import User
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post(
    "/generate",
    response_model=JokeCipherQRResponse,
    status_code=status.HTTP_200_OK,
    description="Fetch joke, cipher it, and generate QR code"
)
async def generate_joke_cipher_qr(
    payload: JokeCipherQRRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Complete flow: Fetch random joke → [Optional: Cipher] → Generate QR code.
    
    This endpoint can work in two modes:
    
    Mode 1: Joke + Cipher + QR
    {
        "cipher_type": "caesar",      // atbash, caesar, or vigenere
        "caesar_shift": 3,            // Only for caesar (default: 3)
        "vigenere_key": "SECRET"      // Only for vigenere (default: "SECRET")
    }
    
    Mode 2: Joke + QR (no cipher)
    {
        "cipher_type": null           // or omit this field entirely
    }
    
    Response includes:
    - original_joke: The joke from API
    - ciphered_joke: Joke after cipher (null if no cipher used)
    - cipher_used: Which cipher was applied (null if no cipher used)
    - qr_code_base64: QR code as base64 PNG (of ciphered or original joke)
    
    Requires authentication.
    """
    return await joke_cipher_qr_service.generate_joke_cipher_qr(payload)

