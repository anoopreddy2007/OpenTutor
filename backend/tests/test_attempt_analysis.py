from app.services.attempt_analysis import (
    analyze_attempt,
    calculate_speed_signal,
    normalize_confidence,
)


def test_confidence_is_normalized_to_zero_one():
    assert normalize_confidence(1) == 0.0
    assert normalize_confidence(3) == 0.5
    assert normalize_confidence(5) == 1.0


def test_missing_confidence_is_neutral():
    assert normalize_confidence(None) == 0.5


def test_fast_response_has_high_speed_signal():
    signal = calculate_speed_signal(
        time_taken=30,
        expected_time=60,
    )

    assert signal == 1.0


def test_slow_response_has_lower_speed_signal():
    signal = calculate_speed_signal(
        time_taken=120,
        expected_time=60,
    )

    assert signal == 0.5


def test_attempt_analysis_rewards_correct_confident_fast_response():
    analysis = analyze_attempt(
        is_correct=True,
        confidence=5,
        time_taken=20,
    )

    assert analysis.correctness_signal == 1.0
    assert analysis.confidence_signal == 1.0
    assert analysis.speed_signal == 1.0
    assert analysis.learning_signal == 1.0


def test_attempt_analysis_penalizes_incorrect_response():
    analysis = analyze_attempt(
        is_correct=False,
        confidence=2,
        time_taken=120,
    )

    assert analysis.correctness_signal == 0.0
    assert analysis.confidence_signal == 0.25
    assert analysis.speed_signal == 0.5
    assert 0.0 <= analysis.learning_signal < 0.5


def test_negative_time_is_rejected():
    try:
        calculate_speed_signal(
            time_taken=-1,
            expected_time=60,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_expected_time_is_rejected():
    try:
        calculate_speed_signal(
            time_taken=30,
            expected_time=0,
        )
        assert False
    except ValueError:
        assert True