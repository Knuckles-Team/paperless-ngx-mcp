# Installation

`paperless-ngx-mcp` is a standard Python package and a prebuilt container image.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable target service instance and access token.

## From PyPI (recommended)

```bash
pip install paperless-ngx-mcp
```

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "paperless-ngx-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "paperless-ngx-mcp[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "paperless-ngx-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/paperless-ngx-mcp.git
cd paperless-ngx-mcp
pip install -e ".[all]"
```

## Docker

```bash
docker pull knucklessg1/paperless-ngx-mcp:latest
```
