import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

DB_PASSWORD = os.environ.get("DB_PASSWORD", "meridian_db_pass_2024")
INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "sk-internal-meridian-key")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "smtp_meridian_2024!")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin-token-meridian-2024")

FALLBACK_DB_PASS = "meridian_db_pass_2024"
FALLBACK_SMTP_PASS = "smtp_meridian_2024!"

APP_ENV = os.environ.get("APP_ENV", "production")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./data/chroma")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.meridian.internal")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "agentvault@meridian.com")

LLM_MODEL = os.environ.get("LLM_MODEL", "claude-3-haiku-20240307")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", "./knowledge-base")
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./knowledge-base")

DATABASE_PATH = os.environ.get("DATABASE_PATH", "./data/meridian.db")
