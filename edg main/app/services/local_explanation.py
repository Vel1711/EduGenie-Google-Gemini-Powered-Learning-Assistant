from config import settings


class LocalExplanationService:
    def __init__(self):
        self._pipeline = None
        self._load_error = None

    def available(self) -> bool:
        try:
            import torch  # noqa: F401
            import transformers  # noqa: F401
            return True
        except ImportError:
            return False

    def _load(self):
        if self._pipeline is not None:
            return

        try:
            from transformers import pipeline
            self._pipeline = pipeline(
                "text2text-generation",
                model=settings.local_explanation_model,
            )
        except Exception as exc:
            self._load_error = str(exc)
            raise RuntimeError(
                f"Could not load local explanation model: {exc}"
            ) from exc

    def explain(self, topic: str) -> str:
        self._load()
        prompt = f"""
Explain this topic to a beginner in simple language.
Topic: {topic}
Include a definition, main idea, and one simple example.
"""
        output = self._pipeline(
            prompt,
            max_new_tokens=300,
            do_sample=False,
        )
        return output[0]["generated_text"].strip()


local_explanation_service = LocalExplanationService()
