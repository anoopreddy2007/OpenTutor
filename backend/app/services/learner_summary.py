from datetime import datetime

from app.services.mastery import classify_mastery
from app.services.revision_scheduler import is_review_due
from app.services.retrievability import calculate_retrievability


def build_learner_summary(
    mastery: float,
    confidence: float,
    attempts_count: int,
    correct_count: int,
    last_review_at: datetime | None = None,
    stability: float | None = None,
    current_time: datetime | None = None,
) -> dict:
    """Build a compact summary of the learner's current state."""

    accuracy = (
        correct_count / attempts_count
        if attempts_count > 0
        else 0.0
    )

    summary = {
        "mastery": mastery,
        "confidence": confidence,
        "mastery_level": classify_mastery(mastery),
        "attempts_count": attempts_count,
        "correct_count": correct_count,
        "accuracy": accuracy,
        "revision_need": 0.0,
        "revision_due": False,
    }

    if (
        last_review_at is not None
        and stability is not None
        and stability > 0
    ):
        if current_time is None:
            current_time = datetime.utcnow()

        retrievability = calculate_retrievability(
            last_review_at=last_review_at,
            current_time=current_time,
            stability=stability,
        )

        summary["revision_need"] = max(
            0.0,
            min(1.0, 1.0 - retrievability),
        )

        summary["revision_due"] = is_review_due(
            last_review_at=last_review_at,
            stability=stability,
            current_time=current_time,
        )

    return summary