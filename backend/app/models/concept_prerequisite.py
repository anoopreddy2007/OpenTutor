from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"

    __table_args__ = (
        CheckConstraint(
            "concept_id != prerequisite_concept_id",
            name="check_no_self_prerequisite",
        ),
        UniqueConstraint(
            "concept_id",
            "prerequisite_concept_id",
            name="uq_concept_prerequisite",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id", ondelete="CASCADE"),
        nullable=False,
    )

    prerequisite_concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id", ondelete="CASCADE"),
        nullable=False,
    )