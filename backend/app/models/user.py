"""
User ORM model.

Stores user account information with hashed passwords for authentication.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """Registered user account."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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

    # ── Relationships ────────────────────────────────────────────
    resumes: Mapped[list["Resume"]] = relationship(  # noqa: F821
        "Resume",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    tailored_resumes: Mapped[list["TailoredResume"]] = relationship(  # noqa: F821
        "TailoredResume",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    resume_profile: Mapped[Optional["UserResumeProfile"]] = relationship(  # noqa: F821
        "UserResumeProfile",
        back_populates="owner",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
