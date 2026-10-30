# CONN-PAPERLESS-NGX-MCP-SDK requirements

Each row defines one requirement. [`status.json`](status.json) holds the generated state.

| ID | Requirement | Verification |
|---|---|---|
| `CONN-PAPERLESS-NGX-MCP-SDK-R001` | **Requests use the governed SDK client.** paperless-ngx-mcp must send every vendor request through the SDK governed HTTP client with its TLS profile. It must not build its own session This row follows `SCION-CENTRALIZED-CAPABILITIES-R001`, `SCION-CENTRALIZED-CAPABILITIES-R008`. | A unit test shows the API client holds a governed client with redirects off and token auth |
| `CONN-PAPERLESS-NGX-MCP-SDK-R002` | **Retries come from the SDK retry policy.** paperless-ngx-mcp must delete its own backoff loop. The SDK retry policy must retry 429 and 5xx replies and honour Retry-After This row follows `SCION-CENTRALIZED-CAPABILITIES-R001`. | A unit test sends 503 then 200 through a mock transport and sees one result |
| `CONN-PAPERLESS-NGX-MCP-SDK-R003` | **SDK floor and dependency set.** The package must require scion-sdk 0.5.6 or later, preserving the centralized capabilities introduced by scion-sdk 0.3.11. It must not pin requests This row follows `SCION-CENTRALIZED-CAPABILITIES-R040`. | pyproject.toml shows the floor and no requests pin |
| `CONN-PAPERLESS-NGX-MCP-SDK-R004` | **Production wiring.** `ApiClientBase.__init__` in `paperless_ngx_mcp/api/api_client_base.py` calls `create_http_client`. Every domain client and MCP tool calls `ApiClientBase.request` | A test enters at the production entry point and reaches the wired call site. |
| `CONN-PAPERLESS-NGX-MCP-SDK-R005` | **Hot-path proof.** A test builds `ApiClientDocuments` and calls a list operation. The test reaches the governed client through `ApiClientBase.request` and retries once | The named integration test passes. |
