---
name: paperless-ngx-metadata-curation
skill_type: skill
description: >-
  Curate the organizing taxonomy of a Paperless-ngx archive — correspondents,
  tags, document types, storage paths, and custom fields — via the
  paperless-ngx-mcp MCP server. Use when the agent must list/create/rename these
  metadata objects, resolve a name to its numeric id, or design the tagging
  scheme. Do NOT use to search or edit documents themselves (use
  paperless-ngx-document-management) or to ingest into the knowledge graph (use
  paperless-ngx-kg-ingestion).
license: MIT
tags: [paperless-ngx, correspondents, tags, taxonomy, metadata, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Paperless-ngx Metadata Curation

Domain-typed access to the metadata objects that organize a Paperless-ngx
archive: **correspondents**, **tags**, **document types**, **storage paths** and
**custom fields**. These are the ids that documents reference — curate them here,
then apply them to documents with `paperless-ngx-document-management`.

## When to use
- List existing correspondents / tags / document types / storage paths / custom fields.
- Create or rename a tag, correspondent, or document type.
- Resolve a human name (e.g. "Acme Corp") to the numeric id a document needs.
- Design or clean up the tagging / document-type scheme.

## When NOT to use
- Searching, reading, uploading, or editing documents → `paperless-ngx-document-management`.
- Pushing the taxonomy + documents into the medulla → `paperless-ngx-kg-ingestion`.
- Consumption tasks, statistics, system status → `paperless-ngx-system-status`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`paperless-ngx-mcp`** MCP server.
Same env as document management (`PAPERLESS_URL`, `PAPERLESS_TOKEN`,
`PAPERLESS_SSL_VERIFY`).

## Tools
One typed tool per API operation.

| Tool | Purpose |
|------|---------|
| `paperless_ngx_list_correspondents` | List correspondents (filter with `name__icontains`). |
| `paperless_ngx_create_correspondent` | Create a correspondent. |
| `paperless_ngx_update_correspondent` | Rename or retune a correspondent. |
| `paperless_ngx_delete_correspondent` | Delete a correspondent (documents stay). |
| `paperless_ngx_list_tags` | List tags. |
| `paperless_ngx_create_tag` | Create a tag. |
| `paperless_ngx_update_tag` | Rename or recolor a tag. |
| `paperless_ngx_delete_tag` | Delete a tag. |
| `paperless_ngx_list_document_types` | List document types. |
| `paperless_ngx_create_document_type` | Create a document type. |
| `paperless_ngx_delete_document_type` | Delete a document type. |
| `paperless_ngx_list_storage_paths` | List storage paths. |
| `paperless_ngx_create_storage_path` | Create a storage path. |
| `paperless_ngx_list_custom_fields` | List custom fields. |
| `paperless_ngx_create_custom_field` | Create a custom field. |
| `paperless_ngx_list_saved_views` | List saved views. |

### Key parameters
- `body` - object for the create and update tools (for example `{"name": "Acme Corp"}`, or a tag `{"name": "Invoices", "color": "#ff8800"}`).
- `correspondent_id`, `tag_id`, `document_type_id` - required for update and delete.
- List tools accept DRF filters such as `name__icontains`.

## Recipes
Find a correspondent id by name:
```json
{"name__icontains": "acme"}
```
Create a new tag with a color:
```json
{"body": {"name": "Invoices", "color": "#ff8800", "is_inbox_tag": false}}
```
Create a document type:
```json
{"body": {"name": "Bank Statement", "matching_algorithm": 0}}
```
Rename a correspondent:
```json
{"correspondent_id": 14, "body": {"name": "Acme Corporation"}}
```

## Gotchas
- These objects are **referenced by numeric id** from documents — always list to
  resolve the id before setting it on a document via `paperless-ngx-document-management`.
- Tag `color` is a hex string; some instances also accept a legacy `colour` field.
- Deleting a correspondent/tag/type does **not** delete the documents that used it;
  it just unlinks the reference.
- `matching_algorithm` on tags/correspondents/types drives auto-tagging on
  consumption — set it deliberately (0 = none) to avoid surprise auto-classification.

## Related
- `paperless-ngx-document-management` — apply these ids to documents.
- `paperless-ngx-kg-ingestion` — ingest the taxonomy as `:Correspondent` / `:Tag` /
  `:DocumentType` / `:StoragePath` nodes.
