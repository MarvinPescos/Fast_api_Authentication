from app.core import settings
from app.activities.trivia.schema import TriviaResponse, TriviaQuestion

from fastapi import HTTPException, status
import structlog
import httpx

logger = structlog.get_logger(__name__)


class TriviaService:
    """
    Service for fetching trivia questions from OpenTDB API
    """
    
    def __init__(self):
        self.base_url = settings.OPENTDB_API_URL
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_single_question(self) -> TriviaQuestion:
        """
        Fetches a single, multiple-choice trivia question from the OpenTDB API.
        
        Returns:
            A single TriviaQuestion object.
            
        Raises:
            HTTPException: If the API request fails or returns an unexpected status.
        """
        
        params = {
            "amount": 1,
            "type": "multiple"
        }
        
        try:
            logger.info("Fetching trivia question from OpenTDB")
            
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status() 
            
            data = response.json()
            
            validated_response = TriviaResponse(**data)
            
            if validated_response.response_code != 0:
                logger.error(f"OpenTDB API returned error code: {validated_response.response_code}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Trivia service is temporarily unavailable"
                )
            
            if not validated_response.results:
                logger.error("OpenTDB API returned empty results")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No trivia questions found"
                )
            
            logger.info("Successfully fetched trivia question")
            return validated_response.results[0]
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.error("OpenTDB API rate limit exceeded (429)")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests to trivia service. Please wait a moment and try again."
                )
            logger.error(f"HTTP error from OpenTDB API: {e.response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to fetch trivia question"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Trivia service connection failed"
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching trivia: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    
trivia_service = TriviaService()
