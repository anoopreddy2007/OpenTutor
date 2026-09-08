from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AttemptCreate(BaseModel):
    user_id: int
    question_id: int
    answer: str
    is_correct: bool
    time_taken: float | None = Field(default=None, ge=0)
    confidence: int | None = Field(default=None, ge=1, le=5)


class AttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    question_id: int
    answer: str
    is_correct: bool
    time_taken: float | None
    confidence: int | None
    created_at: datetime