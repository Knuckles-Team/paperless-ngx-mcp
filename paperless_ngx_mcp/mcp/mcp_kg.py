"""Privacy-preserving Paperless-ngx projection and governed ingestion tools."""

from __future__ import annotations

import json
from typing import Any

from agent_utilities.mcp.concurrency import invoke_client_method
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ..kg_ingest import ingest_projection, project_records


def _options(params_json: str) -> dict[str, Any]:
    try:
        value = json.loads(params_json or "{}")
    except (TypeError, ValueError):
        raise ValueError("params_json is not valid JSON") from None
    if not isinstance(value, dict):
        raise ValueError("params_json must be a JSON object")
    return {key: item for key, item in value.items() if item is not None}


async def _projection(client: Any, options: dict[str, Any]) -> dict[str, Any]:
    correspondents = await invoke_client_method(client.list_correspondents)
    tags = await invoke_client_method(client.list_tags)
    document_types = await invoke_client_method(client.list_document_types)
    storage_paths = await invoke_client_method(client.list_storage_paths)
    documents = await invoke_client_method(client.list_documents, **options)
    return project_records(
        documents,
        correspondents=correspondents,
        tags=tags,
        document_types=document_types,
        storage_paths=storage_paths,
    )


def register_kg_tools(mcp: FastMCP) -> None:
    """Register zero-PII source projection and ChangeEnvelope ingestion."""

    @mcp.tool(tags={"kg"})
    async def paperless_ingestion_projection(
        params_json: str = Field(
            default="{}",
            description="Bounded list_documents filters encoded as a JSON object.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """Return keyed opaque nodes and relationships for governed source sync."""

        if ctx:
            await ctx.info("Preparing Paperless-ngx structural projection")
        return await _projection(client, _options(params_json))

    @mcp.tool(tags={"kg"})
    async def paperless_ingest_projection(
        params_json: str = Field(
            default="{}",
            description="Bounded list_documents filters encoded as a JSON object.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """Commit the keyed structural projection through governed ChangeEnvelope."""

        if ctx:
            await ctx.info("Ingesting Paperless-ngx structural projection")
        projection = await _projection(client, _options(params_json))
        return {"ingested": ingest_projection(projection)}
