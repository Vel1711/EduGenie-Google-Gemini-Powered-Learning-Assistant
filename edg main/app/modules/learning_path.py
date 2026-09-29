from fastapi import APIRouter, HTTPException

from app.dependencies import require_gemini
from app.prompts import learning_path_prompt
from app.schemas import LearningPathResponse, TextRequest
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["Learning Path"])


@router.post("/learn/recommendations", response_model=LearningPathResponse)
@router.post("/api/learn/recommendations", response_model=LearningPathResponse)
async def learning_recommendations(payload: TextRequest):
    require_gemini()
    try:
        result = gemini_service.structured(
            learning_path_prompt(payload.text),
            LearningPathResponse,
            temperature=0.5,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
