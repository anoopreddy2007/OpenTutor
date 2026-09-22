from dataclasses import dataclass


PREREQUISITE_MASTERY_THRESHOLD = 0.70


@dataclass(frozen=True)
class ConceptDependency:
    concept_id: int
    prerequisite_id: int


@dataclass(frozen=True)
class DependencyStatus:
    concept_id: int
    prerequisite_id: int
    mastery: float
    ready: bool


def is_prerequisite_ready(
    mastery: float,
    threshold: float = PREREQUISITE_MASTERY_THRESHOLD,
) -> bool:
    mastery = max(0.0, min(1.0, mastery))

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "threshold must be between 0.0 and 1.0"
        )

    return mastery >= threshold


def evaluate_dependency(
    dependency: ConceptDependency,
    prerequisite_mastery: float,
    threshold: float = PREREQUISITE_MASTERY_THRESHOLD,
) -> DependencyStatus:
    prerequisite_mastery = max(
        0.0,
        min(1.0, prerequisite_mastery),
    )

    ready = is_prerequisite_ready(
        mastery=prerequisite_mastery,
        threshold=threshold,
    )

    return DependencyStatus(
        concept_id=dependency.concept_id,
        prerequisite_id=dependency.prerequisite_id,
        mastery=prerequisite_mastery,
        ready=ready,
    )


def calculate_dependency_gap(
    prerequisite_masteries: list[float],
    threshold: float = PREREQUISITE_MASTERY_THRESHOLD,
) -> float:
    if not prerequisite_masteries:
        return 0.0

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "threshold must be between 0.0 and 1.0"
        )

    normalized_masteries = [
        max(0.0, min(1.0, mastery))
        for mastery in prerequisite_masteries
    ]

    average_mastery = (
        sum(normalized_masteries)
        / len(normalized_masteries)
    )

    return max(0.0, threshold - average_mastery)


def all_prerequisites_ready(
    prerequisite_masteries: list[float],
    threshold: float = PREREQUISITE_MASTERY_THRESHOLD,
) -> bool:
    if not prerequisite_masteries:
        return True

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "threshold must be between 0.0 and 1.0"
        )

    return all(
        is_prerequisite_ready(
            mastery=mastery,
            threshold=threshold,
        )
        for mastery in prerequisite_masteries
    )