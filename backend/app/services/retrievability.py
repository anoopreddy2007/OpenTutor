from datetime import datetime


def calculate_retrievability(
    last_review_at: datetime | None,
    current_time: datetime,
    stability: float,
) -> float:
    """
    Calculate memory retrievability using an FSRS-style
    forgetting curve.

    Retrievability represents the estimated probability
    that a learner can currently recall a concept.
    """

    if stability <= 0:
        raise ValueError("stability must be greater than 0")

    if last_review_at is None:
        return 0.0

    elapsed_seconds = (
        current_time - last_review_at
    ).total_seconds()

    elapsed_days = max(
        0.0,
        elapsed_seconds / (24 * 60 * 60),
    )

    retrievability = (
        1.0 + elapsed_days / (9.0 * stability)
    ) ** -1

    return max(
        0.0,
        min(1.0, retrievability),
    )


def calculate_elapsed_days(
    last_review_at: datetime | None,
    current_time: datetime,
) -> float:
    """
    Calculate the number of days elapsed since the
    learner's previous review.
    """

    if last_review_at is None:
        return 0.0

    elapsed_seconds = (
        current_time - last_review_at
    ).total_seconds()

    return max(
        0.0,
        elapsed_seconds / (24 * 60 * 60),
    )