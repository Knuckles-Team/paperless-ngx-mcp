from unittest.mock import MagicMock, patch

import pytest

import paperless_ngx_mcp.auth as auth_module
from paperless_ngx_mcp.auth import get_client


@pytest.fixture(autouse=True)
def reset_client():
    auth_module._client = None
    yield
    auth_module._client = None


@pytest.mark.concept("PL-OS.identity.pngx")
def test_get_client_uses_profile_driven_tls():
    profile = MagicMock()
    with patch("paperless_ngx_mcp.auth.ApiClientSystem") as client_type:
        client = get_client(
            url="https://service.example.invalid",
            token="runtime-value",
            tls_profile=profile,
            config={"enable_delegation": False},
        )
    assert client is client_type.return_value
    client_type.assert_called_once_with(
        base_url="https://service.example.invalid",
        token="runtime-value",
        tls_profile=profile,
    )


def test_get_client_requires_connection_and_fixed_token():
    with pytest.raises(RuntimeError, match="PAPERLESS_URL is required"):
        get_client(config={"enable_delegation": False})
    with pytest.raises(RuntimeError, match="PAPERLESS_TOKEN is required"):
        get_client(
            url="https://service.example.invalid",
            config={"enable_delegation": False},
        )


def test_get_client_error_is_sanitized_and_cleans_profile():
    profile = MagicMock()
    with patch("paperless_ngx_mcp.auth.ApiClientSystem") as client_type:
        client_type.side_effect = Exception("provider body with identity")
        with pytest.raises(RuntimeError) as error:
            get_client(
                url="https://service.example.invalid",
                token="runtime-value",
                tls_profile=profile,
                config={"enable_delegation": False},
            )
    assert "provider body" not in str(error.value)
    assert "example.invalid" not in str(error.value)
    profile.cleanup.assert_called_once_with()


def test_delegated_client_is_request_scoped(monkeypatch):
    profile = MagicMock()
    config = {"enable_delegation": True}

    import agent_connector_sdk.auth.delegation as delegation

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")
    tokens = iter(["first-token", "second-token"])

    def _fake_exchange(settings, *, subject_token, http_client, resolver=None):
        from agent_connector_sdk.auth.tokens import AccessToken

        return AccessToken(value=next(tokens), ttl_seconds=3600, expires_at=0.0)

    monkeypatch.setattr(delegation, "exchange_token", _fake_exchange)

    with patch("paperless_ngx_mcp.auth.ApiClientSystem") as client_type:
        first = get_client(
            url="https://service.example.invalid",
            tls_profile=profile,
            config=config,
        )
        second = get_client(
            url="https://service.example.invalid",
            tls_profile=profile,
            config=config,
        )
    assert first is client_type.return_value
    assert second is client_type.return_value
    assert client_type.call_count == 2
    assert client_type.call_args_list[0].kwargs["token"] == "first-token"
    assert client_type.call_args_list[1].kwargs["token"] == "second-token"
