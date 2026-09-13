from app.services.bkt_mastery import estimate_mastery


def test_initial_mastery_is_used_for_empty_history():
    mastery = estimate_mastery([])

    assert mastery == 0.20


def test_correct_responses_increase_mastery():
    mastery = estimate_mastery(
        [True, True, True],
    )

    assert mastery > 0.20


def test_incorrect_responses_provide_lower_mastery():
    mastery = estimate_mastery(
        [False, False, False],
    )

    assert mastery < 0.20


def test_mastery_stays_within_valid_range():
    mastery = estimate_mastery(
        [True, False, True, False, True],
    )

    assert 0.0 <= mastery <= 1.0