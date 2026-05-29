from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "CivicPulse"
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)
    APP_PORT: int = Field(default=8000)
    APP_SECRET_KEY: str = Field(default="change-me")
    DATABASE_URL: str = Field(default="postgresql+asyncpg://civic:password@localhost:5432/civicpulse")
    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_MAX_OVERFLOW: int = Field(default=10)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = Field(default=3600)
    JWT_SECRET_KEY: str = Field(default="change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ROCM_ENABLED: bool = Field(default=False)
    ROCM_DEVICE_ID: int = Field(default=0)
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_WINDOW: int = Field(default=60)
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
