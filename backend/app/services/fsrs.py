from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class FSRSParameters:
    """
    Parameters for the OpenTutor FSRS-style memory model.

    These parameters provide the foundation for estimating
    memory stability and retrievability.
    """

    initial_stability: float = 1.0
    initial_difficulty: float = 0.3
    target_retrievability: float = 0.90

    def __post_init__(self):
        if self.initial_stability <= 0:
            raise ValueError(
                "initial_stability must be greater than 0"
            )

        if not 0.0 <= self.initial_difficulty <= 1.0:
            raise ValueError(
                "initial_difficulty must be between 0 and 1"
            )

        if not 0.0 < self.target_retrievability < 1.0:
            raise ValueError(
                "target_retrievability must be between 0 and 1"
            )


@dataclass(frozen=True)
class FSRSState:
    """
    Memory state for a learner-concept pair.
    """

    stability: float
    difficulty: float
    retrievability: float


def calculate_retrievability(
    elapsed_days: float,
    stability: float,
) -> float:
    """
    Estimate the probability that a learner can retrieve
    a concept after a given number of days.

    Higher stability means slower memory decay.
    """

    if stability <= 0:
        raise ValueError(
            "stability must be greater than 0"
        )

    elapsed_days = max(0.0, elapsed_days)

    retrievability = exp(
        -elapsed_days / stability
    )

    return max(
        0.0,
        min(
            1.0,
            retrievability,
        ),
    )


def initialize_fsrs_state(
    parameters: FSRSParameters | None = None,
) -> FSRSState:
    """
    Create the initial memory state for a concept.
    """

    if parameters is None:
        parameters = FSRSParameters()

    return FSRSState(
        stability=parameters.initial_stability,
        difficulty=parameters.initial_difficulty,
        retrievability=1.0,
    )


def update_fsrs_state(
    state: FSRSState,
    rating: int,
    elapsed_days: float,
) -> FSRSState:
    """
    Update memory state after a review.

    Rating:

        1 = Again
        2 = Hard
        3 = Good
        4 = Easy
    """

    if rating not in {1, 2, 3, 4}:
        raise ValueError(
            "rating must be between 1 and 4"
        )

    if elapsed_days < 0:
        raise ValueError(
            "elapsed_days cannot be negative"
        )

    current_retrievability = calculate_retrievability(
        elapsed_days=elapsed_days,
        stability=state.stability,
    )

    if rating == 1:
        stability_multiplier = 0.50
        difficulty_change = 0.10

    elif rating == 2:
        stability_multiplier = 0.85
        difficulty_change = 0.05

    elif rating == 3:
        stability_multiplier = 1.30
        difficulty_change = 0.0

    else:
        stability_multiplier = 1.70
        difficulty_change = -0.05

    # A review should increase stability when the learner
    # successfully recalls the concept. Retrievability is
    # used as a difficulty/decay factor rather than directly
    # multiplying the entire stability by a value below 1.
    memory_factor = 1.0 + (
        (1.0 - current_retrievability) * 0.5
    )

    new_stability = max(
        0.1,
        state.stability
        * stability_multiplier
        * memory_factor,
    )

    new_difficulty = max(
        0.0,
        min(
            1.0,
            state.difficulty + difficulty_change,
        ),
    )

    return FSRSState(
        stability=new_stability,
        difficulty=new_difficulty,
        retrievability=1.0,
    )