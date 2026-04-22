"""Redis connection management."""
from redis import Redis
from typing import Optional
from app.auth.core.config import get_settings


class RedisClient:
    """Redis client manager."""
    
    def __init__(self, redis_url: str | None = None):
        """Initialize Redis connection.
        
        Args:
            redis_url: Redis connection URL. If None, reads from config.
        """
        if redis_url:
            self.redis_url = redis_url
        else:
            settings = get_settings()
            self.redis_url = settings.redis.url
        
        self.client: Optional[Redis] = None
    
    def connect(self) -> Redis:
        """Connect to Redis.
        
        Returns:
            Redis client instance.
        """
        if self.client is None:
            self.client = Redis.from_url(
                self.redis_url,
                decode_responses=True,
                encoding="utf-8"
            )
        return self.client
    
    def disconnect(self):
        """Disconnect from Redis."""
        if self.client:
            self.client.close()
            self.client = None
    
    def get_client(self) -> Redis:
        """Get Redis client (connects if not connected).
        
        Returns:
            Redis client instance.
        """
        if self.client is None:
            return self.connect()
        return self.client


# Global Redis client instance
redis_client: RedisClient | None = None


def get_redis_client() -> RedisClient:
    """Get or create global Redis client instance."""
    global redis_client
    if redis_client is None:
        redis_client = RedisClient()
    return redis_client


def get_redis() -> Redis:
    """Get Redis connection for dependency injection.
    
    Returns:
        Redis client instance.
    """
    client = get_redis_client()
    return client.get_client()
