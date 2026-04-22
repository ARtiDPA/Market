"""Database configuration and connection management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
from app.auth.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class DatabaseConfig:
    """Database configuration manager."""
    
    def __init__(self, database_url: str | None = None):
        """Initialize database configuration.
        
        Args:
            database_url: Database connection URL. If None, reads from config.
        """
        if database_url:
            self.database_url = database_url
        else:
            settings = get_settings()
            self.database_url = settings.database.url
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get new database session.
        
        Returns:
            SQLAlchemy Session instance.
        """
        return self.SessionLocal()


# Global database instance
db_config: DatabaseConfig | None = None


def get_database_config() -> DatabaseConfig:
    """Get or create global database config instance."""
    global db_config
    if db_config is None:
        db_config = DatabaseConfig()
    return db_config


def get_db() -> Generator[Session, None, None]:
    """Get database session for FastAPI dependency injection.
    
    Yields:
        SQLAlchemy Session instance.
    """
    config = get_database_config()
    session = config.get_session()
    try:
        yield session
    finally:
        session.close()
