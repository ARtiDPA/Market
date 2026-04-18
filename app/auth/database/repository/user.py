"""User repository for database operations.

This module provides the UserRepository class that handles all database
operations related to User model. It follows the Repository pattern to
separate data access logic from business logic.

The repository provides CRUD operations:
- Create new users
- Read users by various criteria (id, email)
- Update user information (name, email, password)
- Delete users

Example:
    from app.auth.database.repository.user import UserRepo
    
    # Create user
    user = UserRepo.create_user(
        login="user123",
        password="secret",
        email="user@example.com",
        name="John",
        last_name="Doe"
    )
    
    # Get user
    user = UserRepo.get_user_by_email("user@example.com")
    
    # Update user
    UserRepo.change_user_info(user_id=1, name="Jane", last_name="Smith")
"""
# pylint: disable=not-context-manager
# pylint: disable=no-member
from sqlalchemy.orm import Session

from app.auth.database.database import get_db
from app.auth.database.models.user import User
from app.auth.security import PasswordHasher as hash

class UserRepository:
    """Repository for User model database operations."""

    def create_user(
        self,
        login: str,
        password: str,
        email: str,
        name: str,
        last_name: str,
    ):
        """Create new user in database.

        Args:
            login (str): User login (unique).
            password (str): Plain text password (will be hashed).
            email (str): User email (unique).
            name (str): User first name.
            last_name (str): User last name.
            
        Returns:
            User: Created user instance.
            
        Raises:
            ValueError: If email or login already exists.
        """
        db: Session
        user = User(
            login=login,
            hash_password=hash.hash_password(password),
            email=email,
            name=name,
            last_name=last_name,
        )

        with get_db() as db:
            ex = db.query(User).filter(
                (User.login == user.login) | (User.email == user.email)
            ).first()
            if ex:
                raise ValueError('Email or login already exists')

            db.add(user)
            db.commit()

            return user

    def login_user(self, login: str):
        db: Session

        with get_db() as db:
            user = db.query(User).filter(
                (User.login == login)
            ).first()

            if user:
                return user
            
            raise ValueError('User not found')

    def get_user_by_id(self, user_id: int):
        """Get user by ID.
        
        Args:
            user_id (int): User ID.
            
        Returns:
            User: User instance.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session

        with get_db() as db:
            ex = db.query(User).filter(User.id == user_id).first()
            if not ex:
                raise ValueError('User not found')

            return ex
    
    def get_user_by_email(self, email: str):
        """Get user by email.
        
        Args:
            email (str): User email.
            
        Returns:
            User: User instance.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session

        with get_db() as db:
            ex = db.query(User).filter(User.email == email).first()
            if not ex:
                raise ValueError('User not found')

            return ex

    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID.
        
        Args:
            user_id (int): User ID.
            
        Returns:
            bool: True if user was deleted.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
                db.commit()
                return True
            raise ValueError('User not found')

    def change_user_info(self, user_id: int, name: str, last_name: str):
        """Update user name and last name.
        
        Args:
            user_id (int): User ID.
            name (str): New first name.
            last_name (str): New last name.
            
        Returns:
            User: Updated user instance.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.name = name
                user.last_name = last_name
                db.commit()
                return user

            raise ValueError('User not found')

    def change_password(self, user_id: int, hash_password: str):
        """Update user password.
        
        Args:
            user_id (int): User ID.
            hash_password (str): New hashed password.
            
        Returns:
            User: Updated user instance.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.hash_password = hash_password
                db.commit()
                return user

            raise ValueError('User not found')

    def change_email(self, user_id: int, email: str):
        """Update user email.
        
        Args:
            user_id (int): User ID.
            email (str): New email address.
            
        Returns:
            User: Updated user instance.
            
        Raises:
            ValueError: If user not found.
        """
        db: Session
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.email = email
                db.commit()
                return user

            raise ValueError('User not found')


UserRepo = UserRepository()
