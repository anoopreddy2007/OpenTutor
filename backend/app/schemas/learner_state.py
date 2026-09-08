from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LearnerStateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    concept_id: int
    mastery: float
    confidence: float
    attempts_count: int
    correct_count: int
    last_attempt_at: datetime | None
    updated_at: datetime