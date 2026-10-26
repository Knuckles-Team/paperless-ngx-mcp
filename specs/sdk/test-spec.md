# CONN-PAPERLESS-NGX-MCP-SDK test specification

Tests use synthetic credentials and mock transports. They need no network.

| Scenario | Requirements | Expected result |
|---|---|---|
| Requests use the governed SDK client | `CONN-PAPERLESS-NGX-MCP-SDK-R001` | A unit test shows the API client holds a governed client with redirects off and token auth |
| Retries come from the SDK retry policy | `CONN-PAPERLESS-NGX-MCP-SDK-R002` | A unit test sends 503 then 200 through a mock transport and sees one result |
| SDK floor and dependency set | `CONN-PAPERLESS-NGX-MCP-SDK-R003` | pyproject.toml shows scion-sdk >=0.5.6 and no requests pin |
| Production wiring | `CONN-PAPERLESS-NGX-MCP-SDK-R004` | A test enters at the production entry point and reaches the wired call site. |
| Hot-path proof | `CONN-PAPERLESS-NGX-MCP-SDK-R005` | The named integration test passes. |
