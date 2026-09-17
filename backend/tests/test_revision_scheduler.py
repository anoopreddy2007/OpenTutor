from datetime import datetime, timedelta

import pytest

from app.services.revision_scheduler import (
    calculate_review_interval,
    is_review_due,
    schedule_next_review,
)


def test_review_interval_is_positive():
    interval = calculate_review_interval(
        stability=5.0,
    )

    assert interval > 0


def test_higher_stability_produces_longer_interval():
    low_stability = calculate_review_interval(
        stability=2.0,
    )

    high_stability = calculate_review_interval(
        stability=10.0,
    )

    assert high_stability > low_stability


def test_invalid_stability_is_rejected():
    with pytest.raises(ValueError):
        calculate_review_interval(
            stability=0.0,
        )


def test_invalid_target_retrievability_is_rejected():
    with pytest.raises(ValueError):
        calculate_review_interval(
            stability=5.0,
            target_retrievability=1.0,
        )


def test_next_review_is_after_last_review():
    last_review = datetime.utcnow()

    next_review = schedule_next_review(
        last_review_at=last_review,
        stability=5.0,
    )

    assert next_review > last_review


def test_review_is_due_without_previous_review():
    current_time = datetime.utcnow()

    assert is_review_due(
        last_review_at=None,
        stability=5.0,
        current_time=current_time,
    )


def test_recent_review_is_not_due():
    current_time = datetime.utcnow()

    assert not is_review_due(
        last_review_at=current_time,
        stability=5.0,
        current_time=current_time,
    )


def test_old_review_becomes_due():
    current_time = datetime.utcnow()

    old_review = current_time - timedelta(days=30)

    assert is_review_due(
        last_review_at=old_review,
        stability=1.0,
        current_time=current_time,
    )


def test_interval_is_bounded():
    interval = calculate_review_interval(
        stability=1000.0,
    )

    assert interval <= 30.0

    interval = calculate_review_interval(
        stability=0.01,
    )

    assert interval >= 1.0