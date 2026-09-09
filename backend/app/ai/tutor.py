from sqlalchemy.orm import Session

from app.ai.providers import LLMProvider
from app.models.learner_state import LearnerState


class TutorService:
    """Coordinates learner context with an LLM provider."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate_response(
        self,
        db: Session,
        user_id: int,
        concept_id: int,
        question: str,
    ) -> str:
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

        system_prompt = (
            "You are OpenTutor, an adaptive AI tutor. "
            "Help the learner understand the concept without "
            "immediately giving away the answer."
        )

        prompt = (
            f"Learner mastery: {mastery:.2f}\n"
            f"Learner confidence: {confidence:.2f}\n\n"
            f"Student question:\n{question}"
        )

        return self.provider.generate(
            prompt,
            system_prompt=system_prompt,
        )