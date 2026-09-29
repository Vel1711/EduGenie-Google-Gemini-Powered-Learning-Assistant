import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    explanation_provider: str = os.getenv("EXPLANATION_PROVIDER", "auto").lower()
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000",
    )


settings = Settings()
