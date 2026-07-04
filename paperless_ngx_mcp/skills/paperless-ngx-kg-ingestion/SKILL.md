---
name: paperless-ngx-kg-ingestion
description: >-
  Natively ingest a Paperless-ngx archive into the epistemic-graph knowledge
  graph via the paperless-ngx-mcp MCP server — documents become :Document nodes
  (with OCR text) linked to :Correspondent / :Tag / :DocumentType / :StoragePath,
  and the scanned PDF/image bytes become durable :Blob / :MediaAsset. Use when the
  agent must make the document archive queryable/searchable inside the KG or keep
  it in sync. Do NOT use for day-to-day document search/edit (use
  paperless-ngx-document-management) or taxonomy curation (use
  paperless-ngx-metadata-curation).
license: MIT
tags: [paperless-ngx, knowledge-graph, ingestion, blob, ocr, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---

# Paperless-ngx Knowledge-Graph Ingestion

Push a Paperless-ngx archive into the ONE epistemic-graph engine as typed OWL
nodes, in every modality: **documents** → `:Document` (carrying OCR text for
semantic search), their **metadata** → `:Correspondent` / `:Tag` /
`:DocumentType` / `:StoragePath`, and the **raw scans** → content-addressed
`:Blob` / `:MediaAsset`. Ids follow `paperless:<class>:<externalId>`; the classes
match `paperless_ngx_mcp/ontology/paperless.ttl`.

## When to use
- Make the document archive searchable / joinable inside the knowledge graph.
- Seed or refresh the KG with documents + their correspondents/tags/types links.
- Also make the scanned PDFs durable and deduped as blobs (`include_files`).

## When NOT to use
- Interactive document search / read / edit → `paperless-ngx-document-management`.
- Curating correspondents/tags/types → `paperless-ngx-metadata-curation`.
- When no epistemic-graph engine is reachable — ingestion cleanly no-ops
  (`"ingested": null`); it never blocks the connector.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`paperless-ngx-mcp`** MCP server.
Same Paperless env (`PAPERLESS_URL`, `PAPERLESS_TOKEN`, `PAPERLESS_SSL_VERIFY`).
Ingestion is best-effort: it writes through the fast `GraphComputeEngine` client
when an engine is reachable and no-ops otherwise, so no KG infra is required to
call it.

## Tools & actions
| Tool | Purpose |
|------|---------|
| `paperless_ingest_documents` | List documents + metadata via the client and push typed nodes/links (and optionally scanned blobs) into the KG. |

### Key parameters (`params_json`, a JSON string)
- Any `list_documents` filter (`query`, `tags__id__in`, `created__gte`, `max_pages`, `page_size`).
- `include_files`: `true` to also download each scan and store it as a `:Blob`/`:MediaAsset`.
- `max_files`: cap on blob downloads per run (default 25).

## Recipes (`params_json`)
Ingest all recent invoices as typed document nodes (no blobs):
```json
{"query": "invoice", "created__gte": "2026-01-01", "max_pages": 2}
```
Ingest a page of documents AND their scanned PDFs:
```json
{"page_size": 20, "max_pages": 1, "include_files": true, "max_files": 20}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- The tool lists correspondents/tags/types/storage-paths first so the referenced
  nodes carry real names — expect those metadata nodes to appear even for a small
  document page.
- `include_files` downloads the archived PDF per document (bandwidth + engine
  writes) — bound it with `max_files` and a tight document filter.
- Node ids are stable (`paperless:document:<id>`), so re-running **MERGEs**
  (updates) rather than duplicating — safe to schedule as a delta sync.
- Under the hood this uses `paperless_ngx_mcp.kg_ingest` (typed records +
  documents) and `paperless_ngx_mcp.kg_media` (blobs) — the same code the Tier-1
  `paperless-documents` source preset drives for a text-only sync.

## Related
- `paperless-ngx-document-management` / `paperless-ngx-metadata-curation` — the
  operational tools whose records this ingests.
- The `agent-utilities-source-integration` universal skill — the fleet-wide
  `source_sync` path that can drive the `paperless-documents` preset.
