# Usage

## Discover first

Use the default GraphOS intent verbs to discover the current Paperless-ngx capability.
The provider registers `document_operations`, `system_operations`,
`paperless_ingestion_projection`, and `paperless_ingest_projection` as gated backing
tools that GraphOS can load on demand. Do not cache action schemas across deployments.

## Bounded reads

After GraphOS loads `document_operations`, pass an explicit action and a serialized JSON
object:

```json
{
  "action": "list_documents",
  "params_json": "{\"query\":\"<authorized-query>\",\"page_size\":20,\"max_pages\":1}"
}
```

Treat all returned document fields as sensitive. Keep only the minimum authorized detail
in the final response and never copy results into traces or reports.

## Mutations

Resolve the relevant correspondent, tag, or document type with a bounded read, then read
the target immediately before changing it. Confirm deletes, bulk edits, uploads, and
taxonomy changes. Verify by reading the target again.

Uploads accept only a regular file inside the AgentConfig workspace boundary and are
size-bounded. Upload acceptance is not OCR completion; poll the returned task.

## Structural synchronization

Use `paperless_ingestion_projection` to inspect content-free keyed topology. Use
`paperless_ingest_projection` only with a verified GraphSession and current signed
capability bundle. Verify the returned node/edge counts with a governed graph read-back.

## Python API

Import current clients from `paperless_ngx_mcp.api` or construct the configured client
with `paperless_ngx_mcp.auth.get_client`. No deprecated package-level API facade exists.
