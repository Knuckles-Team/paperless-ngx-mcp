#!/usr/bin/python
"""Search, task and system-status API operations for Paperless-ngx.

Covers the non-resource endpoints under ``/api/``: global search, autocomplete,
statistics, system status, remote-version, and the tasks ViewSet.
"""

from typing import Any

from .api_client_documents import ApiClientDocuments


class ApiClientSystem(ApiClientDocuments):
    """Unified Paperless-ngx client.

    Exposes the full surface: document/metadata resource operations (inherited from
    :class:`ApiClientDocuments`) plus search, tasks and system status defined here.
    A single client class keeps ``auth.get_client`` and the verbose tool surface
    simple.
    """

    # --------------------------------------------------------------- search
    def global_search(self, query: str, db_only: bool | None = None) -> Any:
        """Run a global search across documents, correspondents, tags, etc.
        (``GET /api/search/``)."""
        return self._get("/api/search/", params={"query": query, "db_only": db_only})

    def autocomplete(self, term: str, limit: int | None = None) -> Any:
        """Search-term autocomplete (``GET /api/search/autocomplete/``)."""
        return self._get(
            "/api/search/autocomplete/", params={"term": term, "limit": limit}
        )

    # ---------------------------------------------------------------- tasks
    def list_tasks(self, max_pages: int = 0, **filters: Any) -> list:
        """List background/consumption tasks (``GET /api/tasks/``)."""
        return self._fetch_all("/api/tasks/", params=filters, max_pages=max_pages)

    def get_task(self, task_id: str) -> Any:
        """Retrieve a single task by id (``GET /api/tasks/?task_id=...``)."""
        return self._get("/api/tasks/", params={"task_id": task_id})

    def acknowledge_tasks(self, tasks: list) -> Any:
        """Acknowledge (dismiss) tasks (``POST /api/acknowledge_tasks/``)."""
        return self.request("POST", "/api/acknowledge_tasks/", json={"tasks": tasks})

    # -------------------------------------------------------------- system
    def get_statistics(self) -> Any:
        """Document/inbox statistics (``GET /api/statistics/``)."""
        return self._get("/api/statistics/")

    def get_system_status(self) -> Any:
        """Backend/service health & version info (``GET /api/status/``)."""
        return self._get("/api/status/")

    def get_remote_version(self) -> Any:
        """Latest available Paperless-ngx version (``GET /api/remote_version/``)."""
        return self._get("/api/remote_version/")

    def get_ui_settings(self) -> Any:
        """Current user's UI settings and permissions (``GET /api/ui_settings/``)."""
        return self._get("/api/ui_settings/")

    def obtain_token(self, username: str, password: str) -> Any:
        """Obtain an API auth token from username/password
        (``POST /api/token/``)."""
        return self.request(
            "POST",
            "/api/token/",
            json={"username": username, "password": password},
        )

    def get_schema(self) -> Any:
        """Retrieve the live OpenAPI schema (``GET /api/schema/``, drf-spectacular)."""
        return self._get("/api/schema/")
