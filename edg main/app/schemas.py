from pydantic import BaseModel, Field, field_validator
from typing import List


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="User input text")

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=20000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        return value.strip()


class ExplanationResponse(BaseModel):
    answer: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=3, max_length=3)


class LearningStep(BaseModel):
    level: str
    topic: str
    description: str
    resources: List[str] = Field(default_factory=list)


class LearningPathResponse(BaseModel):
    title: str
    overview: str
    steps: List[LearningStep] = Field(min_length=3)


class TextResponse(BaseModel):
    answer: str
