from pydantic import BaseModel
from typing import List


class TriviaQuestion(BaseModel):
    """Single trivia question from OpenTDB API"""
    type: str
    difficulty: str
    category: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]


class TriviaResponse(BaseModel):
    """Response wrapper from OpenTDB API"""
    response_code: int
    results: List[TriviaQuestion]
