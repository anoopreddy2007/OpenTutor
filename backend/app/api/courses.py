from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
):
    existing_course = (
        db.query(Course)
        .filter(Course.name == course_data.name)
        .first()
    )

    if existing_course:
        raise HTTPException(
            status_code=409,
            detail="Course already exists",
        )

    course = Course(
        name=course_data.name,
        description=course_data.description,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


@router.get("/", response_model=list[CourseResponse])
def list_courses(
    db: Session = Depends(get_db),
):
    return db.query(Course).order_by(Course.id).all()


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course