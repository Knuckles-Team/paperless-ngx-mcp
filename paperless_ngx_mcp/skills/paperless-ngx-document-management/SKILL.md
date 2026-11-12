---
name: paperless-ngx-document-management
skill_type: skill
description: >-
  Search, read, upload, and edit documents in Paperless-ngx via the
  paperless-ngx-mcp MCP server. Use when the agent must full-text search the
  archive, fetch a document's metadata or OCR content, upload a file for
  consumption/OCR, add notes, or bulk-edit tags/correspondents on documents. Do
  NOT use for curating the correspondents/tags/document-types taxonomy (use
  paperless-ngx-metadata-curation) or for pushing documents into the knowledge
  graph (use paperless-ngx-kg-ingestion).
license: MIT
tags: [paperless-ngx, documents, dms, ocr, rest-api, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Paperless-ngx Document Management

Domain-typed access to the Paperless-ngx **documents** resource — the OCR'd
archive of scanned PDFs and images. Use the typed per-operation
tools below instead of raw HTTP; they carry the DRF field conventions and return
document-shaped records.

## When to use
- Full-text search / filter the archive (`query`, `tags__id__in`, `correspondent__id`, `created__gte`).
- Fetch a single document's metadata, raw parsed metadata, or notes.
- Upload a new file for consumption/OCR (`post_document`) and poll the task.
- Edit a document (title, tags, correspondent) or run a bulk edit across many ids.

## When NOT to use
- Creating/renaming the taxonomy (correspondents, tags, document types, storage
  paths) → `paperless-ngx-metadata-curation`.
- Pushing documents + their scans into the medulla → `paperless-ngx-kg-ingestion`.
- System health, tasks, statistics, global search → `paperless-ngx-system-status`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`paperless-ngx-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PAPERLESS_URL` | ✅ | Base URL of the Paperless-ngx instance |
| `PAPERLESS_TOKEN` | ✅ | DRF API token (My Profile → API Auth Token); sent as `Authorization: Token <key>` |
| `PAPERLESS_SSL_VERIFY` | optional | TLS verification toggle |


## Tools
One typed tool per API operation. Parameters are passed as named arguments; extra DRF
filters on the list tools go in `params_json`.

| Tool | Purpose |
|------|---------|
| `paperless_ngx_global_search` | Search documents, correspondents, tags and other objects at once. |
| `paperless_ngx_autocomplete` | Complete a search term. |
| `paperless_ngx_list_documents` | List or full-text search documents with DRF filters. |
| `paperless_ngx_get_document` | Read one document's metadata and content. |
| `paperless_ngx_get_document_metadata` | Read raw parsed metadata and checksums. |
| `paperless_ngx_get_document_notes` | List a document's notes. |
| `paperless_ngx_add_document_note` | Add a note to a document. |
| `paperless_ngx_update_document` | Patch title, tags, correspondent, type or storage path. |
| `paperless_ngx_create_document` | Create a bare document record from a JSON body. |
| `paperless_ngx_post_document` | Upload a workspace file for OCR consumption; returns a task id. |
| `paperless_ngx_bulk_edit_documents` | Apply one bulk method over a list of document ids. |
| `paperless_ngx_delete_document` | Move a document to the trash. |
| `paperless_ngx_get_task` | Poll a consumption task after an upload. |
| `paperless_ngx_list_tasks` | List consumption tasks. |
| `paperless_ngx_acknowledge_tasks` | Dismiss finished tasks. |

### Key parameters
- `query` - full-text search string for `paperless_ngx_list_documents`.
- `document_id` - required for get, update, delete, notes and metadata.
- `body` - object of field to value for `paperless_ngx_update_document` (for example `{"title": "...", "tags": [3,4]}`).
- `file_path` - local workspace path for `paperless_ngx_post_document`.
- `documents`, `method`, `parameters` - for `paperless_ngx_bulk_edit_documents`.

## Recipes
Full-text search, newest first, a few fields:
```json
{"query": "invoice acme", "ordering": "-created", "page_size": 25}
```
Filter by tag ids and a created-after date:
```json
{"tags__id__in": "3,4", "created__gte": "2026-01-01"}
```
Retitle and re-tag one document:
```json
{"document_id": 812, "body": {"title": "Acme Invoice 2026-03", "tags": [3, 7]}}
```
Bulk add a tag to many documents:
```json
{"documents": [11, 12, 13], "method": "add_tag", "parameters": {"tag": 7}}
```

## Gotchas
- Auth is DRF **`Token <key>`**, NOT `Bearer` — a `Bearer` token yields 401.
- List endpoints are **page-number paginated**; the client follows `next` up to
  `max_pages` (default 50). Pass `page_size` and a filter to bound big reads.
- `update_document` is a PATCH (partial) — send only the fields you change.
- `delete_document` moves the document to the **trash**, it is not a hard delete.
- `correspondent` / `document_type` / `storage_path` on a document are **numeric
  ids**, and `tags` is a list of ids — resolve names via `paperless-ngx-metadata-curation`.

## Related
- `paperless-ngx-metadata-curation` — curate the correspondents/tags/types taxonomy.
- `paperless-ngx-kg-ingestion` — push documents + scans into the knowledge graph.
