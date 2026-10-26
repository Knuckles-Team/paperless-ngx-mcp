#!/usr/bin/python
import logging
import sys
from typing import Any, NamedTuple

from agent_connector_sdk.config import load_config
from agent_connector_sdk.connector import build_server
from agent_connector_sdk.connector_identity import connector_version
from agent_connector_sdk.mcp.tool_surface import register_tool_surface

from . import mcp as tool_modules
from .api import ApiClientSystem
from .auth import get_client

__version__ = connector_version("paperless_ngx_mcp")

logger = logging.getLogger("MCP_Server")
logger.setLevel(logging.INFO)


def register_server_surface(mcp):
    """Register the existing Paperless API tool surface unchanged."""
    register_tool_surface(
        mcp,
        service="paperless-ngx-mcp",
        client_cls=ApiClientSystem,
        get_client=get_client,
        tools_module=tool_modules,
    )


class ServerComponents(NamedTuple):
    """Preserve the legacy startup tuple with named collaborators."""

    server: Any
    args: Any
    middlewares: list[Any]


def get_mcp_instance(*, command_args=None) -> ServerComponents:
    """Load legacy configuration and compose the declared SDK connector."""
    load_config()
    args, mcp = build_server("paperless_ngx_mcp", command_args=command_args)
    return ServerComponents(mcp, args, list(mcp.middleware))


def mcp_server():
    mcp, args, _ = get_mcp_instance()

    print(f"Paperless-ngx MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport selection")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
