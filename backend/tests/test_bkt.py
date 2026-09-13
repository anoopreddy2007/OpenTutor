from app.services.bkt import BKTParameters


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