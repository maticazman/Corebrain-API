from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any

# Cargar variables de entorno
load_dotenv()

def get_cors_origins() -> List[str]:
    """Obtiene los CORS origins desde variables de entorno"""
    cors_origins = os.environ.get("CORS_ORIGINS", "*")
    if cors_origins == "*":
        return ["*"]
    return [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

class SecuritySettings(BaseModel):
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "insecure-secret-key-for-dev")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = "HS256"
    API_KEY_NAME: str = "X-API-Key"
    CORS_ORIGINS: List[str] = Field(default_factory=get_cors_origins)

class MongoDBSettings(BaseModel):
    MONGODB_URL: str = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.environ.get("MONGODB_DB_NAME", "corebrain")
    MAX_CONNECTIONS: int = int(os.environ.get("MONGODB_MAX_CONNECTIONS", "10"))
    MIN_CONNECTIONS: int = int(os.environ.get("MONGODB_MIN_CONNECTIONS", "1"))
    CONNECTION_TIMEOUT: int = int(os.environ.get("MONGODB_CONNECTION_TIMEOUT", "5000"))

class AnthropicSettings(BaseModel):
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.environ.get("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    MAX_TOKENS: int = int(os.environ.get("MAX_TOKENS", "1024"))
    TEMPERATURE: float = float(os.environ.get("TEMPERATURE", "0.7"))

class CacheSettings(BaseModel):
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL: int = int(os.environ.get("CACHE_TTL", "3600"))
    ENABLE_CACHE: bool = os.environ.get("ENABLE_CACHE", "True").lower() in ("true", "1", "yes")

class RateLimitSettings(BaseModel):
    REQUESTS_PER_MINUTE: int = int(os.environ.get("REQUESTS_PER_MINUTE", "60"))
    BURST_SIZE: int = int(os.environ.get("BURST_SIZE", "5"))
    ENABLE_RATE_LIMIT: bool = os.environ.get("ENABLE_RATE_LIMIT", "True").lower() in ("true", "1", "yes")

class Settings(BaseModel):
    # Meta
    APP_NAME: str = "CoreBrain API"
    API_V1_STR: str = "/api"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    
    # Componentes
    SECURITY: SecuritySettings = SecuritySettings()
    MONGODB: MongoDBSettings = MongoDBSettings()
    ANTHROPIC: AnthropicSettings = AnthropicSettings()
    CACHE: CacheSettings = CacheSettings()
    RATE_LIMIT: RateLimitSettings = RateLimitSettings()
    
    # Niveles de acceso para API keys
    API_KEY_PERMISSION_LEVELS: Dict[str, List[str]] = {
        "read": ["read"],
        "write": ["read", "write"],
        "admin": ["read", "write", "admin"]
    }
    
    # Colecciones permitidas por nivel de acceso
    COLLECTION_ACCESS: Dict[str, List[str]] = {
        "read": ["products", "categories", "public_info"],
        "write": ["products", "categories", "orders", "public_info"],
        "admin": ["*"]  # Acceso a todas las colecciones
    }

# Crear instancia global de configuración
settings = Settings()