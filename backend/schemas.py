from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)

class SummaryRequest(BaseModel):
    type: str = "Short"

class MCQRequest(BaseModel):
    count: int = Field(default=5, ge=1, le=20)
    difficulty: str = "Medium"

class QuizSubmitRequest(BaseModel):
    answers: List[str]

class FlashcardRequest(BaseModel):
    count: int = Field(default=10, ge=1, le=30)

class ExplainRequest(BaseModel):
    text: str = Field(min_length=1)
    level: str = "Beginner"

class PlanRequest(BaseModel):
    subject: str
    units: int = Field(ge=1)
    days: int = Field(ge=1)
    hours: float = Field(gt=0)
    exam_date: Optional[str] = None
