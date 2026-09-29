from fastapi import APIRouter, HTTPException

from app.prompts import explanation_prompt
from app.schemas import TextRequest, ExplanationResponse
from app.services.gemini_service import gemini_service
from app.services.local_explanation import local_explanation_service
from config import settings

router = APIRouter(tags=["Explanation"])


@router.post("/explain", response_model=ExplanationResponse)
@router.post("/api/explain", response_model=ExplanationResponse)
async def explain_topic(payload: TextRequest):
    provider = settings.explanation_provider

    try:
        if provider in {"local", "auto"}:
            if local_explanation_service.available():
                try:
                    return ExplanationResponse(
                        answer=local_explanation_service.explain(payload.text)
                    )
                except Exception:
                    if provider == "local":
                        raise

        if provider in {"gemini", "auto"}:
            if not settings.gemini_api_key:
                raise RuntimeError(
                    "Neither a usable local LaMini model nor GEMINI_API_KEY is available."
                )
            return ExplanationResponse(
                answer=gemini_service.text(explanation_prompt(payload.text))
            )

        raise RuntimeError(
            "EXPLANATION_PROVIDER must be auto, local, or gemini."
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
