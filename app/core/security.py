"""
Authentication and authorization utilities.

Implements token creation, validation, and user identity extraction for secured endpoints.

Purpose:
- Provides centralized access control logic.
- Supports integration with OAuth2, JWT, etc.

Impact on SDLC:
- Secures sensitive routes without scattering auth logic.
- Makes updates to auth logic easier and safer.
- Crucial for user-facing APIs or admin panels.
"""

# PassLib provides secure password hashing frameworks.
from passlib.context import CryptContext

# For setting token expiration timestamps and handling time operations.
from datetime import timedelta, datetime

# PyJWT is used to encode and decode JWT tokens.
import jwt

# UUID is used for generating unique token IDs (jti).
import uuid

# Logging for debugging and auditing token decoding errors.
import logging

# Configuration management (e.g., secrets, algorithms) loaded from app settings.
from app.config import Config

# Create a reusable password hashing context using bcrypt, a secure and widely adopted hashing algorithm.
password_context = CryptContext(
    schemes=['bcrypt'],  # Supported hashing algorithms (only bcrypt here)
    deprecated="auto"    # Mark outdated algorithms as deprecated automatically
)

# Default expiration time for access tokens in seconds (1 hour).
ACCESS_TOKEN_EXPIRY = 3600

def get_password_hash(plain_password: str) -> str:
    """
    Hash a plaintext password using bcrypt for secure storage.

    Args:
        plain_password (str): User-provided password in plain text.

    Returns:
        str: The hashed version of the password.

    Usage:
        Store this hashed string in your user database instead of the raw password.
    """
    hashed = password_context.hash(plain_password)
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plaintext password matches a previously hashed one.

    Args:
        plain_password (str): Raw password input (e.g., from login form).
        hashed_password (str): Password hash retrieved from the database.

    Returns:
        bool: True if the password matches the hash, False otherwise.

    Usage:
        Used to validate login credentials.
    """
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    """
    Generate a signed JWT access token for a user.

    Args:
        user_data (dict): Dictionary containing user identity and claims.
        expiry (timedelta, optional): Custom expiration interval. Defaults to 1 hour.
        refresh (bool, optional): Indicates if the token is a refresh token. Defaults to False.

    Returns:
        str: A signed JWT token string that can be returned to clients.

    Usage:
        Used after successful authentication or token refresh to issue credentials.
    """
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),  # Unique token identifier
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    
    return token

def decode_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.

    Args:
        token (str): The JWT token string received from client.

    Returns:
        dict | None: Decoded token data if valid; None if decoding fails.

    Usage:
        Called in dependency logic to extract and verify user identity for protected routes.
    """
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)  # Logs exception with traceback for debugging
        return None
