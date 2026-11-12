"""Paperless-ngx connector package.

Runtime surfaces are imported from their owning modules. The package root does not
probe optional dependencies or manufacture cross-module exports.
"""

from scion_sdk.connector_identity import connector_version

__version__ = connector_version("paperless_ngx_mcp")

__all__ = ["__version__"]

from scion_sdk.connector import Connector

from paperless_ngx_mcp.api import ApiClientSystem
from paperless_ngx_mcp.auth import get_client

connector = Connector(
    api=ApiClientSystem,
    get_client=get_client,
    tools="paperless_ngx_mcp.mcp_server",
    instructions=(
        "Paperless-ngx document archive: one typed tool per API operation for "
        "documents, taxonomy, search, tasks and system status, plus governed "
        "structural ingestion."
    ),
)
