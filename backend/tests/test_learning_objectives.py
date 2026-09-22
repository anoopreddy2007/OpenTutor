import pytest

from app.services.learning_objectives import (
    LearningObjective,
    calculate_objective_progress,
    evaluate_learning_objective,
    calculate_overall_objective_progress,
)


def test_objective_progress():
    assert calculate_objective_progress(0.40, 0.80) == 0.5


def test_objective_progress_is_capped_at_one():
    assert calculate_objective_progress(1.0, 0.80) == 1.0


def test_objective_progress_for_zero_mastery():
    assert calculate_objective_progress(0.0, 0.80) == 0.0


def test_invalid_target_mastery_is_rejected():
    with pytest.raises(ValueError):
        calculate_objective_progress(0.5, 0.0)

    with pytest.raises(ValueError):
        calculate_objective_progress(0.5, 1.1)


def test_completed_objective():
    objective = LearningObjective(
        objective_id=1,
        title="Understand recursion",
        target_mastery=0.80,
    )

    progress = evaluate_learning_objective(
        objective=objective,
        mastery=0.85,
    )

    assert progress.objective_id == 1
    assert progress.mastery == 0.85
    assert progress.progress == 1.0
    assert progress.completed is True


def test_incomplete_objective():
    objective = LearningObjective(
        objective_id=1,
        title="Understand recursion",
        target_mastery=0.80,
    )

    progress = evaluate_learning_objective(
        objective=objective,
        mastery=0.40,
    )

    assert progress.progress == 0.5
    assert progress.completed is False


def test_mastery_is_clamped():
    objective = LearningObjective(
        objective_id=1,
        title="Understand recursion",
        target_mastery=0.80,
    )

    progress = evaluate_learning_objective(
        objective=objective,
        mastery=1.5,
    )

    assert progress.mastery == 1.0
    assert progress.completed is True


def test_overall_objective_progress():
    objectives = [
        evaluate_learning_objective(
            LearningObjective(1, "Objective 1", 0.80),
            0.40,
        ),
        evaluate_learning_objective(
            LearningObjective(2, "Objective 2", 0.80),
            0.80,
        ),
    ]

    assert calculate_overall_objective_progress(objectives) == 0.75


def test_empty_objective_list():
    assert calculate_overall_objective_progress([]) == 0.0