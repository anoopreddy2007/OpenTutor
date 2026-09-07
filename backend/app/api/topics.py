from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.course import Course
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicResponse

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TopicResponse, status_code=201)
def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
):
    course = db.get(Course, topic_data.course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    topic = Topic(
        course_id=topic_data.course_id,
        name=topic_data.name,
        description=topic_data.description,
        order_index=topic_data.order_index,
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic


@router.get("/course/{course_id}", response_model=list[TopicResponse])
def list_course_topics(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return (
        db.query(Topic)
        .filter(Topic.course_id == course_id)
        .order_by(Topic.order_index, Topic.id)
        .all()
    )


@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = db.get(Topic, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return topic