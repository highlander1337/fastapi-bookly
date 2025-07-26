"""
Database configuration and session management layer.

Purpose:
- Encapsulate all logic related to database connectivity, session management, and persistence setup.
- Serve as the boundary between application logic and the underlying relational database.

What to include:
- `main.py`: Initializes the async database engine using SQLAlchemy and SQLModel.
- `session.py`: Provides an async session generator (`get_session`) for dependency injection.
- `models/`: Contains SQLModel-based ORM definitions for all database entities.

Future additions might include:
- `repositories/`: Abstract persistence operations with reusable data access patterns (e.g., CRUD base classes).
- `migration_utils.py`: Custom helpers to manage Alembic migrations or seed data.
- `factories/`: Model factories for integration tests or test fixtures.
- `config.py`: Specialized configuration logic for multi-database environments (e.g., read replicas, shard maps).
- `health.py`: DB health check utilities for uptime monitoring or readiness probes.

Recommended Practices:
- Avoid embedding any domain-specific business logic in this layer.
- Maintain environment-agnostic setup—should work across dev, staging, and prod with `.env` support.
- Design for observability—consider logging slow queries or connection issues here in production.

Impact on SDLC:
- Centralizes all persistence infrastructure for consistency and maintainability.
- Improves testability by exposing clean session and engine factories.
- Simplifies onboarding for new developers by clarifying how the application interacts with the database.
- Enables flexible scaling and easier migrations as the system grows.
"""

