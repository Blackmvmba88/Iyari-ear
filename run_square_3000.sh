#!/bin/zsh
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3.12}"
exec env PYTHONUNBUFFERED=1 "$PYTHON_BIN" "$(dirname "$0")/square_3000_app.py"
