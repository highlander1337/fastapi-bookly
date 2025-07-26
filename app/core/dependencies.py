"""
Core dependency classes for authentication and authorization.

This module defines reusable FastAPI dependency classes that handle
cross-cutting concerns related to security, such as extracting and validating
access tokens from HTTP requests.

Primary components include:

- AccessTokenBearer: A specialized HTTPBearer dependency class that
  parses the Authorization header for Bearer tokens. It serves as the
  foundational building block for token-based authentication in the application.

Purpose:
- Centralize core dependency implementations related to security.
- Promote reuse of authentication dependencies across multiple API versions
  and other application components (e.g., background tasks).
- Separate infrastructure-level authentication concerns from API-specific
  dependency logic.

Impact on SDLC:
- Encourages clean architecture by isolating core auth mechanisms.
- Enhances maintainability and consistency of authentication handling.
- Simplifies testing by enabling targeted overrides of core dependencies.
- Supports scalability by providing reusable security primitives for all app layers.
"""


from fastapi.security import HTTPBearer

class AccessTokenBearer(HTTPBearer):
    pass
