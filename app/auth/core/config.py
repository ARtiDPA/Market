"""Core configuration with validation."""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    url: str = Field(..., alias="DATABASE_URL", description="PostgreSQL connection URL")
    
    @field_validator("url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with 'postgresql://'")
        return v


class RedisSettings(BaseSettings):
    """Redis configuration."""
    
    url: str = Field(..., alias="REDIS_URL", description="Redis connection URL")
    
    @field_validator("url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v.startswith("redis://"):
            raise ValueError("REDIS_URL must start with 'redis://'")
        return v


class SecuritySettings(BaseSettings):
    """Security configuration."""
    
    secret_key: str = Field(..., min_length=32, description="Secret key for JWT")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, gt=0, description="Access token expiration in minutes")
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key is not default."""
        if "change-this" in v.lower() or "dev-secret" in v.lower():
            raise ValueError("SECRET_KEY must be changed from default value in production")
        return v


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # Redis
    redis: RedisSettings = Field(default_factory=RedisSettings)
    
    # Security
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        """Initialize settings with nested configs."""
        super().__init__(**kwargs)
        # Initialize nested settings from environment
        self.database = DatabaseSettings()
        self.redis = RedisSettings()
        self.security = SecuritySettings()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
