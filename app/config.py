"""
Production Configuration - Using LangSmith, LangFuse, RAGAS
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application settings using Pydantic"""
    
    # ========== LangChain Settings ==========
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT: str = "eli-lilly-pharmacy-ai"
    
    # ========== LangFuse Settings ==========
    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    
    # ========== TruLens Settings ==========
    TRULENS_DATABASE_URL: str = "sqlite:///trulens.db"
    
    # ========== RAGAS Settings ==========
    RAGAS_LLM_MODEL: str = "gpt-3.5-turbo"  # or local
    RAGAS_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # ========== LLM Settings ==========
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")  # ollama, openai, anthropic
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # ========== Vector Store ==========
    VECTOR_STORE_TYPE: str = "faiss"  # faiss, chromadb, pinecone
    VECTOR_STORE_PATH: Path = Path("vector_store")
    
    # ========== Retrieval ==========
    TOP_K_RETRIEVAL: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # ========== Agent Settings ==========
    MAX_ITERATIONS: int = 10
    TEMPERATURE: float = 0.1
    
    # ========== Evaluation Thresholds ==========
    FAITHFULNESS_THRESHOLD: float = 0.7
    ANSWER_RELEVANCE_THRESHOLD: float = 0.7
    CONTEXT_RECALL_THRESHOLD: float = 0.6
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create directories
settings.VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

"""
Configuration Management
Central settings for the entire application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================
# PATHS
# ============================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PDFS_DIR = DATA_DIR / "pdfs"
DATABASE_DIR = DATA_DIR / "database"
CASES_DIR = DATA_DIR / "cases"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# Create directories
for dir_path in [DATA_DIR, PDFS_DIR, DATABASE_DIR, CASES_DIR, VECTOR_STORE_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================
# DATABASE
# ============================================
DATABASE_PATH = DATABASE_DIR / "pharmacy.db"

# ============================================
# LLM CONFIGURATION
# ============================================
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ============================================
# RETRIEVAL CONFIGURATION
# ============================================
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ============================================
# RISK THRESHOLDS
# ============================================
HIGH_RISK_THRESHOLD = float(os.getenv("HIGH_RISK_THRESHOLD", "0.6"))
HITL_THRESHOLD = float(os.getenv("HITL_THRESHOLD", "0.5"))

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class Settings:
    """Settings singleton"""
    pass

settings = Settings()