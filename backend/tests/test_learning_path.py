import pytest

from app.services.learning_path import (
    LearningPathCandidate,
    calculate_learning_path_priority,
    select_next_learning_concept,
)


def test_high_mastery_gap_increases_priority():
    priority = calculate_learning_path_priority(
        mastery=0.20,
        revision_need=0.0,
        misconception_severity=0.0,
        prerequisites_ready=True,
    )

    assert priority == pytest.approx(0.32)


def test_revision_need_increases_priority():
    priority = calculate_learning_path_priority(
        mastery=0.70,
        revision_need=1.0,
        misconception_severity=0.0,
        prerequisites_ready=True,
    )

    assert priority == pytest.approx(0.42)


def test_misconception_increases_priority():
    priority = calculate_learning_path_priority(
        mastery=0.70,
        revision_need=0.0,
        misconception_severity=1.0,
        prerequisites_ready=True,
    )

    assert priority == pytest.approx(0.42)


def test_unready_prerequisite_blocks_concept():
    priority = calculate_learning_path_priority(
        mastery=0.10,
        revision_need=1.0,
        misconception_severity=1.0,
        prerequisites_ready=False,
    )

    assert priority == 0.0


def test_priority_is_clamped():
    priority = calculate_learning_path_priority(
        mastery=-1.0,
        revision_need=2.0,
        misconception_severity=2.0,
        prerequisites_ready=True,
    )

    assert priority == 1.0


def test_empty_candidates_returns_no_concept():
    decision = select_next_learning_concept([])

    assert decision.concept_id is None
    assert decision.priority == 0.0


def test_selects_highest_priority_concept():
    candidates = [
        LearningPathCandidate(
            concept_id=1,
            mastery=0.80,
            revision_need=0.20,
            misconception_severity=0.10,
            prerequisites_ready=True,
        ),
        LearningPathCandidate(
            concept_id=2,
            mastery=0.30,
            revision_need=0.80,
            misconception_severity=0.70,
            prerequisites_ready=True,
        ),
    ]

    decision = select_next_learning_concept(candidates)

    assert decision.concept_id == 2
    assert decision.priority == pytest.approx(0.73)


def test_unready_concept_is_not_selected_over_ready_concept():
    candidates = [
        LearningPathCandidate(
            concept_id=1,
            mastery=0.10,
            revision_need=1.0,
            misconception_severity=1.0,
            prerequisites_ready=False,
        ),
        LearningPathCandidate(
            concept_id=2,
            mastery=0.40,
            revision_need=0.50,
            misconception_severity=0.20,
            prerequisites_ready=True,
        ),
    ]

    decision = select_next_learning_concept(candidates)

    assert decision.concept_id == 2


def test_all_unready_concepts_return_zero_priority():
    candidates = [
        LearningPathCandidate(
            concept_id=1,
            mastery=0.10,
            revision_need=1.0,
            misconception_severity=1.0,
            prerequisites_ready=False,
        ),
        LearningPathCandidate(
            concept_id=2,
            mastery=0.20,
            revision_need=0.80,
            misconception_severity=0.80,
            prerequisites_ready=False,
        ),
    ]

    decision = select_next_learning_concept(candidates)

    assert decision.concept_id == 1
    assert decision.priority == 0.0