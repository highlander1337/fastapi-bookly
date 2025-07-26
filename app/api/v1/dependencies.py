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

# FastAPI utility for declaring dependency injection
from fastapi import Depends

# Async session generator defined in the database session layer
from app.db.session import get_session

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
    # Declare the session dependency to be resolved by FastAPI's injection system
    return Depends(get_session)

