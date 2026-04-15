"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import os


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class Database:
    """Database connection manager."""
    
    def __init__(self, database_url: str | None = None):
        """Initialize database connection.
        
        Args:
            database_url: Database connection URL. If None, reads from config.
        """
        if database_url:
            self.database_url = database_url
        else:
            from app.init.config import get_settings
            self.database_url = get_settings().database_url
        
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=Session
        )
    
    def get_session(self) -> Session:
        """Get new database session.
        
        Returns:
            SQLAlchemy Session instance.
        """
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Provide a transactional scope for database operations.
        
        Yields:
            SQLAlchemy Session instance.
            
        Example:
            with db.session_scope() as session:
                user = session.query(User).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Create all tables in database."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables from database."""
        Base.metadata.drop_all(bind=self.engine)


# Global database instance (lazy initialization)
db: Database | None = None


def get_database() -> Database:
    """Get or create global database instance."""
    global db
    if db is None:
        db = Database()
    return db


def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database session.
    
    Yields:
        SQLAlchemy Session instance.
        
    Example:
        @app.get("/users")
        def get_users(session: Session = Depends(get_db)):
            return session.query(User).all()
    """
    database = get_database()
    session = database.get_session()
    try:
        yield session
    finally:
        session.close()
