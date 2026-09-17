from datetime import datetime, timedelta

from app.services.bkt_mastery import estimate_mastery
from app.services.recommendation_service import (
    _calculate_priority,
    _calculate_revision_need,
)


def test_revision_need_is_zero_for_missing_revision_state():
    current_time = datetime.utcnow()

    revision_need = _calculate_revision_need(
        revision_state=None,
        current_time=current_time,
    )

    assert revision_need == 0.0


def test_revision_need_increases_as_review_date_approaches():
    last_review = datetime.utcnow()

    revision_state = type(
        "RevisionStateStub",
        (),
        {
            "last_review_at": last_review,
            "next_review_at": last_review + timedelta(days=10),
        },
    )()

    early = _calculate_revision_need(
        revision_state=revision_state,
        current_time=last_review + timedelta(days=2),
    )

    late = _calculate_revision_need(
        revision_state=revision_state,
        current_time=last_review + timedelta(days=9),
    )

    assert late > early


def test_revision_need_is_one_when_review_is_due():
    last_review = datetime.utcnow()

    revision_state = type(
        "RevisionStateStub",
        (),
        {
            "last_review_at": last_review,
            "next_review_at": last_review + timedelta(days=7),
        },
    )()

    current_time = last_review + timedelta(days=8)

    revision_need = _calculate_revision_need(
        revision_state=revision_state,
        current_time=current_time,
    )

    assert revision_need == 1.0


def test_revision_need_stays_between_zero_and_one():
    last_review = datetime.utcnow()

    revision_state = type(
        "RevisionStateStub",
        (),
        {
            "last_review_at": last_review,
            "next_review_at": last_review + timedelta(days=7),
        },
    )()

    revision_need = _calculate_revision_need(
        revision_state=revision_state,
        current_time=last_review + timedelta(days=3),
    )

    assert 0.0 <= revision_need <= 1.0


def test_revision_urgency_increases_priority():
    current_time = datetime.utcnow()

    last_review = current_time - timedelta(days=8)

    # The review is already due.
    revision_state = type(
        "RevisionStateStub",
        (),
        {
            "last_review_at": last_review,
            "next_review_at": current_time - timedelta(days=1),
        },
    )()

    priority_with_revision = _calculate_priority(
        mastery=0.70,
        difficulty=3,
        last_attempt_at=last_review,
        current_time=current_time,
        revision_state=revision_state,
    )

    priority_without_revision = _calculate_priority(
        mastery=0.70,
        difficulty=3,
        last_attempt_at=None,
        current_time=current_time,
        revision_state=None,
    )

    assert priority_with_revision > priority_without_revision


def test_bkt_mastery_affects_recommendation_priority():
    current_time = datetime.utcnow()

    low_mastery = estimate_mastery(
        [False, False]
    )

    high_mastery = estimate_mastery(
        [True, True]
    )

    low_priority = _calculate_priority(
        mastery=low_mastery,
        difficulty=2,
        last_attempt_at=None,
        current_time=current_time,
    )

    high_priority = _calculate_priority(
        mastery=high_mastery,
        difficulty=2,
        last_attempt_at=None,
        current_time=current_time,
    )

    assert low_priority != high_priority