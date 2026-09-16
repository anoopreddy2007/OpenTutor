from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class LearnerStateHistory(Base):
    __tablename__ = "learner_state_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    mastery: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    attempts_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    correct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        CheckConstraint(
            "mastery >= 0.0 AND mastery <= 1.0",
            name="ck_history_mastery_range",
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_history_confidence_range",
        ),
        CheckConstraint(
            "attempts_count >= 0",
            name="ck_history_attempts_nonnegative",
        ),
        CheckConstraint(
            "correct_count >= 0",
            name="ck_history_correct_nonnegative",
        ),
        CheckConstraint(
            "correct_count <= attempts_count",
            name="ck_history_correct_lte_attempts",
        ),
    )