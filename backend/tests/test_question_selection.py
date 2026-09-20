from types import SimpleNamespace

from app.services.question_selection import (
    calculate_question_priority,
    select_next_question,
)


def create_question(
    question_id: int,
    difficulty: int,
):
    return SimpleNamespace(
        id=question_id,
        difficulty=difficulty,
    )


def test_low_mastery_increases_question_priority():
    question = create_question(
        question_id=1,
        difficulty=3,
    )

    low_mastery = calculate_question_priority(
        question=question,
        mastery=0.2,
        confidence=0.8,
    )

    high_mastery = calculate_question_priority(
        question=question,
        mastery=0.8,
        confidence=0.8,
    )

    assert low_mastery > high_mastery


def test_low_confidence_increases_question_priority():
    question = create_question(
        question_id=1,
        difficulty=3,
    )

    low_confidence = calculate_question_priority(
        question=question,
        mastery=0.6,
        confidence=0.2,
    )

    high_confidence = calculate_question_priority(
        question=question,
        mastery=0.6,
        confidence=0.9,
    )

    assert low_confidence > high_confidence


def test_question_priority_stays_between_zero_and_one():
    question = create_question(
        question_id=1,
        difficulty=5,
    )

    priority = calculate_question_priority(
        question=question,
        mastery=0.0,
        confidence=0.0,
    )

    assert 0.0 <= priority <= 1.0


def test_empty_question_list_returns_none():
    result = select_next_question(
        questions=[],
        mastery=0.5,
        confidence=0.5,
    )

    assert result is None


def test_question_selection_returns_question():
    questions = [
        create_question(
            question_id=1,
            difficulty=1,
        ),
        create_question(
            question_id=2,
            difficulty=4,
        ),
    ]

    result = select_next_question(
        questions=questions,
        mastery=0.8,
        confidence=0.8,
    )

    assert result is not None
    assert result.id in {1, 2}


def test_question_difficulty_affects_selection():
    questions = [
        create_question(
            question_id=1,
            difficulty=1,
        ),
        create_question(
            question_id=2,
            difficulty=5,
        ),
    ]

    result = select_next_question(
        questions=questions,
        mastery=0.2,
        confidence=0.8,
    )

    assert result.id == 1