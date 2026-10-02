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
        mastery=0.2,
        confidence=0.4,
        revision_need=0.3,
        misconception_severity=0.6,
        prerequisites_ready=True,
    )

    assert action.action == "PRACTICE_CONCEPT"
    assert action.concept_id == 10
    assert action.priority == 0.8
    assert action.reason

    assert action.mastery == 0.2
    assert action.confidence == 0.4
    assert action.revision_need == 0.3
    assert action.misconception_severity == 0.6
    assert action.prerequisites_ready is True


def test_learning_action_can_have_no_concept():
    action = LearningAction(
        action="NO_ACTION",
        concept_id=None,
        priority=0.0,
        reason="No suitable learning concept is currently available.",
        mastery=0.0,
        confidence=0.0,
        revision_need=0.0,
        misconception_severity=0.0,
        prerequisites_ready=False,
    )

    assert action.concept_id is None
    assert action.priority == 0.0
    assert action.action == "NO_ACTION"
    assert action.prerequisites_ready is False