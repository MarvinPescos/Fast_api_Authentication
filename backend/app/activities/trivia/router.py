from fastapi import APIRouter, Depends, status

from app.activities.trivia.schema import TriviaQuestion
from app.activities.trivia.service import trivia_service
from app.users import User
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/question",
    response_model=TriviaQuestion,
    status_code=status.HTTP_200_OK,
    description="Get a single random trivia question"
)
async def get_trivia_question(
    current_user: User = Depends(get_current_user)
):
    """
    Fetch a single random multiple-choice trivia question from OpenTDB API.
    
    Response includes:
    - question: The trivia question text
    - correct_answer: The correct answer
    - incorrect_answers: List of wrong answers (3 options)
    - category: Question category
    - difficulty: easy, medium, or hard
    - type: Question type (multiple choice)
    
    Requires authentication.
    """
    return await trivia_service.get_single_question()
