from dataclasses import dataclass


@dataclass(frozen=True)
class DifficultyCalibration:
    """
    Result of calibrating a question's difficulty
    against the learner's response.
    """

    current_difficulty: float
    calibrated_difficulty: float
    adjustment: float


def calibrate_question_difficulty(
    current_difficulty: int | float,
    learning_signal: float,
    confidence_signal: float,
    min_difficulty: float = 1.0,
    max_difficulty: float = 5.0,
) -> DifficultyCalibration:
    """
    Adjust question difficulty based on learner performance.

    Strong performance can justify increasing difficulty,
    while weak performance can justify decreasing difficulty.

    The difficulty is always kept within the configured range.
    """

    if min_difficulty >= max_difficulty:
        raise ValueError(
            "min_difficulty must be less than max_difficulty"
        )

    current_difficulty = max(
        min_difficulty,
        min(max_difficulty, float(current_difficulty)),
    )

    learning_signal = max(
        0.0,
        min(1.0, learning_signal),
    )

    confidence_signal = max(
        0.0,
        min(1.0, confidence_signal),
    )

    performance_signal = (
        0.70 * learning_signal
        + 0.30 * confidence_signal
    )

    if performance_signal >= 0.80:
        adjustment = 0.50

    elif performance_signal >= 0.60:
        adjustment = 0.25

    elif performance_signal <= 0.30:
        adjustment = -0.50

    elif performance_signal <= 0.45:
        adjustment = -0.25

    else:
        adjustment = 0.0

    calibrated_difficulty = max(
        min_difficulty,
        min(
            max_difficulty,
            current_difficulty + adjustment,
        ),
    )

    return DifficultyCalibration(
        current_difficulty=current_difficulty,
        calibrated_difficulty=calibrated_difficulty,
        adjustment=adjustment,
    )