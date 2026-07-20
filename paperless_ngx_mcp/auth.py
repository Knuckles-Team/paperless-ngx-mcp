"""Request-scoped delegation and fixed-token client construction.

Connection values arrive through the AgentConfig/XDG projection.  TLS always uses
the shared mandatory-verification profile resolver; there is no boolean bypass.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from .api import ApiClientSystem

logger = get_logger(__name__)
_client: ApiClientSystem | None = None


def get_client(
    url: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict[str, Any] | None = None,
) -> ApiClientSystem:
    """Return a delegated client or the process-scoped fixed-token client."""

    global _client

    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        is_delegation_enabled,
    )

    delegated = is_delegation_enabled(config)
    if not delegated and _client is not None:
        return _client

    base_url = str(url or setting("PAPERLESS_URL", "") or "").strip()
    if not base_url:
        raise RuntimeError("PAPERLESS_URL is required")
    fixed_token = str(token or setting("PAPERLESS_TOKEN", "") or "")
    if not delegated and not fixed_token:
        raise RuntimeError("PAPERLESS_TOKEN is required when delegation is disabled")

    profile = tls_profile or resolve_configured_tls_profile("paperless")
    if delegated:
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", base_url),
                scopes=(config or {}).get("delegated_scopes", "api"),
            )
            logger.info("Using OIDC delegated credentials")
            return ApiClientSystem(
                base_url=base_url,
                token=delegated_token,
                tls_profile=profile,
            )
        except Exception as exc:
            profile.cleanup()
            logger.error(
                "OIDC delegation failed",
                extra={"error_type": type(exc).__name__},
            )
            raise RuntimeError("Token exchange failed") from exc

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
