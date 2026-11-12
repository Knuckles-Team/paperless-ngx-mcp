#!/usr/bin/python
"""Server entry points for the Paperless-ngx connector.

The SDK derives one typed tool per public client operation from the API class
declared in the package root. This module binds the connector's own governed
ingestion tools for the SDK's tool discovery.
"""

import logging
import sys
from typing import Any, NamedTuple

from scion_sdk.config import load_config
from scion_sdk.connector import build_server
from scion_sdk.connector_identity import connector_version

from .mcp import register_kg_tools  # noqa: F401

__version__ = connector_version("paperless_ngx_mcp")

logger = logging.getLogger("MCP_Server")
logger.setLevel(logging.INFO)

__all__ = ["register_kg_tools", "get_mcp_instance", "mcp_server"]


class ServerComponents(NamedTuple):
    """Preserve the startup tuple with named collaborators."""

    server: Any
    args: Any
    middlewares: list[Any]


def get_mcp_instance(*, command_args=None) -> ServerComponents:
    """Load configuration and compose the declared SDK connector."""
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
