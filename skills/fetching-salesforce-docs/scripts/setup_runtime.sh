#!/usr/bin/env bash
# One-time provisioning for the fetching-salesforce-docs isolated runtime.
# Idempotent: safe to re-run. The extraction scripts also auto-provision on
# first use, but you can run this explicitly (e.g. to pre-warm or debug).
set -euo pipefail

RUNTIME_ROOT="${SF_DOCS_RUNTIME_ROOT:-$HOME/.claude/.fetching-salesforce-docs-runtime}"
VENV="$RUNTIME_ROOT/venv"
PY="$VENV/bin/python"
export PLAYWRIGHT_BROWSERS_PATH="$RUNTIME_ROOT/ms-playwright"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQS="$SCRIPT_DIR/../requirements.txt"

echo "[setup_runtime] Runtime root: $RUNTIME_ROOT"

if [ ! -x "$PY" ]; then
  echo "[setup_runtime] Creating venv at $VENV ..."
  mkdir -p "$RUNTIME_ROOT"
  python3 -m venv "$VENV"
fi

echo "[setup_runtime] Installing Python dependencies ..."
"$PY" -m pip install --quiet --upgrade pip
if [ -f "$REQS" ]; then
  "$PY" -m pip install --quiet -r "$REQS"
else
  "$PY" -m pip install --quiet playwright playwright-stealth
fi

echo "[setup_runtime] Installing chromium browser ..."
"$PY" -m playwright install chromium

echo "[setup_runtime] Done. Runtime ready at $RUNTIME_ROOT"
