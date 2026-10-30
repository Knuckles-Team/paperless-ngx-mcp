#!/usr/bin/python
"""Base HTTP client for the Paperless-ngx Django REST Framework API.

Handles the cross-cutting concerns shared by every domain client:

* **Authentication** — Paperless-ngx uses DRF ``TokenAuthentication``: the API token
  is sent as ``Authorization: Token <key>`` (NOT ``Bearer``). The token is
  provisioned outside the MCP runtime.
* **Pagination** — DRF page-number pagination: list endpoints return
  ``{"count", "next", "previous", "results": [...]}``. ``_fetch_all`` follows the
  ``next`` link until exhausted (bounded by ``max_pages``).
* **Transient errors** — the SDK governed client retries ``408``/``429``/``502``/
  ``503``/``504`` for idempotent methods with bounded backoff and honours
  ``Retry-After``.
"""

from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx
from scion_sdk.auth.static import ApiKeyAuth
from scion_sdk.exceptions import (
    AuthError,
    ParameterError,
    UnauthorizedError,
)
from scion_sdk.http.client import create_http_client
from scion_sdk.http.options import HttpClientOptions
from scion_sdk.http.retry import RetryPolicy
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile


def _validated_base_url(value: str) -> str:
    """Return an HTTPS provider base URL without disclosing it on failure."""

    rendered = str(value or "").strip().rstrip("/")
    try:
        parsed = urlsplit(rendered)
    except ValueError:
        parsed = None
    if (
        parsed is None
        or parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Paperless-ngx base URL must be an absolute HTTPS URL")
    return rendered


class ApiClientBase:
    """Base HTTP API client for Paperless-ngx (DRF token auth)."""

    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
        max_retries: int = 3,
    ):
        self.base_url = _validated_base_url(base_url)
        if not token or "\r" in token or "\n" in token:
            raise ValueError("Paperless-ngx API token is required")
        parsed = urlsplit(self.base_url)
        self._origin = (parsed.scheme, parsed.netloc)
        self.max_retries = max_retries
        self.tls_profile = tls_profile or resolve_tls_profile("paperless")
        # DRF TokenAuthentication — "Token <key>", not Bearer.
        self.session = create_http_client(
            HttpClientOptions(
                base_url=self.base_url,
                timeout=120,
                retry=RetryPolicy(max_attempts=max_retries + 1),
                tls=self.tls_profile,
                auth=ApiKeyAuth(token, header="Authorization", prefix="Token "),
                headers={"Accept": "application/json; version=9"},
            )
        )

    def close(self) -> None:
        """Release the HTTP session and any runtime-materialized trust files."""

        self.session.close()
        self.tls_profile.cleanup()

    # ------------------------------------------------------------------ request
    def _url(self, path: str) -> str:
        """Build a same-origin URL, including provider pagination links."""

        url = urljoin(self.base_url + "/", str(path).lstrip("/"))
        parsed = urlsplit(url)
        if (
            (parsed.scheme, parsed.netloc) != self._origin
            or parsed.username is not None
            or parsed.password is not None
            or parsed.fragment
        ):
            raise ParameterError("Paperless-ngx pagination URL was rejected")
        return url

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
        **transport_overrides: Any,
    ) -> httpx.Response:
        """Perform a single HTTP request; the SDK client retries transient errors."""
        if {"cert", "proxies", "verify"}.intersection(transport_overrides):
            raise ValueError("per-request TLS policy overrides are not accepted")
        url = self._url(path)
        try:
            response = self.session.request(
                method.upper(),
                url,
                params={k: v for k, v in (params or {}).items() if v is not None}
                or None,
                json=json,
                data=data,
                files=files,
            )
        except httpx.HTTPError:
            raise ParameterError("Paperless-ngx request failed") from None
        if response.status_code == 401:
            raise AuthError("Paperless-ngx credentials were rejected")
        if response.status_code == 403:
            raise UnauthorizedError("Paperless-ngx operation was forbidden")
        return response

    @staticmethod
    def _decode(response: httpx.Response) -> Any:
        if not response.content:
            return {"status": response.status_code}
        ctype = response.headers.get("Content-Type", "")
        if "application/json" in ctype:
            try:
                return response.json()
            except ValueError:
                raise ParameterError("Paperless-ngx returned invalid JSON") from None
        return {"status": response.status_code, "content_type": ctype}

    # ----------------------------------------------------------------- helpers
    def request(self, method: str, path: str, **kwargs) -> Any:
        """Perform a request and return the decoded body (raises on >=400)."""
        response = self._request(method, path, **kwargs)
        if response.status_code >= 400:
            raise ParameterError(
                f"Paperless-ngx request failed with status {response.status_code}"
            )
        return self._decode(response)

    def _get(self, path: str, params: dict | None = None) -> Any:
        return self.request("GET", path, params=params)

    def _fetch_all(
        self, path: str, params: dict | None = None, max_pages: int = 0
    ) -> list:
        """Follow DRF page-number pagination, collecting every ``results`` item."""
        max_pages = max_pages if max_pages and max_pages > 0 else 50
        body = self._get(path, params=params)
        if isinstance(body, list):
            return body
        if not isinstance(body, dict):
            return []
        items = list(body.get("results", []))
        nxt = body.get("next")
        pages = 1
        while nxt and pages < max_pages:
            body = self._get(nxt)
            if not isinstance(body, dict):
                break
            items.extend(body.get("results", []))
            nxt = body.get("next")
            pages += 1
        return items
