from app.ai.socratic import select_socratic_level


def test_tutor_adapts_to_low_mastery():
    level = select_socratic_level(
        mastery=0.20,
        confidence=0.20,
    )

    assert level.level == 3
    assert level.name == "partial_example"


def test_tutor_adapts_to_medium_mastery():
    level = select_socratic_level(
        mastery=0.40,
        confidence=0.50,
    )

    assert level.level == 2
    assert level.name == "prerequisite_hint"


def test_tutor_adapts_to_high_mastery():
    level = select_socratic_level(
        mastery=0.80,
        confidence=0.80,
    )

    assert level.level == 1
    assert level.name == "leading_question"


def test_tutor_provides_more_support_when_confidence_is_low():
    high_confidence = select_socratic_level(
        mastery=0.80,
        confidence=0.80,
    )

    low_confidence = select_socratic_level(
        mastery=0.80,
        confidence=0.20,
    )

    assert low_confidence.level > high_confidence.level