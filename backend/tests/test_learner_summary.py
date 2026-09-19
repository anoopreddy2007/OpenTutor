from datetime import datetime, timedelta

from app.services.learner_summary import build_learner_summary


def test_build_learner_summary():
    summary = build_learner_summary(
        mastery=0.6,
        confidence=0.8,
        attempts_count=10,
        correct_count=7,
    )

    assert summary["mastery"] == 0.6
    assert summary["confidence"] == 0.8
    assert summary["mastery_level"] == "developing"
    assert summary["attempts_count"] == 10
    assert summary["correct_count"] == 7
    assert summary["accuracy"] == 0.7


def test_summary_handles_no_attempts():
    summary = build_learner_summary(
        mastery=0.0,
        confidence=0.0,
        attempts_count=0,
        correct_count=0,
    )

    assert summary["accuracy"] == 0.0


def test_summary_includes_revision_information():
    current_time = datetime.utcnow()
    last_review = current_time - timedelta(days=5)

    summary = build_learner_summary(
        mastery=0.7,
        confidence=0.8,
        attempts_count=10,
        correct_count=7,
        last_review_at=last_review,
        stability=2.0,
        current_time=current_time,
    )

    assert "revision_need" in summary
    assert "revision_due" in summary
    assert 0.0 <= summary["revision_need"] <= 1.0
    assert isinstance(summary["revision_due"], bool)


def test_summary_without_revision_state_keeps_defaults():
    summary = build_learner_summary(
        mastery=0.6,
        confidence=0.7,
        attempts_count=5,
        correct_count=3,
    )

    assert summary["revision_need"] == 0.0
    assert summary["revision_due"] is False