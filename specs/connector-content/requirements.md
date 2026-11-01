# CONN-PAPERLESS-NGX-MCP-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-PAPERLESS-NGX-MCP-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `paperless-ngx-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Caller chain: `paperless-ngx-mcp` in `pyproject.toml` runs `paperless_ngx_mcp.mcp_server:mcp_server`, which builds the server from the `scion_sdk.connector` entry point `paperless_ngx_mcp:connector` (`paperless_ngx_mcp/__init__.py:24`); the SDK `Connector` then lists the packaged skills, ontology and prompts. Shape: `pyproject.toml` entry point `paperless-ngx-mcp` plus the `connector = Connector(.)` object in `paperless_ngx_mcp/__init__.py`; the packaged `skills/`, `ontology/` and `prompts/` directories of `paperless_ngx_mcp` are reused as is, with no connector-local registration code. Proving test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
