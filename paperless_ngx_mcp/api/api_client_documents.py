#!/usr/bin/python
"""Document-management API operations for Paperless-ngx.

Covers the core DRF resource ViewSets exposed under ``/api/`` (see the paperless-ngx
``src/paperless/urls.py`` router registration): documents, correspondents, tags,
document_types, storage_paths, custom_fields, saved_views and tasks.
"""

from typing import Any

from .api_client_base import ApiClientBase


class ApiClientDocuments(ApiClientBase):
    """Paperless-ngx document & metadata resource operations."""

    # ----------------------------------------------------------- documents
    def list_documents(
        self,
        query: str | None = None,
        ordering: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        max_pages: int = 0,
        **filters: Any,
    ) -> list:
        """List/search documents. ``query`` is full-text search; ``filters`` accepts
        DRF filters such as ``tags__id__in``, ``correspondent__id``, ``created__gte``."""
        params = {
            "query": query,
            "ordering": ordering,
            "page": page,
            "page_size": page_size,
            **filters,
        }
        return self._fetch_all("/api/documents/", params=params, max_pages=max_pages)

    def get_document(self, document_id: int) -> Any:
        """Retrieve a single document's metadata."""
        return self._get(f"/api/documents/{document_id}/")

    def get_document_metadata(self, document_id: int) -> Any:
        """Retrieve raw parsed metadata (EXIF, media filename, archive checksum…)."""
        return self._get(f"/api/documents/{document_id}/metadata/")

    def update_document(self, document_id: int, body: dict) -> Any:
        """Partially update a document (PATCH) — title, tags, correspondent, etc."""
        return self.request("PATCH", f"/api/documents/{document_id}/", json=body)

    def delete_document(self, document_id: int) -> Any:
        """Move a document to the trash."""
        return self.request("DELETE", f"/api/documents/{document_id}/")

    def get_document_notes(self, document_id: int) -> Any:
        """List the notes attached to a document."""
        return self._get(f"/api/documents/{document_id}/notes/")

    def add_document_note(self, document_id: int, note: str) -> Any:
        """Add a note to a document."""
        return self.request(
            "POST", f"/api/documents/{document_id}/notes/", json={"note": note}
        )

    def post_document(
        self,
        file_path: str,
        title: str | None = None,
        correspondent: int | None = None,
        document_type: int | None = None,
        tags: list | None = None,
        created: str | None = None,
    ) -> Any:
        """Upload a new document for consumption via ``POST /api/documents/post_document/``.

        Returns the consumption task UUID; poll ``tasks`` for completion.
        """
        data = {
            "title": title,
            "correspondent": correspondent,
            "document_type": document_type,
            "created": created,
        }
        data = {k: v for k, v in data.items() if v is not None}
        if tags:
            data["tags"] = tags
        with open(file_path, "rb") as fh:
            files = {"document": fh}
            return self.request(
                "POST", "/api/documents/post_document/", data=data, files=files
            )

    def bulk_edit_documents(
        self, documents: list, method: str, parameters: dict | None = None
    ) -> Any:
        """Run a bulk edit (``set_correspondent``, ``add_tag``, ``delete``, …) over
        a list of document ids via ``POST /api/documents/bulk_edit/``."""
        payload = {
            "documents": documents,
            "method": method,
            "parameters": parameters or {},
        }
        return self.request("POST", "/api/documents/bulk_edit/", json=payload)

    # --------------------------------------------------------- correspondents
    def list_correspondents(self, max_pages: int = 0, **filters: Any) -> list:
        """List correspondents."""
        return self._fetch_all(
            "/api/correspondents/", params=filters, max_pages=max_pages
        )

    def create_correspondent(self, body: dict) -> Any:
        """Create a correspondent."""
        return self.request("POST", "/api/correspondents/", json=body)

    def update_correspondent(self, correspondent_id: int, body: dict) -> Any:
        """Update a correspondent (PATCH)."""
        return self.request(
            "PATCH", f"/api/correspondents/{correspondent_id}/", json=body
        )

    def delete_correspondent(self, correspondent_id: int) -> Any:
        """Delete a correspondent."""
        return self.request("DELETE", f"/api/correspondents/{correspondent_id}/")

    # ---------------------------------------------------------------- tags
    def list_tags(self, max_pages: int = 0, **filters: Any) -> list:
        """List tags."""
        return self._fetch_all("/api/tags/", params=filters, max_pages=max_pages)

    def create_tag(self, body: dict) -> Any:
        """Create a tag."""
        return self.request("POST", "/api/tags/", json=body)

    def update_tag(self, tag_id: int, body: dict) -> Any:
        """Update a tag (PATCH)."""
        return self.request("PATCH", f"/api/tags/{tag_id}/", json=body)

    def delete_tag(self, tag_id: int) -> Any:
        """Delete a tag."""
        return self.request("DELETE", f"/api/tags/{tag_id}/")

    # ------------------------------------------------------- document_types
    def list_document_types(self, max_pages: int = 0, **filters: Any) -> list:
        """List document types."""
        return self._fetch_all(
            "/api/document_types/", params=filters, max_pages=max_pages
        )

    def create_document_type(self, body: dict) -> Any:
        """Create a document type."""
        return self.request("POST", "/api/document_types/", json=body)

    def delete_document_type(self, document_type_id: int) -> Any:
        """Delete a document type."""
        return self.request("DELETE", f"/api/document_types/{document_type_id}/")

    # -------------------------------------------------------- storage_paths
    def list_storage_paths(self, max_pages: int = 0, **filters: Any) -> list:
        """List storage paths."""
        return self._fetch_all(
            "/api/storage_paths/", params=filters, max_pages=max_pages
        )

    def create_storage_path(self, body: dict) -> Any:
        """Create a storage path."""
        return self.request("POST", "/api/storage_paths/", json=body)

    # --------------------------------------------------------- custom_fields
    def list_custom_fields(self, max_pages: int = 0, **filters: Any) -> list:
        """List custom fields."""
        return self._fetch_all(
            "/api/custom_fields/", params=filters, max_pages=max_pages
        )

    def create_custom_field(self, body: dict) -> Any:
        """Create a custom field."""
        return self.request("POST", "/api/custom_fields/", json=body)

    # ----------------------------------------------------------- saved_views
    def list_saved_views(self, max_pages: int = 0, **filters: Any) -> list:
        """List saved views."""
        return self._fetch_all("/api/saved_views/", params=filters, max_pages=max_pages)
