"""Native epistemic-graph ingestion for Paperless-ngx records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source leg of the
package's "maximum ingestion" contribution: paperless-ngx-mcp natively pushes its data
into the ONE epistemic-graph engine as **typed OWL nodes** — ``:Document`` (carrying the
OCR text for semantic search), plus ``:Correspondent`` / ``:Tag`` / ``:DocumentType`` /
``:StoragePath`` metadata nodes and the ``:fromCorrespondent`` / ``:hasTag`` /
``:hasDocumentType`` / ``:storedAt`` links between them. The raw scanned PDF/image bytes
are handled by the blob leg (``kg_media.py``).

This module is a thin mapper: the txn write path lives in the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. The import is guarded — when the
KG stack is absent (the primitive is not yet in the installed agent_utilities), a
self-contained txn fallback drives ``GraphComputeEngine()._client`` directly, and with no
reachable engine every entry point **no-ops** (returns ``None``), so the connector runs
with zero KG infrastructure. Node ids follow ``paperless:<class>:<externalId>``; each
``type`` matches a class the package's ``ontology_providers`` ``paperless.ttl`` federates.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("paperless_ngx_mcp.kg")

_SOURCE = "paperless-ngx-mcp"
_DOMAIN = "paperless"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------- primitive
def _native():
    """Return the shared native-ingest primitive module, or ``None`` when absent."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest
    except Exception as e:  # noqa: BLE001 — primitive not yet in installed agent_utilities
        logger.debug("native_ingest primitive unavailable: %s", e)
        return None


def _fallback_client() -> tuple[Any | None, str]:
    """Self-contained engine-client resolver used when the shared primitive is absent."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write_nodes(
    client: Any,
    graph: str,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    source: str,
    domain: str,
) -> dict[str, int] | None:
    """Stamp provenance, MERGE the nodes in one txn, then add the edges (fallback path)."""
    nodes = [n for n in nodes if n.get("id")]
    if not nodes:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)
    logger.info("KG ingest[%s]: wrote %d nodes, %d edges", domain, len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


# ------------------------------------------------------------------- public write seams
def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into the engine (delegates to the primitive).

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None``. ``client``/``graph`` may be injected
    (tests); otherwise resolved on demand. Never raises.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    prim = _native()
    if prim is not None and client is None:
        return prim.ingest_entities(
            entities, relationships, source=source, domain=domain
        )
    if prim is not None and client is not None:
        return prim.ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    # fallback: primitive absent
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    return _fallback_write_nodes(
        client,
        graph or _DEFAULT_GRAPH,
        entities,
        relationships,
        source=source,
        domain=domain,
    )


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``. Never raises.
    """
    docs = [
        d for d in (docs or []) if d.get("id") and (d.get("text") or d.get("content"))
    ]
    if not docs:
        return None
    prim = _native()
    if prim is not None:
        kw: dict[str, Any] = {"source": source, "domain": domain}
        if client is not None:
            kw["client"] = client
            kw["graph"] = graph
        return prim.ingest_documents(docs, **kw)
    # fallback: build :Document nodes ourselves
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    nodes: list[dict[str, Any]] = []
    for doc in docs:
        text = doc.get("text") or doc.get("content")
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = doc["id"]
        node["type"] = "Document"
        node["text"] = text
        node.setdefault("created_at", now)
        nodes.append(node)
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    return _fallback_write_nodes(
        client, graph or _DEFAULT_GRAPH, nodes, None, source=source, domain=domain
    )


def media_store() -> Any | None:
    """Return a ``MediaStore`` over a live engine (raw-blob ingestion), or ``None``."""
    prim = _native()
    if prim is not None:
        try:
            return prim.media_store()
        except Exception as e:  # noqa: BLE001
            logger.debug("KG ingest: primitive media_store unavailable: %s", e)
            return None
    client, _ = _fallback_client()
    if client is None:
        return None
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore

        return MediaStore(GraphComputeEngine())
    except Exception as e:  # noqa: BLE001
        logger.debug("KG ingest: media_store unavailable: %s", e)
        return None


