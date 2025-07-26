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

from app.api.v1.dependencies import get_db_session
# - get_db_session: dependency function to provide an async database session.

from app.core.security import create_access_token, decode_token, verify_password
# - create_access_token: function to generate JWT tokens.
# - decode_token: function to decode and validate JWT tokens.
# - verify_password: function to validate plaintext password against hashed password.

from fastapi.responses import JSONResponse
# - JSONResponse: utility to create HTTP JSON responses with customizable status and headers.

from datetime import timedelta
# - timedelta: used to handle time intervals (e.g., token expiration durations).


auth_router = APIRouter()

user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/signup', 
                  response_model=UserReadModel,
                  status_code=status.HTTP_201_CREATED)
async def create_a_user(user_data: UserCreateModel, session: AsyncSession = get_db_session()) -> dict:
    """
    Create a new user.

    Args:
        user_data (User): User data payload validated by Pydantic.
        session (AsyncSession): Async database session dependency.

    Returns:
        dict: The newly created user object.
    """
    
    email = user_data.email
    
    user_exists  = await user_service.user_exists(email, session)
        
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"User with email {email} already exists!"
        )
    
    # Pass validated user data to service for creation
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = get_db_session()):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user(email, session)
    
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        
        if password_valid:
            access_token = create_access_token(
                user_data ={
                    'email': email,
                    'user_uid': str(user.uid)
                }
            )
            
            refresh_token = create_access_token(
                user_data ={
                    'email': email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Password"
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email"
    )