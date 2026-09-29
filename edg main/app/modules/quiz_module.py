from fastapi import APIRouter, HTTPException

from app.dependencies import require_gemini
from app.prompts import quiz_prompt
from app.schemas import QuizResponse, TextRequest
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["Quiz"])


@router.post("/quiz", response_model=QuizResponse)
@router.post("/api/quiz", response_model=QuizResponse)
async def generate_quiz(payload: TextRequest):
    require_gemini()
    try:
        quiz = gemini_service.structured(
            quiz_prompt(payload.text),
            QuizResponse,
            temperature=0.4,
        )

        # Defensive validation beyond schema generation.
        if len(quiz.questions) != 3:
            raise ValueError("The model did not return exactly 3 questions.")

        for item in quiz.questions:
            if len(item.options) != 4:
                raise ValueError("Each question must contain exactly 4 options.")
            if item.correct_answer not in item.options:
                raise ValueError(
                    "correct_answer must exactly match one of the options."
                )

        return quiz
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
