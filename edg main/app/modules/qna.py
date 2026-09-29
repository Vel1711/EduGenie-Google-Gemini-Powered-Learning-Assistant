from fastapi import APIRouter, HTTPException

from app.dependencies import require_gemini
from app.prompts import qa_prompt
from app.schemas import QARequest, TextResponse
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["Q&A"])


@router.post("/qa", response_model=TextResponse)
@router.post("/api/qa", response_model=TextResponse)
async def ask_question(payload: QARequest):
    require_gemini()
    try:
        answer = gemini_service.text(qa_prompt(payload.question))
        return TextResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
