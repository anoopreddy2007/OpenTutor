from app.services.bkt import BKTParameters


def update_knowledge(
    knowledge: float,
    is_correct: bool,
    params: BKTParameters | None = None,
) -> float:
    """Update knowledge probability after one learner response."""

    if params is None:
        params = BKTParameters()

    knowledge = max(0.0, min(1.0, knowledge))

    if is_correct:
        numerator = knowledge * (1.0 - params.slip_probability)
        denominator = numerator + (
            (1.0 - knowledge) * params.guess_probability
        )
    else:
        numerator = knowledge * params.slip_probability
        denominator = numerator + (
            (1.0 - knowledge) * (1.0 - params.guess_probability)
        )

    if denominator == 0:
        posterior = knowledge
    else:
        posterior = numerator / denominator

    posterior += params.learning_rate * (1.0 - posterior)

    return max(0.0, min(1.0, posterior))