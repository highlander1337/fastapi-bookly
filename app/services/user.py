"""
Business logic layer for user operations.

This module implements the core functionality related to users, including creating accounts,
authenticating credentials, retrieving user profiles, and updating user information.
It encapsulates non-trivial logic and coordinates communication between database models,
schemas, and external components like authentication or hashing utilities.

Purpose:
- Centralize and encapsulate user-related business rules and behaviors.
- Separate domain logic from route handlers and persistence concerns.
- Enable service reuse across APIs, backg+round tasks, and CLI tools.

Impact on SDLC:
- Promotes separation of concerns by decoupling route logic from domain behavior.
- Enhances testability by allowing services to be tested independently from the API.
- Increases maintainability and scalability as business logic grows in complexity.
- Facilitates unit testing and mocking by isolating logic behind service interfaces.
- Supports clean architecture by acting as the “use case” or “application service” layer.
"""
# Import the asynchronous SQLModel session for executing async database operations
from sqlmodel.ext.asyncio.session import AsyncSession

# Import Pydantic schemas for user creation and update, which provide structure and validation
from app.schemas import UserCreateModel

# Import SQLModel tools to construct SQL statements and sorting
from sqlmodel import select, desc

# Import the User ORM model used to interact with the books table in the database
from app.db.models.user import User

from app.core.security import get_password_hash, verify_password



class UserService:
    """
    Service class responsible for handling user-related business logic.
    
    It abstracts all database operations for users, acting as a middle layer 
    between API routes and the persistence layer.
    """
    
    async def get_user(self, email:str, session:AsyncSession):
        """
        Retrieve a single user by its email.

        Args:
            email (str): The email of the user to fetch.
            session (AsyncSession): The database session to use for querying.

        Returns:
            User or None: The matching User object if found, otherwise None.
        """
        # Construct a query to find the user by email
        statement = select(User).where(User.email == email)
        
        # Execute the query
        result = await session.exec(statement)
        
        # Fetch the first result (should only be one due to email uniqueness)
        user = result.first()
        
        return None if user is None else user
    
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        """
        Check whether a user with the given email exists in the database.

        This method delegates the lookup logic to `get_user` and simply returns
        a boolean value indicating whether the user was found.

        Args:
            email (str): The email address to check for existence.
            session (AsyncSession): The database session used for querying.

        Returns:
            bool: True if a user with the specified email exists, False otherwise.

        Usage:
            Used during registration to prevent duplicate accounts, or during login
            flows to validate if the account is registered.
        """
        # Attempt to retrieve the user by email
        user = await self.get_user(email, session)

        # Return True if user was found, otherwise False
        return user is not None

    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """
        Create a new user record in the database.

        Args:
            user_data (UserCreateModel): The validated data for creating the user.
            session (AsyncSession): The database session used for the operation.

        Returns:
            User: The newly created User object.
        """
        
        # Convert Pydantic model to dictionary
        user_data_dict = user_data.model_dump()
        
        # Create a User instance with the provided data
        new_user = User(**user_data_dict)
        
        new_user.password_hash = get_password_hash(user_data_dict['password'])
        
        # Add the new book to the session
        session.add(new_user)
        
        # Commit the transaction to save it to the database
        await session.commit()
        
        return new_user