"""
Pydantic schemas for user-related data validation and serialization.

This module defines request and response models used in user-related API operations,
such as registration, login, profile output, and user updates. These schemas validate
input data from clients and shape output data returned by the API.

Purpose:
- Enforce strict data validation rules for user-related HTTP requests and responses.
- Separate data contract definitions from internal database models.
- Enable auto-generated API documentation via FastAPI and OpenAPI.

Impact on SDLC:
- Promotes input/output consistency across the user domain.
- Reduces risk of invalid or malformed data entering the system.
- Supports clean architecture by decoupling transport-layer data from persistence models.
- Facilitates versioning and backwards compatibility of the API.
- Improves testability, type safety, and IDE support throughout the codebase.
"""
# Base class for creating Pydantic models (data validation, serialization, etc.)
from pydantic import BaseModel, Field

# Used for timestamp fields (created_at, updated_at)
from datetime import datetime

# Used for UUID primary key field (uid)
import uuid

class User(BaseModel):
    """
    Full internal representation of a user entity, including sensitive and system-managed fields.

    This schema is typically used within the backend (e.g., services or admin panels),
    where complete user information is needed, including fields like `password_hash` and 
    verification status.

    Fields:
        uid (uuid.UUID): Unique, immutable identifier for the user.
        username (str): User's login name (must be unique within the system).
        password_hash (str): Securely hashed version of the user's password.
            This field is excluded from serialization output by default.
        email (str): User's registered email address, used for recovery and communication.
        first_name (str): User's first name for display and personalization.
        last_name (str): User's last name for display and personalization.
        is_verified (bool): Indicates whether the user's email/account has been verified.
        created_at (datetime): Timestamp when the user account was initially created.
        updated_at (datetime): Timestamp of the most recent update to the user record.

    Usage:
        - Used in internal logic where full user context is required.
        - May be excluded from external API responses to avoid exposing sensitive data.
        - Supports serialization/deserialization in business logic, services, or admin tools.

    Impact on SDLC:
        - Centralizes all user-related attributes in a single schema.
        - Encourages separation between internal models and public-facing response schemas.
        - Enables fine-grained control over what data is exposed through FastAPI or other APIs.
        - Improves security by clearly marking sensitive fields like `password_hash`.
    """

    uid: uuid.UUID                                      # Unique identifier for the user
    username: str                                       # Username used for login
    password_hash: str = Field(exclude=True)           # Hashed password (excluded from output)
    email: str                                          # User's email address
    first_name: str                                     # First name for display
    last_name: str                                      # Last name for display
    is_verified: bool                                   # Email/account verification status
    created_at: datetime                                # Account creation timestamp
    updated_at: datetime                                # Last update timestamp

class UserCreateModel(BaseModel):
    """
    Schema for user registration (account creation) request payload.

    Defines the structure and validation constraints for data submitted by clients
    during user sign-up typically via a POST request endpoint.

    Fields:
        username (str): Desired username for login and display.
            Max length: 8 characters.
        password (str): Plaintext password chosen by the user.
            Max length: 6 characters.
        email (str): Email address used for recovery, notifications, or identification.
            Max length: 40 characters.
        first_name (str): User's given name for personalization and display.
            Max length: 25 characters.
        last_name (str): User's surname for personalization and display.
            Max length: 25 characters.

    Usage:
        - Used to validate incoming user registration forms or API payloads.
        - Ensures all required information is present and within acceptable bounds.

    Impact on SDLC:
        - Enforces clear contract for creating new users.
        - Reduces risk of malformed or malicious data entering the system.
        - Supports documentation and testing of account creation endpoints.
    """

    username: str = Field(max_length=8)           # Username for login
    password: str = Field(max_length=6)           # Plaintext password input
    email: str = Field(max_length=40)             # User email for identification and recovery
    first_name: str = Field(max_length=25)        # User's first name
    last_name: str = Field(max_length=25)         # User's last name

class UserReadModel(BaseModel):
    """
    Schema for reading user profile data in API responses.

    Represents a sanitized, read-only view of user information, typically returned 
    in response to authenticated GET requests (e.g., profile endpoints, admin views).

    Fields:
        uid (uuid.UUID): Unique identifier for the user, used for referencing and auditing.
        username (str): Public username used for login and display.
        email (str): User's registered email address (may be used for contact or recovery).
        first_name (str): User's first name for display purposes.
        last_name (str): User's last name for display purposes.
        created_at (datetime): Timestamp indicating when the user account was created.
        updated_at (datetime): Timestamp of the last update to the user profile.

    Usage:
        - Returned by endpoints that expose user details.
        - Excludes sensitive fields like passwords or internal flags.

    Impact on SDLC:
        - Promotes safe exposure of user data to external consumers.
        - Supports response consistency across user-facing endpoints.
        - Decouples transport-layer representation from internal database or ORM models.
    """

    uid: uuid.UUID                          # Unique identifier for the user
    username: str                           # Username used for login and display
    email: str                              # Registered email address
    first_name: str                         # First name for personalization
    last_name: str                          # Last name for personalization
    created_at: datetime                    # Account creation timestamp
    updated_at: datetime                    # Last profile update timestamp

class UserLoginModel(BaseModel):
    """
    Schema for user login request payload.

    Defines the required structure and validation rules for login credentials submitted 
    by clients (typically via a POST request to an authentication endpoint).

    Fields:
        email (str): User's email address used for identification. 
            Max length: 40 characters.
        password (str): User's plaintext password to be verified against the stored hash.
            Max length: 6 characters.

    Usage:
        - Used in login forms or API calls to validate the input before attempting authentication.
        - Ensures minimal, required fields are present and properly formatted.

    Impact on SDLC:
        - Improves security by validating input early.
        - Reduces attack surface by rejecting malformed login attempts.
        - Supports clean separation between authentication logic and transport-layer concerns.
    """

    password: str = Field(max_length=6)          # Password input for login
    email: str = Field(max_length=40)            # Email input for login
