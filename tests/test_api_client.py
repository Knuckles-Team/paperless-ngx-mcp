from unittest.mock import MagicMock, patch

import pytest
import requests
from agent_utilities.core.exceptions import ParameterError

from paperless_ngx_mcp.api import ApiClientBase


def _client() -> tuple[ApiClientBase, MagicMock]:
    profile = MagicMock()
    profile.configure_requests_session.side_effect = lambda session: session
    return (
        ApiClientBase(
            base_url="https://service.example.invalid",
            token="runtime-value",
            tls_profile=profile,
        ),
        profile,
    )


@pytest.mark.concept("PL-OS.identity.pngx")
def test_request_returns_json_without_transport_override():
    client, _ = _client()
    response = MagicMock()
    response.status_code = 200
    response.content = b'{"ok": true}'
    response.headers = {"Content-Type": "application/json"}
    response.json.return_value = {"ok": True}
    with patch.object(client.session, "request", return_value=response) as request:
        assert client.request("GET", "/api/status/") == {"ok": True}
    assert "verify" not in request.call_args.kwargs
    assert request.call_args.kwargs["allow_redirects"] is False


@pytest.mark.concept("PL-OS.identity.pngx")
def test_token_auth_header_and_tls_profile_cleanup():
    client, profile = _client()
    assert client.session.headers["Authorization"] == "Token runtime-value"
    client.close()
    profile.cleanup.assert_called_once_with()


def test_base_url_requires_https_and_has_no_inline_credentials():
    profile = MagicMock()
    with pytest.raises(ValueError, match="absolute HTTPS"):
        ApiClientBase("http://service.example.invalid", "token", profile)
    with pytest.raises(ValueError, match="absolute HTTPS"):
        ApiClientBase("https://user:token@service.example.invalid", "token", profile)


def test_token_is_required_and_rejects_header_injection():
    profile = MagicMock()
    with pytest.raises(ValueError, match="token is required"):
        ApiClientBase("https://service.example.invalid", "", profile)
    with pytest.raises(ValueError, match="token is required"):
        ApiClientBase("https://service.example.invalid", "token\r\ninjected", profile)


def test_pagination_rejects_cross_origin():
    client, _ = _client()
    with pytest.raises(ParameterError, match="pagination URL was rejected"):
        client._url("https://other.example.invalid/api/documents/")


def test_request_error_omits_response_body_and_target():
    client, _ = _client()
    response = MagicMock()
    response.status_code = 500
    response.content = b"sensitive provider content"
    response.text = "sensitive provider content"
    response.headers = {"Content-Type": "text/plain"}
    with patch.object(client.session, "request", return_value=response):
        with pytest.raises(ParameterError) as error:
            client.request("GET", "/api/documents/")
    rendered = str(error.value)
    assert "sensitive" not in rendered
    assert "example.invalid" not in rendered


def test_per_request_tls_override_is_rejected():
    client, _ = _client()
    with pytest.raises(ValueError, match="TLS policy overrides"):
        client._request("GET", "/api/status/", verify=False)


def test_transport_error_omits_connection_value():
    client, _ = _client()
    with patch.object(
        client.session,
        "request",
        side_effect=requests.ConnectionError("connection details"),
    ):
        with pytest.raises(ParameterError) as error:
            client.request("GET", "/api/status/")
    assert str(error.value) == "Paperless-ngx request failed"
