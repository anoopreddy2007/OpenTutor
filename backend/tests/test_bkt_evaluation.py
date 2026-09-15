from app.services.bkt_mastery import estimate_mastery
from app.services.mastery_comparison import compare_mastery_models


def test_all_correct_increases_mastery():
    mastery = estimate_mastery(
        [True, True, True, True]
    )

    assert mastery > 0.20


def test_all_incorrect_keeps_mastery_lower():
    mastery = estimate_mastery(
        [False, False, False, False]
    )

    assert mastery < 0.20


def test_bkt_mastery_is_bounded():
    mastery = estimate_mastery(
        [True, False, True, False, True, True]
    )

    assert 0.0 <= mastery <= 1.0


def test_bkt_differs_from_simple_accuracy():
    result = compare_mastery_models(
        [True, True, False, True]
    )

    assert result["bkt_mastery"] != result["baseline_mastery"]