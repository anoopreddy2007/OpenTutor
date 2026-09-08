from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class QuestionCreate(BaseModel):
    concept_id: int
    question_text: str
    question_type: str
    difficulty: int = Field(default=1, ge=1, le=5)
    options: dict | None = None
    correct_answer: str
    explanation: str | None = None


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    concept_id: int
    question_text: str
    question_type: str
    difficulty: int
    options: dict | None
    correct_answer: str
    explanation: str | None
    created_at: datetime