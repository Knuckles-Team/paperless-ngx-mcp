---
name: paperless-ngx-operations
skill_type: skill
description: Operate Paperless-ngx through its governed MCP and GraphOS capabilities, including document discovery, intake, metadata curation, task monitoring, privacy-preserving structural ingestion, and verification. Use when a request involves Paperless-ngx documents, correspondents, tags, document types, storage paths, custom fields, saved views, search, tasks, system inspection, or epistemic-graph synchronization.
---

# Paperless-ngx Operations

Use the provider's governed MCP tools through GraphOS delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current capability through GraphOS intent delegation and load only the
   required backing tool; do not assume a cached schema.
3. Begin with a bounded read. Resolve metadata labels to current provider identifiers
   before issuing a mutation.
4. Confirm the target and impact before delete, bulk edit, upload, or taxonomy changes.
5. Execute mutations as fenced WorkItems so retries are idempotent and auditable.
6. Synchronize only the keyed structural projection. Require the central signed
   capability bundle and ChangeEnvelope governance before materialization.
7. Verify the provider result and its privacy-safe trace evidence.

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
