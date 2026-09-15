from app.services.mastery_comparison import (
    calculate_baseline_mastery,
    compare_mastery_models,
)


def test_baseline_mastery_uses_accuracy():
    mastery = calculate_baseline_mastery(
        correct_count=3,
        attempts_count=5,
    )

    assert mastery == 0.6


def test_baseline_handles_no_attempts():
    mastery = calculate_baseline_mastery(
        correct_count=0,
        attempts_count=0,
    )

    assert mastery == 0.0


def test_comparison_returns_both_models():
    result = compare_mastery_models(
        [True, True, False, True]
    )

    assert "baseline_mastery" in result
    assert "bkt_mastery" in result
    assert "difference" in result


def test_comparison_difference_is_correct():
    result = compare_mastery_models(
        [True, False]
    )

    assert result["difference"] == (
        result["bkt_mastery"] - result["baseline_mastery"]
    )