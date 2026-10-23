# CONN-PAPERLESS-NGX-MCP-SDK design and implementation plan

## Existing system and reuse

The SDK owns every capability named in the rows. paperless-ngx-mcp adds no module that repeats one. Each row deletes connector code and calls the SDK module.

## Live call path

`ApiClientBase.__init__` in `paperless_ngx_mcp/api/api_client_base.py` calls `create_http_client`. Every domain client and MCP tool calls `ApiClientBase.request`

## Compatibility

Tool names, arguments, and results stay identical. The SDK floor is `agent-connector-sdk>=0.3.11`.
