#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SOURCE="${1:-/Volumes/config}"

python3 "$SCRIPT_DIR/export_home_assistant.py" \
  --source "$SOURCE" \
  --repo "$REPO_ROOT"

python3 "$SCRIPT_DIR/public_safety.py" \
  --repo "$REPO_ROOT"

# This runs after privacy filtering so the dependency report reflects only
# dashboards that remain in the public export.
python3 "$REPO_ROOT/tools/repo-audit/dashboard_dependencies.py" \
  --repo "$REPO_ROOT"
