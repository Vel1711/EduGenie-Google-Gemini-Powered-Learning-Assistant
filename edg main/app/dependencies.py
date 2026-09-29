from fastapi import HTTPException
from config import settings


def require_gemini():
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY is not configured. Add it to .env and restart the server.",
        )
