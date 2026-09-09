from app.ai.socratic import select_socratic_level


def test_low_mastery_gets_partial_example():
    level = select_socratic_level(
        mastery=0.20,
        confidence=0.20,
    )

    assert level.level == 3
    assert level.name == "partial_example"


def test_medium_low_mastery_gets_prerequisite_hint():
    level = select_socratic_level(
        mastery=0.40,
        confidence=0.40,
    )

    assert level.level == 2
    assert level.name == "prerequisite_hint"


def test_reasonable_mastery_gets_leading_question():
    level = select_socratic_level(
        mastery=0.60,
        confidence=0.70,
    )

    assert level.level == 1
    assert level.name == "leading_question"


def test_low_confidence_increases_support():
    level = select_socratic_level(
        mastery=0.80,
        confidence=0.20,
    )

    assert level.level == 2
    assert level.name == "prerequisite_hint"