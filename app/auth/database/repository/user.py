"""Repository from user."""
# pylint: disable=not-context-manager
# pylint: disable=no-member
from sqlalchemy.orm import Session

from app.init.database import get_db
from app.init.models.user import User
from app.auth.security import PasswordHasher as hash

class UserRepository:
    def create_user(
        self,
        login: str,
        password: str,
        email: str,
        name: str,
        last_name: str,
    ):
        """Register user

        Args:
            login (str): login
            password (str): password(no hash)
            email (str): email
            name (str): name
            last_name (str): last_name
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

repo = UserRepository()
