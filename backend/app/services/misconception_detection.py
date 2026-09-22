from dataclasses import dataclass


@dataclass(frozen=True)
class MisconceptionSignal:
    concept_id: int
    incorrect_attempts: int
    total_attempts: int
    error_rate: float
    detected: bool


def calculate_error_rate(
    incorrect_attempts: int,
    total_attempts: int,
) -> float:
    if total_attempts <= 0:
        return 0.0

    incorrect_attempts = max(
        0,
        min(incorrect_attempts, total_attempts),
    )

    return incorrect_attempts / total_attempts


def detect_misconception(
    concept_id: int,
    incorrect_attempts: int,
    total_attempts: int,
    minimum_attempts: int = 3,
    error_threshold: float = 0.60,
) -> MisconceptionSignal:
    if minimum_attempts <= 0:
        raise ValueError(
            "minimum_attempts must be greater than 0"
        )

    if not 0.0 <= error_threshold <= 1.0:
        raise ValueError(
            "error_threshold must be between 0.0 and 1.0"
        )

    incorrect_attempts = max(
        0,
        min(incorrect_attempts, total_attempts),
    )

    total_attempts = max(0, total_attempts)

    error_rate = calculate_error_rate(
        incorrect_attempts=incorrect_attempts,
        total_attempts=total_attempts,
    )

    detected = (
        total_attempts >= minimum_attempts
        and error_rate >= error_threshold
    )

    return MisconceptionSignal(
        concept_id=concept_id,
        incorrect_attempts=incorrect_attempts,
        total_attempts=total_attempts,
        error_rate=error_rate,
        detected=detected,
    )


def calculate_misconception_severity(
    error_rate: float,
) -> float:
    error_rate = max(0.0, min(1.0, error_rate))
    return error_rate