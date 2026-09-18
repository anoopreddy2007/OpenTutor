import pytest

from app.services.adaptive_decision import (
    calculate_adaptive_priority,
)


def test_low_mastery_increases_priority():
    low_mastery = calculate_adaptive_priority(
        mastery=0.2,
        confidence=0.8,
        revision_need=0.0,
        difficulty=2,
    )

    high_mastery = calculate_adaptive_priority(
        mastery=0.8,
        confidence=0.8,
        revision_need=0.0,
        difficulty=2,
    )

    assert low_mastery > high_mastery


def test_low_confidence_increases_priority():
    low_confidence = calculate_adaptive_priority(
        mastery=0.6,
        confidence=0.2,
        revision_need=0.0,
        difficulty=2,
    )

    high_confidence = calculate_adaptive_priority(
        mastery=0.6,
        confidence=0.9,
        revision_need=0.0,
        difficulty=2,
    )

    assert low_confidence > high_confidence


def test_revision_need_increases_priority():
    no_revision = calculate_adaptive_priority(
        mastery=0.6,
        confidence=0.8,
        revision_need=0.0,
        difficulty=2,
    )

    urgent_revision = calculate_adaptive_priority(
        mastery=0.6,
        confidence=0.8,
        revision_need=1.0,
        difficulty=2,
    )

    assert urgent_revision > no_revision


def test_priority_stays_between_zero_and_one():
    priority = calculate_adaptive_priority(
        mastery=0.0,
        confidence=0.0,
        revision_need=1.0,
        difficulty=5,
    )

    assert 0.0 <= priority <= 1.0


def test_invalid_max_difficulty_raises_error():
    with pytest.raises(ValueError):
        calculate_adaptive_priority(
            mastery=0.5,
            confidence=0.5,
            revision_need=0.5,
            difficulty=3,
            max_difficulty=0,
        )