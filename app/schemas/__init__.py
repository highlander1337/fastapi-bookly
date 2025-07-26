"""
Root package for all Pydantic schemas.

Purpose:
- Acts as the entry point for all schema definitions used throughout the application.
- Organizes versioned schema packages (e.g., `v1`, `v2`) for clear separation of API contracts.
- Facilitates importing and reusing schemas scoped by API version.

What to include:
- Subpackages for each API version, e.g., `v1/`, `v2/`.
- Shared/common schemas not tied to any API version (optional).

Recommended Practices:
- Avoid defining version-specific schemas here; instead, delegate to respective version packages.
- Use this package to centralize schema imports if desired, simplifying imports elsewhere.

Impact on SDLC:
- Improves modularity and clarity in schema versioning.
- Enhances maintainability by explicitly separating schemas per API version.
- Supports incremental API evolution and backward compatibility.
"""

from .v1.book import Book, BookCreateModel, BookUpdateModel, BookReadModel

__all__ = [
    "Book",
    "BookCreateModel",
    "BookUpdateModel",
    "BookReadModel",
]


from .v1.user import User, UserCreateModel, UserReadModel, UserLoginModel

__all__ = [
    "User",
    "UserCreateModel",
    "UserReadModel",
    "UserLoginModel",
]



