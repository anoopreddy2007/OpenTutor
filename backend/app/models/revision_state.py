from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RevisionState(Base):
    """
    Stores forgetting-aware revision information for a
    learner and concept.
    """

    __tablename__ = "revision_states"

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

    stability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    difficulty: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.3,
    )

    retrievability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    last_review_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    next_review_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    review_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    __table_args__ = (
        CheckConstraint(
            "stability > 0",
            name="ck_revision_stability_positive",
        ),
        CheckConstraint(
            "difficulty >= 0.0 AND difficulty <= 1.0",
            name="ck_revision_difficulty_range",
        ),
        CheckConstraint(
            "retrievability >= 0.0 AND retrievability <= 1.0",
            name="ck_revision_retrievability_range",
        ),
        CheckConstraint(
            "review_count >= 0",
            name="ck_revision_review_count_nonnegative",
        ),
    )