"""
Book-related API routes (v1).

Defines RESTful endpoints for managing book resources using FastAPI's APIRouter.

Purpose:
- Implements versioned API endpoints: list, create, retrieve, update, delete books.
- Ties together Pydantic schemas, service layer, and route-level validation.

Impact on SDLC:
- Facilitates backward compatibility by isolating version-specific behavior.
- Supports API evolution without breaking existing consumers.
- Keeps domain logic modular and testable.
"""
# FastAPI imports:
from fastapi import APIRouter, status
# - APIRouter: to create a modular group of routes.
# - status: to provide HTTP status code constants.

from fastapi.exceptions import HTTPException  
# - HTTPException: used to raise HTTP errors with status codes and details.

from typing import List  
# - List: for type hinting the response as a list of Pydantic models.

# Pydantic schemas for request and response validation:
from app.schemas import Book, BookCreateModel, BookUpdateModel, BookReadModel
# - Book, BookCreateModel, BookUpdateModel, BookReadModel:
#   Pydantic models defining the structure and validation of book-related API payloads.

from app.api.v1.dependencies import get_db_session, get_user_details
# - get_db_session: dependency function to provide an async database session.
# - get_user_details: dependency that extracts user info via access token authentication.

# SQLModel async session type for typing the session parameter:
from sqlmodel.ext.asyncio.session import AsyncSession
# - AsyncSession: SQLModel's asynchronous session type used for database operations.

# Service layer encapsulating business logic for book management:
from app.services.book import BookService
# - BookService: business logic class handling operations like CRUD for books.

# Create an APIRouter instance to register book-related routes
book_router = APIRouter()

# Instantiate the BookService that handles the core business logic
book_service = BookService()


@book_router.get('/', response_model=List[Book])
async def get_all_books(session: AsyncSession = get_db_session(), user_details=get_user_details()):
    """
    Retrieve all books.

    Args:
        session (AsyncSession): Async database session dependency.

    Returns:
        List[Book]: A list of all books serialized via Pydantic schema.
    """
    # Delegate the fetch operation to the service layer
    books = await book_service.get_all_books(session)
    return books


@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = get_db_session(), user_details=get_user_details()) -> dict:
    """
    Create a new book.

    Args:
        book_data (Book): Book data payload validated by Pydantic.
        session (AsyncSession): Async database session dependency.

    Returns:
        dict: The newly created book object.
    """
    # Pass validated book data to service for creation
    new_book = await book_service.create_book(book_data, session)
    return new_book
     

@book_router.get('/{book_uid}', response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = get_db_session(), user_details=get_user_details()) -> dict:
    """
    Retrieve a book by its unique ID.

    Args:
        book_uid (int): Unique identifier of the book.
        session (AsyncSession): Async database session dependency.

    Returns:
        dict: Book data if found.

    Raises:
        HTTPException 404: If book with given ID does not exist.
    """
    # Fetch book from service layer
    book = await book_service.get_book(book_uid, session)
    
    if book is not None:
        return book
    
    # Raise 404 if book not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 


@book_router.patch('/{book_uid}', response_model=BookUpdateModel)
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = get_db_session(), user_details=get_user_details()) -> dict:
    """
    Update a book partially by its unique ID.

    Args:
        book_uid (int): Unique identifier of the book.
        book_update_data (BookUpdateModel): Partial update data validated by Pydantic.
        session (AsyncSession): Async database session dependency.

    Returns:
        dict: Updated book data if successful.

    Raises:
        HTTPException 404: If book with given ID does not exist.
    """
    # Delegate update to service layer
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    
    if updated_book is not None:
        return updated_book
    
    # Raise 404 if no book found to update
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = get_db_session(), user_details=get_user_details()):
    """
    Delete a book by its unique ID.

    Args:
        book_uid (int): Unique identifier of the book.
        session (AsyncSession): Async database session dependency.

    Raises:
        HTTPException 404: If book with given ID does not exist.
    """
    # Perform deletion via service
    book_deleted = await book_service.delete_book(book_uid, session)
    
    # If no book was deleted, raise 404 error
    if book_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
