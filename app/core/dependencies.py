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

# Import FastAPI's Request object for accessing request-level data
from fastapi import Request, status

# Import HTTPBearer, a FastAPI class for handling HTTP bearer token authentication
from fastapi.security import HTTPBearer

# Import credentials model used to parse and validate the Authorization header
from fastapi.security.http import HTTPAuthorizationCredentials

# Import the function responsible for decoding and validating JWT tokens
from app.core.security import decode_token

# Import HTTPException for raising custom HTTP error responses
from fastapi.exceptions import HTTPException


class AccessTokenBearer(HTTPBearer):
    """
    Custom authentication class that validates access tokens (JWT).

    This class extends FastAPI's HTTPBearer scheme and integrates JWT validation
    logic, ensuring that incoming requests include a valid access token.

    It also enforces that only access tokens (not refresh tokens) are accepted,
    preventing misuse of refresh tokens in protected routes.

    Attributes:
        auto_error (bool): Whether to automatically raise HTTPException
                           if authentication fails (default: True).
    """

    def __init__(self, auto_error=True):
        """
        Initialize the AccessTokenBearer instance.

        Args:
            auto_error (bool): Whether to automatically raise an exception if 
                               credentials are invalid or missing.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        """
        Extract and validate the bearer token from the request.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            dict: The decoded token payload if validation succeeds.

        Raises:
            HTTPException: If the token is invalid, expired, or is a refresh token.
        """
        # Retrieve and validate credentials from the Authorization header
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        # Extract the raw token string
        token = credentials.credentials

        # Decode the JWT and extract token data
        token_data = decode_token(token)

        # Reject if token is invalid or expired
        if not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        # Prevent refresh tokens from being used in place of access tokens
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

        # Return the token payload if valid
        return token_data

    def token_valid(self, token_data: dict | None) -> bool:
        """
        Check whether the decoded token data is valid.

        Args:
            token_data (dict | None): The payload extracted from the JWT.

        Returns:
            bool: True if the token data is valid, False otherwise.
        """
        return token_data is not None

