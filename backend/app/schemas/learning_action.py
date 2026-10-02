from pydantic import BaseModel


class LearningActionResponse(BaseModel):
    action: str
    concept_id: int | None
    priority: float
    reason: str
    mastery: float
    confidence: float
    revision_need: float
    misconception_severity: float
    prerequisites_ready: bool