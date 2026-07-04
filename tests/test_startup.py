import importlib

import pytest


@pytest.mark.concept("PL-OS.identity.pngx")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:PL-OS.identity.pngx"""
    assert importlib.import_module("paperless_ngx_mcp.mcp_server") is not None
