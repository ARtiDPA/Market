"""Database session management for auth service."""
from typing import Generator
from sqlalchemy.orm import Session
from app.init.database import get_database


def get_db() -> Generator[Session, None, None]:
    """Get database session for auth service.
    
    Yields:
        SQLAlchemy Session instance.
    """
    database = get_database()
    session = database.get_session()
    try:
        yield session
    finally:
        session.close()
