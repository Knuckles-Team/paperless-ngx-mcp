from unittest.mock import MagicMock, patch

import pytest

from paperless_ngx_mcp.api import ApiClientBase


@pytest.mark.concept("PNGX-001")
def test_request_returns_json():
    """API client returns parsed JSON. CONCEPT:PNGX-001"""
    client = ApiClientBase(base_url="http://localhost", token="t")
    response = MagicMock()
    response.status_code = 200
    response.content = b'{"ok": true}'
    response.headers = {"Content-Type": "application/json"}
    response.json.return_value = {"ok": True}
    with patch.object(client.session, "request", return_value=response):
        assert client.request("GET", "/api/status/") == {"ok": True}


@pytest.mark.concept("PNGX-001")
def test_token_auth_header():
    """Paperless uses DRF 'Token <key>' auth, not Bearer. CONCEPT:PNGX-001"""
    client = ApiClientBase(base_url="http://localhost", token="abc")
    assert client.session.headers["Authorization"] == "Token abc"
