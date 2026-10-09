import json
from types import SimpleNamespace

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from paperless_ngx_mcp.kg_ingest import ingest_projection, project_records

KEY = b"k" * 32


class _FakeTransport:
    def __init__(self):
        self.requests = []

    async def source_status(self, connector, stream):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data):
        raise AssertionError("this connector's structural ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _projection(key: bytes = KEY):
    return project_records(
        [
            {
                "id": 42,
                "title": "sensitive title",
                "content": "sensitive OCR content",
                "original_file_name": "sensitive-name.pdf",
                "correspondent": 2,
                "document_type": 3,
                "storage_path": 7,
                "tags": [1, 5],
            }
        ],
        correspondents=[{"id": 2, "name": "sensitive identity"}],
        tags=[{"id": 1, "name": "sensitive label"}],
        document_types=[{"id": 3, "name": "sensitive category"}],
        storage_paths=[{"id": 7, "path": "sensitive location"}],
        pseudonymization_key=key,
    )


def test_projection_is_keyed_structural_and_zero_pii():
    projection = _projection()
    assert len(projection["records"]) == 6
    assert len(projection["relationships"]) == 5
    assert all(set(node) == {"id", "node_type"} for node in projection["records"])
    rendered = json.dumps(projection, sort_keys=True)
    for forbidden in (
        "sensitive",
        "pdf",
        "OCR",
    ):
        assert forbidden not in rendered


def test_projection_is_stable_per_key_and_domain_separated():
    first = _projection()
    assert first == _projection()
    assert first != _projection(b"z" * 32)
    node_ids = [node["id"] for node in first["records"]]
    assert len(node_ids) == len(set(node_ids))


def test_projection_rejects_missing_identifier_and_malformed_tags():
    with pytest.raises(ValueError, match="no identifier"):
        project_records([{}], pseudonymization_key=KEY)
    with pytest.raises(ValueError, match="tags are malformed"):
        project_records([{"id": 1, "tags": "not-a-list"}], pseudonymization_key=KEY)


def test_projection_requires_deployment_key(monkeypatch):
    monkeypatch.delenv("PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY", raising=False)
    with pytest.raises(RuntimeError, match="pseudonymization key"):
        project_records([{"id": 1}])


async def test_ingest_projection_uses_only_governed_native_boundary(ingest):
    service, transport = ingest
    projection = _projection()
    result = await ingest_projection(projection, ingest=service)
    assert result == {"nodes": 6, "edges": 5}
    request = transport.requests[0]
    assert {record.record_id for record in request.records} == {
        node["id"] for node in projection["records"]
    }


async def test_ingest_projection_rejects_unprojected_content_and_invalid_edges(ingest):
    service, transport = ingest
    projection = _projection()
    projection["records"][0]["title"] = "must not persist"
    with pytest.raises(ValueError, match="invalid node"):
        await ingest_projection(projection, ingest=service)
    assert transport.requests == []

    projection = _projection()
    projection["relationships"][0]["target"] = "paperless:unknown:record"
    with pytest.raises(ValueError, match="invalid relationship"):
        await ingest_projection(projection, ingest=service)
    assert transport.requests == []


async def test_empty_projection_is_an_explicit_zero_write(ingest):
    service, transport = ingest
    assert await ingest_projection(
        {"records": [], "relationships": []}, ingest=service
    ) == {
        "nodes": 0,
        "edges": 0,
    }
    assert transport.requests == []
