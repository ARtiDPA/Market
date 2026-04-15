"""Dummy model for testing."""
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.init.database import Base


class Dummy(Base):
    """Dummy table for testing migrations."""
    
    __tablename__ = "dummy"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
