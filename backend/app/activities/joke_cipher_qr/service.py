from app.activities.joke_cipher_qr.schemas import JokeCipherQRRequest, JokeCipherQRResponse
from app.activities.ciphers.schemas import AtbashRequest, CaesarRequest, VigenereRequest
from app.activities.ciphers.service import ciphers_service
from app.activities.qr_generator.schemas import QRRequest
from app.activities.qr_generator.service import qr_service
from app.core import settings

from fastapi import HTTPException, status
import structlog
import httpx

logger = structlog.get_logger(__name__)


class JokeCipherQRService:
    """Service for fetching jokes, ciphering them, and generating QR codes."""
    
    def __init__(self):
        self.joke_api_url = settings.JOKE_API_URL
    
    async def fetch_joke(self) -> str:
        """
        Fetch a random joke from JokeAPI.
        
        Returns:
            str: The joke text
            
        Raises:
            HTTPException: If API request fails
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.joke_api_url)
                response.raise_for_status()
                
                data = response.json()
                
                # JokeAPI returns single jokes with "joke" field
                if "joke" in data:
                    return data["joke"]
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No joke found in API response"
                    )
                    
        except httpx.HTTPStatusError as e:
            logger.error("joke_api_http_error", status_code=e.response.status_code)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to fetch joke from API"
            )
        except httpx.RequestError as e:
            logger.error("joke_api_request_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Joke API connection failed"
            )
        except Exception as e:
            logger.error("joke_fetch_unexpected_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch joke"
            )
    
    async def generate_joke_cipher_qr(self, data: JokeCipherQRRequest) -> JokeCipherQRResponse:
        """
        Orchestrate: fetch joke → cipher it → generate QR code.
        
        Args:
            data: Request containing cipher type and parameters
            
        Returns:
            JokeCipherQRResponse with original joke, ciphered joke, and QR code
        """
        try:
            
            logger.info("fetching_joke_from_api")
            joke = await self.fetch_joke()
            logger.info("joke_fetched_successfully", joke_length=len(joke))
            
            
            ciphered_joke = None
            cipher_used = None
            text_for_qr = joke  
            
            if data.cipher_type:
                logger.info("applying_cipher", cipher_type=data.cipher_type)
                
                if data.cipher_type == "atbash":
                    ciphered_joke = ciphers_service.atbash_cipher(AtbashRequest(text=joke))
                elif data.cipher_type == "caesar":
                    ciphered_joke = ciphers_service.caesar_cipher(
                        CaesarRequest(text=joke, shift=data.caesar_shift)
                    )
                elif data.cipher_type == "vigenere":
                    ciphered_joke = ciphers_service.vigenere_cipher(
                        VigenereRequest(text=joke, key=data.vigenere_key)
                    )
                
                cipher_used = data.cipher_type
                text_for_qr = ciphered_joke  
                logger.info("cipher_applied_successfully", cipher_type=data.cipher_type)
            else:
                logger.info("no_cipher_requested_skipping_cipher_step")
            
            
            logger.info("generating_qr_code", text_length=len(text_for_qr))
            qr_response = qr_service.generate_qr(QRRequest(text=text_for_qr))
            logger.info("qr_code_generated_successfully")
            
            return JokeCipherQRResponse(
                original_joke=joke,
                ciphered_joke=ciphered_joke,
                cipher_used=cipher_used,
                qr_code_base64=qr_response.qr_code_base64
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("joke_cipher_qr_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate joke cipher QR"
            )


joke_cipher_qr_service = JokeCipherQRService()

