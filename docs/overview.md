# Architecture

## Runtime surfaces

The package has four explicit surfaces:

1. `paperless_ngx_mcp.api` owns typed synchronous provider methods.
2. `paperless_ngx_mcp.mcp` owns condensed action routers and structural ingestion tools.
3. `paperless_ngx_mcp.mcp_server` registers intent-gated, condensed, verbose, or combined
   tools with the current Agent Utilities server factory.
4. `paperless_ngx_mcp.agent_server` starts the optional current A2A agent runtime.

There is no package-root dynamic export, duplicate API facade, arbitrary request
method, raw graph transaction, or optional best-effort ingestion implementation.

## Request boundary

The AgentConfig/XDG loader projects runtime values before server construction. The MCP
fleet resolver materializes only the aliases declared by the child catalog. Fixed-token
authentication creates one process-scoped client; delegated authentication creates a
request-scoped client and never reuses another actor's token.

The HTTP client requires an absolute HTTPS base, configures Requests from the selected
TLS profile, pins pagination to the original origin, disables redirects, applies bounded
retry/backoff, and emits body-free error classes.

## Tool model

`document_operations` and `system_operations` route only to explicit action sets.
`register_tool_surface` gates those backing tools in intent mode and derives the verbose
surface from the same public client, so every mode preserves action parity.
`invoke_client_method` keeps synchronous provider calls off the event loop.

## Graph model

The provider projection uses keyed HMAC identifiers and five content-free node classes:
document, correspondent, tag, document-type, and storage-path references. Only their
structural relationships persist. The projection and provider-owned ontology/preset are
inputs to the central capability compiler; deployment materialization requires its
reviewed signed bundle and a verified GraphSession.
