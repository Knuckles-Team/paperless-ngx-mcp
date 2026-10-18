import pytest

from paperless_ngx_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("PL-OS.identity.pngx")
async def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:PL-OS.identity.pngx
    """
    monkeypatch.setattr("sys.argv", ["paperless-ngx-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None
    names = {tool.name for tool in await mcp.list_tools()}
    assert {"paperless_ingestion_projection", "paperless_ingest_projection"} <= names
    assert not {"document_operations", "system_operations"} & names
    operations = [t for t in await mcp.list_tools() if "operation" in (t.tags or set())]
    assert len(operations) == 36
