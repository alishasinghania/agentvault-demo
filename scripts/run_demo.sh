#!/usr/bin/env bash
set -euo pipefail

# AgentVault — One-command demo startup (OpenRouter)
# Usage: ./scripts/run_demo.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "============================================"
echo "  AgentVault — Meridian Corp AI Assistant  "
echo "============================================"
echo ""

# Check for .env
if [ ! -f ".env" ]; then
    echo "No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "Created .env — add your OPENROUTER_API_KEY, then re-run."
    exit 1
fi

# Load env
set -a
# shellcheck disable=SC1091
source .env
set +a

OPENROUTER_MODEL="${OPENROUTER_MODEL:-meta-llama/llama-3.2-3b-instruct:free}"

echo "[0/4] Checking OpenRouter API key..."
if [ -z "${OPENROUTER_API_KEY:-}" ] || [ "$OPENROUTER_API_KEY" = "your-openrouter-api-key-here" ]; then
    echo "Error: OPENROUTER_API_KEY not set in .env"
    echo ""
    echo "  1. Sign up:  https://openrouter.ai"
    echo "  2. Create key: https://openrouter.ai/keys"
    echo "  3. Put it in .env as OPENROUTER_API_KEY=sk-or-..."
    echo "  4. Re-run:  ./scripts/run_demo.sh"
    exit 1
fi

# Create data directories
mkdir -p data/chroma data

echo "[1/4] Checking Python environment..."
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Please install Python 3.9+."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtualenv at .venv ..."
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[2/4] Installing dependencies..."
pip install -q -U pip
pip install -q -r requirements.txt

echo "[3/5] Seeding knowledge base..."
python scripts/seed_vectorstore.py

echo "[4/5] Seeding sample database..."
python scripts/seed_database.py

echo "[5/5] Starting AgentVault (OpenRouter model: ${OPENROUTER_MODEL})..."
echo ""
echo "  Chat interface: http://localhost:8000"
echo "  API docs:       http://localhost:8000/docs"
echo "  Press Ctrl+C to stop."
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
