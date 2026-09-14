from app.services.bkt_mastery import estimate_mastery


def test_single_correct_response_improves_initial_mastery():
    mastery = estimate_mastery([True])

    assert mastery > 0.20


def test_single_incorrect_response_reduces_initial_mastery():
    mastery = estimate_mastery([False])

    assert mastery < 0.20


def test_alternating_responses_remain_valid():
    mastery = estimate_mastery(
        [True, False, True, False, True, False]
    )

    assert 0.0 <= mastery <= 1.0


def test_strong_learning_history_produces_high_mastery():
    mastery = estimate_mastery([True] * 50)

    assert mastery > 0.90


def test_persistent_failure_does_not_produce_high_mastery():
    mastery = estimate_mastery([False] * 50)

    assert mastery < 0.30