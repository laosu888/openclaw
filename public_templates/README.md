# Public Workspace Templates

This directory contains contribution-safe templates for an OpenClaw-style agent workspace.

Design goals:

- Keep the structure reusable across users and teams
- Avoid personal identity, business data, and private operating details
- Separate public protocol files from local runtime state

Use `scripts/export_public_workspace.sh` to build a clean bundle under `dist/public-workspace-template/`.
