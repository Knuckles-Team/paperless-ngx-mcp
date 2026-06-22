import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client

_ACTIONS = {
    "list_documents",
    "create_document",
    "get_document",
    "get_document_metadata",
    "update_document",
    "delete_document",
    "get_document_notes",
    "add_document_note",
    "post_document",
    "bulk_edit_documents",
    "list_correspondents",
    "create_correspondent",
    "update_correspondent",
    "delete_correspondent",
    "list_tags",
    "create_tag",
    "update_tag",
    "delete_tag",
    "list_document_types",
    "create_document_type",
    "delete_document_type",
    "list_storage_paths",
    "create_storage_path",
    "list_custom_fields",
    "create_custom_field",
    "list_saved_views",
}


def register_documents_tools(mcp: FastMCP):
    """Register the document-management dynamic tool (Paperless-ngx resources)."""

    @mcp.tool(tags={"documents"})
    async def document_operations(
        action: str = Field(
            description=(
                "Action to perform on Paperless-ngx documents and metadata. One of: "
                + ", ".join(sorted(_ACTIONS))
                + "."
            )
        ),
        params_json: str = Field(
            default="{}",
            description=(
                "JSON object of keyword arguments for the action, e.g. "
                '{"query": "invoice", "tags__id__in": "3,4"} for list_documents, or '
                '{"document_id": 12, "body": {"title": "New title"}} for update_document.'
            ),
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage Paperless-ngx documents, correspondents, tags, document types,
        storage paths, custom fields and saved views. CONCEPT:PNGX-001"""
        if ctx:
            await ctx.info(f"document_operations: {action}")

        try:
            kwargs = json.loads(params_json or "{}")
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, _ACTIONS, service="paperless-ngx-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        method = getattr(client, action, None)
        if method is None:
            return {"error": f"Unsupported action: {action}"}
        result = await run_blocking(method, **kwargs)
        return {"action": action, "result": result}
