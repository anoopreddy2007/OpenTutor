from app.services.bkt_mastery import estimate_mastery


def estimate_state_mastery(
    correct_count: int,
    attempts_count: int,
) -> float:
    """Estimate mastery from learner attempt history using BKT."""

    if attempts_count <= 0:
        return estimate_mastery([])

    correct_count = max(0, min(correct_count, attempts_count))

    responses = (
        [True] * correct_count
        + [False] * (attempts_count - correct_count)
    )

    return estimate_mastery(responses)