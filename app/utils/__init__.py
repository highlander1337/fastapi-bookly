"""
Utility package initializer.

This package serves as a collection of general-purpose utilities and helper functions
that are shared across the application. These utilities are **domain-agnostic** and
should not depend on business logic, API routes, or persistence layers.

Contents:
- `helpers.py`: Contains low-level reusable functions for formatting, parsing,
  slugifying, ID generation, timestamp formatting, and other cross-cutting concerns.

Purpose:
- Provide a centralized location for functions that support multiple parts of the codebase.
- Prevent duplication of logic across services, routes, or models.
- Keep higher-level modules (e.g., services, schemas) focused by offloading boilerplate logic.

Recommended Practices:
- Keep utilities **stateless and pure** whenever possible.
- Ensure that utilities are **well-named** and covered by unit tests.
- Avoid mixing domain logic with utilities — utilities should not import models or services.
- If utilities grow too complex, consider splitting them into focused submodules
  (e.g., `string_utils.py`, `date_utils.py`, `file_utils.py`).

Impact on SDLC:
- Encourages DRY principles and modularization.
- Supports better test coverage and reusability.
- Enhances scalability by cleanly separating infrastructure support logic from core behavior.
"""

