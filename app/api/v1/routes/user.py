"""
User-related API route definitions for version v1.

This module defines HTTP endpoints related to user operations, such as registration,
authentication, profile retrieval, and account management. It wires route handlers to
FastAPI's routing system and connects them to business logic through services and dependencies.

Purpose:
- Define versioned RESTful endpoints for user functionality.
- Connect user-facing routes to service-layer logic via dependency injection.
- Enforce separation between transport (HTTP) and business logic.

Impact on SDLC:
- Encourages clean architecture by keeping routing logic isolated from business logic.
- Enables modular API evolution by scoping functionality under versioned namespaces (e.g., `/api/v1/users`).
- Improves maintainability by grouping all user-related endpoints in a single cohesive module.
- Enhances testability and clarity by separating route definitions from core logic and database interaction.
"""

from fastapi import APIRouter, status
# - APIRouter: to create a modular group of routes.
# - status: to provide HTTP status code constants.

from fastapi.exceptions import HTTPException  
# - HTTPException: used to raise HTTP errors with status codes and details.

# SQLModel async session type for typing the session parameter:
from sqlmodel.ext.asyncio.session import AsyncSession
# - AsyncSession: SQLModel's asynchronous session type used for database operations.

from app.schemas import UserCreateModel, UserReadModel, UserLoginModel
# - UserCreateModel, UserReadModel, UserLoginModel:
#   Pydantic models defining validation and serialization for user API payloads.

from app.services.user import UserService
# - UserService: business logic class handling operations like user registration, login, profile updates.

from app.api.v1.dependencies import get_db_session, get_refresh_token_details, get_access_token_details
# - get_db_session: dependency function to provide an async database session.
# - get_refresh_token_details: dependency wrapper that resolves and validates a refresh token
# - get_access_token_details: Dependency wrapper that resolves and validates an access token.

from app.core.security import create_access_token, decode_token, verify_password
# - create_access_token: function to generate JWT tokens.
# - decode_token: function to decode and validate JWT tokens.
# - verify_password: function to validate plaintext password against hashed password.

from fastapi.responses import JSONResponse
# - JSONResponse: utility to create HTTP JSON responses with customizable status and headers.

from datetime import timedelta, datetime, timezone
# - timedelta: used to define time intervals, such as token expiration durations.
# - datetime: used to generate token issuance (`iat`) and expiration (`exp`) timestamps.
#               Always use timezone-aware values (e.g., `datetime.now(timezone.utc)`)
#               instead of naive ones like `datetime.utcnow()` to ensure consistency and
#               avoid bugs in environments that expect timezone-aware JWT claims.
# - timezone: used to make datetime objects explicitly timezone-aware (UTC),
#               ensuring proper handling in token validation across systems.

# Import async Redis helper functions for token revocation support (adding and checking JTIs)
from app.core.redis import add_jti_to_blocklist, token_in_blocklist

# Define the API router for authentication-related endpoints
auth_router = APIRouter()

# Instantiate the service layer for handling user-related operations
user_service = UserService()

# Define the number of days the refresh token should remain valid
REFRESH_TOKEN_EXPIRY = 2  # Token is valid for 2 days


@auth_router.post(
    '/signup',
    response_model=UserReadModel,
    status_code=status.HTTP_201_CREATED
)
async def create_a_user(
    user_data: UserCreateModel,
    session: AsyncSession = get_db_session()
) -> dict:
    """
    Create a new user.

    This endpoint receives user registration data, checks for duplicate emails,
    and stores the new user in the database if validation passes.

    Args:
        user_data (UserCreateModel): User data payload validated by Pydantic.
        session (AsyncSession): Async database session injected via dependency.

    Returns:
        dict: The newly created user object as defined by the response model.

    Raises:
        HTTPException: 
            - 403 if a user with the same email already exists.
    """

    # Extract the email from the incoming request data
    email = user_data.email

    # Check whether a user with the given email already exists in the database
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        # Reject the request if the email is already in use
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {email} already exists!"
        )

    # Create a new user in the database using the service layer
    new_user = await user_service.create_user(user_data, session)

    # Return the new user data, which will be serialized by the response model
    return new_user


@auth_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = get_db_session()):
    """
    Authenticate a user and issue access and refresh tokens.

    This endpoint handles user login by verifying the provided email and password.
    If the credentials are valid, it generates a short-lived access token and a long-lived
    refresh token. These tokens can be used to authorize future requests and renew sessions.

    Args:
        login_data (UserLoginModel): A validated Pydantic model containing email and password.
        session (AsyncSession): The database session injected as a dependency.

    Returns:
        JSONResponse: A response with a success message, access and refresh tokens, and user info.

    Raises:
        HTTPException: 
            - 403 Forbidden if the email is not found.
            - 403 Forbidden if the password is incorrect.

    Usage:
        POST /login
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
    """
    # Extract email and password from the validated request body
    email = login_data.email
    password = login_data.password

    # Attempt to fetch the user by email
    user = await user_service.get_user(email, session)

    # If user exists, validate the password
    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            # Generate a short-lived access token for immediate authorization
            access_token = create_access_token(
                user_data={
                    'email': email,
                    'user_uid': str(user.uid)
                }
            )

            # Generate a long-lived refresh token for renewing sessions
            refresh_token = create_access_token(
                user_data={
                    'email': email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            # Return both tokens and basic user info
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        else:
            # Password did not match
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Password"
            )

    # No user found for the given email
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email"
    )

    
@auth_router.get('/refresh_token')
async def get_user_new_access_token(token_details: dict = get_refresh_token_details()):
    """
    Generate a new access token using a valid refresh token.

    Args:
        token_details (dict): The decoded JWT payload, validated as a refresh token.

    Returns:
        JSONResponse: Contains a new access token if the refresh token is still valid.

    Raises:
        HTTPException: If the refresh token is expired or otherwise invalid.
    """
    # Extract the expiration timestamp from the refresh token payload
    expire_timestamp = token_details['exp']

    # Check whether the refresh token has not yet expired
    # Use timezone-aware comparison to avoid TypeError and ensure consistency
    if datetime.fromtimestamp(expire_timestamp, tz=timezone.utc) > datetime.now(timezone.utc):
        # If the token is still valid, generate a new access token using the embedded user data
        new_access_token = create_access_token(
            user_data=token_details['user']  # The 'user' claim was encoded during original login
        )

        # Return the new access token as a JSON response
        return JSONResponse(content={
            "access_token": new_access_token
        })

    # If the refresh token is expired, raise a 400 error indicating it is no longer valid
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token"
    )

@auth_router.get('/logout')
async def revooke_token(token_details:dict=get_access_token_details()):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged out succesful"
        },
        status_code=status.HTTP_200_OK
    )

