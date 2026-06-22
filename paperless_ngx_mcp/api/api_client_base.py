#!/usr/bin/python
"""Base HTTP client for the Paperless-ngx Django REST Framework API.

Handles the cross-cutting concerns shared by every domain client:

* **Authentication** — Paperless-ngx uses DRF ``TokenAuthentication``: the API token
  is sent as ``Authorization: Token <key>`` (NOT ``Bearer``). The token is obtained
  from the Paperless web UI (My Profile → API Auth Token) or
  ``POST /api/token/`` with username/password.
* **Pagination** — DRF page-number pagination: list endpoints return
  ``{"count", "next", "previous", "results": [...]}``. ``_fetch_all`` follows the
  ``next`` link until exhausted (bounded by ``max_pages``).
* **Transient errors** — retries ``429``/``502``/``503``/``504`` with bounded
  exponential backoff and honours ``Retry-After``.
"""

import logging
import time
from typing import Any
from urllib.parse import urljoin

import requests
import urllib3
from agent_utilities.base_utilities import get_logger
from agent_utilities.core.exceptions import (
    AuthError,
    ParameterError,
    UnauthorizedError,
)

logger = get_logger(__name__)


class ApiClientBase:
    """Base HTTP API client for Paperless-ngx (DRF token auth)."""

    def __init__(
        self,
        base_url: str,
        token: str,
        verify: bool = True,
        max_retries: int = 3,
        debug: bool = False,
    ):
        logger.setLevel(logging.DEBUG if debug else logging.ERROR)
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify = verify
        self.max_retries = max_retries
        self.session = requests.Session()
        # DRF TokenAuthentication — "Token <key>", not Bearer.
        self.session.headers.update(
            {
                "Authorization": f"Token {token}",
                "Accept": "application/json; version=9",
            }
        )
        if verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # ------------------------------------------------------------------ request
    def _url(self, path: str) -> str:
        """Build an absolute URL. ``path`` may be a full URL (paginated ``next``)."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> requests.Response:
        """Perform a single HTTP request with transient-error retries."""
        url = self._url(path)
        attempt = 0
        while True:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params={k: v for k, v in (params or {}).items() if v is not None}
                or None,
                json=json,
                data=data,
                files=files,
                verify=self.verify,
                timeout=120,
            )
            if (
                response.status_code in (429, 502, 503, 504)
                and attempt < self.max_retries
            ):
                time.sleep(self._retry_delay(response, attempt))
                attempt += 1
                continue
            if response.status_code == 401:
                raise AuthError(
                    f"Paperless-ngx request to {url} was rejected (401). "
                    "Check PAPERLESS_TOKEN."
                )
            if response.status_code == 403:
                raise UnauthorizedError(
                    f"Paperless-ngx request to {url} was forbidden (403)."
                )
            return response

    @staticmethod
    def _retry_delay(response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        if not response.content:
            return {"status": response.status_code}
        ctype = response.headers.get("Content-Type", "")
        if "application/json" in ctype:
            try:
                return response.json()
            except ValueError:
                return response.text
        return {"status": response.status_code, "content_type": ctype}

    # ----------------------------------------------------------------- helpers
    def request(self, method: str, path: str, **kwargs) -> Any:
        """Perform a request and return the decoded body (raises on >=400)."""
        response = self._request(method, path, **kwargs)
        if response.status_code >= 400:
            raise ParameterError(
                f"Paperless-ngx {method.upper()} {path} -> {response.status_code}: "
                f"{response.text[:500]}"
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

    # --------------------------------------------------------------- escape hatch
    def api_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> Any:
        """Make an arbitrary Paperless-ngx REST request against the configured host.

        ``endpoint`` is a path appended to the base URL, e.g. ``/api/documents/``.
        Use this for operations not covered by a typed method.
        """
        if method.upper() not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        return self.request(method, endpoint, params=params, json=json, data=data)
