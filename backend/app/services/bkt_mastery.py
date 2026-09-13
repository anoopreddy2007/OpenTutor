from app.services.bkt import BKTParameters
from app.services.bkt_update import update_knowledge


def estimate_mastery(
    responses: list[bool],
    params: BKTParameters | None = None,
) -> float:
    """Estimate learner mastery from a sequence of responses."""

    if params is None:
        params = BKTParameters()

    knowledge = params.initial_knowledge

    for is_correct in responses:
        knowledge = update_knowledge(
            knowledge=knowledge,
            is_correct=is_correct,
            params=params,
        )

    return knowledge