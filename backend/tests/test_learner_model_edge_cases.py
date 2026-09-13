from app.services.learner_model import (
    clamp,
    mastery_gap,
    normalize_confidence,
)


def test_clamp_handles_extreme_values():
    assert clamp(100.0) == 1.0
    assert clamp(-100.0) == 0.0


def test_mastery_gap_handles_boundaries():
    assert mastery_gap(0.0) == 1.0
    assert mastery_gap(1.0) == 0.0


def test_confidence_normalization_handles_boundaries():
    assert normalize_confidence(1) == 0.2
    assert normalize_confidence(5) == 1.0


def test_confidence_normalization_clamps_invalid_high_value():
    assert normalize_confidence(10) == 1.0