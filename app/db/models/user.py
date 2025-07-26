"""
User database model definition.

This module defines the SQLModel-based schema for the `User` table in the database.
It includes database columns, constraints, and optional ORM-related configuration.

Purpose:
- Represent the `users` table structure in Python using SQLModel.
- Define fields such as username, email, hashed password, and timestamps.
- Support type-safe, declarative database interaction using an ORM.

Impact on SDLC:
- Centralizes user data schema in a single, reusable model.
- Improves data integrity by enforcing types and constraints at the model level.
- Enhances developer productivity through autocompletion and validation.
- Simplifies migrations, database access, and test data setup.
- Promotes consistency between the database schema and application logic.
"""

# Base class and helpers for ORM mapping using SQLModel (a SQLAlchemy-compatible layer)
from sqlmodel import SQLModel, Field, Column

# PostgreSQL-specific column types (e.g., UUID, TIMESTAMP)
import sqlalchemy.dialects.postgresql as pg

# For handling datetime fields such as created_at and updated_at
from datetime import datetime

# For generating unique identifiers (UUIDs) for primary keys
import uuid


class User(SQLModel, table = True):
    """
    ORM model representing a user record.

    Maps to the 'users' table in the PostgreSQL database, 
    with full support for strong typing and migrations.
    """
    
    __tablename__ = "users"
    # Unique identifier for each book (Primary Key)
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()  # Automatically generate UUID on insert
        )
    )
    
    # user name for login purpose
    username : str
    
    # password for login purpose
    password_hash : str = Field(exclude=True)
    
    # email for recovery purpose
    email : str
    
    # first name for display purpose
    first_name : str
    
    # last name for display purpose
    last_name : str
    
    # flag for account verification purpose
    is_verified : bool = Field(default=False)
    
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
        Developer-friendly string representation of a User object.

        Returns:
            str: A string showing the user first and last name, useful for debugging/logging.
        """
        return f"<User {self.first_name} {self.last_name}>"