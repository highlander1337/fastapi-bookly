"""
Common dependency functions for API version v1.

This module defines reusable dependency injection functions used across v1 route handlers.
Typical responsibilities include retrieving database sessions, resolving the current user,
applying authorization policies, or injecting shared query parameters.

Purpose:
- Centralize shared logic for dependency injection in the v1 API layer.
- Promote reusability and reduce duplication in route handlers.
- Enable clean and declarative composition of route functionality.

Impact on SDLC:
- Enhances modularity and separation of concerns by isolating cross-cutting concerns.
- Improves testability by enabling override of dependencies during testing.
- Supports maintainability and scalability in evolving, versioned APIs.
- Aligns with clean architecture by separating infrastructure concerns from application logic.
"""

# Import FastAPI's dependency declaration utility
from fastapi import Depends
# - `Depends` allows injection of services (like DB sessions or auth handlers) into route functions.

# Import async session generator from the DB layer
from app.db.session import get_session
# - `get_session` is an asynchronous context manager that yields an active SQLModel session.

# Import custom token validation dependencies
from app.core.dependencies import AccessTokenBearer, RefreshTokenBearer
# - `AccessTokenBearer` validates JWT access tokens via the HTTP Authorization header.
# - `RefreshTokenBearer` performs the same for refresh tokens, enforcing different rules.

# Instantiate reusable bearer token dependency for protected endpoints
access_token_bearer = AccessTokenBearer()
# - Used in routes to enforce access token validation and inject user data from the token.

def get_db_session():
    """
    Dependency wrapper for injecting a database session.

    This function wraps the async `get_session` generator from the DB layer in FastAPI's
    `Depends()` mechanism, making it reusable across all route handlers.

    Returns:
        Depends: A FastAPI dependency that provides an active async database session.

    Usage:
        Inject this in any route or service function to access the database, e.g.:

            @router.get("/books/")
            async def list_books(session: AsyncSession = Depends(get_db_session)):
                ...

    Benefits:
        - Centralizes session handling for consistency.
        - Makes unit testing easier via dependency overrides.
        - Keeps routes clean by abstracting infrastructure concerns.
    """
    return Depends(get_session)


def get_user_details():
    """
    Dependency wrapper that resolves the authenticated user's token data.

    This function binds the access token validation logic (`AccessTokenBearer`) into
    FastAPI's dependency system, allowing route handlers to securely access the decoded
    token payload.

    Returns:
        Depends: A FastAPI dependency that returns decoded user info from a valid token.

    Usage:
        Inject this into any protected route to extract identity and authorization data:

            @router.get("/me")
            async def get_profile(user=Depends(get_user_details)):
                return {"user_id": user["sub"]}
    """
    return Depends(access_token_bearer)


def get_token_details():
    """
    Dependency wrapper that resolves and validates a refresh token.

    This function integrates the `RefreshTokenBearer` authentication class into FastAPI's 
    dependency injection system, ensuring that only valid refresh tokens are accepted in 
    routes where it is used.

    Returns:
        Depends: A FastAPI dependency that returns the decoded JWT payload for a refresh token.

    Usage:
        Inject this into routes that handle token renewal or logout functionality:

            @router.post("/auth/refresh")
            async def refresh_access_token(token=Depends(get_token_details)):
                return {"user_id": token["sub"]}

    Benefits:
        - Enforces strict use of refresh tokens for specific endpoints.
        - Prevents access tokens from being misused in token renewal routes.
        - Promotes clean separation of token types for security and maintainability.
    """
    return Depends(RefreshTokenBearer())
