from app.models.question import Question

from app.services.question_selection import (
    calculate_question_priority,
    select_next_question,
)


def make_question(question_id: int, difficulty: int) -> Question:
    return Question(
        id=question_id,
        concept_id=1,
        question_text=f"Question {question_id}",
        difficulty=difficulty,
    )


def test_practice_concept_selects_adaptive_question():
    questions = [
        make_question(1, 1),
        make_question(2, 3),
        make_question(3, 5),
    ]

    selected = select_next_question(
        questions=questions,
        mastery=0.30,
        confidence=0.50,
        action="PRACTICE_CONCEPT",
    )

    assert selected is not None


def test_build_confidence_prefers_easier_question():
    questions = [
        make_question(1, 1),
        make_question(2, 3),
        make_question(3, 5),
    ]

    selected = select_next_question(
        questions=questions,
        mastery=0.40,
        confidence=0.10,
        action="BUILD_CONFIDENCE",
    )

    assert selected is not None
    assert selected.difficulty == 1


def test_remediate_misconception_prefers_easier_question():
    questions = [
        make_question(1, 1),
        make_question(2, 3),
        make_question(3, 5),
    ]

    selected = select_next_question(
        questions=questions,
        mastery=0.20,
        confidence=0.20,
        action="REMEDIATE_MISCONCEPTION",
    )

    assert selected is not None
    assert selected.difficulty == 1


def test_advance_prefers_harder_question():
    questions = [
        make_question(1, 1),
        make_question(2, 3),
        make_question(3, 5),
    ]

    selected = select_next_question(
        questions=questions,
        mastery=0.90,
        confidence=0.90,
        action="ADVANCE",
    )

    assert selected is not None
    assert selected.difficulty == 5


def test_review_prerequisites_returns_no_question():
    questions = [
        make_question(1, 1),
        make_question(2, 3),
        make_question(3, 5),
    ]

    selected = select_next_question(
        questions=questions,
        mastery=0.20,
        confidence=0.20,
        action="REVIEW_PREREQUISITES",
    )

    assert selected is None


def test_empty_questions_returns_none():
    selected = select_next_question(
        questions=[],
        mastery=0.50,
        confidence=0.50,
        action="PRACTICE_CONCEPT",
    )

    assert selected is None


def test_priority_is_bounded():
    question = make_question(1, 5)

    priority = calculate_question_priority(
        question=question,
        mastery=0.50,
        confidence=0.50,
        action="PRACTICE_CONCEPT",
    )

    assert 0.0 <= priority <= 1.0