# CONN-PAPERLESS-NGX-MCP-SDK — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-PAPERLESS-NGX-MCP-SDK-R001` | `tests/test_api_client.py::test_client_is_governed_with_token_auth` | A unit test shows the API client holds a governed client with redirects off and token auth |
| T-002 | `CONN-PAPERLESS-NGX-MCP-SDK-R002` | `tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client` | A unit test sends 503 then 200 through a mock transport and sees one result |
| T-003 | `CONN-PAPERLESS-NGX-MCP-SDK-R003` | `tests/test_api_client.py::test_dependencies_carry_sdk_floor_and_no_requests_pin` | pyproject.toml shows the floor and no requests pin |
| T-004 | `CONN-PAPERLESS-NGX-MCP-SDK-R004` | `tests/test_api_client.py::test_client_is_governed_with_token_auth` | A test enters at the production entry point and reaches the wired call site. |
| T-005 | `CONN-PAPERLESS-NGX-MCP-SDK-R005` | `tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client` | The named integration test passes. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
