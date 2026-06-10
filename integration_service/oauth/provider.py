"""
OAuth2 token provider — issues and validates JWT tokens.
Simulates an enterprise OAuth2 authorization server.
Supports: password grant (dev), authorization code flow (prod).
"""
import jwt
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Mock user store (db in the real world)
MOCK_USERS = {
    "admin@company.com": {"password": "admin123", "role": "admin"},
    "researcher@company.com": {"password": "research123", "role": "researcher"},
    "aiengineer@company.com": {"password": "aiengineer123", "role": "aiengineer"}
}


def create_access_token(subject: str, role: str, expired_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject: User identifier (email)
        role: User role for authorization
        expires_delta: Optional custom expiry

    Returns:
        Signed JWT string """
    expire = datetime.now(timezone.utc) + \
        (expired_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": "plexus-integration-service"
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    logger.info(f"Created access token for {subject}")
    return token


def create_refresh_token(subject: str) -> str:
    """
    Create a long-lived refresh token for token renewal.

    Args:
        subject: User identifier

    Returns:
        Signed refresh JWT string
    """
    expire = datetime.now(timezone.utc) + \
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "exp": expire,
        "typ": "refresh"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Validate user credentials against store.

    Args:
        email: User email
        password: Plain text password (hash in production)

    Returns:
        User dict if valid, None if invalid
    """
    user = MOCK_USERS.get(email)
    if not user:
        return None
    if user["password"] == password:
        return {"email": email, "role": user["role"]}
    return None
