# CONN-PAPERLESS-NGX-MCP-SDK tasks

| Task | Deliverable | Proof |
|---|---|---|
| T01 | Requests use the governed SDK client | A unit test shows the API client holds a governed client with redirects off and token auth |
| T02 | Retries come from the SDK retry policy | A unit test sends 503 then 200 through a mock transport and sees one result |
| T03 | SDK floor and dependency set | pyproject.toml shows the floor and no requests pin |
| T04 | Production wiring | A test enters at the production entry point and reaches the wired call site. |
| T05 | Hot-path proof | The named integration test passes. |
