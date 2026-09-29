from fastapi import APIRouter, HTTPException

from app.dependencies import require_gemini
from app.prompts import summary_prompt
from app.schemas import TextRequest, TextResponse
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["Summary"])


@router.post("/summarize", response_model=TextResponse)
@router.post("/api/summarize", response_model=TextResponse)
async def summarize(payload: TextRequest):
    require_gemini()
    try:
        answer = gemini_service.text(summary_prompt(payload.text))
        return TextResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
