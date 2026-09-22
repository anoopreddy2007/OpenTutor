import pytest

from app.services.misconception_detection import (
    calculate_error_rate,
    calculate_misconception_severity,
    detect_misconception,
)


def test_calculate_error_rate():
    assert calculate_error_rate(3, 5) == 0.6


def test_error_rate_returns_zero_for_no_attempts():
    assert calculate_error_rate(0, 0) == 0.0


def test_error_rate_clamps_invalid_counts():
    assert calculate_error_rate(8, 5) == 1.0
    assert calculate_error_rate(-2, 5) == 0.0


def test_misconception_is_detected():
    signal = detect_misconception(
        concept_id=10,
        incorrect_attempts=3,
        total_attempts=5,
    )

    assert signal.concept_id == 10
    assert signal.incorrect_attempts == 3
    assert signal.total_attempts == 5
    assert signal.error_rate == 0.6
    assert signal.detected is True


def test_misconception_is_not_detected_with_low_error_rate():
    signal = detect_misconception(
        concept_id=10,
        incorrect_attempts=2,
        total_attempts=5,
    )

    assert signal.error_rate == 0.4
    assert signal.detected is False


def test_misconception_requires_minimum_attempts():
    signal = detect_misconception(
        concept_id=10,
        incorrect_attempts=2,
        total_attempts=2,
        minimum_attempts=3,
    )

    assert signal.error_rate == 1.0
    assert signal.detected is False


def test_custom_error_threshold():
    signal = detect_misconception(
        concept_id=10,
        incorrect_attempts=2,
        total_attempts=5,
        error_threshold=0.40,
    )

    assert signal.detected is True


def test_invalid_minimum_attempts():
    with pytest.raises(ValueError):
        detect_misconception(
            concept_id=10,
            incorrect_attempts=1,
            total_attempts=2,
            minimum_attempts=0,
        )


def test_invalid_error_threshold():
    with pytest.raises(ValueError):
        detect_misconception(
            concept_id=10,
            incorrect_attempts=1,
            total_attempts=2,
            error_threshold=1.5,
        )


def test_misconception_severity():
    assert calculate_misconception_severity(0.75) == 0.75


def test_misconception_severity_is_clamped():
    assert calculate_misconception_severity(-1.0) == 0.0
    assert calculate_misconception_severity(2.0) == 1.0