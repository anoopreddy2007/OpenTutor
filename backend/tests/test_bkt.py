from app.services.bkt import BKTParameters
import pytest

def test_bkt_parameters_have_defaults():
    params = BKTParameters()

    assert params.initial_knowledge == 0.20
    assert params.learning_rate == 0.10
    assert params.guess_probability == 0.20
    assert params.slip_probability == 0.10


def test_bkt_parameters_can_be_customized():
    params = BKTParameters(
        initial_knowledge=0.30,
        learning_rate=0.15,
        guess_probability=0.10,
        slip_probability=0.05,
    )

    assert params.initial_knowledge == 0.30
    assert params.learning_rate == 0.15
    assert params.guess_probability == 0.10
    assert params.slip_probability == 0.05
    import pytest


def test_bkt_parameters_reject_invalid_values():
    with pytest.raises(ValueError):
        BKTParameters(initial_knowledge=1.5)

    with pytest.raises(ValueError):
        BKTParameters(learning_rate=-0.1)

    with pytest.raises(ValueError):
        BKTParameters(guess_probability=2.0)

    with pytest.raises(ValueError):
        BKTParameters(slip_probability=-1.0)