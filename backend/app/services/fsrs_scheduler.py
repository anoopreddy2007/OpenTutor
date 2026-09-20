from datetime import datetime, timedelta

from app.services.fsrs import calculate_retrievability


DEFAULT_TARGET_RETRIEVABILITY = 0.90
MIN_REVIEW_INTERVAL_DAYS = 1.0
MAX_REVIEW_INTERVAL_DAYS = 30.0


def calculate_fsrs_review_interval(
    stability: float,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> float:
    """
    Calculate the number of days until the next review.

    The interval is chosen so that the predicted
    retrievability reaches the target value.

    R(t) = exp(-t / S)

    Therefore:

    t = -S * ln(target_retrievability)
    """

    if stability <= 0:
        raise ValueError(
            "stability must be greater than 0"
        )

    if not 0.0 < target_retrievability < 1.0:
        raise ValueError(
            "target_retrievability must be between 0 and 1"
        )

    import math

    interval_days = (
        -stability
        * math.log(target_retrievability)
    )

    return max(
        MIN_REVIEW_INTERVAL_DAYS,
        min(
            MAX_REVIEW_INTERVAL_DAYS,
            interval_days,
        ),
    )


def schedule_next_fsrs_review(
    last_review_at: datetime,
    stability: float,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> datetime:
    """
    Calculate the next review timestamp.
    """

    interval_days = calculate_fsrs_review_interval(
        stability=stability,
        target_retrievability=target_retrievability,
    )

    return last_review_at + timedelta(
        days=interval_days
    )


def is_fsrs_review_due(
    last_review_at: datetime | None,
    stability: float,
    current_time: datetime,
    target_retrievability: float = DEFAULT_TARGET_RETRIEVABILITY,
) -> bool:
    """
    Determine whether a concept should be reviewed.

    A review is due when predicted retrievability
    falls to or below the target threshold.
    """

    if last_review_at is None:
        return True

    if stability <= 0:
        raise ValueError(
            "stability must be greater than 0"
        )

    retrievability = calculate_retrievability(
        elapsed_days=max(
            0.0,
            (
                current_time - last_review_at
            ).total_seconds()
            / (24 * 60 * 60),
        ),
        stability=stability,
    )

    return retrievability <= target_retrievability