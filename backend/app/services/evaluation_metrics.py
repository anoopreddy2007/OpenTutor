from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMetrics:
    accuracy: float
    average_learning_signal: float
    average_confidence: float
    completion_rate: float


def calculate_accuracy(correct_answers: int, total_answers: int) -> float:
    if total_answers <= 0:
        return 0.0

    correct_answers = max(0, min(correct_answers, total_answers))
    return correct_answers / total_answers


def calculate_average_learning_signal(
    learning_signals: list[float],
) -> float:
    if not learning_signals:
        return 0.0

    normalized_signals = [
        max(0.0, min(1.0, signal))
        for signal in learning_signals
    ]

    return round(
        sum(normalized_signals) / len(normalized_signals),
        4,
    )


def calculate_average_confidence(
    confidence_signals: list[float],
) -> float:
    if not confidence_signals:
        return 0.0

    normalized_confidence = [
        max(0.0, min(1.0, confidence))
        for confidence in confidence_signals
    ]

    return round(
        sum(normalized_confidence) / len(normalized_confidence),
        4,
    )


def calculate_completion_rate(
    completed_sessions: int,
    total_sessions: int,
) -> float:
    if total_sessions <= 0:
        return 0.0

    completed_sessions = max(
        0,
        min(completed_sessions, total_sessions),
    )

    return completed_sessions / total_sessions


def calculate_evaluation_metrics(
    correct_answers: int,
    total_answers: int,
    learning_signals: list[float],
    confidence_signals: list[float],
    completed_sessions: int,
    total_sessions: int,
) -> EvaluationMetrics:
    return EvaluationMetrics(
        accuracy=calculate_accuracy(
            correct_answers=correct_answers,
            total_answers=total_answers,
        ),
        average_learning_signal=calculate_average_learning_signal(
            learning_signals
        ),
        average_confidence=calculate_average_confidence(
            confidence_signals
        ),
        completion_rate=calculate_completion_rate(
            completed_sessions=completed_sessions,
            total_sessions=total_sessions,
        ),
    )