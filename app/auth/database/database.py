"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class Database:
    """Database connection manager."""
    
    def __init__(self, database_url: str | None = None):
        """Initialize database connection."""
        if database_url:
            self.database_url = database_url
        else:
            from app.auth.config import get_settings
            self.database_url = get_settings().database_url
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get new database session."""
        return self.SessionLocal()


db: Database | None = None


def get_database() -> Database:
    """Get or create global database instance."""
    global db
    if db is None:
        db = Database()
    return db


def get_db() -> Generator[Session, None, None]:
    """Get database session for FastAPI."""
    database = get_database()
    session = database.get_session()
    try:
        yield session
    finally:
        session.close()
