from datetime import datetime, timedelta

import pytest

from app.services.fsrs_scheduler import (
    calculate_fsrs_review_interval,
    schedule_next_fsrs_review,
    is_fsrs_review_due,
)


def test_higher_stability_produces_longer_interval():
    low_stability = calculate_fsrs_review_interval(
        stability=2.0,
    )

    high_stability = calculate_fsrs_review_interval(
        stability=10.0,
    )

    assert high_stability > low_stability


def test_lower_target_retrievability_produces_longer_interval():
    high_target = calculate_fsrs_review_interval(
        stability=5.0,
        target_retrievability=0.95,
    )

    lower_target = calculate_fsrs_review_interval(
        stability=5.0,
        target_retrievability=0.80,
    )

    assert lower_target > high_target


def test_interval_is_at_least_one_day():
    interval = calculate_fsrs_review_interval(
        stability=0.01,
    )

    assert interval >= 1.0


def test_interval_is_at_most_thirty_days():
    interval = calculate_fsrs_review_interval(
        stability=1000.0,
    )

    assert interval <= 30.0


def test_invalid_stability_raises_error():
    with pytest.raises(ValueError):
        calculate_fsrs_review_interval(
            stability=0.0,
        )


def test_invalid_target_retrievability_raises_error():
    with pytest.raises(ValueError):
        calculate_fsrs_review_interval(
            stability=5.0,
            target_retrievability=1.0,
        )


def test_next_review_is_after_last_review():
    last_review = datetime(2026, 9, 20, 10, 0, 0)

    next_review = schedule_next_fsrs_review(
        last_review_at=last_review,
        stability=5.0,
    )

    assert next_review > last_review


def test_review_is_due_when_no_previous_review_exists():
    current_time = datetime(2026, 9, 20, 10, 0, 0)

    assert is_fsrs_review_due(
        last_review_at=None,
        stability=5.0,
        current_time=current_time,
    )


def test_review_is_not_due_immediately_after_review():
    current_time = datetime(2026, 9, 20, 10, 0, 0)

    assert not is_fsrs_review_due(
        last_review_at=current_time,
        stability=5.0,
        current_time=current_time,
    )


def test_review_becomes_due_after_interval():
    last_review = datetime(2026, 9, 1, 10, 0, 0)
    current_time = last_review + timedelta(days=30)

    assert is_fsrs_review_due(
        last_review_at=last_review,
        stability=5.0,
        current_time=current_time,
    )


def test_invalid_stability_for_due_check_raises_error():
    current_time = datetime(2026, 9, 20, 10, 0, 0)

    with pytest.raises(ValueError):
        is_fsrs_review_due(
            last_review_at=current_time,
            stability=0.0,
            current_time=current_time,
        )