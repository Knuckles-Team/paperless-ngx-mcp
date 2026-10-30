# Installation

Paperless-ngx MCP supports Python 3.11 through 3.14.

## MCP server

```bash
uvx --from "paperless-ngx-mcp[mcp]" paperless-ngx-mcp
```

## Installed package

```bash
uv pip install "paperless-ngx-mcp[mcp]"
```

`paperless-ngx-mcp[all]` for both runtime surfaces. The current Scion SDK base
dependency includes the full Epistemic Graph feature set.

Installation does not configure a provider connection. Supply reference-only runtime
configuration as described in [Configuration](configuration.md).
