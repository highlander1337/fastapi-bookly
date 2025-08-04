"""
Redis client configuration and connection management.

This module provides a reusable interface for interacting with a Redis server using
an asynchronous Redis client from the official `redis` package. It is designed to be
used by other application components that require caching, pub/sub messaging, token
revocation (blacklisting), or distributed locking.

Purpose:
- Initialize and expose a shared Redis client instance for use across the app.
- Encapsulate Redis connection configuration and lifecycle management.
- Support infrastructure needs such as token blacklisting, rate limiting, and background queues.

Impact on SDLC:
- Promotes reusability by centralizing Redis integration logic.
- Improves maintainability by separating infrastructure concerns from business logic.
- Enhances testability through a single injectable Redis client dependency.
- Supports scalability by enabling fast, centralized caching and real-time data flows.
"""

# Async Redis client for non-blocking operations
import redis.asyncio as redis

# Loads configuration values, including the database URL
from app.config import Config

# Default expiration time (in seconds) for revoked JWT token identifiers (JTI).
JTI_EXPIRY = 3600  # 1 hour

# Redis client instance configured for the application's Redis server.
# Used to store JWT token JTIs that have been revoked (blacklisted).
token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    """
    Add a JWT token's unique identifier (JTI) to the Redis blocklist.

    This operation marks a token as revoked by storing its JTI in Redis with a TTL,
    preventing further use of that token until it naturally expires.

    Args:
        jti (str): The unique identifier of the JWT token to blacklist.

    Returns:
        None
    """
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY  # Set expiry to automatically remove the revoked JTI after TTL
    )

async def token_in_blocklist(jti: str) -> bool:
    """
    Check whether a JWT token's unique identifier (JTI) is present in the Redis blocklist.

    This is used during token validation to reject tokens that have been revoked explicitly.

    Args:
        jti (str): The unique identifier of the JWT token to check.

    Returns:
        bool: True if the JTI is found in Redis (token revoked), False otherwise.
    """
    jti_value = await token_blocklist.get(jti)
    return jti_value is not None
