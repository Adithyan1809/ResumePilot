"""
Authentication business logic service.

Handles user creation, registration validation, and password credential authentication.
"""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import SignupRequest

logger = logging.getLogger(__name__)


async def create_user(db: AsyncSession, payload: SignupRequest) -> User | None:
    """Register a new user in the system.

    Checks if the email is already registered, hashes the password,
    and inserts the User record.

    Args:
        db: Async database session.
        payload: Pydantic registration request schema.

    Returns:
        The created User instance, or None if the email already exists.
    """
    logger.info(f"Attempting to register user email: {payload.email}")

    # Check if email is already taken
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        logger.warning(f"Registration failed. Email already exists: {payload.email}")
        return None

    # Hash password and create record
    hashed = hash_password(payload.password)
    new_user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hashed,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info(f"User registration completed successfully: {new_user.id}")
    return new_user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    """Verify user credentials and authenticate.

    Args:
        db: Async database session.
        email: Registered email.
        password: Plain password text.

    Returns:
        The authenticated User instance if valid, else None.
    """
    logger.info(f"Attempting login authentication for: {email}")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        logger.warning(f"Authentication failed. User not found: {email}")
        return None

    if not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed. Incorrect password for: {email}")
        return None

    if not user.is_active:
        logger.warning(f"Authentication failed. Account deactivated: {email}")
        return None

    logger.info(f"User login successfully authenticated: {user.id}")
    return user
