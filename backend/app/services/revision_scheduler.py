from datetime import datetime, timedelta

from app.services.retrievability import calculate_retrievability


DEFAULT_TARGET_RETRIEVABILITY = 0.90
MIN_REVIEW_INTERVAL_DAYS = 1.0
MAX_REVIEW_INTERVAL_DAYS = 30.0


def calculate_review_interval(
    stability: float,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> float:
    """
    Calculate the number of days until the next review.

    The interval is derived from memory stability and the
    target retrievability that the learner should retain.
    """

    if stability <= 0:
        raise ValueError("stability must be greater than 0")

    if not 0.0 < target_retrievability < 1.0:
        raise ValueError(
            "target_retrievability must be between 0 and 1"
        )

    # Invert the retrievability equation:
    #
    # R = (1 + t / (9S)) ^ -1
    #
    # Therefore:
    #
    # t = 9S(1/R - 1)

    interval_days = (
        9.0
        * stability
        * (
            (1.0 / target_retrievability)
            - 1.0
        )
    )

    return max(
        MIN_REVIEW_INTERVAL_DAYS,
        min(MAX_REVIEW_INTERVAL_DAYS, interval_days),
    )


def schedule_next_review(
    last_review_at: datetime,
    stability: float,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> datetime:
    """
    Calculate the next review timestamp.
    """

    interval_days = calculate_review_interval(
        stability=stability,
        target_retrievability=target_retrievability,
    )

    return last_review_at + timedelta(
        days=interval_days
    )


def is_review_due(
    last_review_at: datetime | None,
    stability: float,
    current_time: datetime,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> bool:
    """
    Determine whether a concept should currently be reviewed.
    """

    if last_review_at is None:
        return True

    retrievability = calculate_retrievability(
        last_review_at=last_review_at,
        current_time=current_time,
        stability=stability,
    )

    return retrievability <= target_retrievability