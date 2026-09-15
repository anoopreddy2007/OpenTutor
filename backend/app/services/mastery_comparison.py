from app.services.bkt_mastery import estimate_mastery


def calculate_baseline_mastery(
    correct_count: int,
    attempts_count: int,
) -> float:
    """Calculate simple accuracy-based mastery."""

    if attempts_count <= 0:
        return 0.0

    correct_count = max(
        0,
        min(correct_count, attempts_count),
    )

    return correct_count / attempts_count


def compare_mastery_models(
    responses: list[bool],
) -> dict:
    """Compare simple accuracy mastery with BKT mastery."""

    attempts_count = len(responses)
    correct_count = sum(responses)

    baseline = calculate_baseline_mastery(
        correct_count=correct_count,
        attempts_count=attempts_count,
    )

    bkt = estimate_mastery(responses)

    return {
        "baseline_mastery": baseline,
        "bkt_mastery": bkt,
        "difference": bkt - baseline,
    }