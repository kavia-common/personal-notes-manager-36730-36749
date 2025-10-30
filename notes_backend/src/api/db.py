from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Use .env if present (optional)
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # dotenv is optional; ignore if not available
    pass


class Base(DeclarativeBase):
    """SQLAlchemy base model."""


def _get_database_url() -> str:
    """
    Resolve the database URL from environment or default to local SQLite file.
    NOTES_DB_URL can be provided via environment variables.
    """
    # Prefer NOTES_DB_URL if provided, fallback to a local SQLite file
    return os.getenv("NOTES_DB_URL", "sqlite:///./notes.db")


DATABASE_URL = _get_database_url()

# SQLite requires check_same_thread=False when used with standard threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """
    Dependency provider for FastAPI routes to get a database session.

    Yields:
        Session: SQLAlchemy session. Closes after request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Context manager for non-request DB usage (scripts, tasks)."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
