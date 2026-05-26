"""
UserResumeProfile ORM model.
Defines persistent master resume profiles, structured whitelisted evidence, applications logs,
and user profile memory.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserResumeProfile(Base):
    """Stores a single persistent master profile representing the candidate's verified evidence."""

    __tablename__ = "user_resume_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    master_resume_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True,
    )
    structured_evidence: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    profile_memory: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    applications_log: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
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

    # Relationships
    owner: Mapped["User"] = relationship(  # noqa: F821
        "User",
        back_populates="resume_profile",
    )

    def __repr__(self) -> str:
        return f"<UserResumeProfile user_id={self.user_id}>"
