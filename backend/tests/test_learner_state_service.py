import pytest

from app.services.bkt_update import update_knowledge
from app.services.fsrs import (
    initialize_fsrs_state,
    update_fsrs_state,
)


def test_mastery_increases_after_correct_answer():
    old_mastery = 0.4

    new_mastery = update_knowledge(
        knowledge=old_mastery,
        is_correct=True,
    )

    assert new_mastery > old_mastery
    assert 0.0 <= new_mastery <= 1.0


def test_mastery_decreases_after_incorrect_answer():
    old_mastery = 0.7

    new_mastery = update_knowledge(
        knowledge=old_mastery,
        is_correct=False,
    )

    assert new_mastery < old_mastery
    assert 0.0 <= new_mastery <= 1.0


def test_correct_attempt_updates_fsrs_as_good_review():
    state = initialize_fsrs_state()

    updated_state = update_fsrs_state(
        state=state,
        rating=3,
        elapsed_days=1.0,
    )

    assert updated_state.stability > state.stability
    assert updated_state.difficulty == state.difficulty
    assert updated_state.retrievability == 1.0


def test_incorrect_attempt_updates_fsrs_as_again_review():
    state = initialize_fsrs_state()

    updated_state = update_fsrs_state(
        state=state,
        rating=1,
        elapsed_days=1.0,
    )

    assert updated_state.stability < state.stability
    assert updated_state.difficulty > state.difficulty
    assert updated_state.retrievability == 1.0


def test_good_review_increases_memory_stability_more_than_again():
    state = initialize_fsrs_state()

    good_state = update_fsrs_state(
        state=state,
        rating=3,
        elapsed_days=1.0,
    )

    again_state = update_fsrs_state(
        state=state,
        rating=1,
        elapsed_days=1.0,
    )

    assert good_state.stability > state.stability
    assert again_state.stability < state.stability
    assert good_state.stability > again_state.stability


def test_fsrs_state_values_remain_valid():
    state = initialize_fsrs_state()

    updated_state = update_fsrs_state(
        state=state,
        rating=3,
        elapsed_days=5.0,
    )

    assert updated_state.stability > 0.0
    assert 0.0 <= updated_state.difficulty <= 1.0
    assert 0.0 <= updated_state.retrievability <= 1.0