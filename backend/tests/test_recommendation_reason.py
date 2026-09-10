from app.services.recommendation_reason import build_recommendation_reason


def test_low_mastery_reason():
    reason = build_recommendation_reason(
        mastery=0.20,
        revision_need=0.0,
        difficulty=2,
    )

    assert "significant practice" in reason


def test_revision_reason():
    reason = build_recommendation_reason(
        mastery=0.80,
        revision_need=1.0,
        difficulty=2,
    )

    assert "revision" in reason


def test_developing_mastery_reason():
    reason = build_recommendation_reason(
        mastery=0.50,
        revision_need=0.0,
        difficulty=2,
    )

    assert "additional practice" in reason


def test_challenging_concept_reason():
    reason = build_recommendation_reason(
        mastery=0.80,
        revision_need=0.0,
        difficulty=5,
    )

    assert "challenging" in reason