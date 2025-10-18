from app.activities.ciphers.schemas import ProccessTextResponse, AtbashRequest, CaesarRequest, VigenereRequest
from fastapi import HTTPException, status
import structlog

logger = structlog.get_logger(__name__)

class CiphersService:

    @staticmethod
    def atbash_cipher(data: AtbashRequest) -> str:
        """Cipher the given text using Atbash."""
        try:
            text = data.text
            if not text:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required")

            result = []
            for char in text:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    transformed = chr(base + (25 - (ord(char) - base)))
                    result.append(transformed)
                else:
                    result.append(char)
            
            logger.info("atbash_cipher_success", text_length=len(text))
            return ''.join(result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error("atbash_cipher_failed", error=str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process Atbash cipher")

    @staticmethod
    def caesar_cipher(data: CaesarRequest) -> str:
        """Cipher the given text using Caesar cipher."""
        try:
            text = data.text
            shift = data.shift
            if not text:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required")

            result = []
            for char in text:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    transformed = chr((ord(char) - base + shift) % 26 + base)
                    result.append(transformed)
                else:
                    result.append(char)
            
            logger.info("caesar_cipher_success", text_length=len(text), shift=shift)
            return ''.join(result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error("caesar_cipher_failed", error=str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process Caesar cipher")
            
    @staticmethod
    def vigenere_cipher(data: VigenereRequest) -> str:
        """Cipher the given text using Vigenère cipher (spaces in key are ignored)."""
        try:
            text = data.text
            raw_key = data.key
            key = ''.join(ch.lower() for ch in raw_key if ch.isalpha())
            if not text:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text is required")
            if not key:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Key must contain at least one letter")

            result = []
            key_index = 0

            for char in text:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)]) - ord('a')
                    base = ord('a') if char.islower() else ord('A')
                    result.append(chr((ord(char) - base + shift) % 26 + base))
                    key_index += 1
                else:
                    result.append(char)
            
            logger.info("vigenere_cipher_success", text_length=len(text), key_length=len(key))
            return ''.join(result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error("vigenere_cipher_failed", error=str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process Vigenere cipher")

ciphers_service = CiphersService()


