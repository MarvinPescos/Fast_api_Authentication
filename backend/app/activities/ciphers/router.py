from fastapi import APIRouter, Depends, status
from app.activities.ciphers.schemas import ProccessTextResponse, AtbashRequest, CaesarRequest, VigenereRequest
from app.activities.ciphers.service import ciphers_service
from app.users import User
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post(
    "/atbash",
    response_model=ProccessTextResponse,
    status_code=status.HTTP_200_OK,
    description="Cipher the given text using Atbash"
)
def atbash_cipher(
    payload: AtbashRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Encode text using Atbash cipher (reverse alphabet).
    
    Example: "hello" -> "svool"
    
    Body: { "text": "your text here" }
    Requires authentication.
    """
    result = ciphers_service.atbash_cipher(payload)
    return ProccessTextResponse(result=result)


@router.post(
    "/caesar",
    response_model=ProccessTextResponse,
    status_code=status.HTTP_200_OK,
    description="Cipher the given text using Caesar cipher"
)
def caesar_cipher(
    payload: CaesarRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Encode text using Caesar cipher (shift alphabet).
    
    Example: "hello" with shift 3 -> "khoor"
    
    Body: { "text": "your text here", "shift": 3 }
    Requires authentication.
    """
    result = ciphers_service.caesar_cipher(payload)
    return ProccessTextResponse(result=result)


@router.post(
    "/vigenere",
    response_model=ProccessTextResponse,
    status_code=status.HTTP_200_OK,
    description="Cipher the given text using Vigenère cipher"
)
def vigenere_cipher(
    payload: VigenereRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Encode text using Vigenère cipher (keyword-based polyalphabetic).
    
    Example: "hello" with key "KEY" -> "rijvs"
    
    Body: { "text": "your text here", "key": "SECRET" }
    Requires authentication.
    """
    result = ciphers_service.vigenere_cipher(payload)
    return ProccessTextResponse(result=result)
