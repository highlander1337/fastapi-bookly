"""
SQLModel-based ORM model for the Book entity.

Defines database table structure for the books table, compatible with SQLModel/SQLAlchemy.

Purpose:
- Maps database fields to Python objects.
- Enables query-building and migrations with strong typing.

Impact on SDLC:
- Serves as a single source of truth for data schema.
- Reduces risk of schema drift between API and DB.
- Makes migration tools (e.g., Alembic) easier to apply.
"""

# Base class and helpers for ORM mapping using SQLModel (a SQLAlchemy-compatible layer)
from sqlmodel import SQLModel, Field, Column

# PostgreSQL-specific column types (e.g., UUID, TIMESTAMP)
import sqlalchemy.dialects.postgresql as pg

# For handling datetime fields such as created_at and updated_at
from datetime import datetime, date

# For generating unique identifiers (UUIDs) for primary keys
import uuid


class Book(SQLModel, table=True):
    """
    ORM model representing a book record.

    Maps to the 'books' table in the PostgreSQL database, 
    with full support for strong typing and migrations.
    """
    __tablename__ = "books"  # Explicitly declare the table name

    # Unique identifier for each book (Primary Key)
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()  # Automatically generate UUID on insert
        )
    )

    # Title of the book
    title: str

    # Author of the book
    author: str

    # Publisher of the book
    publisher: str

    # Date the book was published
    published_date: date

    # Number of pages in the book
    page_count: int

    # Language the book is written in
    language: str

    # Timestamp of when the book record was created
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now  # Automatically set current timestamp
        )
    )

    # Timestamp of when the book record was last updated
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now  # Initial value; can be updated on save
        )
    )

    def __repr__(self):
        """
        Developer-friendly string representation of a Book object.

        Returns:
            str: A string showing the book title, useful for debugging/logging.
        """
        return f"<Book {self.title}>"
