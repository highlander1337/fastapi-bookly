"""
Database engine setup using SQLAlchemy and SQLModel.

Initializes an async database engine using credentials from the configuration module.

Purpose:
- Centralized creation of the async engine.
- Foundation for async session creation and ORM integration.

Impact on SDLC:
- Encourages DRY (Don't Repeat Yourself) principle for DB access.
- Facilitates switching databases or engines without widespread refactoring.
- Supports high concurrency, a must for scalable APIs.
"""

# Creates a SQLModel-compatible engine and executes raw SQL queries
from sqlmodel import create_engine, SQLModel

# Provides support for asynchronous engine use (non-blocking DB I/O)
from sqlalchemy.ext.asyncio import AsyncEngine

# Loads configuration values, including the database URL
from app.config import Config

# Create an asynchronous engine using the database URL from the config
engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,  # Connection string for PostgreSQL or other DB
        echo=True  # Enables SQL logging for debugging (set to False in production)
    )
)


async def init_db():
    """
    Initialize the database schema by creating tables defined in SQLModel metadata.

    This function:
    - Establishes a connection using the async engine.
    - Runs `create_all` within a transaction to create tables if they don't exist.

    Should be called at app startup to ensure schema is initialized.

    Returns:
        None
    """
    # Begin an async transaction with the database
    async with engine.begin() as conn:
        # Run the synchronous create_all function in an async context
        await conn.run_sync(SQLModel.metadata.create_all)
        
    