from pydantic import BaseModel, Field
from typing import Literal, Optional


class JokeCipherQRRequest(BaseModel):
    """Request schema for joke cipher QR generation"""
    cipher_type: Optional[Literal["atbash", "caesar", "vigenere"]] = Field(None, description="Type of cipher to use (optional - if not provided, joke won't be ciphered)")
    caesar_shift: int = Field(default=3, ge=1, le=25, description="Shift value for Caesar cipher (only used if cipher_type is 'caesar')")
    vigenere_key: str = Field(default="SECRET", description="Key for Vigenere cipher (only used if cipher_type is 'vigenere')")


class JokeCipherQRResponse(BaseModel):
    """Response schema with joke, ciphered text, and QR code"""
    original_joke: str = Field(..., description="Original joke from API")
    ciphered_joke: Optional[str] = Field(None, description="Joke after applying cipher (null if no cipher was used)")
    cipher_used: Optional[str] = Field(None, description="Which cipher was used (null if no cipher was used)")
    qr_code_base64: str = Field(..., description="Base64-encoded QR code image")

