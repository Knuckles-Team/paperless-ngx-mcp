from unittest.mock import MagicMock, patch

import pytest
from agent_utilities.core.exceptions import ParameterError

from paperless_ngx_mcp.api import ApiClientDocuments


def _client() -> ApiClientDocuments:
    profile = MagicMock()
    profile.configure_requests_session.side_effect = lambda session: session
    return ApiClientDocuments(
        "https://service.example.invalid",
        "runtime-value",
        tls_profile=profile,
    )


def test_upload_requires_agentconfig_workspace(monkeypatch, tmp_path):
    source = tmp_path / "document.bin"
    source.write_bytes(b"content")
    monkeypatch.delenv("WORKSPACE_PATH", raising=False)
    with pytest.raises(ParameterError, match="configured workspace"):
        _client().post_document(str(source))


def test_upload_rejects_source_outside_workspace(monkeypatch, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    source = tmp_path / "document.bin"
    source.write_bytes(b"content")
    monkeypatch.setenv("WORKSPACE_PATH", str(workspace))
    with pytest.raises(ParameterError, match="outside the workspace"):
        _client().post_document(str(source))


def test_upload_reads_approved_regular_file(monkeypatch, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    source = workspace / "document.bin"
    source.write_bytes(b"content")
    monkeypatch.setenv("WORKSPACE_PATH", str(workspace))
    client = _client()
    with patch.object(client, "request", return_value={"task": "opaque"}) as request:
        result = client.post_document(str(source), tags=[1])
    assert result == {"task": "opaque"}
    assert request.call_args.args == ("POST", "/api/documents/post_document/")
    assert request.call_args.kwargs["data"] == {"tags": [1]}
    filename, handle = request.call_args.kwargs["files"]["document"]
    assert filename == "document.bin"
    assert handle.closed
