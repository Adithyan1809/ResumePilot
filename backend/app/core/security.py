"""
Security utilities for JWT token management and password hashing.

Provides functions for:
- Creating and verifying JWT access tokens
- Hashing and verifying passwords with bcrypt
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# ── Password Hashing
# Use `pbkdf2_sha256` for local development to avoid native `bcrypt` C-extension
# installation issues on developer machines. In production you may prefer
# `bcrypt` or `argon2` and should configure accordingly.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        The bcrypt hash string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash.

    Args:
        plain_password: The plain-text password to check.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches, False otherwise.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as ve:
        # Bcrypt has a 72-byte limit. If a too-long password was provided,
        # try a safe fallback by truncating to 72 bytes and re-checking.
        try:
            truncated = plain_password[:72]
            return pwd_context.verify(truncated, hashed_password)
        except Exception:
            # Log and return False to avoid raising a 500 to callers
            return False
    except Exception:
        # Any other verification error should not crash the request handler
        return False


# ── JWT Tokens ───────────────────────────────────────────────────

def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload to encode in the token. Must include a "sub" claim.
        expires_delta: Optional custom expiration. Defaults to
            ACCESS_TOKEN_EXPIRE_MINUTES from settings.

    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """Decode and validate a JWT access token.

    Args:
        token: The JWT string to decode.

    Returns:
        The decoded payload dict, or None if the token is invalid / expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
