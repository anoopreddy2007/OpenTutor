from pydantic import BaseModel, ConfigDict, Field


class ConceptCreate(BaseModel):
    topic_id: int
    name: str
    description: str | None = None
    difficulty: int = Field(default=1, ge=1, le=5)


class ConceptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    name: str
    description: str | None
    difficulty: int