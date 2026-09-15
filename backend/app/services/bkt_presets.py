from app.services.bkt import BKTParameters


DEFAULT_BKT = BKTParameters()

CAUTIOUS_BKT = BKTParameters(
    initial_knowledge=0.10,
    learning_rate=0.05,
    guess_probability=0.15,
    slip_probability=0.05,
)

FAST_LEARNING_BKT = BKTParameters(
    initial_knowledge=0.25,
    learning_rate=0.20,
    guess_probability=0.20,
    slip_probability=0.10,
)