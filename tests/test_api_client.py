from unittest.mock import MagicMock, patch

import pytest
import httpx
from agent_connector_sdk.exceptions import ParameterError
from agent_connector_sdk.tls.resolve import resolve_tls_profile

from paperless_ngx_mcp.api import ApiClientBase


def _client() -> tuple[ApiClientBase, MagicMock]:
    profile = resolve_tls_profile("paperless")
    object.__setattr__(profile, "cleanup", MagicMock())
    return (
        ApiClientBase(
            base_url="https://service.example.invalid",
            token="runtime-value",
            tls_profile=profile,
        ),
        profile,
    )


@pytest.mark.concept("PL-OS.identity.pngx")
# spec: CONN-PAPERLESS-NGX-MCP-SDK-R001, CONN-PAPERLESS-NGX-MCP-SDK-R004
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
    assert client.session.follow_redirects is False


@pytest.mark.concept("PL-OS.identity.pngx")
def test_token_auth_header_and_tls_profile_cleanup():
    client, profile = _client()
    request = client.session.build_request("GET", "https://service.example.invalid/")
    request = next(client.session.auth.auth_flow(request))
    assert request.headers["Authorization"] == "Token runtime-value"
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
        side_effect=httpx.ConnectError("connection details"),
    ):
        with pytest.raises(ParameterError) as error:
            client.request("GET", "/api/status/")
    assert str(error.value) == "Paperless-ngx request failed"


def _mock_client(handler):
    from unittest.mock import patch as _patch

    from agent_connector_sdk.http.client import create_http_client as real

    def build(options):
        return real(options, transport=httpx.MockTransport(handler))

    with _patch("paperless_ngx_mcp.api.api_client_base.create_http_client", build):
        return _client()[0]


# spec: CONN-PAPERLESS-NGX-MCP-SDK-R001, CONN-PAPERLESS-NGX-MCP-SDK-R004
def test_client_is_governed_with_token_auth():
    client, _ = _client()
    assert isinstance(client.session, httpx.Client)
    request = client.session.build_request("GET", "https://service.example.invalid/")
    request = next(client.session.auth.auth_flow(request))
    assert request.headers["Authorization"] == "Token runtime-value"
    assert client.session.follow_redirects is False


# spec: CONN-PAPERLESS-NGX-MCP-SDK-R002, CONN-PAPERLESS-NGX-MCP-SDK-R005
def test_transient_status_is_retried_by_the_sdk_client(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _s: None)
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(503, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"results": []})

    from paperless_ngx_mcp.api import ApiClientDocuments

    client = _mock_client(handler)
    documents = ApiClientDocuments.__new__(ApiClientDocuments)
    documents.__dict__.update(client.__dict__)
    assert documents.request("GET", "/api/documents/") == {"results": []}
    assert len(calls) == 2


# spec: CONN-PAPERLESS-NGX-MCP-SDK-R003
def test_dependencies_carry_sdk_floor_and_no_requests_pin():
    import pathlib
    import tomllib

    root = pathlib.Path(__file__).resolve().parents[1]
    deps = tomllib.loads((root / "pyproject.toml").read_text())["project"]["dependencies"]
    assert any(d.startswith("agent-connector-sdk[mcp]>=0.3.18") for d in deps)
    assert not any(d.lower().startswith("requests") for d in deps)
