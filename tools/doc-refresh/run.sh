#!/usr/bin/env bash
# Run the /refresh-skills routine headless (claude -p) and log the output.
#
#   tools/doc-refresh/run.sh               run now
#   tools/doc-refresh/run.sh --scheduled   run only on "on" weeks (every other Sunday,
#                                          counted from ANCHOR); used by launchd
#
# Logs: tools/doc-refresh/.out/logs/<timestamp>.log
# Tool permissions for the unattended run come from .claude/settings.json.
set -euo pipefail

ANCHOR="2026-11-08"   # first scheduled Sunday; runs every 14 days from here
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$REPO/tools/doc-refresh/.out/logs"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

if [[ "${1:-}" == "--scheduled" ]]; then
  if ! python3 -I -c "import datetime as d,sys; sys.exit(((d.date.today()-d.date.fromisoformat('$ANCHOR')).days//7) % 2)"; then
    echo "$(date '+%F %T') off week (anchor $ANCHOR) — skipping"
    exit 0
  fi
fi

command -v claude >/dev/null || { echo "claude CLI not found on PATH" >&2; exit 127; }
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%F_%H%M%S).log"
cd "$REPO"

PROMPT='Run the refresh-skills routine in .claude/skills/refresh-skills/SKILL.md exactly as written, from step 1 to step 7. This is an unattended run: do not ask questions; wherever the routine says STOP, stop and give the step 7 report.'

echo "$(date '+%F %T') doc refresh starting in $REPO" | tee "$LOG"
# caffeinate keeps the Mac awake for the duration of the run.
caffeinate -i claude -p "$PROMPT" --output-format text 2>&1 | tee -a "$LOG"
status=${PIPESTATUS[0]}
echo "$(date '+%F %T') doc refresh finished (exit $status)" | tee -a "$LOG"
exit "$status"
