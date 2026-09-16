from types import SimpleNamespace

from app.services.bkt_update import update_knowledge
from app.services.learner_state_service import update_learner_state


def test_bkt_update_changes_mastery_after_correct_answer():
    initial_mastery = 0.20

    updated_mastery = update_knowledge(
        knowledge=initial_mastery,
        is_correct=True,
    )

    assert updated_mastery > initial_mastery


def test_bkt_update_changes_mastery_after_incorrect_answer():
    initial_mastery = 0.20

    updated_mastery = update_knowledge(
        knowledge=initial_mastery,
        is_correct=False,
    )

    assert updated_mastery < initial_mastery


def test_bkt_mastery_stays_within_valid_range():
    mastery = 0.20

    for _ in range(20):
        mastery = update_knowledge(
            knowledge=mastery,
            is_correct=True,
        )

    assert 0.0 <= mastery <= 1.0


def test_bkt_mastery_decreases_after_repeated_incorrect_answers():
    mastery = 0.80

    for _ in range(5):
        mastery = update_knowledge(
            knowledge=mastery,
            is_correct=False,
        )

    assert mastery < 0.80


def test_bkt_mastery_increases_after_repeated_correct_answers():
    mastery = 0.20

    for _ in range(5):
        mastery = update_knowledge(
            knowledge=mastery,
            is_correct=True,
        )

    assert mastery > 0.20