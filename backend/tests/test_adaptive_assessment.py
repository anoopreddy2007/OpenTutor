from app.services.adaptive_assessment import (
    calculate_target_difficulty,
)


def test_high_mastery_and_confidence_increase_target_difficulty():
    result = calculate_target_difficulty(
        mastery=0.90,
        confidence=0.90,
        current_difficulty=3,
    )

    assert result.difficulty_adjustment > 0
    assert result.target_difficulty > 3


def test_low_mastery_and_confidence_decrease_target_difficulty():
    result = calculate_target_difficulty(
        mastery=0.20,
        confidence=0.20,
        current_difficulty=3,
    )

    assert result.difficulty_adjustment < 0
    assert result.target_difficulty < 3


def test_medium_readiness_keeps_difficulty_stable():
    result = calculate_target_difficulty(
        mastery=0.55,
        confidence=0.55,
        current_difficulty=3,
    )

    assert result.difficulty_adjustment == 0.0
    assert result.target_difficulty == 3


def test_target_difficulty_respects_maximum():
    result = calculate_target_difficulty(
        mastery=1.0,
        confidence=1.0,
        current_difficulty=5,
    )

    assert result.target_difficulty == 5


def test_target_difficulty_respects_minimum():
    result = calculate_target_difficulty(
        mastery=0.0,
        confidence=0.0,
        current_difficulty=1,
    )

    assert result.target_difficulty == 1


def test_mastery_and_confidence_are_clamped():
    result = calculate_target_difficulty(
        mastery=2.0,
        confidence=2.0,
        current_difficulty=3,
    )

    assert result.target_difficulty == 3.5


def test_invalid_difficulty_range_is_rejected():
    try:
        calculate_target_difficulty(
            mastery=0.5,
            confidence=0.5,
            current_difficulty=3,
            min_difficulty=5,
            max_difficulty=1,
        )
        assert False
    except ValueError:
        assert True