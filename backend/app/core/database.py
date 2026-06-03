"""
Async SQLAlchemy database engine, session factory, and declarative Base.

Uses asyncpg as the PostgreSQL driver with SQLAlchemy 2.0 async style.
"""

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# ── Async Engine ─────────────────────────────────────────────────
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

is_sqlite = db_url.startswith("sqlite")

engine_kwargs = {
    "echo": settings.DEBUG,
}

if is_sqlite:
    # Prevent OneDrive/network file locking from blocking startup indefinitely
    engine_kwargs["connect_args"] = {
        "timeout": 5,
        "check_same_thread": False,
    }
else:
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 3600,
    })

engine = create_async_engine(
    db_url,
    **engine_kwargs
)

# ── Session Factory ──────────────────────────────────────────────
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Declarative Base ─────────────────────────────────────────────
class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


async def create_tables() -> None:
    """Create all tables defined on the Base metadata.

    Should only be used in development. In production, use Alembic migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    """Gracefully dispose the database engine and close all connections."""
    await engine.dispose()
