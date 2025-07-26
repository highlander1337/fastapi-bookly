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

from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.core.security import decode_token
from fastapi.exceptions import HTTPException


from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.core.security import decode_token
from fastapi.exceptions import HTTPException


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        token = credentials.credentials
        token_data = decode_token(token)

        if not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

        return token_data

    def token_valid(self, token_data: dict | None) -> bool:
        return token_data is not None
