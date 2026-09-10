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