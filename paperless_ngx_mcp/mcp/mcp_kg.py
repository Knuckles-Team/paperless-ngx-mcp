"""Wire-First native KG-ingestion tool for Paperless-ngx (CONCEPT:AU-KG.ingest.enterprise-source-extractor).

Lists documents (+ the correspondents/tags/document-types/storage-paths that organize
them) via the real client and pushes them into the epistemic-graph as typed OWL nodes —
``:Document`` (with OCR text), ``:Correspondent`` / ``:Tag`` / ``:DocumentType`` /
``:StoragePath`` — plus their links. Optionally downloads each document's scanned
PDF/image and stores it as a durable ``:Blob`` / ``:MediaAsset``. Best-effort: no-ops
(``"ingested": None``) when no engine is reachable.
"""

import json

from agent_utilities.mcp_utilities import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_kg_tools(mcp: FastMCP):
    """Register the native paperless→KG ingestion tool."""

    @mcp.tool(tags={"misc", "kg"})
    async def paperless_ingest_documents(
        params_json: str = Field(
            default="{}",
            description=(
                "JSON string of options: list_documents filters (e.g. "
                '{"query": "invoice", "max_pages": 1}), plus optional '
                '"include_files": true to also ingest each scanned PDF as a blob, and '
                '"max_files": N to cap blob downloads (default 25).'
            ),
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Natively ingest Paperless-ngx documents + metadata into epistemic-graph.

        Maps documents → :Document (OCR text) with :fromCorrespondent / :hasTag /
        :hasDocumentType / :storedAt links, and (when ``include_files``) the scanned
        bytes → :Blob/:MediaAsset via :scannedAs. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from ..kg_ingest import (
            ingest_documents_records,
            ingest_metadata,
        )
        from ..kg_media import ingest_document_blob

        try:
            opts = json.loads(params_json or "{}")
        except Exception as e:  # noqa: BLE001
            return {"error": f"Invalid params_json: {e}"}
        if not isinstance(opts, dict):
            return {"error": "params_json must be a JSON object"}

        include_files = bool(opts.pop("include_files", False))
        max_files = int(opts.pop("max_files", 25) or 25)
        opts.pop("max_files", None)

        base_url = getattr(client, "base_url", "")

        if ctx:
            await ctx.info("paperless_ingest_documents: listing documents + metadata")

        # Metadata first so the referenced nodes carry names.
        correspondents = await run_blocking(client.list_correspondents)
        tags = await run_blocking(client.list_tags)
        document_types = await run_blocking(client.list_document_types)
        storage_paths = await run_blocking(client.list_storage_paths)
        ingest_metadata(
            correspondents=correspondents,
            tags=tags,
            document_types=document_types,
            storage_paths=storage_paths,
        )

        documents = await run_blocking(client.list_documents, **opts)
        if not isinstance(documents, list):
            documents = [documents] if documents else []

        doc_result = ingest_documents_records(documents, base_url=base_url)

        files_ingested = 0
        if include_files:
            for rec in documents[:max_files]:
                did = rec.get("id")
                if did is None:
                    continue
                try:
                    data = await run_blocking(client.download_document, did)
                except Exception:  # noqa: BLE001 — a single scan failing is non-fatal
                    continue
                res = ingest_document_blob(
                    did,
                    data,
                    info=rec,
                    source_uri=f"{base_url.rstrip('/')}/documents/{did}/"
                    if base_url
                    else "",
                )
                if res is not None:
                    files_ingested += 1

        return {
            "listed_documents": len(documents),
            "listed_correspondents": len(correspondents)
            if isinstance(correspondents, list)
            else 0,
            "listed_tags": len(tags) if isinstance(tags, list) else 0,
            "ingested": doc_result,
            "files_ingested": files_ingested if include_files else None,
        }

    return None
