"""
Business logic layer for book operations.

Encapsulates non-trivial logic like filtering, validation, and database interaction.

Purpose:
- Keeps routes thin by moving core logic into services.
- Acts as a middle layer between routes and database.

Impact on SDLC:
- Encourages reusability and testability.
- Makes business rules easier to locate and modify.
- Improves separation of concerns and reduces duplication.
"""

# Import the asynchronous SQLModel session for executing async database operations
from sqlmodel.ext.asyncio.session import AsyncSession

# Import Pydantic schemas for book creation and update, which provide structure and validation
from app.schemas import BookCreateModel, BookUpdateModel

# Import SQLModel tools to construct SQL statements and sorting
from sqlmodel import select, desc

# Import the Book ORM model used to interact with the books table in the database
from app.db.models.book import Book


class BookService:
    """
    Service class responsible for handling book-related business logic.
    
    It abstracts all database operations for books, acting as a middle layer 
    between API routes and the persistence layer.
    """

    async def get_all_books(self, session: AsyncSession):
        """
        Retrieve all books from the database, sorted by creation date descending.

        Args:
            session (AsyncSession): The database session to use for querying.

        Returns:
            List[Book]: A list of all Book records, most recently created first.
        """
        # Construct SQL query to select all books ordered by created_at descending
        statement = select(Book).order_by(desc(Book.created_at))
        
        # Execute the query asynchronously
        result = await session.exec(statement)
        
        # Return all fetched records
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        """
        Retrieve a single book by its unique identifier.

        Args:
            book_uid (str): The UID of the book to fetch.
            session (AsyncSession): The database session to use for querying.

        Returns:
            Book or None: The matching Book object if found, otherwise None.
        """
        # Construct a query to find the book by UID
        statement = select(Book).where(Book.uid == book_uid)
        
        # Execute the query
        result = await session.exec(statement)
        
        # Fetch the first result (should only be one due to UID uniqueness)
        book = result.first()
        
        return None if book is None else book

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """
        Create a new book record in the database.

        Args:
            book_data (BookCreateModel): The validated data for creating the book.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Book: The newly created Book object.
        """
        # Convert Pydantic model to dictionary
        book_data_dict = book_data.model_dump()
        
        # Create a Book instance with the provided data
        new_book = Book(**book_data_dict)
        
        # new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
        
        # Add the new book to the session
        session.add(new_book)
        
        # Commit the transaction to save it to the database
        await session.commit()
        
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        """
        Update an existing book's fields with new data.

        Args:
            book_uid (str): The UID of the book to update.
            update_data (BookUpdateModel): The validated update data.
            session (AsyncSession): The database session to use for the operation.

        Returns:
            Book or None: The updated Book object, or None if the book was not found.
        """
        # Try to retrieve the book to be updated
        book_to_update = await self.get_book(book_uid, session)
        
        if book_to_update is None:
            return None  # Book not found
        
        # Convert the update data into a dictionary
        update_data_dict = update_data.model_dump()
        
        # Apply each update field to the book object
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        
        # Commit the transaction to apply the changes
        await session.commit()
        
        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        """
        Delete a book from the database by its UID.

        Args:
            book_uid (str): The UID of the book to delete.
            session (AsyncSession): The database session used for the deletion.

        Returns:
            None or Book: The deleted Book object if it existed, otherwise None.
        """
        # Try to retrieve the book to be deleted
        book_to_delete = await self.get_book(book_uid, session)
        
        if book_to_delete is None:
            return None  # Book not found
        
        # Delete the book from the session
        await session.delete(book_to_delete)
        
        # Commit the transaction to finalize the deletion
        await session.commit()
        
        return book_to_delete
