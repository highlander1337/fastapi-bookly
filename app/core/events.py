"""
Application lifecycle event handlers.

This module defines startup and shutdown functions that are executed when the FastAPI
application starts or stops. These handlers can be used to initialize resources such as
database connections, load caches, configure logging, or perform graceful shutdowns.

Purpose:
- Run initialization logic (e.g., test DB connection, warm-up services).
- Release resources or close connections on shutdown.
- Register background tasks or health check hooks.

Impact on SDLC:
- Improves observability and reliability during deployment.
- Ensures consistent environment initialization across dev/stage/prod.
- Encourages separation of concerns: keeps app startup logic modular and testable.
- Supports scalability by managing third-party services (e.g., Redis, message queues).
"""

# Import function to initialize database tables and metadata
from app.db.main import init_db


async def startup_event():
    """
    FastAPI startup event handler.

    Called once when the application starts. Use this to initialize services like:
    - Database setup
    - Logging configuration
    - Cache warm-up
    - Health checks or background jobs
    """
    print(" Application starting up...")

    # Initialize the database schema (tables, metadata)
    await init_db()


async def shutdown_event():
    """
    FastAPI shutdown event handler.

    Called once when the application is stopping. Use this to:
    - Close open resources
    - Disconnect from services
    - Perform cleanup tasks
    """
    print(" Application shutting down...")

    # Example: Close DB pools, flush caches, etc. (not implemented yet)
