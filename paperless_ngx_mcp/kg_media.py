"""Native epistemic-graph blob ingestion for Paperless-ngx scanned documents.

CONCEPT:AU-KG.ingest.list-durable-media. Paperless-ngx documents are scans — the raw
PDF/image bytes are worth making durable, deduped and queryable inside the knowledge
graph, not just their OCR text. This stores the file as a content-addressed ``:Blob``
wrapped by a ``:MediaAsset`` entity in one atomic change-set submission through the
agent-connector-sdk knowledge-ingest facade (``agent_connector_sdk.ingest``), and links
it back to the ``:Document`` node with a ``:scannedAs`` relationship in the same
``ChangeSet``.

Best-effort: with no reachable engine (``IngestError``/``IngestUnavailableError``) the
one entry point **no-ops** (returns ``None``) rather than raising, so the connector runs
with zero KG infrastructure. This is the blob leg of the package's "maximum ingestion"
contribution; ``kg_ingest.py`` is the typed-record leg.

AU-BOUNDARY-R005: migrated off ``agent_utilities.knowledge_graph.memory.native_ingest`` /
``media_store`` onto the SDK's ``ingest.MediaAsset`` + ``ChangeSet`` per
plans/refactor/reconciliation-20261006/FLEET-SDK-MIGRATION-RECIPE.md.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    EntityRef,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    MediaAsset,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("paperless_ngx_mcp.kg.media")

_SOURCE = "paperless-ngx-mcp"
_BINDING = IngestBinding(
    connector=_SOURCE, stream="document-media", tool="ingest_document_blob"
)

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


async def ingest_document_blob(
    document_id: int | str,
    data: bytes | None,
    *,
    info: dict[str, Any] | None = None,
    mime_type: str = "application/pdf",
    source_uri: str = "",
    source: str = _SOURCE,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store a scanned document's raw bytes as a ``:Blob`` / ``:MediaAsset`` in the KG.

    Also links the document node (``paperless:document:<id>``) to the new asset with a
    ``:scannedAs`` relationship in the same change set. Returns
    ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None`` (no bytes, no
    reachable engine, or the submission failed — never raises). ``ingest`` may be
    injected (tests); it defaults to the process-global facade.
    """
    if not data:
        return None

    info = info or {}
    media_type = "image" if str(mime_type).startswith("image") else "file"
    extra = {k: info[k] for k in _INFO_FIELDS if info.get(k) is not None}
    if source_uri:
        extra["source_uri"] = source_uri
    extra["document_id"] = str(document_id)
    extra["source"] = source
    name = (
        info.get("title") or info.get("original_file_name") or f"document-{document_id}"
    )

    # A stable, caller-known id (rather than the CAS default `blob:<digest>`) so the
    # :scannedAs relationship can name its target before the asset is stored, and so
    # the caller gets back a deterministic asset_id.
    asset_id = f"paperless:asset:{document_id}"
    digest = hashlib.sha256(data).hexdigest()
    asset = MediaAsset(
        data=data, mime_type=mime_type, id=asset_id, name=name, properties=extra
    )
    document_ref = f"paperless:document:{document_id}"
    change_set = ChangeSet(
        media=(asset,),
        relationships=(
            Relationship(
                source=EntityRef(document_ref, node_type="document"),
                target=EntityRef(asset_id, node_type=_BINDING.media_type),
                relationship="scannedAs",
            ),
        ),
    )

    service = ingest if ingest is not None else current_ingest()
    try:
        await service.submit(_BINDING, change_set)
    except IngestError as e:  # noqa: BLE001 — best-effort, engine/store failure is non-fatal
        logger.debug("KG media ingest: submission failed: %s", e)
        return None

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
