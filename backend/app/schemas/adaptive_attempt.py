from datetime import datetime

from pydantic import BaseModel


class AdaptiveAttemptResponse(BaseModel):
    attempt_id: int
    user_id: int
    question_id: int
    is_correct: bool
    created_at: datetime

    action: str
    concept_id: int | None
    priority: float
    reason: str

    mastery: float
    confidence: float
    revision_need: float
    misconception_severity: float
    prerequisites_ready: bool

    next_question_id: int | None