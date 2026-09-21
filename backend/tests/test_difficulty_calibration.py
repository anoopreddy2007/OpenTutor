from app.services.difficulty_calibration import (
    calibrate_question_difficulty,
)


def test_strong_performance_increases_difficulty():
    result = calibrate_question_difficulty(
        current_difficulty=3,
        learning_signal=0.95,
        confidence_signal=1.0,
    )

    assert result.adjustment > 0
    assert result.calibrated_difficulty > 3


def test_weak_performance_decreases_difficulty():
    result = calibrate_question_difficulty(
        current_difficulty=3,
        learning_signal=0.10,
        confidence_signal=0.20,
    )

    assert result.adjustment < 0
    assert result.calibrated_difficulty < 3


def test_medium_performance_keeps_difficulty_stable():
    result = calibrate_question_difficulty(
        current_difficulty=3,
        learning_signal=0.50,
        confidence_signal=0.50,
    )

    assert result.adjustment == 0.0
    assert result.calibrated_difficulty == 3


def test_difficulty_does_not_exceed_maximum():
    result = calibrate_question_difficulty(
        current_difficulty=5,
        learning_signal=1.0,
        confidence_signal=1.0,
    )

    assert result.calibrated_difficulty == 5


def test_difficulty_does_not_go_below_minimum():
    result = calibrate_question_difficulty(
        current_difficulty=1,
        learning_signal=0.0,
        confidence_signal=0.0,
    )

    assert result.calibrated_difficulty == 1


def test_learning_signal_is_clamped():
    result = calibrate_question_difficulty(
        current_difficulty=3,
        learning_signal=2.0,
        confidence_signal=2.0,
    )

    assert result.calibrated_difficulty == 3.5


def test_invalid_difficulty_range_is_rejected():
    try:
        calibrate_question_difficulty(
            current_difficulty=3,
            learning_signal=0.5,
            confidence_signal=0.5,
            min_difficulty=5,
            max_difficulty=1,
        )
        assert False
    except ValueError:
        assert True