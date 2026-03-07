---
name: lean-workmode
description: Token-saving operating mode for repetitive user workflows. Use when the user wants lower token usage, faster replies, less repeated context, compact progress updates, structured summaries, or reusable task scaffolding. Especially useful for long-running assistant relationships, repeated analysis tasks, and ongoing build/debug work where context cost grows too fast.
---

# Lean Workmode

Use a low-token working style.

## Core rules

1. Prefer fixed templates over free-form long replies.
2. Reuse status files instead of re-reading long chat history.
3. Separate long-term memory from daily logs.
4. Summarize work in short blocks: `已完成 / 当前 / 下一步`.
5. For repetitive domains, trigger the dedicated skill directly instead of rebuilding context from scratch.

## Reply modes

### Default compact mode
Use short replies unless the user asks for detail.

### Progress mode
When reporting progress, use:
- 已完成
- 当前
- 下一步

### Analysis mode
For repeated analysis tasks, use a fixed section order and avoid repeating general disclaimers unless risk changes.

## File discipline

Prefer these files:
- `MEMORY.md` for long-term facts only
- `memory/YYYY-MM-DD.md` for raw daily events
- task-local `STATUS.md` for active project state
- task-local registries/json files for machine-readable state

## Compression behavior

When context gets heavy:
1. move resolved details into task status files
2. keep only active decisions in the conversation
3. reference files instead of re-embedding all prior reasoning

## Ideal use cases
- football match analysis
- ETH monitoring
- ongoing automation builds
- repeated daily briefings
- long-running personal assistant sessions
