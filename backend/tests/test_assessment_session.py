import pytest

from app.services.assessment_session import AssessmentSession


def test_new_assessment_session_starts_empty():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
    )

    assert session.questions_asked == 0
    assert session.correct_answers == 0
    assert session.accuracy == 0.0
    assert session.progress == 0.0
    assert session.remaining_questions() == 10
    assert session.completed is False


def test_record_correct_question_updates_session():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
        max_questions=5,
    )

    session.record_question(
        question_id=100,
        is_correct=True,
    )

    assert session.questions_asked == 1
    assert session.correct_answers == 1
    assert session.accuracy == 1.0
    assert session.progress == 0.2
    assert session.remaining_questions() == 4


def test_record_incorrect_question_updates_accuracy():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
        max_questions=5,
    )

    session.record_question(
        question_id=100,
        is_correct=True,
    )

    session.record_question(
        question_id=101,
        is_correct=False,
    )

    assert session.questions_asked == 2
    assert session.correct_answers == 1
    assert session.accuracy == 0.5
    assert session.progress == 0.4


def test_session_completes_at_question_limit():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
        max_questions=2,
    )

    session.record_question(
        question_id=100,
        is_correct=True,
    )

    assert session.completed is False

    session.record_question(
        question_id=101,
        is_correct=False,
    )

    assert session.completed is True
    assert session.remaining_questions() == 0
    assert session.progress == 1.0


def test_duplicate_question_is_rejected():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
    )

    session.record_question(
        question_id=100,
        is_correct=True,
    )

    with pytest.raises(ValueError, match="already been recorded"):
        session.record_question(
            question_id=100,
            is_correct=False,
        )


def test_completed_session_cannot_record_more_questions():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
        max_questions=1,
    )

    session.record_question(
        question_id=100,
        is_correct=True,
    )

    with pytest.raises(
        ValueError,
        match="already completed",
    ):
        session.record_question(
            question_id=101,
            is_correct=True,
        )


def test_invalid_max_questions_is_handled_by_progress():
    session = AssessmentSession(
        user_id=1,
        concept_id=10,
        max_questions=0,
    )

    assert session.progress == 1.0
    assert session.remaining_questions() == 0