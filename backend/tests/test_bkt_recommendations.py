from datetime import datetime, timedelta

from app.services.bkt_mastery import estimate_mastery
from app.services.recommendation_service import _calculate_priority


def test_lower_bkt_mastery_gets_higher_priority():
    current_time = datetime.utcnow()

    weak_mastery = estimate_mastery(
        [False, False, False]
    )

    strong_mastery = estimate_mastery(
        [True, True, True]
    )

    weak_priority = _calculate_priority(
        mastery=weak_mastery,
        difficulty=3,
        last_attempt_at=None,
        current_time=current_time,
    )

    strong_priority = _calculate_priority(
        mastery=strong_mastery,
        difficulty=3,
        last_attempt_at=None,
        current_time=current_time,
    )

    assert weak_priority > strong_priority


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


def test_revision_need_can_increase_priority():
    current_time = datetime.utcnow()

    mastery = estimate_mastery(
        [True, True]
    )

    recent_priority = _calculate_priority(
        mastery=mastery,
        difficulty=3,
        last_attempt_at=current_time,
        current_time=current_time,
    )

    old_priority = _calculate_priority(
        mastery=mastery,
        difficulty=3,
        last_attempt_at=current_time - timedelta(days=14),
        current_time=current_time,
    )

    assert old_priority > recent_priority