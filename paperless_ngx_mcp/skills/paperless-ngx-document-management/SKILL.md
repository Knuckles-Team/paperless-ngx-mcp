---
name: paperless-ngx-document-management
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
  author: Genius
  version: '0.1.0'
---

# Paperless-ngx Document Management

Domain-typed access to the Paperless-ngx **documents** resource — the OCR'd
archive of scanned PDFs and images. Prefer the condensed `document_operations`
tool over raw HTTP; it carries the DRF field conventions and returns
document-shaped records.

## When to use
- Full-text search / filter the archive (`query`, `tags__id__in`, `correspondent__id`, `created__gte`).
- Fetch a single document's metadata, raw parsed metadata, or notes.
- Upload a new file for consumption/OCR (`post_document`) and poll the task.
- Edit a document (title, tags, correspondent) or run a bulk edit across many ids.

## When NOT to use
- Creating/renaming the taxonomy (correspondents, tags, document types, storage
  paths) → `paperless-ngx-metadata-curation`.
- Pushing documents + their scans into the epistemic-graph → `paperless-ngx-kg-ingestion`.
- System health, tasks, statistics, global search → the `system_operations` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`paperless-ngx-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PAPERLESS_URL` | ✅ | Base URL of the Paperless-ngx instance |
| `PAPERLESS_TOKEN` | ✅ | DRF API token (My Profile → API Auth Token); sent as `Authorization: Token <key>` |
| `PAPERLESS_SSL_VERIFY` | optional | TLS verification toggle |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface
(used below) vs. the 1:1 verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `document_operations` | `list_documents`, `get_document`, `get_document_metadata`, `update_document`, `create_document`, `delete_document`, `post_document`, `get_document_notes`, `add_document_note`, `bulk_edit_documents` |

### Key parameters
- `query` — full-text search string for `list_documents`.
- `document_id` — required for `get_document` / `update_document` / notes.
- `body` — object of field→value for `update_document` (e.g. `{"title": "...", "tags": [3,4]}`).
- `file_path` — local path for `post_document` (returns a consumption task UUID).
- `documents` + `method` + `parameters` — for `bulk_edit_documents`.

## Recipes (`params_json`)
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
- `params_json` is a **string** of JSON, not an object — serialize it.
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
