from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.learning_action import LearningActionResponse
from app.services.learning_action import get_next_learning_action


router = APIRouter(
    prefix="/learning-actions",
    tags=["Learning Actions"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{user_id}",
    response_model=LearningActionResponse,
)
def get_learning_action(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_next_learning_action(
        db=db,
        user_id=user_id,
    )