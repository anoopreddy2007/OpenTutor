from app.services.bkt_mastery import estimate_mastery


def test_correct_learning_path_beats_incorrect_path():
    correct_mastery = estimate_mastery(
        [True, True, True, True, True]
    )

    incorrect_mastery = estimate_mastery(
        [False, False, False, False, False]
    )

    assert correct_mastery > incorrect_mastery


def test_mixed_performance_produces_intermediate_mastery():
    correct_mastery = estimate_mastery(
        [True, True, True, True, True]
    )

    mixed_mastery = estimate_mastery(
        [True, False, True, False, True]
    )

    incorrect_mastery = estimate_mastery(
        [False, False, False, False, False]
    )

    assert correct_mastery > mixed_mastery
    assert mixed_mastery > incorrect_mastery


def test_long_correct_sequence_approaches_high_mastery():
    mastery = estimate_mastery([True] * 20)

    assert mastery > 0.80


def test_long_incorrect_sequence_remains_low():
    mastery = estimate_mastery([False] * 20)

    assert mastery < 0.30