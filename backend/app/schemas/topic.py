from pydantic import BaseModel, ConfigDict


class TopicCreate(BaseModel):
    course_id: int
    name: str
    description: str | None = None
    order_index: int = 0


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    name: str
    description: str | None
    order_index: int