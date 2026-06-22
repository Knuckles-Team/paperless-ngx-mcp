import importlib

import pytest


@pytest.mark.concept("PNGX-001")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:PNGX-001"""
    assert importlib.import_module("paperless_ngx_mcp.mcp_server") is not None
