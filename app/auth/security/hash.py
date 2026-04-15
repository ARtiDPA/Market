"""Security utilities for password hashing and verification."""
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    """Password hashing and verification."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password.
        
        Args:
            password: Plain text password.
            
        Returns:
            Hashed password.
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash.
        
        Args:
            plain_password: Plain text password.
            hashed_password: Hashed password to verify against.
            
        Returns:
            True if password matches, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)
