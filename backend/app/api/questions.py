from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.concept import Concept
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionResponse

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=QuestionResponse, status_code=201)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
):
    concept = db.get(Concept, question_data.concept_id)

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found",
        )

    question = Question(
        concept_id=question_data.concept_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type,
        difficulty=question_data.difficulty,
        options=question_data.options,
        correct_answer=question_data.correct_answer,
        explanation=question_data.explanation,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get("/concept/{concept_id}", response_model=list[QuestionResponse])
def list_concept_questions(
    concept_id: int,
    db: Session = Depends(get_db),
):
    concept = db.get(Concept, concept_id)

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found",
        )

    return (
        db.query(Question)
        .filter(Question.concept_id == concept_id)
        .order_by(Question.id)
        .all()
    )


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    question = db.get(Question, question_id)

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    return question