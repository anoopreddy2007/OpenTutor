from app.services.bkt import BKTParameters
from app.services.bkt_update import update_knowledge


def test_correct_answer_increases_knowledge():
    before = 0.20

    after = update_knowledge(
        knowledge=before,
        is_correct=True,
    )

    assert after > before


def test_incorrect_answer_can_reduce_knowledge():
    before = 0.80

    after = update_knowledge(
        knowledge=before,
        is_correct=False,
    )

    assert after < before


def test_knowledge_stays_within_valid_range():
    for knowledge in [0.0, 0.5, 1.0]:
        for is_correct in [True, False]:
            result = update_knowledge(
                knowledge=knowledge,
                is_correct=is_correct,
            )

            assert 0.0 <= result <= 1.0


def test_custom_parameters_are_used():
    params = BKTParameters(
        initial_knowledge=0.20,
        learning_rate=0.50,
        guess_probability=0.10,
        slip_probability=0.05,
    )

    result = update_knowledge(
        knowledge=0.20,
        is_correct=True,
        params=params,
    )

    assert result > 0.20