from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.user import User
from app.services.recommendation_service import recommend_next_concept
from app.schemas.recommendation import RecommendationResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/next/{user_id}", response_model=RecommendationResponse)
def get_next_recommendation(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    concept_id = recommend_next_concept(
        db=db,
        user_id=user_id,
    )

    return RecommendationResponse(
        concept_id=concept_id,
    )