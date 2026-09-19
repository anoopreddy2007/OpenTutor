def build_recommendation_reason(
    mastery: float,
    revision_need: float,
    difficulty: int,
    confidence: float | None = None,
) -> str:
    """
    Explain why a concept was recommended.

    The explanation is based on learner mastery,
    confidence, revision urgency, and difficulty.

    Confidence is optional so existing callers that do
    not provide confidence retain their previous behavior.
    """

    if mastery < 0.30:
        return (
            "Recommended because this concept needs "
            "significant practice."
        )

    if confidence is not None and confidence < 0.30:
        return (
            "Recommended because your confidence in "
            "this concept is low."
        )

    if revision_need >= 1.0:
        return (
            "Recommended because this concept is "
            "due for revision."
        )

    if revision_need >= 0.70:
        return (
            "Recommended because this concept is "
            "approaching its revision point."
        )

    if mastery < 0.70:
        return (
            "Recommended because additional practice "
            "can improve mastery."
        )

    if difficulty >= 4:
        return (
            "Recommended as a challenging concept "
            "to extend your learning."
        )

    return (
        "Recommended as the next suitable concept "
        "for your learning."
    )