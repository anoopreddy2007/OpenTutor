from dataclasses import dataclass


@dataclass(frozen=True)
class SocraticLevel:
    level: int
    name: str
    instruction: str


SOCRATIC_LEVELS = {
    1: SocraticLevel(
        level=1,
        name="leading_question",
        instruction=(
            "Ask a short leading question that helps the learner "
            "make the next reasoning step themselves."
        ),
    ),
    2: SocraticLevel(
        level=2,
        name="prerequisite_hint",
        instruction=(
            "Give a hint that points the learner toward a relevant "
            "prerequisite concept without solving the problem."
        ),
    ),
    3: SocraticLevel(
        level=3,
        name="partial_example",
        instruction=(
            "Provide a partial example or worked first step, then "
            "ask the learner to continue."
        ),
    ),
    4: SocraticLevel(
        level=4,
        name="full_explanation",
        instruction=(
            "Give a clear full explanation with the reasoning and "
            "answer, while still encouraging understanding."
        ),
    ),
}


def select_socratic_level(
    mastery: float,
    confidence: float,
) -> SocraticLevel:
    """
    Select the amount of tutoring support based on learner state.

    Lower mastery receives more direct support.
    Confident-but-low-mastery learners receive an intermediate level
    to help expose possible misconceptions.
    """
    mastery = max(0.0, min(1.0, mastery))
    confidence = max(0.0, min(1.0, confidence))

    if mastery < 0.30:
        return SOCRATIC_LEVELS[3]

    if mastery < 0.50:
        return SOCRATIC_LEVELS[2]

    if mastery < 0.75:
        return SOCRATIC_LEVELS[1]

    if confidence < 0.40:
        return SOCRATIC_LEVELS[2]

    return SOCRATIC_LEVELS[1]