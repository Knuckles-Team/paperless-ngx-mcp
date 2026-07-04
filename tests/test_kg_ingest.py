"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` / ``ingest_metadata`` /
``ingest_documents_records`` seam with a fake engine client (no engine required),
asserting the txn add_node/commit + edge calls and the Paperless-ngx document ->
:Document / :Correspondent / :Tag mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from paperless_ngx_mcp.kg_ingest import (
    ingest_documents,
    ingest_documents_records,
    ingest_entities,
    ingest_metadata,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = 0

    def begin(self, graph=None):
        self.graph = graph
        return f"txn-{self.committed}"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed += 1
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "paperless:tag:1", "type": "Tag", "name": "Invoices"},
            {"id": "paperless:correspondent:2", "type": "Correspondent"},
        ],
        [
            {
                "source": "paperless:document:9",
                "target": "paperless:tag:1",
                "type": "hasTag",
            }
        ],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    # provenance is stamped by the fallback path.
    assert c.txn.nodes["paperless:tag:1"]["source"] == "paperless-ngx-mcp"
    assert c.txn.nodes["paperless:tag:1"]["domain"] == "paperless"
    assert c.edges.edges == [
        ("paperless:document:9", "paperless:tag:1", {"type": "hasTag"})
    ]


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "paperless:document:5", "text": "OCR body", "title": "Invoice"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["paperless:document:5"]
    assert node["type"] == "Document"
    assert node["text"] == "OCR body"


def test_ingest_documents_skips_textless():
    c = _FakeClient()
    assert ingest_documents([{"id": "x"}], client=c) is None


def test_ingest_metadata_maps_typed_nodes():
    c = _FakeClient()
    res = ingest_metadata(
        correspondents=[{"id": 2, "name": "Acme", "slug": "acme", "document_count": 4}],
        tags=[{"id": 1, "name": "Invoices", "color": "#ff8800"}],
        document_types=[{"id": 3, "name": "Invoice"}],
        storage_paths=[{"id": 7, "name": "Archive", "path": "{created}"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 4, "edges": 0}
    assert c.txn.nodes["paperless:correspondent:2"]["type"] == "Correspondent"
    assert c.txn.nodes["paperless:correspondent:2"]["externalToolId"] == "2"
    assert c.txn.nodes["paperless:tag:1"]["color"] == "#ff8800"
    assert c.txn.nodes["paperless:document_type:3"]["type"] == "DocumentType"
    assert c.txn.nodes["paperless:storage_path:7"]["path"] == "{created}"


def test_ingest_documents_records_maps_document_and_links():
    c = _FakeClient()
    res = ingest_documents_records(
        [
            {
                "id": 42,
                "title": "Acme Invoice",
                "content": "Total due: 100.00",
                "correspondent": 2,
                "document_type": 3,
                "storage_path": 7,
                "tags": [1, 5],
                "archive_serial_number": "ASN-9",
                "original_file_name": "acme.pdf",
            }
        ],
        base_url="https://paperless.example",
        client=c,
        graph="__commons__",
    )
    # 1 document node + 5 referenced metadata nodes (corr, type, storage, 2 tags)
    doc = c.txn.nodes["paperless:document:42"]
    assert doc["type"] == "Document"
    assert doc["text"] == "Total due: 100.00"
    assert doc["archiveSerialNumber"] == "ASN-9"
    assert doc["source_uri"] == "https://paperless.example/documents/42/"
    # referenced entities were created
    assert c.txn.nodes["paperless:correspondent:2"]["type"] == "Correspondent"
    assert c.txn.nodes["paperless:tag:5"]["type"] == "Tag"
    # edges: fromCorrespondent, hasDocumentType, storedAt, hasTag x2 = 5
    edge_types = sorted(props["type"] for _, _, props in c.edges.edges)
    assert edge_types == [
        "fromCorrespondent",
        "hasDocumentType",
        "hasTag",
        "hasTag",
        "storedAt",
    ]
    assert res == {"nodes": 6, "edges": 5}


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op (never raises).
    assert ingest_entities([{"id": "a", "type": "Tag"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_metadata(client=_FakeClient()) is None
    assert ingest_documents_records([], client=_FakeClient()) is None
