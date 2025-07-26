"""
Application entry point.

This module creates and configures the FastAPI app instance, registers API routes,
and serves as the root for dependency injection, startup/shutdown events, and middleware.

Purpose:
- Launches the application via ASGI (e.g., with Uvicorn).
- Organizes the app's root structure (title, description, routes).
- Central place for initializing CORS, logging, error handlers.

Impact on SDLC:
- Encourages clean initialization flow for development and deployment.
- Minimizes coupling between routing and business logic.
- Acts as the focal point for scalability and environment-specific customization.
"""

# Core FastAPI app class used to create the ASGI application
from fastapi import FastAPI

# Router for book-related endpoints (e.g., CRUD operations)
from app.api.v1.routes.book import book_router

# Router for auth-related endpoints (e.g., CRUD operations)
from app.api.v1.routes.user import auth_router

# Context manager utility for defining app lifespan hooks (startup and shutdown)
from contextlib import asynccontextmanager

# Application startup and shutdown event handlers (e.g., database, logging setup)
from app.core.events import startup_event, shutdown_event


@asynccontextmanager
async def life_span(app: FastAPI):
    """
    Lifespan handler for the FastAPI app.

    Runs application-level startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    # Trigger custom startup logic (e.g., database initialization)
    await startup_event()

    # Yield control to allow app execution
    yield

    # Trigger custom shutdown logic (e.g., resource cleanup)
    await shutdown_event()


# Application version used in routing and documentation
version = "v1"

# Create the FastAPI app instance with metadata and lifespan handler
app = FastAPI(
    title="Bookly",  # API title for OpenAPI docs
    description="A REST API for a book review web service",  # Description in Swagger UI
    version=version,  # Version used in OpenAPI and URL prefixing
    lifespan=life_span  # Custom lifespan context manager
)

# Register the book router with a versioned API prefix and tag for documentation grouping
app.include_router(
    book_router,
    prefix=f"/api/{version}/books",  # e.g., /api/v1/books
    tags=["books"]  # OpenAPI grouping
)

# Register the auth router with a versioned API prefix and tag for documentation grouping
app.include_router(
    auth_router,
    prefix=f"/api/{version}/auth",  # e.g., /api/v1/books
    tags=["auth"]  # OpenAPI grouping
)