# ------------------------------------------------------------------- domain mappers
def _meta_node(record: dict[str, Any], node_type: str) -> dict[str, Any] | None:
    """Map a paperless correspondent/tag/document_type/storage_path record → typed node."""
    rid = record.get("id")
    if rid is None:
        return None
    prefix = {
        "Correspondent": "correspondent",
        "Tag": "tag",
        "DocumentType": "document_type",
        "StoragePath": "storage_path",
    }[node_type]
    node: dict[str, Any] = {
        "id": f"paperless:{prefix}:{rid}",
        "type": node_type,
        "name": record.get("name"),
        "slug": record.get("slug"),
        "documentCount": record.get("document_count"),
        "externalToolId": str(rid),
    }
    if node_type == "Tag":
        node["color"] = record.get("color") or record.get("colour")
    if node_type == "StoragePath":
        node["path"] = record.get("path")
    return {k: v for k, v in node.items() if v is not None}


def ingest_metadata(
    *,
    correspondents: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    document_types: list[dict[str, Any]] | None = None,
    storage_paths: list[dict[str, Any]] | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map + ingest the organizing metadata (correspondents/tags/types/storage paths)."""
    entities: list[dict[str, Any]] = []
    for rec in correspondents or []:
        n = _meta_node(rec, "Correspondent")
        if n:
            entities.append(n)
    for rec in tags or []:
        n = _meta_node(rec, "Tag")
        if n:
            entities.append(n)
    for rec in document_types or []:
        n = _meta_node(rec, "DocumentType")
        if n:
            entities.append(n)
    for rec in storage_paths or []:
        n = _meta_node(rec, "StoragePath")
        if n:
            entities.append(n)
    return ingest_entities(entities, None, client=client, graph=graph)


def ingest_documents_records(
    documents: list[dict[str, Any]],
    *,
    base_url: str = "",
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Paperless-ngx document records → ``:Document`` nodes + metadata links.

    Writes the OCR text as ``:Document`` (semantic search), then the referenced
    ``:Correspondent`` / ``:Tag`` / ``:DocumentType`` / ``:StoragePath`` nodes and the
    ``:fromCorrespondent`` / ``:hasTag`` / ``:hasDocumentType`` / ``:storedAt`` edges.
    Returns merged ``{"nodes":n, "edges":m}`` or ``None``.
    """
    docs: list[dict[str, Any]] = []
    related: dict[str, dict[str, Any]] = {}
    relationships: list[dict[str, Any]] = []

    def _ref(rid: Any, node_type: str, prefix: str) -> str:
        nid = f"paperless:{prefix}:{rid}"
        related.setdefault(nid, {"id": nid, "type": node_type})
        return nid

    for rec in documents or []:
        did = rec.get("id")
        if did is None:
            continue
        doc_id = f"paperless:document:{did}"
        text = rec.get("content") or rec.get("text") or rec.get("title") or ""
        node: dict[str, Any] = {
            "id": doc_id,
            "title": rec.get("title"),
            "text": text,
            "archiveSerialNumber": rec.get("archive_serial_number"),
            "originalFileName": rec.get("original_file_name"),
            "created": rec.get("created") or rec.get("created_date"),
            "modified": rec.get("modified"),
            "addedAt": rec.get("added"),
            "externalToolId": str(did),
        }
        if base_url:
            node["source_uri"] = f"{base_url.rstrip('/')}/documents/{did}/"
        docs.append({k: v for k, v in node.items() if v is not None})

        corr = rec.get("correspondent")
        if corr is not None:
            relationships.append(
                {
                    "source": doc_id,
                    "target": _ref(corr, "Correspondent", "correspondent"),
                    "type": "fromCorrespondent",
                }
            )
        dtype = rec.get("document_type")
        if dtype is not None:
            relationships.append(
                {
                    "source": doc_id,
                    "target": _ref(dtype, "DocumentType", "document_type"),
                    "type": "hasDocumentType",
                }
            )
        spath = rec.get("storage_path")
        if spath is not None:
            relationships.append(
                {
                    "source": doc_id,
                    "target": _ref(spath, "StoragePath", "storage_path"),
                    "type": "storedAt",
                }
            )
        for tid in rec.get("tags") or []:
            relationships.append(
                {
                    "source": doc_id,
                    "target": _ref(tid, "Tag", "tag"),
                    "type": "hasTag",
                }
            )

    # 1) documents (with text) first so edges resolve, 2) related metadata + edges.
    doc_res = ingest_documents(docs, client=client, graph=graph)
    ent_res = ingest_entities(
        list(related.values()), relationships, client=client, graph=graph
    )

    nodes = (doc_res or {}).get("nodes", 0) + (ent_res or {}).get("nodes", 0)
    edges = (ent_res or {}).get("edges", 0)
    if doc_res is None and ent_res is None:
        return None
    return {"nodes": nodes, "edges": edges}
