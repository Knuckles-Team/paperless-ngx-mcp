"""Native epistemic-graph blob ingestion — Wire-First live-path coverage.

Exercises the real ``ingest_document_blob`` seam against a fake SDK ingest
transport (no engine required), asserting the media asset + :scannedAs
relationship the SDK's own request builder produces.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from paperless_ngx_mcp.kg_media import ingest_document_blob


class _FakeTransport:
    def __init__(self):
        self.requests = []

    async def source_status(self, _connector, _stream):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data):
        import hashlib

        return hashlib.sha256(data).hexdigest()


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_document_blob_stores_bytes_and_links(ingest):
    service, transport = ingest
    res = await ingest_document_blob(
        42,
        b"%PDF-1.7 scan-bytes",
        info={"id": 42, "title": "Acme Invoice", "correspondent": 2},
        mime_type="application/pdf",
        source_uri="https://paperless.example/documents/42/",
        ingest=service,
    )
    assert res is not None
    assert res["asset_id"] == "paperless:asset:42"
    assert res["media_type"] == "file"
    assert res["size_bytes"] == len(b"%PDF-1.7 scan-bytes")

    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert len(request.records) == 1
    assert request.records[0].record_id == "paperless:asset:42"
    assert request.records[0].payload["name"] == "Acme Invoice"
    assert request.records[0].payload["document_id"] == "42"
    # the SDK's PersistencePrivacyGuard redacts URL-shaped property values.
    assert "source_uri" in request.records[0].payload

    assert len(request.relationships) == 1
    rel = request.relationships[0]
    assert rel.source.record_id == "paperless:document:42"
    assert rel.target.record_id == "paperless:asset:42"


@pytest.mark.asyncio
async def test_ingest_document_blob_image_mime(ingest):
    service, _ = ingest
    res = await ingest_document_blob(7, b"\x89PNG scan", mime_type="image/png", ingest=service)
    assert res is not None
    assert res["media_type"] == "image"


@pytest.mark.asyncio
async def test_ingest_document_blob_noops_on_empty_bytes(ingest):
    service, _ = ingest
    assert await ingest_document_blob(1, b"", ingest=service) is None
    assert await ingest_document_blob(1, None, ingest=service) is None
