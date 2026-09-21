from dataclasses import dataclass


@dataclass(frozen=True)
class AttemptAnalysis:
    """
    Derived information about a learner's attempt.

    The analysis does not modify the stored attempt.
    It converts correctness, confidence, and response time
    into signals that can be used by adaptive assessment.
    """

    correctness_signal: float
    confidence_signal: float
    speed_signal: float
    learning_signal: float


def normalize_confidence(confidence: int | None) -> float:
    """
    Convert confidence from the stored 1-5 scale
    into a 0-1 scale.

    Missing confidence is treated as neutral.
    """

    if confidence is None:
        return 0.5

    confidence = max(1, min(5, confidence))

    return (confidence - 1) / 4.0


def calculate_speed_signal(
    time_taken: float | None,
    expected_time: float = 60.0,
) -> float:
    """
    Estimate how quickly a learner answered.

    A response at or below expected_time receives a
    maximum speed signal.

    Slower responses receive progressively lower values.
    """

    if expected_time <= 0:
        raise ValueError("expected_time must be greater than 0")

    if time_taken is None:
        return 0.5

    if time_taken < 0:
        raise ValueError("time_taken cannot be negative")

    if time_taken == 0:
        return 1.0

    speed_signal = expected_time / time_taken

    return max(0.0, min(1.0, speed_signal))


def analyze_attempt(
    is_correct: bool,
    confidence: int | None,
    time_taken: float | None,
    expected_time: float = 60.0,
) -> AttemptAnalysis:
    """
    Analyze a learner response using correctness,
    confidence, and response time.
    """

    correctness_signal = 1.0 if is_correct else 0.0

    confidence_signal = normalize_confidence(
        confidence
    )

    speed_signal = calculate_speed_signal(
        time_taken=time_taken,
        expected_time=expected_time,
    )

    learning_signal = (
        0.50 * correctness_signal
        + 0.30 * confidence_signal
        + 0.20 * speed_signal
    )

    return AttemptAnalysis(
        correctness_signal=correctness_signal,
        confidence_signal=confidence_signal,
        speed_signal=speed_signal,
        learning_signal=max(
            0.0,
            min(1.0, learning_signal),
        ),
    )