# Paperless-ngx MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/paperless-ngx-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/paperless-ngx-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/paperless-ngx-mcp)
![PyPI - License](https://img.shields.io/pypi/l/paperless-ngx-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/paperless-ngx-mcp)

*Version: 0.1.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing platform are maintained in the
> [official documentation](https://knuckles-team.github.io/paperless-ngx-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Available MCP Tools](#available-mcp-tools)
- [Installation](#installation)
- [Usage](#usage)
- [MCP](#mcp)
- [Documentation](#documentation)

---

## Overview

**Paperless-ngx MCP MCP Server + A2A Agent**

Paperless-ngx API + MCP Server + A2A Server

This repository is actively maintained - Contributions are welcome!

## Key Features

- **Action-routed MCP tools** — each domain is exposed as a single MCP tool that routes
  to many underlying operations via an `action` argument, keeping the tool surface small.
- **Three interfaces, one package** — use it as a Python **API client**, an **MCP server**
  (`stdio` / `streamable-http` / `sse`), or a Pydantic-AI **A2A agent**.
- **`agent-utilities` native** — built on the shared framework (auth, action router,
  telemetry, governance) for fleet consistency.
- **Per-tool toggles** — enable or disable each tool domain with environment switches.
- **Enterprise-ready** — OTEL/Langfuse telemetry and optional Eunomia access governance.

## Available MCP Tools

Each tool is **action-routed**: pass an `action` and a JSON `params_json` payload. Tool
domains can be toggled on or off with the listed environment variable. The table below is
**auto-generated from the live server** by the `mcp-readme-table` pre-commit hook
(`python -m agent_utilities.mcp.readme_tools`) — do not edit it by hand.

<!-- MCP-TOOLS-TABLE:START -->
<!-- MCP-TOOLS-TABLE:END -->

## Installation

### Install with `uvx` (no install — run on demand)

```bash
uvx --from paperless-ngx-mcp paperless-ngx-mcp      # MCP server
uvx --from paperless-ngx-mcp paperless-ngx-agent    # A2A agent server
```

### Install with `pip`

```bash
python -m pip install paperless-ngx-mcp            # core (API client)
python -m pip install "paperless-ngx-mcp[all]"     # + MCP server + A2A agent + telemetry
```

### Console scripts

After installation the following entry points are available on your `PATH`:

| Command | Description |
|---------|-------------|
| `paperless-ngx-mcp` | Launch the MCP server |
| `paperless-ngx-agent` | Launch the A2A agent server |

## Usage

### As a Python API client

```python
from paperless_ngx_mcp.auth import get_client

client = get_client()
status = client.get_system_status()
print(status)
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
paperless-ngx-mcp

# Networked streamable-http
paperless-ngx-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "system_operations",
  "arguments": {
    "action": "status",
    "params_json": "{}"
  }
}
```

## MCP

### Using as an MCP Server

The MCP Server can be run in `stdio` (local), `streamable-http` (networked), or
`sse` mode.

#### Environment Variables

*   `PAPERLESS_URL`: The URL of the target service.
*   `PAPERLESS_TOKEN`: The API token or access token.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": {
      "command": "uvx",
      "args": ["--from", "paperless-ngx-mcp", "paperless-ngx-mcp"],
      "env": {
        "PAPERLESS_URL": "https://service.example.com",
        "PAPERLESS_TOKEN": "your_token"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": {
      "command": "uvx",
      "args": ["--from", "paperless-ngx-mcp", "paperless-ngx-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "PAPERLESS_URL": "https://service.example.com",
        "PAPERLESS_TOKEN": "your_token"
      }
    }
  }
}
```

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`paperless-ngx-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/paperless-ngx-mcp/deployment/) has full,
copy-paste `mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://paperless-ngx-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Install Python Package

```bash
python -m pip install paperless-ngx-mcp
```

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/paperless-ngx-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)
