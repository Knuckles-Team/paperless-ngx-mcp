---
name: paperless-ngx-system-status
skill_type: skill
description: >-
  Inspect the health of a Paperless-ngx instance via the paperless-ngx-mcp MCP
  server - system status, archive statistics, the latest available version, the
  caller's UI settings and permissions, the live API schema, and background task
  state. Use when the agent must report whether the archive is healthy, find
  failed consumption tasks, or check for an update. Do NOT use to search or edit
  documents (use paperless-ngx-document-management) or for taxonomy changes (use
  paperless-ngx-metadata-curation).
license: MIT
tags: [paperless-ngx, health, statistics, tasks, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Paperless-ngx System Status

Read-only health reporting for a Paperless-ngx instance.

## Tools

| Tool | Purpose |
|------|---------|
| `paperless_ngx_get_system_status` | Version, database, storage, index and classifier health. |
| `paperless_ngx_get_statistics` | Document totals, inbox count and character count. |
| `paperless_ngx_get_remote_version` | Latest released version and whether an update exists. |
| `paperless_ngx_get_ui_settings` | The caller's user, permissions and UI settings. |
| `paperless_ngx_get_schema` | The live OpenAPI schema of the instance. |
| `paperless_ngx_list_tasks` | Consumption and maintenance tasks, filterable by status. |

## Workflow
1. Call `paperless_ngx_get_system_status` and name any component that is not healthy.
2. Call `paperless_ngx_get_statistics` for totals and the inbox backlog.
3. Call `paperless_ngx_list_tasks` with a failure status filter to find failed consumption.
4. Call `paperless_ngx_get_remote_version` when asked whether an update is due.

## Gotchas
- `paperless_ngx_get_schema` returns a large document; call it only when an operation's shape is in doubt.
- Task payloads can carry filenames; report counts and statuses, not names, unless asked.
