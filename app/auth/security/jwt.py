"""JWT token creation and validation."""
from datetime import datetime, timedelta
from typing import Dict, Any
from jose import JWTError, jwt
from app.init.config import get_settings


class JWTManager:
    """JWT token manager for access and refresh tokens."""
    
    def __init__(self):
        """Initialize JWT manager with settings."""
        self.settings = get_settings()
        self.secret_key = self.settings.secret_key
        self.algorithm = self.settings.algorithm
        self.access_token_expire_minutes = self.settings.access_token_expire_minutes
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
        """Create access token.
        
        Args:
            data: Data to encode in token.
            expires_delta: Optional custom expiration time.
            
        Returns:
            Encoded JWT token.
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
        """Create refresh token.
        
        Args:
            data: Data to encode in token.
            expires_delta: Optional custom expiration time (default 7 days).
            
        Returns:
            Encoded JWT token.
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any] | None:
        """Verify and decode token.
        
        Args:
            token: JWT token to verify.
            token_type: Expected token type ("access" or "refresh").
            
        Returns:
            Decoded token payload or None if invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None


# Global JWT manager instance
jwt_manager = JWTManager()
