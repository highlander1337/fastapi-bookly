"""
Session factory for creating asynchronous DB sessions.

This module defines an async session generator (`get_session`) used for dependency
injection in FastAPI routes and services. It leverages SQLAlchemy's async capabilities
to manage database sessions cleanly and safely.

Purpose:
- Encapsulates session lifecycle management.
- Prevents repetitive boilerplate code across modules.
- Enables easy mocking and testing of DB sessions.

Impact on SDLC:
- Supports testability by isolating session creation logic.
- Promotes clean architecture by centralizing persistence setup.
- Reduces the risk of unclosed sessions and transactional leaks.
"""

# Standard collections import for defining async generator return type
from collections.abc import AsyncGenerator

# Import the SQLModel AsyncSession, which extends SQLAlchemy AsyncSession with .exec()
from sqlmodel.ext.asyncio.session import AsyncSession

# SQLAlchemy's session factory utility
from sqlalchemy.orm import sessionmaker

# Reuse the preconfigured async engine created in main.py
from app.db.main import engine


# Async sessionmaker instance to create sessions tied to our async engine
async_session_maker = sessionmaker(
    bind=engine,               # The async SQLAlchemy engine from main.py
    class_=AsyncSession,       # Use the async session class
    expire_on_commit=False     # Prevents automatic expiration of attributes after commit
)

# Dependency-injectable async session generator for use in FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an asynchronous SQLAlchemy session for DB access.

    This function is designed to be used as a FastAPI dependency:
        - It manages session creation and automatic cleanup.
        - It yields a session that can be used within request scopes.
        - It allows FastAPI to manage transaction lifecycles cleanly.

    Yields:
        AsyncSession: An instance of SQLAlchemy AsyncSession bound to the app's engine.
    """
    async with async_session_maker() as session:
        yield session
