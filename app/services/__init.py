"""
Service layer package initializer.

This package contains application service modules that implement core business logic
for various functional domains (e.g., books, users). Services encapsulate use-case-specific
operations and act as a bridge between the API layer (routes/controllers) and the persistence
layer (e.g., database models or repositories).

Purpose:
- Centralize domain-specific operations and workflows.
- Reduce duplication of logic across API routes and background tasks.
- Promote testability and separation of concerns by isolating business rules.

Included Service Modules:
- `book.py`: Handles book-related operations such as filtering, validation, and DB access.
- `user.py`: Manages user workflows such as authentication, account creation, and profile updates.

Recommended Practices:
- Services should not directly depend on route/request objects.
- Services may orchestrate calls to repositories, validators, or external APIs.
- Keep services pure and stateless when possible to maximize reusability.

Impact on SDLC:
- Supports clean architecture by clearly separating business logic from infrastructure and presentation.
- Makes it easier to test domain behaviors without spinning up a full API stack.
- Allows code reuse across delivery mechanisms like FastAPI routes, Celery workers, or CLI commands.
"""

