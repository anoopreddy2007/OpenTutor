from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class LearnerState(Base):
    __tablename__ = "learner_states"

    __table_args__ = (
        CheckConstraint(
            "mastery BETWEEN 0 AND 1",
            name="check_learner_state_mastery",
        ),
        CheckConstraint(
            "confidence BETWEEN 0 AND 1",
            name="check_learner_state_confidence",
        ),
        CheckConstraint(
            "attempts_count >= 0",
            name="check_learner_state_attempts",
        ),
        CheckConstraint(
            "correct_count >= 0",
            name="check_learner_state_correct",
        ),
        CheckConstraint(
            "correct_count <= attempts_count",
            name="check_correct_not_exceed_attempts",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id", ondelete="CASCADE"),
        nullable=False,
    )

    mastery: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    attempts_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    correct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )