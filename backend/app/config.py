"""
Application Configuration Settings
Supports environment variables with sensible defaults for development and production.
"""
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Algorithm Benchmark & Recommendation System"
    PROJECT_VERSION: str = "1.0.0"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment & Debug
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # Database
    # Default to SQLite for zero-config out-of-the-box operation; PostgreSQL via env variable
    DATABASE_URL: str = Field(
        default="sqlite:///./algorithm_benchmark.db",
        env="DATABASE_URL"
    )

    # Security
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production-daa-algorithm-benchmark-2026", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Benchmark Sandbox Settings
    BENCHMARK_TIMEOUT_SECONDS: float = 10.0  # Max execution time per algorithm run
    MAX_ARRAY_SIZE: int = 1000000
    MAX_GRAPH_VERTICES: int = 5000
    MAX_REPETITIONS: int = 50
    DEFAULT_WARMUP_RUNS: int = 2

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except Exception:
                return [v]
        elif isinstance(v, list):
            return v
        return ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
