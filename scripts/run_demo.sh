#!/usr/bin/env bash
set -euo pipefail

# AgentVault — One-command demo startup
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
    echo "Please edit .env and add your ANTHROPIC_API_KEY, then re-run."
    exit 1
fi

# Check for ANTHROPIC_API_KEY
source .env
if [ -z "${ANTHROPIC_API_KEY:-}" ] || [ "$ANTHROPIC_API_KEY" = "your-anthropic-api-key-here" ]; then
    echo "Error: ANTHROPIC_API_KEY not set in .env"
    echo "Please add your Anthropic API key to .env and try again."
    exit 1
fi

# Create data directories
mkdir -p data/chroma data

echo "[1/4] Checking Python environment..."
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Please install Python 3.9+."
    exit 1
fi

echo "[2/4] Installing dependencies..."
pip install -q -r requirements.txt

echo "[3/4] Seeding knowledge base..."
python3 scripts/seed_vectorstore.py

echo "[4/4] Starting AgentVault..."
echo ""
echo "  Chat interface: http://localhost:8000"
echo "  API docs:       http://localhost:8000/docs"
echo "  Press Ctrl+C to stop."
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
