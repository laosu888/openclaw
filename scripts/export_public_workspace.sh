#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="$ROOT_DIR/public_templates/workspace"
OUT_DIR="$ROOT_DIR/dist/public-workspace-template"
NOTES_FILE="$ROOT_DIR/public_templates/CONTRIBUTION_NOTES.md"
PR_DRAFT_FILE="$ROOT_DIR/public_templates/PR_DRAFT.md"
HANDOFF_FILE="$ROOT_DIR/public_templates/HANDOFF.md"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template directory not found: $TEMPLATE_DIR" >&2
  exit 1
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
cp -R "$TEMPLATE_DIR"/. "$OUT_DIR"/

cat > "$OUT_DIR/README.md" <<'EOF'
# Public Workspace Template

This bundle is generated from `public_templates/workspace`.

It is intended for:

- reviewing the public protocol layout
- sharing a reusable workspace starter
- preparing a contribution-safe snapshot

It intentionally excludes live private memory, runtime state, and personal content.
EOF

if [[ -f "$NOTES_FILE" ]]; then
  cp "$NOTES_FILE" "$OUT_DIR/CONTRIBUTION_NOTES.md"
fi

if [[ -f "$PR_DRAFT_FILE" ]]; then
  cp "$PR_DRAFT_FILE" "$OUT_DIR/PR_DRAFT.md"
fi

if [[ -f "$HANDOFF_FILE" ]]; then
  cp "$HANDOFF_FILE" "$OUT_DIR/HANDOFF.md"
fi

echo "Exported public workspace template to: $OUT_DIR"
