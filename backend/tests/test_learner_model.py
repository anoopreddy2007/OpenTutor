from app.services.learner_model import (
    clamp,
    mastery_gap,
    normalize_confidence,
)


def test_clamp_keeps_value_in_range():
    assert clamp(1.5) == 1.0
    assert clamp(-0.5) == 0.0
    assert clamp(0.5) == 0.5


def test_mastery_gap():
    assert mastery_gap(0.25) == 0.75
    assert mastery_gap(1.0) == 0.0


def test_normalize_confidence():
    assert normalize_confidence(5) == 1.0
    assert normalize_confidence(1) == 0.2
    assert normalize_confidence(None) == 0.0