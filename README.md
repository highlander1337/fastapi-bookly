# How to create a FastAPI application

<https://youtu.be/TO4aQ3ghFOc?t=21005>

## Create a folder structure

``` md

sql-bookly/
│
├── app/                            # Core application source code
│   ├── __init__.py                 # Package initialization
│   ├── main.py                    # FastAPI app instance, including startup and shutdown event handlers
│   ├── config.py                  # Application configuration using Pydantic BaseSettings
│
│   ├── api/                       # API layer with versioned routers and dependencies
│   │   ├── __init__.py
│   │   ├── v1/                    # API version 1 (client-facing endpoints)
│   │   │   ├── __init__.py
│   │   │   ├── routes/            # Domain-specific route handlers/endpoints
│   │   │   │   ├── books.py       # Book resource endpoints (CRUD)
│   │   │   │   └── users.py       # User resource endpoints (auth, profile, etc.)
│   │   │   └── dependencies.py   # Reusable dependency injection functions (e.g., DB session, auth)
│
│   ├── core/                      # Core infrastructure and cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── security.py           # Authentication/authorization helpers (JWT creation, password hashing)
│   │   ├── dependencies.py       # Core reusable security dependencies (e.g., AccessTokenBearer)
│   │   └── events.py             # Application startup/shutdown event handlers
│
│   ├── db/                       # Database configuration and models
│   │   ├── __init__.py
│   │   ├── main.py               # Database engine and connection setup
│   │   ├── session.py            # Async session factory for dependency injection
│   │   └── models/               # Data models using SQLModel/ORM
│   │       ├── __init__.py
│   │       ├── book.py
│   │       └── user.py
│
│   ├── schemas/                  # Pydantic data validation and serialization schemas
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── book.py           # Book-related request and response models
│   │   │   └── user.py           # User-related request and response models
│
│   ├── services/                 # Business logic layer abstracting database operations
│   │   ├── __init__.py
│   │   ├── book.py               # Book domain services (CRUD logic, validations)
│   │   └── user.py               # User domain services (auth, registration, profile updates)
│
│   └── utils/                    # Helper functions and utility modules
│       ├── __init__.py
│       └── helpers.py
│
├── .env                         # Environment variables (local development and production configs)
├── requirements.txt             # Python package dependencies
├── alembic/                     # Alembic migration scripts (DB version control)
├── alembic.ini                  # Alembic configuration file
├── tests/                       # Automated test suite (unit and integration tests)
│   ├── __init__.py
│   ├── test_books.py             # Tests for book domain and API
│   └── test_users.py             # Tests for user domain and API
└── README.md                    # Project overview and instructions

```

---

## Create an alembic folder

``` bash
alembic init -t async `folder_name`
```

Alembic plays a **critical role** in managing the **evolution of the database schema** in a FastAPI + PostgreSQL project. To understand *why it's needed*, let’s break it down from the perspectives of:

## 🧠 High-Level Design (HLD)

At a high level, your FastAPI application consists of:

* **Business Logic Layer (FastAPI routes, services)**
* **Data Layer (PostgreSQL database with models)**
* **Schema Definitions (SQLModel / SQLAlchemy models)**
* **DevOps/Deployment infrastructure**

Without Alembic:

* You have no clean mechanism to evolve the database schema over time.
* Any schema change (e.g., adding a new column) would require manual SQL migrations, which is error-prone and hard to track.

With Alembic:

* You introduce a **migration system** that tracks changes to the schema **as part of the source code**.
* It enables **versioned schema evolution**, aligned with application code updates.
* It's part of the **Infrastructure as Code** philosophy.

> ✅ In HLD terms, Alembic serves as the **Schema Version Control Subsystem**.

---

## 🔧 Low-Level Design (LLD)

From the LLD perspective, let’s say you have a model like:

```python
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
```

Now you add a new field:

```python
email: str | None = None
```

You need this change to reflect in the **actual database table**.

Without Alembic:

* You’d need to manually ALTER the table via SQL.
* Hard to automate, error-prone, not trackable.

With Alembic:

* You generate a migration with:

  ```bash
  alembic revision --autogenerate -m "add email to user"
  ```

* It detects the change and produces a versioned migration file.
* You apply it with:

  ```bash
  alembic upgrade head
  ```

* Migration scripts become part of your repository and deployment flow.

> ✅ In LLD, Alembic acts as the **automated database schema migration engine** that supports **code-first database design**.

---

## 🔄 Software Development Life Cycle (SDLC)

Here’s how Alembic fits into each phase of the SDLC:

| Phase           | Role of Alembic                                                                 |
| --------------- | ------------------------------------------------------------------------------- |
| **Planning**    | Database schema changes are planned alongside feature planning.                 |
| **Design**      | Alembic integrates into architectural design as the schema change manager.      |
| **Development** | Developers write models, autogenerate Alembic migrations, and test them.        |
| **Testing**     | Test databases are spun up with the latest schema via `alembic upgrade`.        |
| **Deployment**  | Alembic migrations run as part of CI/CD pipelines (e.g., in Docker entrypoint). |
| **Maintenance** | Future changes are handled safely through new migrations; history is preserved. |

> ✅ In SDLC terms, Alembic enables **repeatable, auditable, and automated schema changes**, which is vital for collaboration, deployment, rollback, and maintainability.

---

## 🔒 Why Alembic is **Needed**, Not Just "Nice to Have"

* Schema changes are inevitable.
* Manual SQL migrations don’t scale.
* Migrations must be versioned, tested, and deployed just like code.
* It avoids desync between models and the actual database.
* Alembic is fully compatible with **async**, **SQLModel**, and **SQLAlchemy**, making it the de-facto standard in FastAPI projects.

---

## ✅ Summary

| Perspective | Why Alembic Matters                                                      |
| ----------- | ------------------------------------------------------------------------ |
| **HLD**     | Provides a schema versioning system as a core infrastructure component   |
| **LLD**     | Automates and tracks DB schema changes aligned with model changes        |
| **SDLC**    | Supports safe, repeatable migrations in dev, test, CI/CD, and production |

## How to generate a secret key

``` python
  import secrets
  secrets.token_hex(16) # generate a 16 bits key
```

## How to install dependencies from requirments.txt

``` bash
  pip install -r requirements.txt
```

## How to start the app

``` bash
  uvicorn app.main:app --reload
```