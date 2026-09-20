from sqlalchemy.orm import Session

from app.models import LearnerState, Question
from app.services.question_selection import select_next_question
from app.services.recommendation_service import recommend_next_concept


def select_next_learning_question(
    db: Session,
    user_id: int,
) -> Question | None:
    """
    Select the next question for a learner.

    The adaptive loop is:

    1. Recommend the next concept.
    2. Retrieve questions for that concept.
    3. Retrieve the learner's state for that concept.
    4. Select the most suitable question.
    """

    concept_id = recommend_next_concept(
        db=db,
        user_id=user_id,
    )

    if concept_id is None:
        return None

    questions = (
        db.query(Question)
        .filter(
            Question.concept_id == concept_id,
        )
        .all()
    )

    if not questions:
        return None

    learner_state = (
        db.query(LearnerState)
        .filter(
            LearnerState.user_id == user_id,
            LearnerState.concept_id == concept_id,
        )
        .first()
    )

    if learner_state is None:
        mastery = 0.0
        confidence = 0.0
    else:
        mastery = learner_state.mastery
        confidence = learner_state.confidence

    return select_next_question(
        questions=questions,
        mastery=mastery,
        confidence=confidence,
    )