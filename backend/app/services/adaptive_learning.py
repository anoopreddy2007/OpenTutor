from sqlalchemy.orm import Session

from app.models import LearnerState, Question
from app.services.learning_action import get_next_learning_action
from app.services.question_selection import select_next_question
from app.services.recommendation_service import recommend_next_concept


def select_next_learning_question(
    db: Session,
    user_id: int,
) -> Question | None:
    """
    Select the next question for a learner.

    The adaptive loop is:

    1. Determine the next recommended concept.
    2. Determine the adaptive learning action.
    3. Retrieve questions for that concept.
    4. Retrieve the learner's state.
    5. Select a question according to the learning action.

    Example:

        PRACTICE_CONCEPT
            -> normal adaptive question selection

        REMEDIATE_MISCONCEPTION
            -> prefer easier questions

        BUILD_CONFIDENCE
            -> prefer easier questions

        REVIEW_CONCEPT
            -> select revision-appropriate questions

        ADVANCE
            -> prefer harder questions

        REVIEW_PREREQUISITES
            -> do not select a question
    """

    concept_id = recommend_next_concept(
        db=db,
        user_id=user_id,
    )

    if concept_id is None:
        return None

    learning_action = get_next_learning_action(
        db=db,
        user_id=user_id,
    )

    if learning_action.concept_id != concept_id:
        return None

    action = learning_action.action

    if action == "REVIEW_PREREQUISITES":
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
        action=action,
    )