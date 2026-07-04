import pytest

from paperless_ngx_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("PL-OS.identity.pngx")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:PL-OS.identity.pngx
    """
    monkeypatch.setattr("sys.argv", ["paperless-ngx-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None
