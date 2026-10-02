from app.services.learning_action import (
    LearningAction,
    get_next_learning_action,
)


def test_learning_action_type():
    action = LearningAction(
        action="PRACTICE_CONCEPT",
        concept_id=10,
        priority=0.8,
        reason="Mastery is low and additional practice is needed.",
    )

    assert action.action == "PRACTICE_CONCEPT"
    assert action.concept_id == 10
    assert action.priority == 0.8
    assert action.reason


def test_learning_action_can_have_no_concept():
    action = LearningAction(
        action="NO_ACTION",
        concept_id=None,
        priority=0.0,
        reason="No suitable learning concept is currently available.",
    )

    assert action.concept_id is None
    assert action.priority == 0.0