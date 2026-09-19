from app.services.recommendation_evaluation import (
    calculate_mastery_only_priority,
    calculate_revision_aware_priority,
    calculate_policy_priorities,
    compare_recommendation_policies,
)


def test_low_mastery_has_higher_baseline_priority():
    low_mastery = calculate_mastery_only_priority(
        mastery=0.2,
    )

    high_mastery = calculate_mastery_only_priority(
        mastery=0.8,
    )

    assert low_mastery > high_mastery


def test_revision_need_increases_revision_aware_priority():
    no_revision = calculate_revision_aware_priority(
        mastery=0.6,
        revision_need=0.0,
    )

    urgent_revision = calculate_revision_aware_priority(
        mastery=0.6,
        revision_need=1.0,
    )

    assert urgent_revision > no_revision


def test_policy_priorities_returns_all_policies():
    priorities = calculate_policy_priorities(
        mastery=0.5,
        confidence=0.6,
        revision_need=0.4,
        difficulty=3,
    )

    assert set(priorities.keys()) == {
        "mastery_only",
        "revision_aware",
        "adaptive",
    }


def test_adaptive_policy_responds_to_confidence():
    low_confidence = calculate_policy_priorities(
        mastery=0.6,
        confidence=0.2,
        revision_need=0.0,
        difficulty=2,
    )

    high_confidence = calculate_policy_priorities(
        mastery=0.6,
        confidence=0.9,
        revision_need=0.0,
        difficulty=2,
    )

    assert (
        low_confidence["adaptive"]
        > high_confidence["adaptive"]
    )


def test_compare_policies_returns_sample_count():
    learner_states = [
        {
            "mastery": 0.2,
            "confidence": 0.3,
            "revision_need": 0.8,
            "difficulty": 3,
        },
        {
            "mastery": 0.7,
            "confidence": 0.8,
            "revision_need": 0.2,
            "difficulty": 2,
        },
    ]

    result = compare_recommendation_policies(
        learner_states
    )

    assert result["sample_count"] == 2


def test_compare_policies_returns_average_priorities():
    learner_states = [
        {
            "mastery": 0.2,
            "confidence": 0.3,
            "revision_need": 0.8,
            "difficulty": 3,
        },
        {
            "mastery": 0.7,
            "confidence": 0.8,
            "revision_need": 0.2,
            "difficulty": 2,
        },
    ]

    result = compare_recommendation_policies(
        learner_states
    )

    averages = result["average_priority"]

    assert set(averages.keys()) == {
        "mastery_only",
        "revision_aware",
        "adaptive",
    }

    for priority in averages.values():
        assert 0.0 <= priority <= 1.0


def test_empty_evaluation_is_supported():
    result = compare_recommendation_policies([])

    assert result["sample_count"] == 0

    assert result["average_priority"] == {
        "mastery_only": 0.0,
        "revision_aware": 0.0,
        "adaptive": 0.0,
    }