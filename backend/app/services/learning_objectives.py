from dataclasses import dataclass


@dataclass(frozen=True)
class LearningObjective:
    objective_id: int
    title: str
    target_mastery: float = 0.80


@dataclass(frozen=True)
class ObjectiveProgress:
    objective_id: int
    mastery: float
    target_mastery: float
    progress: float
    completed: bool


def calculate_objective_progress(
    mastery: float,
    target_mastery: float = 0.80,
) -> float:
    mastery = max(0.0, min(1.0, mastery))

    if not 0.0 < target_mastery <= 1.0:
        raise ValueError(
            "target_mastery must be greater than 0 and at most 1"
        )

    progress = mastery / target_mastery

    return max(0.0, min(1.0, progress))


def evaluate_learning_objective(
    objective: LearningObjective,
    mastery: float,
) -> ObjectiveProgress:
    if not 0.0 <= mastery <= 1.0:
        mastery = max(0.0, min(1.0, mastery))

    progress = calculate_objective_progress(
        mastery=mastery,
        target_mastery=objective.target_mastery,
    )

    completed = mastery >= objective.target_mastery

    return ObjectiveProgress(
        objective_id=objective.objective_id,
        mastery=mastery,
        target_mastery=objective.target_mastery,
        progress=progress,
        completed=completed,
    )


def calculate_overall_objective_progress(
    objectives: list[ObjectiveProgress],
) -> float:
    if not objectives:
        return 0.0

    total_progress = sum(
        objective.progress
        for objective in objectives
    )

    return total_progress / len(objectives)