from unittest.mock import patch

import pytest

from paperless_ngx_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("PL-OS.identity.pngx")
async def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:PL-OS.identity.pngx
    """
    monkeypatch.setattr("sys.argv", ["paperless-ngx-mcp"])
    with patch("agent_utilities.mcp.verbose_tools.tool_mode", return_value="intent"):
        mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None
    names = {tool.name for tool in await mcp.list_tools()}
    assert names == {
        "document_operations",
        "system_operations",
        "paperless_ingestion_projection",
        "paperless_ingest_projection",
    }
    assert set(mcp._intent_gated_tools) == names
