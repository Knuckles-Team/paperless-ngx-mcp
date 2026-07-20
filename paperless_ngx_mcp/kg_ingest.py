"""Keyed zero-PII Paperless-ngx projection and governed graph ingestion.

Provider records are reduced in memory to opaque typed nodes and structural edges.
OCR content, titles, names, filenames, storage paths, timestamps, URLs, raw bytes, and
provider identifiers never cross this boundary.  Writes use Agent Utilities' sole
ChangeEnvelope authority; no raw transaction or best-effort path exists.
"""

from __future__ import annotations

import hashlib
import hmac
import re
from typing import Any

from agent_utilities.core.config import setting

_SOURCE = "paperless-ngx-mcp"
_DOMAIN = "paperless"
_NODE_TYPES = frozenset(
    {
        "PaperlessDocumentReference",
        "PaperlessCorrespondentReference",
        "PaperlessTagReference",
        "PaperlessDocumentTypeReference",
        "PaperlessStoragePathReference",
    }
)
_RELATIONSHIPS = frozenset(
    {
        "hasCorrespondentReference",
        "hasTagReference",
        "hasDocumentTypeReference",
        "hasStoragePathReference",
    }
)
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


def _native_ingest_entities(*args: Any, **kwargs: Any) -> dict[str, int]:
    """Resolve the governed engine boundary only when an ingest is requested."""

    from agent_utilities.knowledge_graph.memory.native_ingest import ingest_entities

    return ingest_entities(*args, **kwargs)


def _projection_key(explicit: bytes | None = None) -> bytes:
    key = explicit
    if key is None:
        configured = setting("PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY", "")
        key = str(configured or "").encode()
    if len(key) < 32:
        raise RuntimeError(
            "Paperless-ngx ingestion requires a deployment-owned pseudonymization key"
        )
    return key


def _opaque_id(node_type: str, provider_id: Any, key: bytes) -> str:
    if provider_id in (None, ""):
        raise ValueError("Paperless-ngx record has no identifier")
    digest = hmac.new(
        key,
        f"paperless-ngx-mcp\x00{node_type}\x00{provider_id}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"paperless:{node_type}:{digest}"


def _records(value: Any, *, kind: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f"Paperless-ngx {kind} response is malformed")
    return value


def project_records(
    documents: list[dict[str, Any]],
    *,
    correspondents: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    document_types: list[dict[str, Any]] | None = None,
    storage_paths: list[dict[str, Any]] | None = None,
    pseudonymization_key: bytes | None = None,
) -> dict[str, list[dict[str, str]]]:
    """Return opaque document topology without retaining source values."""

    key = _projection_key(pseudonymization_key)
    entities: list[dict[str, str]] = []
    relationships: list[dict[str, str]] = []
    seen: set[str] = set()

    def add_node(node_type: str, provider_id: Any) -> str:
        node_id = _opaque_id(node_type, provider_id, key)
        if node_id not in seen:
            entities.append({"id": node_id, "node_type": node_type})
            seen.add(node_id)
        return node_id

    metadata_sets = (
        ("PaperlessCorrespondentReference", correspondents),
        ("PaperlessTagReference", tags),
        ("PaperlessDocumentTypeReference", document_types),
        ("PaperlessStoragePathReference", storage_paths),
    )
    for node_type, values in metadata_sets:
        for record in _records(values, kind=node_type) if values is not None else []:
            add_node(node_type, record.get("id"))

    edge_fields = (
        (
            "correspondent",
            "PaperlessCorrespondentReference",
            "hasCorrespondentReference",
        ),
        (
            "document_type",
            "PaperlessDocumentTypeReference",
            "hasDocumentTypeReference",
        ),
        (
            "storage_path",
            "PaperlessStoragePathReference",
            "hasStoragePathReference",
        ),
    )
    for record in _records(documents, kind="document"):
        document_id = add_node("PaperlessDocumentReference", record.get("id"))
        for field, node_type, relationship in edge_fields:
            provider_id = record.get(field)
            if provider_id is None:
                continue
            target = add_node(node_type, provider_id)
            relationships.append(
                {
                    "source": document_id,
                    "target": target,
                    "relationship": relationship,
                }
            )
        raw_tags = record.get("tags") or []
        if not isinstance(raw_tags, list):
            raise ValueError("Paperless-ngx document tags are malformed")
        for provider_id in raw_tags:
            target = add_node("PaperlessTagReference", provider_id)
            relationships.append(
                {
                    "source": document_id,
                    "target": target,
                    "relationship": "hasTagReference",
                }
            )
    return {"records": entities, "relationships": relationships}


def ingest_projection(
    projection: dict[str, list[dict[str, str]]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Commit one previously projected structural slice through ChangeEnvelope."""

    if not isinstance(projection, dict) or set(projection) - {
        "records",
        "relationships",
    }:
        raise ValueError("Paperless-ngx projection is malformed")
    raw_entities = projection.get("records") or []
    raw_relationships = projection.get("relationships") or []
    if not isinstance(raw_entities, list) or not isinstance(raw_relationships, list):
        raise ValueError("Paperless-ngx projection is malformed")

    entities: list[dict[str, str]] = []
    node_ids: set[str] = set()
    for record in raw_entities:
        if not isinstance(record, dict) or set(record) != {"id", "node_type"}:
            raise ValueError("Paperless-ngx projection contains an invalid node")
        node_id = record.get("id")
        node_type = record.get("node_type")
        if not isinstance(node_id, str) or node_type not in _NODE_TYPES:
            raise ValueError("Paperless-ngx projection contains an invalid node")
        prefix = f"paperless:{node_type}:"
        digest = node_id.removeprefix(prefix)
        if not node_id.startswith(prefix) or not _DIGEST.fullmatch(digest):
            raise ValueError("Paperless-ngx projection contains an invalid node")
        if node_id not in node_ids:
            node_ids.add(node_id)
            entities.append({"id": node_id, "node_type": node_type})

    relationships: list[dict[str, str]] = []
    for edge in raw_relationships:
        if not isinstance(edge, dict) or set(edge) != {
            "source",
            "target",
            "relationship",
        }:
            raise ValueError(
                "Paperless-ngx projection contains an invalid relationship"
            )
        source = edge.get("source")
        target = edge.get("target")
        relationship = edge.get("relationship")
        if (
            not isinstance(source, str)
            or not isinstance(target, str)
            or not isinstance(relationship, str)
            or source not in node_ids
            or target not in node_ids
            or relationship not in _RELATIONSHIPS
        ):
            raise ValueError(
                "Paperless-ngx projection contains an invalid relationship"
            )
        relationships.append(
            {
                "source": source,
                "target": target,
                "relationship": relationship,
            }
        )
    if not entities:
        return {"nodes": 0, "edges": 0}
    return _native_ingest_entities(
        entities,
        relationships,
        source=_SOURCE,
        domain=_DOMAIN,
        client=client,
        graph=graph,
    )


def ingest_documents_records(
    documents: list[dict[str, Any]],
    *,
    correspondents: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    document_types: list[dict[str, Any]] | None = None,
    storage_paths: list[dict[str, Any]] | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Project and commit a content-free Paperless-ngx graph slice."""

    projection = project_records(
        documents,
        correspondents=correspondents,
        tags=tags,
        document_types=document_types,
        storage_paths=storage_paths,
    )
    return ingest_projection(projection, client=client, graph=graph)
