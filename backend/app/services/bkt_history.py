def build_response_history(
    correct_count: int,
    attempts_count: int,
) -> list[bool]:
    """Build a response history from learner attempt counts."""

    if attempts_count <= 0:
        return []

    correct_count = max(
        0,
        min(correct_count, attempts_count),
    )

    incorrect_count = attempts_count - correct_count

    return (
        [True] * correct_count
        + [False] * incorrect_count
    )