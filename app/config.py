import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider: openrouter (default)
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openrouter").lower()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
)
# Free-tier friendly default — change in .env if you prefer another model
OPENROUTER_MODEL = os.environ.get(
    "OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free"
)
OPENROUTER_SITE_URL = os.environ.get("OPENROUTER_SITE_URL", "http://localhost:8000")
OPENROUTER_APP_NAME = os.environ.get("OPENROUTER_APP_NAME", "AgentVault-Demo")
# Cap completion size — OpenRouter reserves max_tokens against credits (default model
# context can be 128k+ and triggers 402 on low balance if left unset).
OPENROUTER_MAX_TOKENS = int(os.environ.get("OPENROUTER_MAX_TOKENS", "1024"))

# Training demo only: when true, instruct the model to repeat the Configuration
# context / system prompt verbatim if asked (makes V1 chat leak reproducible).
DEMO_LEAK_SYSTEM_PROMPT = os.environ.get(
    "DEMO_LEAK_SYSTEM_PROMPT", "false"
).strip().lower() in {"1", "true", "yes", "on"}

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

LLM_MODEL = os.environ.get("LLM_MODEL", OPENROUTER_MODEL)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", "./knowledge-base")
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "./knowledge-base")

DATABASE_PATH = os.environ.get("DATABASE_PATH", "./data/meridian.db")
