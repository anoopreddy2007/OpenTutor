from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptiveLearningDecision:
    action: str
    priority: float
    reason: str


def calculate_adaptive_policy_priority(
    mastery: float,
    confidence: float,
    revision_need: float,
    misconception_severity: float,
    prerequisites_ready: bool,
) -> float:
    mastery = max(0.0, min(1.0, mastery))
    confidence = max(0.0, min(1.0, confidence))
    revision_need = max(0.0, min(1.0, revision_need))
    misconception_severity = max(
        0.0,
        min(1.0, misconception_severity),
    )

    if not prerequisites_ready:
        return 0.0

    mastery_gap = 1.0 - mastery
    confidence_gap = 1.0 - confidence

    priority = (
        0.30 * mastery_gap
        + 0.20 * confidence_gap
        + 0.20 * revision_need
        + 0.30 * misconception_severity
    )

    return max(0.0, min(1.0, priority))


def determine_adaptive_action(
    mastery: float,
    confidence: float,
    revision_need: float,
    misconception_severity: float,
    prerequisites_ready: bool,
) -> AdaptiveLearningDecision:
    priority = calculate_adaptive_policy_priority(
        mastery=mastery,
        confidence=confidence,
        revision_need=revision_need,
        misconception_severity=misconception_severity,
        prerequisites_ready=prerequisites_ready,
    )

    mastery = max(0.0, min(1.0, mastery))
    confidence = max(0.0, min(1.0, confidence))
    revision_need = max(0.0, min(1.0, revision_need))
    misconception_severity = max(
        0.0,
        min(1.0, misconception_severity),
    )

    if not prerequisites_ready:
        return AdaptiveLearningDecision(
            action="REVIEW_PREREQUISITES",
            priority=priority,
            reason="Prerequisite concepts are not ready.",
        )

    if misconception_severity >= 0.70:
        return AdaptiveLearningDecision(
            action="REMEDIATE_MISCONCEPTION",
            priority=priority,
            reason="A strong misconception signal was detected.",
        )

    if mastery < 0.40:
        return AdaptiveLearningDecision(
            action="PRACTICE_CONCEPT",
            priority=priority,
            reason="Mastery is low and additional practice is needed.",
        )

    if revision_need >= 0.70:
        return AdaptiveLearningDecision(
            action="REVIEW_CONCEPT",
            priority=priority,
            reason="The concept has a high revision need.",
        )

    if confidence < 0.30:
        return AdaptiveLearningDecision(
            action="BUILD_CONFIDENCE",
            priority=priority,
            reason="Learner confidence is low.",
        )

    return AdaptiveLearningDecision(
        action="ADVANCE",
        priority=priority,
        reason="The learner is ready to continue.",
    )