from app.services.bkt_state import estimate_state_mastery


def test_no_attempts_use_initial_mastery():
    mastery = estimate_state_mastery(
        correct_count=0,
        attempts_count=0,
    )

    assert mastery == 0.20


def test_more_correct_answers_increase_mastery():
    low = estimate_state_mastery(
        correct_count=1,
        attempts_count=5,
    )

    high = estimate_state_mastery(
        correct_count=5,
        attempts_count=5,
    )

    assert high > low


def test_invalid_counts_are_handled():
    mastery = estimate_state_mastery(
        correct_count=10,
        attempts_count=5,
    )

    assert 0.0 <= mastery <= 1.0


def test_estimated_mastery_stays_valid():
    mastery = estimate_state_mastery(
        correct_count=3,
        attempts_count=6,
    )

    assert 0.0 <= mastery <= 1.0