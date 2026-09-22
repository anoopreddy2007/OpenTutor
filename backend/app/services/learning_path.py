from dataclasses import dataclass


@dataclass(frozen=True)
class LearningPathCandidate:
    concept_id: int
    mastery: float
    revision_need: float
    misconception_severity: float
    prerequisites_ready: bool


@dataclass(frozen=True)
class LearningPathDecision:
    concept_id: int | None
    priority: float


def calculate_learning_path_priority(
    mastery: float,
    revision_need: float,
    misconception_severity: float,
    prerequisites_ready: bool,
) -> float:
    mastery = max(0.0, min(1.0, mastery))
    revision_need = max(0.0, min(1.0, revision_need))
    misconception_severity = max(
        0.0,
        min(1.0, misconception_severity),
    )

    if not prerequisites_ready:
        return 0.0

    mastery_gap = 1.0 - mastery

    priority = (
        0.40 * mastery_gap
        + 0.30 * revision_need
        + 0.30 * misconception_severity
    )

    return max(0.0, min(1.0, priority))


def select_next_learning_concept(
    candidates: list[LearningPathCandidate],
) -> LearningPathDecision:
    if not candidates:
        return LearningPathDecision(
            concept_id=None,
            priority=0.0,
        )

    best_concept_id = None
    best_priority = -1.0

    for candidate in candidates:
        priority = calculate_learning_path_priority(
            mastery=candidate.mastery,
            revision_need=candidate.revision_need,
            misconception_severity=candidate.misconception_severity,
            prerequisites_ready=candidate.prerequisites_ready,
        )

        if priority > best_priority:
            best_priority = priority
            best_concept_id = candidate.concept_id

    if best_priority < 0.0:
        return LearningPathDecision(
            concept_id=None,
            priority=0.0,
        )

    return LearningPathDecision(
        concept_id=best_concept_id,
        priority=best_priority,
    )