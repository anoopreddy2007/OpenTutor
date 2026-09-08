from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.learner_state import LearnerState
from app.models.user import User
from app.models.concept import Concept
from app.schemas.learner_state import LearnerStateResponse

router = APIRouter(
    prefix="/learner-states",
    tags=["Learner States"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/user/{user_id}",
    response_model=list[LearnerStateResponse],
)
def list_user_learner_states(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return (
        db.query(LearnerState)
        .filter(LearnerState.user_id == user_id)
        .order_by(LearnerState.concept_id)
        .all()
    )


@router.get(
    "/user/{user_id}/concept/{concept_id}",
    response_model=LearnerStateResponse,
)
def get_concept_learner_state(
    user_id: int,
    concept_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    concept = db.get(Concept, concept_id)

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found",
        )

    learner_state = (
        db.query(LearnerState)
        .filter(
            LearnerState.user_id == user_id,
            LearnerState.concept_id == concept_id,
        )
        .first()
    )

    if learner_state is None:
        raise HTTPException(
            status_code=404,
            detail="Learner state not found",
        )

    return learner_state