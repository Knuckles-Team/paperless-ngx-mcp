---
name: paperless-ngx-kg-ingestion
skill_type: skill
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
  author: Knuckles-Team
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
| `paperless_ingestion_projection` | Read-only: return the keyed, opaque structural projection (documents, correspondents, tags, document types, storage paths and their relationships) for governed source sync. No document content or titles leave Paperless. |
| `paperless_ingest_projection` | Commit that same projection through a governed ChangeEnvelope; returns the ingest receipt. |

### Key parameters (`params_json`, a JSON string)
- Any bounded `list_documents` filter (`query`, `tags__id__in`, `created__gte`, `max_pages`, `page_size`).

## Recipes (`params_json`)
Preview the projection for recent invoices, then commit it:
```json
{"query": "invoice", "created__gte": "2026-01-01", "max_pages": 2}
```
Call `paperless_ingestion_projection` first to inspect it, then `paperless_ingest_projection` with the same parameters.

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- The tool lists correspondents/tags/types/storage-paths first so the referenced
  nodes carry real names — expect those metadata nodes to appear even for a small
  document page.
- Node ids are stable (`paperless:document:<id>`), so re-running **MERGEs**
  (updates) rather than duplicating — safe to schedule as a delta sync.
- Under the hood this uses `paperless_ngx_mcp.kg_ingest` — the same projection the
  Tier-1 `paperless-documents` source preset drives for a structural sync. Scanned
  files are not copied into the graph.

## Related
- `paperless-ngx-document-management` / `paperless-ngx-metadata-curation` — the
  operational tools whose records this ingests.
- The `scion-sdk-source-integration` universal skill — the fleet-wide
  `source_sync` path that can drive the `paperless-documents` preset.
