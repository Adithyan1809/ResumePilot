"""
TailoredResume ORM model.

Stores the result of tailoring a resume for a specific job description,
including ATS scores, missing keywords, suggestions, and cover letter.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TailoredResume(Base):
    """A resume tailored to a specific job description."""

    __tablename__ = "tailored_resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Job Details ──────────────────────────────────────────────
    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        default="",
    )
    company: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        default="",
    )

    # ── AI-Generated Content ─────────────────────────────────────
    tailored_sections: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    ats_score: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    missing_keywords: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    suggestions: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    cover_letter: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )
    template: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="classic",
    )

    # ── Timestamps ───────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ────────────────────────────────────────────
    owner: Mapped["User"] = relationship(  # noqa: F821
        "User",
        back_populates="tailored_resumes",
    )
    source_resume: Mapped["Resume"] = relationship(  # noqa: F821
        "Resume",
        back_populates="tailored_resumes",
    )

    def __repr__(self) -> str:
        return f"<TailoredResume {self.job_title} @ {self.company}>"
