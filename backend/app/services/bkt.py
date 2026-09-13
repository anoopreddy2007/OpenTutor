from dataclasses import dataclass


@dataclass(frozen=True)
class BKTParameters:
    """Parameters used by Bayesian Knowledge Tracing."""

    initial_knowledge: float = 0.20
    learning_rate: float = 0.10
    guess_probability: float = 0.20
    slip_probability: float = 0.10