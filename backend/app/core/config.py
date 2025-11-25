"""
Application Configuration
Uses Pydantic Settings for environment variable management
"""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Core
    app_env: str = "development"
    redis_url: str = "redis://localhost:6379"
    
    # LLM Provider Configuration
    llm_provider: Literal["openai", "gemini", "local"] = "openai"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Gemini
    gemini_api_key: str = ""
    
    # Local (Ollama)
    local_llm_base_url: str = "http://localhost:11434/v1"
    local_llm_model: str = "llama3"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

