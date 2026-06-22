# paperless-ngx-mcp

Paperless-ngx MCP **API + MCP Server + A2A Agent** for the agent-utilities ecosystem — a
typed, action-routed connector.

!!! info "Official documentation"
    This site is the canonical reference for `paperless-ngx-mcp`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/paperless-ngx-mcp)](https://pypi.org/project/paperless-ngx-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/paperless-ngx-mcp)](https://github.com/Knuckles-Team/paperless-ngx-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/paperless-ngx-mcp)

## Overview

`paperless-ngx-mcp` wraps the target service with typed, deterministic MCP tools and an
optional Pydantic-AI agent server.

The connector remains inactive when credentials are absent: configure
`PAPERLESS_URL` and `PAPERLESS_TOKEN` to connect it to an instance.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the Python client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy the target service with Docker.
- :material-sitemap: **[Overview](overview.md)** — the action-routed tool surface and architecture.
- :material-graph: **[Concepts](concepts.md)** — the CONCEPT ID registry.

</div>
