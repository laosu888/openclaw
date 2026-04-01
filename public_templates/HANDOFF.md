# Handoff

## Files To Use First

- `CONTRIBUTION_NOTES.md`
- `PR_DRAFT.md`
- `workspace/`

## If You Later Clone Your Fork

1. Pick a target path inside the repo, for example `templates/workspace/`
2. Run:

```bash
/root/.openclaw/workspace/scripts/install_public_workspace_template.sh /path/to/repo templates/workspace
```

3. Review the copied files
4. Adjust naming or placement to match the target repository
5. Commit only the copied template files

## If You Just Want The Bundle

Use:

```bash
/root/.openclaw/workspace/scripts/package_public_workspace.sh
```

Archive path:

`/root/.openclaw/workspace/dist/public-workspace-template.tar.gz`
