from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.concept import Concept
from app.models.topic import Topic
from app.schemas.concept import ConceptCreate, ConceptResponse

router = APIRouter(
    prefix="/concepts",
    tags=["Concepts"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ConceptResponse, status_code=201)
def create_concept(
    concept_data: ConceptCreate,
    db: Session = Depends(get_db),
):
    topic = db.get(Topic, concept_data.topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    concept = Concept(
        topic_id=concept_data.topic_id,
        name=concept_data.name,
        description=concept_data.description,
        difficulty=concept_data.difficulty,
    )

    db.add(concept)
    db.commit()
    db.refresh(concept)

    return concept


@router.get("/topic/{topic_id}", response_model=list[ConceptResponse])
def list_topic_concepts(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = db.get(Topic, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return (
        db.query(Concept)
        .filter(Concept.topic_id == topic_id)
        .order_by(Concept.id)
        .all()
    )


@router.get("/{concept_id}", response_model=ConceptResponse)
def get_concept(
    concept_id: int,
    db: Session = Depends(get_db),
):
    concept = db.get(Concept, concept_id)

    if concept is None:
        raise HTTPException(
            status_code=404,
            detail="Concept not found",
        )

    return concept