import pytest

from app.services.fsrs import (
    FSRSParameters,
    FSRSState,
    calculate_retrievability,
    initialize_fsrs_state,
    update_fsrs_state,
)


def test_default_parameters_are_valid():
    parameters = FSRSParameters()

    assert parameters.initial_stability > 0
    assert 0.0 <= parameters.initial_difficulty <= 1.0
    assert 0.0 < parameters.target_retrievability < 1.0


def test_invalid_initial_stability_raises_error():
    with pytest.raises(ValueError):
        FSRSParameters(
            initial_stability=0.0,
        )


def test_invalid_initial_difficulty_raises_error():
    with pytest.raises(ValueError):
        FSRSParameters(
            initial_difficulty=1.5,
        )


def test_invalid_target_retrievability_raises_error():
    with pytest.raises(ValueError):
        FSRSParameters(
            target_retrievability=1.0,
        )


def test_retrievability_is_one_at_review_time():
    retrievability = calculate_retrievability(
        elapsed_days=0.0,
        stability=1.0,
    )

    assert retrievability == pytest.approx(1.0)


def test_retrievability_decreases_with_time():
    current = calculate_retrievability(
        elapsed_days=0.0,
        stability=5.0,
    )

    later = calculate_retrievability(
        elapsed_days=5.0,
        stability=5.0,
    )

    assert later < current


def test_higher_stability_slows_decay():
    low_stability = calculate_retrievability(
        elapsed_days=5.0,
        stability=2.0,
    )

    high_stability = calculate_retrievability(
        elapsed_days=5.0,
        stability=10.0,
    )

    assert high_stability > low_stability


def test_invalid_stability_raises_error():
    with pytest.raises(ValueError):
        calculate_retrievability(
            elapsed_days=1.0,
            stability=0.0,
        )


def test_initial_fsrs_state():
    state = initialize_fsrs_state()

    assert isinstance(state, FSRSState)
    assert state.stability == 1.0
    assert state.difficulty == 0.3
    assert state.retrievability == 1.0


def test_good_review_increases_stability():
    state = initialize_fsrs_state()

    updated = update_fsrs_state(
        state=state,
        rating=3,
        elapsed_days=1.0,
    )

    assert updated.stability > state.stability


def test_easy_review_increases_stability_more_than_good():
    state = initialize_fsrs_state()

    good = update_fsrs_state(
        state=state,
        rating=3,
        elapsed_days=1.0,
    )

    easy = update_fsrs_state(
        state=state,
        rating=4,
        elapsed_days=1.0,
    )

    assert easy.stability > good.stability


def test_again_review_reduces_stability():
    state = initialize_fsrs_state()

    updated = update_fsrs_state(
        state=state,
        rating=1,
        elapsed_days=1.0,
    )

    assert updated.stability < state.stability


def test_hard_review_increases_difficulty():
    state = initialize_fsrs_state()

    updated = update_fsrs_state(
        state=state,
        rating=2,
        elapsed_days=1.0,
    )

    assert updated.difficulty > state.difficulty


def test_easy_review_reduces_difficulty():
    state = initialize_fsrs_state()

    updated = update_fsrs_state(
        state=state,
        rating=4,
        elapsed_days=1.0,
    )

    assert updated.difficulty < state.difficulty


def test_invalid_rating_raises_error():
    state = initialize_fsrs_state()

    with pytest.raises(ValueError):
        update_fsrs_state(
            state=state,
            rating=5,
            elapsed_days=1.0,
        )


def test_negative_elapsed_days_raises_error():
    state = initialize_fsrs_state()

    with pytest.raises(ValueError):
        update_fsrs_state(
            state=state,
            rating=3,
            elapsed_days=-1.0,
        )