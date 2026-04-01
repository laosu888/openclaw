#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_SCRIPT="$ROOT_DIR/scripts/export_public_workspace.sh"
OUT_DIR="$ROOT_DIR/dist/public-workspace-template"
ARCHIVE_PATH="$ROOT_DIR/dist/public-workspace-template.tar.gz"

"$EXPORT_SCRIPT" >/dev/null

tar -C "$ROOT_DIR/dist" -czf "$ARCHIVE_PATH" public-workspace-template

echo "Packaged public workspace template at: $ARCHIVE_PATH"
