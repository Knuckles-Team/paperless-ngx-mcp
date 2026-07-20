# Paperless-ngx operation catalog

## Condensed tools

`document_operations` accepts `action` and a JSON-object string in `params_json`.
Its current actions are:

- document reads and changes: `list_documents`, `create_document`, `get_document`,
  `get_document_metadata`, `update_document`, `delete_document`,
  `get_document_notes`, `add_document_note`, `post_document`, and
  `bulk_edit_documents`;
- correspondent actions: `list_correspondents`, `create_correspondent`,
  `update_correspondent`, and `delete_correspondent`;
- tag actions: `list_tags`, `create_tag`, `update_tag`, and `delete_tag`;
- taxonomy actions: `list_document_types`, `create_document_type`,
  `delete_document_type`, `list_storage_paths`, `create_storage_path`,
  `list_custom_fields`, `create_custom_field`, and `list_saved_views`.

`system_operations` accepts the same envelope. Its current actions are
`global_search`, `autocomplete`, `list_tasks`, `get_task`, `acknowledge_tasks`,
`get_statistics`, `get_system_status`, `get_remote_version`, `get_ui_settings`, and
`get_schema`.

No action accepts arbitrary HTTP methods or mints a credential from a username and
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

`post_document` accepts a file already inside the AgentConfig workspace boundary. The
client rejects absent workspace policy, traversal outside that root, non-files, and
oversized inputs. Poll the returned task with `get_task`; do not infer successful OCR
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
