from sqlalchemy.orm import Session


def recommend_next_concept(
    db: Session,
    user_id: int,
) -> int | None:
    """
    Select the next concept the learner should study.
    """

    raise NotImplementedError