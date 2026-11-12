# Usage

## Discover first

Use the default Arbora intent verbs to discover the current Paperless-ngx capability.
The provider registers one typed tool per API operation (`paperless_ngx_<operation>`)
plus `paperless_ingestion_projection` and `paperless_ingest_projection` as gated backing
tools that Arbora can load on demand. Do not cache tool schemas across deployments.

## Bounded reads

After Arbora loads `paperless_ngx_list_documents`, pass bounded arguments:

```json
{
  "query": "<authorized-query>",
  "page_size": 20,
  "max_pages": 1
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
