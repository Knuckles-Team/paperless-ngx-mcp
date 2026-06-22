import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client

_ACTIONS = {
    "global_search",
    "autocomplete",
    "list_tasks",
    "get_task",
    "acknowledge_tasks",
    "get_statistics",
    "get_system_status",
    "get_remote_version",
    "get_ui_settings",
}


def register_system_tools(mcp: FastMCP):
    """Register the search/task/system dynamic tool."""

    @mcp.tool(tags={"system"})
    async def system_operations(
        action: str = Field(
            description=(
                "Search, task and system action for Paperless-ngx. One of: "
                + ", ".join(sorted(_ACTIONS))
                + "."
            )
        ),
        params_json: str = Field(
            default="{}",
            description=(
                "JSON object of keyword arguments, e.g. "
                '{"query": "tax 2024"} for global_search, '
                '{"task_id": "abc-123"} for get_task.'
            ),
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Run Paperless-ngx full-text search, inspect background/consumption tasks,
        and read statistics & system status. CONCEPT:PNGX-002"""
        if ctx:
            await ctx.info(f"system_operations: {action}")

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
