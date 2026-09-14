from app.services.bkt_history import build_response_history


def test_empty_history():
    assert build_response_history(0, 0) == []


def test_all_correct_history():
    history = build_response_history(3, 3)

    assert history == [True, True, True]


def test_mixed_history():
    history = build_response_history(2, 5)

    assert len(history) == 5
    assert history.count(True) == 2
    assert history.count(False) == 3


def test_invalid_correct_count_is_clamped():
    history = build_response_history(10, 5)

    assert len(history) == 5
    assert history.count(True) == 5