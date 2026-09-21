from app.services.evaluation_metrics import (
    calculate_accuracy,
    calculate_average_confidence,
    calculate_average_learning_signal,
    calculate_completion_rate,
    calculate_evaluation_metrics,
)


def test_calculate_accuracy():
    assert calculate_accuracy(8, 10) == 0.8


def test_accuracy_returns_zero_for_no_answers():
    assert calculate_accuracy(0, 0) == 0.0


def test_accuracy_clamps_invalid_counts():
    assert calculate_accuracy(12, 10) == 1.0
    assert calculate_accuracy(-2, 10) == 0.0


def test_calculate_average_learning_signal():
    signals = [0.8, 0.6, 1.0]
    assert calculate_average_learning_signal(signals) == 0.8


def test_average_learning_signal_returns_zero_for_empty_list():
    assert calculate_average_learning_signal([]) == 0.0


def test_learning_signal_values_are_clamped():
    signals = [-1.0, 0.5, 2.0]
    assert calculate_average_learning_signal(signals) == 0.5


def test_calculate_average_confidence():
    confidence = [0.8, 0.6, 1.0]
    assert calculate_average_confidence(confidence) == 0.8


def test_average_confidence_returns_zero_for_empty_list():
    assert calculate_average_confidence([]) == 0.0


def test_confidence_values_are_clamped():
    confidence = [-1.0, 0.5, 2.0]
    assert calculate_average_confidence(confidence) == 0.5


def test_calculate_completion_rate():
    assert calculate_completion_rate(8, 10) == 0.8


def test_completion_rate_returns_zero_for_no_sessions():
    assert calculate_completion_rate(0, 0) == 0.0


def test_completion_rate_clamps_invalid_counts():
    assert calculate_completion_rate(12, 10) == 1.0
    assert calculate_completion_rate(-2, 10) == 0.0


def test_calculate_evaluation_metrics():
    metrics = calculate_evaluation_metrics(
        correct_answers=8,
        total_answers=10,
        learning_signals=[0.8, 0.6, 1.0],
        confidence_signals=[0.7, 0.8, 0.9],
        completed_sessions=4,
        total_sessions=5,
    )

    assert metrics.accuracy == 0.8
    assert metrics.average_learning_signal == 0.8
    assert metrics.average_confidence == 0.8
    assert metrics.completion_rate == 0.8