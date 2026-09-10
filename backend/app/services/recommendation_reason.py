def build_recommendation_reason(
    mastery: float,
    revision_need: float,
    difficulty: int,
) -> str:
    """Explain why a concept was recommended."""

    if mastery < 0.30:
        return "Recommended because this concept needs significant practice."

    if revision_need >= 1.0:
        return "Recommended because this concept is due for revision."

    if mastery < 0.70:
        return "Recommended because additional practice can improve mastery."

    if difficulty >= 4:
        return "Recommended as a challenging concept to extend your learning."

    return "Recommended as the next suitable concept for your learning."