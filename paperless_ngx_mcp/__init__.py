"""Paperless-ngx connector package.

Runtime surfaces are imported from their owning modules. The package root does not
probe optional dependencies or manufacture cross-module exports.
"""

from agent_connector_sdk.connector_identity import connector_version

__version__ = connector_version("paperless_ngx_mcp")

__all__ = ["__version__"]

from agent_connector_sdk.connector import Connector
from agent_connector_sdk.connector_hooks import RegistrationContext


def _register_legacy_surface(context: RegistrationContext) -> None:
    """Reuse the existing API registrar through the public SDK hook."""
    from paperless_ngx_mcp.mcp_server import register_server_surface

    register_server_surface(context.server)


connector = Connector(
    instructions="Paperless-ngx tools exposed through the configured current tool surface.",
    extra_registrations=(_register_legacy_surface,),
)
