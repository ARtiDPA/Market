"""Core module with configuration and connections."""
from app.auth.core.config import get_settings, Settings
from app.auth.core.database import get_db, Base, get_database_config
from app.auth.core.redis import get_redis, get_redis_client

__all__ = [
    "get_settings",
    "Settings",
    "get_db",
    "Base",
    "get_database_config",
    "get_redis",
    "get_redis_client",
]
