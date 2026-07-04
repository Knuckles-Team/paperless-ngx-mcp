"""Native epistemic-graph blob ingestion — Wire-First live-path coverage.

Exercises the real ``ingest_document_blob`` seam with a fake ``MediaStore`` + engine
client (no engine required), asserting the store_media call + the :scannedAs edge.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from paperless_ngx_mcp.kg_media import ingest_document_blob


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="paperless:asset:deadbeef", digest="deadbeef")


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.edges = _FakeEdges()


def test_ingest_document_blob_stores_bytes_and_links():
    store = _FakeMediaStore()
    client = _FakeClient()
    res = ingest_document_blob(
        42,
        b"%PDF-1.7 scan-bytes",
        info={"id": 42, "title": "Acme Invoice", "correspondent": 2},
        mime_type="application/pdf",
        source_uri="https://paperless.example/documents/42/",
        store=store,
        client=client,
    )
    assert res is not None
    assert res["asset_id"] == "paperless:asset:deadbeef"
    assert res["digest"] == "deadbeef"
    assert res["media_type"] == "file"
    assert res["size_bytes"] == len(b"%PDF-1.7 scan-bytes")

    # store_media got the raw bytes + propagated metadata.
    assert len(store.calls) == 1
    data, kw = store.calls[0]
    assert data == b"%PDF-1.7 scan-bytes"
    assert kw["source"] == "paperless-ngx-mcp"
    assert kw["mime_type"] == "application/pdf"
    assert kw["name"] == "Acme Invoice"
    assert kw["extra"]["document_id"] == "42"
    assert kw["extra"]["source_uri"] == "https://paperless.example/documents/42/"

    # the document was linked to the stored asset via :scannedAs.
    assert client.edges.edges == [
        ("paperless:document:42", "paperless:asset:deadbeef", {"type": "scannedAs"})
    ]


def test_ingest_document_blob_image_mime():
    store = _FakeMediaStore()
    res = ingest_document_blob(
        7, b"\x89PNG scan", mime_type="image/png", store=store, client=_FakeClient()
    )
    assert res is not None
    assert res["media_type"] == "image"


def test_ingest_document_blob_noops_without_store():
    # No injected store + no reachable engine -> clean no-op (never raises).
    assert ingest_document_blob(1, b"bytes") is None


def test_ingest_document_blob_noops_on_empty_bytes():
    assert ingest_document_blob(1, b"", store=_FakeMediaStore()) is None
    assert ingest_document_blob(1, None, store=_FakeMediaStore()) is None
