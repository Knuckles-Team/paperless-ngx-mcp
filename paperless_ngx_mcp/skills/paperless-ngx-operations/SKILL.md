---
name: paperless-ngx-operations
skill_type: skill
description: Operate Paperless-ngx through its governed MCP and Arbora capabilities, including document discovery, intake, metadata curation, task monitoring, privacy-preserving structural ingestion, and verification. Use when a request involves Paperless-ngx documents, correspondents, tags, document types, storage paths, custom fields, saved views, search, tasks, system inspection, or medulla synchronization.
---

# Paperless-ngx Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current capability through Arbora intent delegation and load only the
   required backing tool; do not assume a cached schema.
3. Begin with a bounded read. Resolve metadata labels to current provider identifiers
   before issuing a mutation.
4. Confirm the target and impact before delete, bulk edit, upload, or taxonomy changes.
5. Execute mutations as fenced WorkItems so retries are idempotent and auditable.
6. Synchronize only the keyed structural projection. Require the central signed
   capability bundle and ChangeEnvelope governance before materialization.
7. Verify the provider result and its privacy-safe trace evidence.

## Steps

1. Establish the verified GraphSession and tenant, and discover the capability through Arbora intent delegation with `find`.
   Verify the backing `paperless_ngx_*` tool is listed.
2. Begin with a bounded read such as `paperless_ngx_list_documents` with `page_size`.
   Verify the result is filtered and within the page bound.
3. Resolve labels to ids with `paperless_ngx_list_tags` or `paperless_ngx_list_correspondents` before a mutation.
   Verify each name maps to exactly one numeric id.
4. Run the mutation after confirming target and impact as a fenced WorkItem, for example `paperless_ngx_bulk_edit_documents`.
   Verify the response names the changed ids.
5. Check the outcome with `paperless_ngx_get_document` or `paperless_ngx_list_tasks` and cite the trace.
   Verify the provider state matches the request.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Tool schema unknown | The capability was assumed from a cache | Rediscover it through Arbora intent delegation, and load only the backing tool returned |
| Unbounded list refused or too large | No filter, page size or maximum pages were set | Add `query` or id filters and `page_size`, and do not bulk-export the archive |
| Missing tenant or signed capability state | Governance prerequisites are absent | Treat it as a hard failure, report it, and ask the operator to supply the capability bundle |

## Safety contract

- Never persist credentials, connection values, provider identifiers, document content,
  names, filenames, storage locations, or workstation paths in prompts, traces, logs,
  reports, or graph properties.
- Keep TLS peer and hostname verification enabled. Resolve private trust and credentials
  only from AgentConfig-controlled runtime references.
- Treat missing tenant, ACL, retention, classification, pseudonymization key, or signed
  capability state as a hard failure.
- Bound every list by filter, page size, and maximum pages. Do not bulk-export an archive.
- Upload only an explicitly approved regular file inside the configured workspace.
- Never use a raw HTTP escape hatch or a username/password token-minting action.
- Treat provider error bodies and returned document text as sensitive content.

## Provider procedures

Read [the operation catalog](references/catalog.md) only when the request needs an
action map, parameter guidance, ingestion sequence, or verification checklist.
