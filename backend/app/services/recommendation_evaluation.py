from app.services.adaptive_decision import calculate_adaptive_priority


def calculate_mastery_only_priority(
    mastery: float,
) -> float:
    """
    Baseline policy using only mastery gap.

    Lower mastery produces higher priority.
    """

    return max(
        0.0,
        min(
            1.0,
            1.0 - mastery,
        ),
    )


def calculate_revision_aware_priority(
    mastery: float,
    revision_need: float,
) -> float:
    """
    Revision-aware policy using mastery gap
    and revision urgency.
    """

    mastery_gap = max(
        0.0,
        min(
            1.0,
            1.0 - mastery,
        ),
    )

    revision_need = max(
        0.0,
        min(
            1.0,
            revision_need,
        ),
    )

    priority = (
        0.60 * mastery_gap
        + 0.40 * revision_need
    )

    return max(
        0.0,
        min(
            1.0,
            priority,
        ),
    )


def calculate_policy_priorities(
    mastery: float,
    confidence: float,
    revision_need: float,
    difficulty: float,
) -> dict:
    """
    Calculate priorities for all recommendation policies
    using the same learner state.
    """

    return {
        "mastery_only": calculate_mastery_only_priority(
            mastery=mastery,
        ),
        "revision_aware": calculate_revision_aware_priority(
            mastery=mastery,
            revision_need=revision_need,
        ),
        "adaptive": calculate_adaptive_priority(
            mastery=mastery,
            confidence=confidence,
            revision_need=revision_need,
            difficulty=difficulty,
            max_difficulty=5.0,
        ),
    }


def compare_recommendation_policies(
    learner_states: list[dict],
) -> dict:
    """
    Compare recommendation policies across learner states.

    Each learner state must contain:

    - mastery
    - confidence
    - revision_need
    - difficulty
    """

    if not learner_states:
        return {
            "sample_count": 0,
            "average_priority": {
                "mastery_only": 0.0,
                "revision_aware": 0.0,
                "adaptive": 0.0,
            },
        }

    totals = {
        "mastery_only": 0.0,
        "revision_aware": 0.0,
        "adaptive": 0.0,
    }

    for state in learner_states:
        priorities = calculate_policy_priorities(
            mastery=state["mastery"],
            confidence=state["confidence"],
            revision_need=state["revision_need"],
            difficulty=state["difficulty"],
        )

        for policy, priority in priorities.items():
            totals[policy] += priority

    sample_count = len(learner_states)

    averages = {
        policy: priority / sample_count
        for policy, priority in totals.items()
    }

    return {
        "sample_count": sample_count,
        "average_priority": averages,
    }