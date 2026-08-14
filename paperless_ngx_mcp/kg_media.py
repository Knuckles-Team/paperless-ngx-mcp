"""Native epistemic-graph blob ingestion for Paperless-ngx scanned documents.

CONCEPT:AU-KG.ingest.list-durable-media. Paperless-ngx documents are scans — the raw
PDF/image bytes are worth making durable, deduped and queryable inside the knowledge
graph, not just their OCR text. When a live engine is reachable this stores the file as a
content-addressed ``:Blob`` wrapped by a ``:MediaAsset`` node (carrying the document's
metadata) in ONE cross-modal ACID commit via the shared ``MediaStore``, and links it back
to the ``:Document`` node with a ``:scannedAs`` edge.

Best-effort and dependency-/engine-guarded: with no KG stack or no reachable engine every
entry point **no-ops** (returns ``None``), so the connector runs with zero KG
infrastructure. This is the blob leg of the package's "maximum ingestion" contribution;
``kg_ingest.py`` is the typed-record leg.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("paperless_ngx_mcp.kg.media")

_SOURCE = "paperless-ngx-mcp"


def media_store() -> Any | None:
    """Return a ``MediaStore`` over a live engine, or ``None`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest.media_store()
    except Exception as e:  # noqa: BLE001 — primitive not installed yet
        logger.debug("KG media: shared primitive unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — no reachable engine
        logger.debug("KG media ingest: engine unreachable: %s", e)
        return None


def _fallback_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or "__commons__")
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG media ingest: engine unreachable: %s", e)
        return None, ""


# Paperless document fields worth carrying onto the :MediaAsset node.
_INFO_FIELDS = (
    "id",
    "title",
    "correspondent",
    "document_type",
    "created",
    "added",
    "archive_serial_number",
    "original_file_name",
)


def ingest_document_blob(
    document_id: int | str,
    data: bytes | None,
    *,
    info: dict[str, Any] | None = None,
    mime_type: str = "application/pdf",
    source_uri: str = "",
    source: str = _SOURCE,
    store: Any | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, Any] | None:
    """Store a scanned document's raw bytes as a ``:Blob`` / ``:MediaAsset`` in the KG.

    Also links the document node (``paperless:document:<id>``) to the new asset with a
    ``:scannedAs`` edge when an engine is reachable. Returns
    ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None`` (no engine, no
    bytes, or store failed — never raises). ``store``/``client`` may be injected (tests).
    """
    if not data:
        return None
    st = store if store is not None else media_store()
    if st is None:
        return None

    info = info or {}
    media_type = "image" if str(mime_type).startswith("image") else "file"
    extra = {k: info[k] for k in _INFO_FIELDS if info.get(k) is not None}
    if source_uri:
        extra["source_uri"] = source_uri
    extra["document_id"] = str(document_id)
    name = (
        info.get("title") or info.get("original_file_name") or f"document-{document_id}"
    )

    try:
        stored = st.store_media(
            data,
            media_type=media_type,
            mime_type=mime_type,
            source=source,
            name=name,
            extra=extra,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("KG media ingest: store_media failed: %s", e)
        return None
    if stored is None:
        return None

    asset_id = getattr(stored, "asset_id", None) or (
        stored.get("asset_id") if isinstance(stored, dict) else None
    )
    digest = getattr(stored, "digest", None) or (
        stored.get("digest") if isinstance(stored, dict) else None
    )

    # Best-effort :scannedAs edge from the document node to the stored asset.
    if asset_id:
        try:
            edge_client = client
            if edge_client is None:
                edge_client, _ = _fallback_client()
            if edge_client is not None:
                edge_client.edges.add(
                    f"paperless:document:{document_id}",
                    asset_id,
                    {"type": "scannedAs"},
                )
        except Exception as e:  # noqa: BLE001 — pure link, best-effort
            logger.debug("KG media ingest: scannedAs edge skipped: %s", e)

    logger.info(
        "KG media ingest: stored document %s (%s bytes) as asset %s",
        document_id,
        len(data),
        asset_id,
    )
    return {
        "asset_id": asset_id,
        "digest": digest,
        "size_bytes": len(data),
        "media_type": media_type,
    }
