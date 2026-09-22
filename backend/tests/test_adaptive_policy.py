import pytest

from app.services.adaptive_policy import (
    calculate_adaptive_policy_priority,
    determine_adaptive_action,
)


def test_priority_is_calculated():
    priority = calculate_adaptive_policy_priority(
        mastery=0.50,
        confidence=0.50,
        revision_need=0.50,
        misconception_severity=0.50,
        prerequisites_ready=True,
    )

    assert priority == pytest.approx(0.50)


def test_priority_is_zero_when_prerequisites_are_not_ready():
    priority = calculate_adaptive_policy_priority(
        mastery=0.10,
        confidence=0.10,
        revision_need=1.0,
        misconception_severity=1.0,
        prerequisites_ready=False,
    )

    assert priority == 0.0


def test_priority_values_are_clamped():
    priority = calculate_adaptive_policy_priority(
        mastery=-1.0,
        confidence=2.0,
        revision_need=2.0,
        misconception_severity=2.0,
        prerequisites_ready=True,
    )

    assert priority == pytest.approx(0.80)


def test_prerequisite_review_action():
    decision = determine_adaptive_action(
        mastery=0.80,
        confidence=0.80,
        revision_need=0.10,
        misconception_severity=0.10,
        prerequisites_ready=False,
    )

    assert decision.action == "REVIEW_PREREQUISITES"
    assert decision.priority == 0.0


def test_misconception_remediation_action():
    decision = determine_adaptive_action(
        mastery=0.60,
        confidence=0.60,
        revision_need=0.30,
        misconception_severity=0.80,
        prerequisites_ready=True,
    )

    assert decision.action == "REMEDIATE_MISCONCEPTION"
    assert decision.priority > 0.0


def test_low_mastery_practice_action():
    decision = determine_adaptive_action(
        mastery=0.20,
        confidence=0.70,
        revision_need=0.20,
        misconception_severity=0.20,
        prerequisites_ready=True,
    )

    assert decision.action == "PRACTICE_CONCEPT"


def test_high_revision_need_review_action():
    decision = determine_adaptive_action(
        mastery=0.60,
        confidence=0.70,
        revision_need=0.80,
        misconception_severity=0.20,
        prerequisites_ready=True,
    )

    assert decision.action == "REVIEW_CONCEPT"


def test_low_confidence_build_confidence_action():
    decision = determine_adaptive_action(
        mastery=0.70,
        confidence=0.20,
        revision_need=0.20,
        misconception_severity=0.20,
        prerequisites_ready=True,
    )

    assert decision.action == "BUILD_CONFIDENCE"


def test_ready_learner_can_advance():
    decision = determine_adaptive_action(
        mastery=0.90,
        confidence=0.90,
        revision_need=0.10,
        misconception_severity=0.10,
        prerequisites_ready=True,
    )

    assert decision.action == "ADVANCE"