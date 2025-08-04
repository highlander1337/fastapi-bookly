"""
Application configuration module using environment variables.

Defines settings using Pydantic's BaseSettings, loading values from `.env` files or the OS environment.

Purpose:
- Centralizes all config values (DB URL, secrets, debug mode).
- Ensures type-safe, validated configuration.

Impact on SDLC:
- Improves portability across environments (dev, staging, prod).
- Reduces hardcoding and increases deployment safety.
- Essential for CI/CD, secrets management, and containerization (e.g., Docker).
"""

# Import BaseSettings for environment-driven configuration and SettingsConfigDict for customization
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration management using Pydantic BaseSettings.

    This class loads environment-specific settings (such as secrets, DB URLs, and 
    cryptographic keys) from either environment variables or a `.env` file.

    Attributes:
        DATABASE_URL (str): The connection URL for the application's database. 
            Format: postgresql+asyncpg://user:password@host:port/dbname
        JWT_SECRET (str): Secret key used to sign and verify JWT tokens.
        JWT_ALGORITHM (str): Algorithm used for JWT token encoding/decoding 
            (e.g., "HS256").

    Behavior:
        - Reads values from a `.env` file or environment variables automatically.
        - Ignores any variables not explicitly declared in the model.
        - Enables secure and environment-agnostic configuration management.
    
    Impact on SDLC:
        - Promotes separation of configuration from code.
        - Supports different environments (development, staging, production) without code changes.
        - Enhances security by keeping secrets out of source code.
    """

    # Database connection string (e.g., postgresql+asyncpg://user:pass@host/db)
    DATABASE_URL: str
    
    # JWT secret key for token access generation
    JWT_SECRET: str
    
    # JWT algorithm for token access generation
    JWT_ALGORITHM: str

    # REDIST host address for token revoking
    REDIS_HOST: str = "localhost"
    
    # REDIST host port for token revoking
    REDIS_PORT: int = 6379

    REDIS_USERNAME: str

    REDIS_PASSWORD: str

    # Configures how Pydantic loads and validates environment variables
    model_config = SettingsConfigDict(
        env_file=".env",   # Specifies the file to load environment variables from
        extra="ignore"     # Ignores any env vars not explicitly defined in this class
    )


# Instantiate the settings at module level for global access
Config = Settings()
