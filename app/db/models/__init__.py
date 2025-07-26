"""
Database model definitions (ORM layer).

Purpose:
- Centralize all SQLModel-based representations of database tables.
- Define the structural schema for core domain entities, enabling ORM-based interactions.
- Act as the canonical layer for application-database mapping.

What to include:
- One file per domain entity or table (e.g., `book.py`, `user.py`, `order.py`).
- Each model should:
  - Inherit from SQLModel and define fields, constraints, and optional metadata.
  - Be used across services, repositories, and migrations to maintain consistency.
- Future additions may include:
  - `__base__.py`: A custom base class for shared columns like `id`, `created_at`, `updated_at`.
  - `mixins.py`: Reusable model mixins (e.g., timestamp tracking, soft deletes).
  - `enums.py`: DB-safe enumerations used across models.
  - `relationships/`: Optional subpackage for complex foreign key or association table definitions.

Recommended Practices:
- Keep models thin and declarative—avoid embedding business logic here.
- Keep field types and names in sync with migrations and Pydantic schemas.
- Define default values and nullable fields clearly for predictable DB behavior.

Impact on SDLC:
- Serves as a single source of truth for data modeling across services, APIs, and migrations.
- Improves testability by enabling test factories and fixtures from models.
- Reduces risk of schema drift and increases confidence during deployments.
- Facilitates smooth schema evolution and maintainable data architecture.
"""

