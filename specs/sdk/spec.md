# CONN-PAPERLESS-NGX-MCP-SDK — Shared SDK capabilities in paperless-ngx-mcp

**Owner:** paperless-ngx-mcp.

See [`requirements.md`](requirements.md) for each row and [`status.json`](status.json) for its generated state.

## Purpose

paperless-ngx-mcp must use the scion-sdk capability for each concern the SDK centralizes. A connector copy of a centralized capability splits policy across the fleet.

## Why a new spec

Search: `git grep -n "SDK" -- specs` found no row that owns SDK capability use in paperless-ngx-mcp. The SDK index spec `SCION-CENTRALIZED-CAPABILITIES` owns the capabilities. This spec owns the connector side of each one.

## Requirements

- `CONN-PAPERLESS-NGX-MCP-SDK-R001`: Requests use the governed SDK client.
- `CONN-PAPERLESS-NGX-MCP-SDK-R002`: Retries come from the SDK retry policy.
- `CONN-PAPERLESS-NGX-MCP-SDK-R003`: SDK floor and dependency set.
- `CONN-PAPERLESS-NGX-MCP-SDK-R004`: Production wiring.
- `CONN-PAPERLESS-NGX-MCP-SDK-R005`: Hot-path proof.
