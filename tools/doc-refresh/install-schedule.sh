#!/usr/bin/env bash
# Register (or remove) a macOS launchd job that runs tools/doc-refresh/run.sh --scheduled
# every Sunday at HOUR:MINUTE local time; run.sh itself skips the off weeks, so the
# routine effectively runs every other Sunday. If the Mac is asleep at that time, launchd
# runs the job when it wakes. If it's powered off, that run is skipped.
#
#   tools/doc-refresh/install-schedule.sh              install / update (Sunday 08:00)
#   HOUR=7 MINUTE=30 tools/doc-refresh/install-schedule.sh
#   tools/doc-refresh/install-schedule.sh --uninstall
#   launchctl kickstart -k gui/$(id -u)/com.salesforce-pixel.essential-skills.refresh   # run now
set -euo pipefail

LABEL="com.salesforce-pixel.essential-skills.refresh"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOUR="${HOUR:-8}"
MINUTE="${MINUTE:-0}"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -f "$PLIST"
  echo "Removed $LABEL"
  exit 0
fi

case "$REPO" in
  "$HOME/Desktop"*|"$HOME/Documents"*|"$HOME/Downloads"*)
    echo "WARNING: $REPO is in a macOS privacy-protected folder. A launchd job may be" >&2
    echo "denied access there (Operation not permitted). Move the clone to e.g." >&2
    echo "~/Developer/essential-skills, or give /bin/bash Full Disk Access." >&2 ;;
esac

mkdir -p "$HOME/Library/LaunchAgents" "$REPO/tools/doc-refresh/.out"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$REPO/tools/doc-refresh/run.sh</string>
    <string>--scheduled</string>
  </array>
  <key>WorkingDirectory</key><string>$REPO</string>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>0</integer>
    <key>Hour</key><integer>$HOUR</integer>
    <key>Minute</key><integer>$MINUTE</integer>
  </dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key><string>$HOME</string>
    <key>PATH</key><string>$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
  </dict>
  <key>StandardOutPath</key><string>$REPO/tools/doc-refresh/.out/launchd.log</string>
  <key>StandardErrorPath</key><string>$REPO/tools/doc-refresh/.out/launchd.log</string>
</dict>
</plist>
EOF

plutil -lint "$PLIST" >/dev/null
launchctl bootstrap "$DOMAIN" "$PLIST"
printf 'Installed %s: Sundays %02d:%02d local, every other week (see ANCHOR in run.sh).\n' "$LABEL" "$HOUR" "$MINUTE"
echo "Run it now:  launchctl kickstart -k $DOMAIN/$LABEL"
