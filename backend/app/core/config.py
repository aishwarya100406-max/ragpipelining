from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = ""
    COHERE_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Provider Selection
    EMBEDDING_PROVIDER: str = "huggingface"  # "openai", "ollama", or "huggingface"
    LLM_PROVIDER: str = "huggingface"  # "openai", "ollama", or "huggingface"
    
    # Services
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    REDIS_URL: str = "redis://localhost:6379"
    DATABASE_URL: str = "postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_db"
    OLLAMA_URL: str = "http://localhost:11434"
    
    # App Config
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # RAG Config
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # HF: sentence-transformers/all-MiniLM-L6-v2, Ollama: nomic-embed-text, OpenAI: text-embedding-3-small
    LLM_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"  # HF: mistralai/Mistral-7B-Instruct-v0.2, Ollama: llama3.2, OpenAI: gpt-4-turbo-preview
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RETRIEVAL: int = 10
    RERANK_TOP_K: int = 5
    
    # Collection Names
    VECTOR_COLLECTION: str = "documents"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
