from dataclasses import dataclass


@dataclass(frozen=True)
class BKTParameters:
    """Parameters used by Bayesian Knowledge Tracing."""

    initial_knowledge: float = 0.20
    learning_rate: float = 0.10
    guess_probability: float = 0.20
    slip_probability: float = 0.10

    def __post_init__(self):
        values = {
            "initial_knowledge": self.initial_knowledge,
            "learning_rate": self.learning_rate,
            "guess_probability": self.guess_probability,
            "slip_probability": self.slip_probability,
        }

        for name, value in values.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{name} must be between 0.0 and 1.0"
                )