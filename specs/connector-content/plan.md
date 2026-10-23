# CONN-PAPERLESS-NGX-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `paperless-ngx-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `paperless_ngx_mcp` from it.
