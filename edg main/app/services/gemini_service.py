from google import genai
from google.genai import types
from pydantic import BaseModel

from config import settings


class GeminiService:
    def __init__(self):
        self.client = None
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)

    def _require_client(self):
        if self.client is None:
            raise RuntimeError(
                "Gemini API is not configured. Set GEMINI_API_KEY in .env."
            )

    def text(self, prompt: str, temperature: float = 0.3) -> str:
        self._require_client()
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
            ),
        )
        result = (response.text or "").strip()
        if not result:
            raise RuntimeError("Gemini returned an empty response.")
        return result

    def structured(self, prompt: str, schema: type[BaseModel], temperature: float = 0.2):
        self._require_client()
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        result = (response.text or "").strip()
        if not result:
            raise RuntimeError("Gemini returned an empty structured response.")
        return schema.model_validate_json(result)


gemini_service = GeminiService()
