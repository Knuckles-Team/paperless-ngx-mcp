# Deployment

This page covers running `paperless-ngx-mcp` as long-lived servers.

> `paperless-ngx-mcp` ships both an **MCP server** (console script `paperless-ngx-mcp`) and an
> **A2A agent server** (console script `paperless-ngx-agent`).

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`paperless-ngx-mcp` exposes its MCP server (console script `paperless-ngx-mcp`) four ways. Pick the
row that matches where the server runs relative to your MCP client, then copy the
matching `mcp_config.json` below.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |

### 1. stdio (local subprocess)

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

### 2. Streamable-HTTP (local process)

```bash
uvx --from paperless-ngx-mcp paperless-ngx-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Connect to the running process by URL:

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

Launch a container directly from `mcp_config.json` (swap `docker` for `podman` for a
daemonless runtime):

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "PAPERLESS_URL=https://service.example.com",
        "-e", "PAPERLESS_TOKEN=your_token",
        "knucklessg1/paperless-ngx-mcp:latest"
      ]
    }
  }
}
```

Or run a local streamable-http container and connect by URL:

```bash
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely and published through Caddy on the internal
`*.arpa` zone, connect with the `"url"` key — no local process or image required:

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": { "url": "http://paperless-ngx-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://paperless-ngx-mcp.arpa` to the container's `:8000`
streamable-http listener.
<!-- END GENERATED: deployment-options -->

## Docker Compose

```bash
docker compose -f docker/mcp.compose.yml up -d      # MCP server only
docker compose -f docker/agent.compose.yml up -d    # MCP + agent
```

## Run the A2A agent server

```bash
paperless-ngx-agent --mcp-config mcp_config.json --web
```
