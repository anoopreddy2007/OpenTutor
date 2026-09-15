from app.services.bkt_presets import (
    DEFAULT_BKT,
    CAUTIOUS_BKT,
    FAST_LEARNING_BKT,
)


def test_default_preset():
    assert DEFAULT_BKT.initial_knowledge == 0.20
    assert DEFAULT_BKT.learning_rate == 0.10


def test_cautious_preset():
    assert CAUTIOUS_BKT.initial_knowledge == 0.10
    assert CAUTIOUS_BKT.learning_rate == 0.05


def test_fast_learning_preset():
    assert FAST_LEARNING_BKT.initial_knowledge == 0.25
    assert FAST_LEARNING_BKT.learning_rate == 0.20