"""
Version 1 (v1) Pydantic schemas for API data validation and serialization.

Purpose:
- Encapsulate all Pydantic models that define request and response payloads for API version v1.
- Serve as the contract between v1 clients and the server, ensuring strict validation and serialization.
- Isolate schema changes to this version, supporting backward compatibility and controlled evolution.

What to include:
- Domain-specific schema modules, e.g., `book.py`, `user.py`.
- Models for input validation (create/update), output serialization, and shared base models.
- Version-specific validation rules, custom validators, and example data for OpenAPI docs.

Future considerations:
- Add subfolders or modules for complex domains or feature sets as v1 grows.
- Include version-specific response envelopes or error schemas if needed.

Impact on SDLC:
- Enables parallel development and maintenance of multiple API versions.
- Minimizes risk of breaking existing clients during schema evolution.
- Supports clean separation of transport-layer contracts per API version.
- Facilitates generating accurate OpenAPI documentation for each API version.
"""

