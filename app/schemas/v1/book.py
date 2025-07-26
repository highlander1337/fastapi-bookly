"""
Pydantic schemas for book data validation.

Defines request and response models for book endpoints, enforcing data structure and types.

Purpose:
- Provides validation and serialization logic.
- Bridges between external input and internal logic.

Impact on SDLC:
- Enhances API reliability and error reporting.
- Encourages strong typing and early bug detection.
- Automatically documents models via OpenAPI.
"""

# Base class for creating Pydantic models (data validation, serialization, etc.)
from pydantic import BaseModel

# Used for timestamp fields (created_at, updated_at)
from datetime import datetime, date

# Used for UUID primary key field (uid)
import uuid


class Book(BaseModel):
    """
    Complete schema for representing a Book, including metadata.

    Typically used for API responses, where full detail (including system-generated fields)
    is required.
    """

    uid: uuid.UUID                   # Unique identifier for the book
    title: str                       # Book title
    author: str                      # Book author
    publisher: str                   # Book publisher
    published_date: date             # Publication date as string (can be validated further)
    page_count: int                 # Number of pages
    language: str                   # Language of the book
    created_at: datetime           # Timestamp when the book was created
    updated_at: datetime           # Timestamp when the book was last updated


class BookUpdateModel(BaseModel):
    """
    Schema for updating an existing book.

    All fields are required for simplicity, but can be made optional if partial updates are supported.
    Typically used in PUT or PATCH requests.
    """

    title: str                      # New title
    author: str                     # New author
    publisher: str                  # New publisher
    page_count: int                 # New page count
    language: str                   # New language


class BookCreateModel(BaseModel):
    """
    Schema for creating a new book.

    Used in POST requests to validate incoming creation data.
    """

    title: str                      # Title of the new book
    author: str                     # Author of the new book
    publisher: str                  # Publisher of the new book
    published_date: date            # Publication date as a string (could be ISO 8601)
    page_count: int                # Number of pages
    language: str                  # Language of the book

class BookReadModel(BaseModel):
    """
    Schema for read an existing book.

    Typically used in GET requests.
    """

    title: str                      # New title
    author: str                     # New author
    publisher: str                  # New publisher
    published_date: date            # Publication date as a string (could be ISO 8601)
    page_count: int                 # New page count
    language: str                   # New language
    created_at: datetime           # Timestamp when the book was created
    updated_at: datetime           # Timestamp when the book was last updated