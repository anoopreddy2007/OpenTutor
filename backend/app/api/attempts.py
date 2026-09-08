from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.user import User
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.services.learner_state_service import update_learner_state

router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AttemptResponse, status_code=201)
def create_attempt(
    attempt_data: AttemptCreate,
    db: Session = Depends(get_db),
):
    user = db.get(User, attempt_data.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    question = db.get(Question, attempt_data.question_id)

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    attempt = Attempt(
        user_id=attempt_data.user_id,
        question_id=attempt_data.question_id,
        answer=attempt_data.answer,
        is_correct=attempt_data.is_correct,
        time_taken=attempt_data.time_taken,
        confidence=attempt_data.confidence,
    )

    db.add(attempt)
    db.flush()

    update_learner_state(db, attempt)

    db.commit()
    db.refresh(attempt)

    return attempt


@router.get("/user/{user_id}", response_model=list[AttemptResponse])
def list_user_attempts(
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
        db.query(Attempt)
        .filter(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .all()
    )


@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = db.get(Attempt, attempt_id)

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found",
        )

    return attempt