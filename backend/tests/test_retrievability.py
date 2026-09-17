from datetime import datetime, timedelta

import pytest

from app.services.retrievability import (
    calculate_elapsed_days,
    calculate_retrievability,
)


def test_no_previous_review_returns_zero():
    current_time = datetime.utcnow()

    retrievability = calculate_retrievability(
        last_review_at=None,
        current_time=current_time,
        stability=5.0,
    )

    assert retrievability == 0.0


def test_retrievability_is_high_immediately_after_review():
    current_time = datetime.utcnow()

    retrievability = calculate_retrievability(
        last_review_at=current_time,
        current_time=current_time,
        stability=5.0,
    )

    assert retrievability == 1.0


def test_retrievability_decreases_over_time():
    current_time = datetime.utcnow()

    recent = calculate_retrievability(
        last_review_at=current_time - timedelta(days=1),
        current_time=current_time,
        stability=5.0,
    )

    old = calculate_retrievability(
        last_review_at=current_time - timedelta(days=20),
        current_time=current_time,
        stability=5.0,
    )

    assert recent > old


def test_higher_stability_preserves_retrievability():
    current_time = datetime.utcnow()
    review_time = current_time - timedelta(days=10)

    low_stability = calculate_retrievability(
        last_review_at=review_time,
        current_time=current_time,
        stability=2.0,
    )

    high_stability = calculate_retrievability(
        last_review_at=review_time,
        current_time=current_time,
        stability=10.0,
    )

    assert high_stability > low_stability


def test_retrievability_stays_within_valid_range():
    current_time = datetime.utcnow()

    retrievability = calculate_retrievability(
        last_review_at=current_time - timedelta(days=1000),
        current_time=current_time,
        stability=1.0,
    )

    assert 0.0 <= retrievability <= 1.0


def test_negative_elapsed_time_is_treated_as_zero():
    current_time = datetime.utcnow()

    retrievability = calculate_retrievability(
        last_review_at=current_time + timedelta(days=1),
        current_time=current_time,
        stability=5.0,
    )

    assert retrievability == 1.0


def test_invalid_stability_is_rejected():
    current_time = datetime.utcnow()

    with pytest.raises(ValueError):
        calculate_retrievability(
            last_review_at=current_time,
            current_time=current_time,
            stability=0.0,
        )


def test_elapsed_days_is_calculated_correctly():
    current_time = datetime.utcnow()
    review_time = current_time - timedelta(days=5)

    elapsed_days = calculate_elapsed_days(
        last_review_at=review_time,
        current_time=current_time,
    )

    assert elapsed_days == pytest.approx(5.0)