"""Request-scoped delegation and fixed-token client construction.

Connection values arrive through the AgentConfig/XDG projection.  TLS always uses
the shared mandatory-verification profile resolver; there is no boolean bypass.
Delegation (RFC 8693 token exchange) runs on ``agent_connector_sdk.auth.delegation``
(see onetrust-api's ``auth.py``, the proven reference for this path).
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile

from .api import ApiClientSystem

logger = logging.getLogger(__name__)
_client: ApiClientSystem | None = None


def _is_delegation_enabled(config: dict[str, Any] | None) -> bool:
    """Whether the OIDC delegation path should be attempted.

    An explicit ``config`` dict (test injection only -- no production caller
    passes one) wins outright; otherwise reads the real ``ENABLE_DELEGATION``
    setting through ``agent_connector_sdk.auth.delegation.DelegationSettings``.
    """
    if config is not None:
        return bool(config.get("enable_delegation", False))
    from agent_connector_sdk.auth.delegation import DelegationSettings

    return DelegationSettings.from_settings().enabled


def _delegated_client(base_url: str, profile: ResolvedTLSProfile) -> ApiClientSystem:
    """Path 1: OIDC Delegation (RFC 8693 Token Exchange)."""
    import httpx
    from agent_connector_sdk.auth.delegation import (
        DelegationSettings,
        current_user_token,
        exchange_token,
    )
    from agent_connector_sdk.exceptions import LoginRequiredError

    try:
        settings = DelegationSettings.from_settings()
        subject_token = current_user_token()
        if not subject_token:
            raise LoginRequiredError("no verified caller token to delegate")
        with httpx.Client(timeout=30) as http_client:
            access_token = exchange_token(
                settings, subject_token=subject_token, http_client=http_client
            )
        logger.info("Using OIDC delegated credentials")
        return ApiClientSystem(
            base_url=base_url,
            token=access_token.value,
            tls_profile=profile,
        )
    except Exception as exc:
        profile.cleanup()
        logger.error(
            "OIDC delegation failed",
            extra={"error_type": type(exc).__name__},
        )
        raise RuntimeError("Token exchange failed") from exc


def get_client(
    url: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict[str, Any] | None = None,
) -> ApiClientSystem:
    """Return a delegated client or the process-scoped fixed-token client."""

    global _client

    delegated = _is_delegation_enabled(config)
    if not delegated and _client is not None:
        return _client

    base_url = str(url or setting("PAPERLESS_URL", "") or "").strip()
    if not base_url:
        raise RuntimeError("PAPERLESS_URL is required")
    fixed_token = str(token or setting("PAPERLESS_TOKEN", "") or "")
    if not delegated and not fixed_token:
        raise RuntimeError("PAPERLESS_TOKEN is required when delegation is disabled")

    profile = tls_profile or resolve_tls_profile("paperless")
    if delegated:
        return _delegated_client(base_url, profile)

    logger.info("Using fixed credentials")
    try:
        _client = ApiClientSystem(
            base_url=base_url,
            token=fixed_token,
            tls_profile=profile,
        )
    except (AuthError, UnauthorizedError) as exc:
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: configured credentials were rejected"
        ) from exc
    except Exception as exc:
        profile.cleanup()
        raise RuntimeError(
            f"AUTHENTICATION ERROR: client initialization failed ({type(exc).__name__})"
        ) from exc
    return _client
