from app.services.bkt_confidence import adjust_mastery_by_confidence


def test_high_confidence_slightly_increases_mastery():
    result = adjust_mastery_by_confidence(
        mastery=0.50,
        confidence=1.0,
    )

    assert result > 0.50


def test_low_confidence_slightly_decreases_mastery():
    result = adjust_mastery_by_confidence(
        mastery=0.50,
        confidence=0.0,
    )

    assert result < 0.50


def test_neutral_confidence_does_not_change_mastery():
    result = adjust_mastery_by_confidence(
        mastery=0.50,
        confidence=0.50,
    )

    assert result == 0.50


def test_adjusted_mastery_stays_in_range():
    high = adjust_mastery_by_confidence(
        mastery=1.0,
        confidence=1.0,
    )

    low = adjust_mastery_by_confidence(
        mastery=0.0,
        confidence=0.0,
    )

    assert 0.0 <= high <= 1.0
    assert 0.0 <= low <= 1.0