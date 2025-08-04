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
# Import FastAPI's Request object for accessing request-level data and standard HTTP status codes
from fastapi import Request, status

# Import HTTPBearer to define and enforce Bearer Token authentication in FastAPI routes
from fastapi.security import HTTPBearer

# Import the credentials class that represents parsed "Authorization: Bearer <token>" headers
from fastapi.security.http import HTTPAuthorizationCredentials

# Import the JWT decoding logic from the application's core security module
from app.core.security import decode_token

# Import FastAPI's exception class for returning HTTP errors to clients
from fastapi.exceptions import HTTPException

# Import async Redis helper functions for token revocation support (adding and checking JTIs)
from app.core.redis import add_jti_to_blocklist, token_in_blocklist

class TokenBearer(HTTPBearer):
    """
    Abstract base authentication class for validating JWT tokens using the HTTP Bearer scheme.

    This class decodes the incoming Bearer token and delegates validation of the token content
    (such as whether it's an access or refresh token) to the `verify_token_data` method,
    which must be implemented by subclasses.

    Attributes:
        auto_error (bool): Whether to raise an automatic HTTPException if authentication fails.
    """

    def __init__(self, auto_error: bool = True):
        """
        Initialize the TokenBearer instance with optional automatic error raising.

        Args:
            auto_error (bool): If True, raise HTTPException on auth failure. Default is True.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        """
        Extract and decode a Bearer token from the request, and validate its content.

        Args:
            request (Request): The incoming HTTP request containing the token.

        Returns:
            dict: The decoded JWT payload.

        Raises:
            HTTPException: If the token is missing, invalid, expired, or of the wrong type.
        """
        # Use the parent class to retrieve the credentials from the Authorization header
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        # Get the raw token string
        token = credentials.credentials

        # Decode the JWT and extract its payload
        token_data = decode_token(token)

        # If decoding failed or token is invalid, raise an error
        if not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error":"Token invalid or expired",
                    "resolution":"Please get a new token"
                }
            )
        
        # If token is in the blocklist or token is invalid, raise and error
        # Only work with redis server
        # if await token_in_blocklist(token_data['jti']):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail={
        #             "error":"Token invalid or has been revoked",
        #             "resolution":"Please get a new token"
        #         }

        #     )

        # Perform additional validation specific to access or refresh tokens
        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token_data: dict | None) -> bool:
        """
        Check whether the decoded JWT payload is valid.

        Args:
            token_data (dict | None): The payload returned from decode_token().

        Returns:
            bool: True if the payload is not None; False otherwise.
        """
        return token_data is not None

    def verify_token_data(self, token_data: dict) -> None:
        """
        Abstract method for validating the token's claims based on context (access or refresh).

        This method should be overridden by subclasses to enforce token-type-specific logic.

        Args:
            token_data (dict): The decoded JWT payload.

        Raises:
            NotImplementedError: If not overridden in a subclass.
        """
        raise NotImplementedError("Please override this method in child classes.")


class AccessTokenBearer(TokenBearer):
    """
    Authentication class that validates access tokens specifically.

    Ensures the token is *not* a refresh token by checking the `refresh` claim.
    """

    def verify_token_data(self, token_data: dict) -> None:
        """
        Ensure the token is a valid access token (not a refresh token).

        Args:
            token_data (dict): The decoded JWT payload.

        Raises:
            HTTPException: If the token is a refresh token instead of an access token.
        """
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    """
    Authentication class that validates refresh tokens specifically.

    Ensures the token *is* a refresh token by checking the `refresh` claim.
    """

    def verify_token_data(self, token_data: dict) -> None:
        """
        Ensure the token is a valid refresh token.

        Args:
            token_data (dict): The decoded JWT payload.

        Raises:
            HTTPException: If the token is an access token instead of a refresh token.
        """
        if token_data and not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )
