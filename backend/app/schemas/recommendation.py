from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    concept_id: int | None