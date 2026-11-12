# Paperless-ngx operation catalog

## Tools

Every operation is its own typed tool, named `paperless_ngx_<operation>`:

- document reads and changes: `paperless_ngx_list_documents`, `paperless_ngx_create_document`,
  `paperless_ngx_get_document`, `paperless_ngx_get_document_metadata`,
  `paperless_ngx_update_document`, `paperless_ngx_delete_document`,
  `paperless_ngx_get_document_notes`, `paperless_ngx_add_document_note`,
  `paperless_ngx_post_document`, and `paperless_ngx_bulk_edit_documents`;
- correspondents: `paperless_ngx_list_correspondents`, `paperless_ngx_create_correspondent`,
  `paperless_ngx_update_correspondent`, and `paperless_ngx_delete_correspondent`;
- tags: `paperless_ngx_list_tags`, `paperless_ngx_create_tag`, `paperless_ngx_update_tag`,
  and `paperless_ngx_delete_tag`;
- taxonomy: `paperless_ngx_list_document_types`, `paperless_ngx_create_document_type`,
  `paperless_ngx_delete_document_type`, `paperless_ngx_list_storage_paths`,
  `paperless_ngx_create_storage_path`, `paperless_ngx_list_custom_fields`,
  `paperless_ngx_create_custom_field`, and `paperless_ngx_list_saved_views`;
- search, tasks and system: `paperless_ngx_global_search`, `paperless_ngx_autocomplete`,
  `paperless_ngx_list_tasks`, `paperless_ngx_get_task`, `paperless_ngx_acknowledge_tasks`,
  `paperless_ngx_get_statistics`, `paperless_ngx_get_system_status`,
  `paperless_ngx_get_remote_version`, `paperless_ngx_get_ui_settings`, and
  `paperless_ngx_get_schema`;
- graph sync: `paperless_ingestion_projection` and `paperless_ingest_projection`.

No tool accepts arbitrary HTTP methods or mints a credential from a username and
password.

## Safe discovery

Use a narrow query, `page_size`, and `max_pages`. Inspect identifiers only within the
active request context. Do not reproduce returned OCR text, notes, titles, metadata, or
identities unless the authorized user explicitly needs that value in the response.

## Metadata mutation

1. List the relevant metadata collection with a bounded query.
2. Resolve the intended object to its current identifier.
3. Read the target document immediately before mutation.
4. Confirm destructive or bulk scope.
5. Apply the smallest update and read the target again.

## Intake

`paperless_ngx_post_document` accepts a file already inside the AgentConfig workspace boundary. The
client rejects absent workspace policy, traversal outside that root, non-files, and
oversized inputs. Poll the returned task with `paperless_ngx_get_task`; do not infer successful OCR
from upload acceptance alone.

## Structural graph synchronization

`paperless_ingestion_projection` lists bounded provider resources and returns only
keyed opaque nodes plus structural relationships. `paperless_ingest_projection`
commits the same projection through the governed ChangeEnvelope authority.

The projection deliberately excludes OCR text, titles, notes, names, filenames,
storage locations, URLs, timestamps, raw bytes, and source identifiers. It requires a
deployment-owned pseudonymization key of at least 32 bytes. Central materialization also
requires the provider-owned ontology and source preset to be compiled into a reviewed,
signed capability bundle.

## Completion checks

- Confirm the exact action and bounded scope used.
- Re-read changed provider state.
- For ingestion, compare projected and committed node/edge counts and perform a
  governed graph read-back.
- Confirm telemetry contains only opaque references, action names, status, counts,
  timing, and bounded error classes.
