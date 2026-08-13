# Paperless-ngx MCP

*Version: 2.0.0*

`paperless-ngx-mcp` provides a typed Python client, current intent/condensed/verbose MCP
surfaces, an optional A2A agent, and a governed epistemic-graph connector for the standard
Paperless-ngx API.

The package is deployment-neutral. It contains no instance profile, connection value,
credential, certificate, user record, customized taxonomy, or durable source content.

## Capabilities

- Manage documents, notes, correspondents, tags, document types, storage paths, custom
  fields, and saved views.
- Search, inspect tasks and statistics, acknowledge tasks, and inspect the provider
  schema and status.
- Upload only approved files inside the AgentConfig workspace boundary.
- Authenticate with a fixed service token projected by the MCP fleet secret resolver or
  with request-scoped RFC 8693 delegation.
- Apply system trust, private CA bundles, mTLS, and proxy policy through a shared
  mandatory-verification TLS profile.
- Project keyed, content-free document topology for governed ChangeEnvelope ingestion.
- Contribute one comprehensive `paperless-ngx-operations` skill and data-only ontology,
  source-preset, and prompt providers.

## MCP tools

Condensed tools accept `action` plus a JSON-object string in `params_json`. Verbose mode
exposes the same public client methods one-to-one. The generated table is derived from
the live server surface.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `document_operations` | `DOCUMENTSTOOL` | Manage Paperless-ngx documents, correspondents, tags, document types, |
| `paperless_ingest_projection` | `KGTOOL` | Commit the keyed structural projection through governed ChangeEnvelope. |
| `paperless_ingestion_projection` | `KGTOOL` | Return keyed opaque nodes and relationships for governed source sync. |
| `system_operations` | `SYSTEMTOOL` | Run Paperless-ngx full-text search, inspect background/consumption tasks, |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>36 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `paperless_ngx_acknowledge_tasks` | `GRANULARTOOL` | Acknowledge (dismiss) tasks (``POST /api/acknowledge_tasks/``). |
| `paperless_ngx_add_document_note` | `DOCUMENTSTOOL` | Add a note to a document. |
| `paperless_ngx_autocomplete` | `GRANULARTOOL` | Search-term autocomplete (``GET /api/search/autocomplete/``). |
| `paperless_ngx_bulk_edit_documents` | `DOCUMENTSTOOL` | Run a bulk edit (``set_correspondent``, ``add_tag``, ``delete``, …) over |
| `paperless_ngx_create_correspondent` | `DOCUMENTSTOOL` | Create a correspondent. |
| `paperless_ngx_create_custom_field` | `DOCUMENTSTOOL` | Create a custom field. |
| `paperless_ngx_create_document` | `DOCUMENTSTOOL` | Create a document record (``POST /api/documents/``). |
| `paperless_ngx_create_document_type` | `DOCUMENTSTOOL` | Create a document type. |
| `paperless_ngx_create_storage_path` | `DOCUMENTSTOOL` | Create a storage path. |
| `paperless_ngx_create_tag` | `DOCUMENTSTOOL` | Create a tag. |
| `paperless_ngx_delete_correspondent` | `DOCUMENTSTOOL` | Delete a correspondent. |
| `paperless_ngx_delete_document` | `DOCUMENTSTOOL` | Move a document to the trash. |
| `paperless_ngx_delete_document_type` | `DOCUMENTSTOOL` | Delete a document type. |
| `paperless_ngx_delete_tag` | `DOCUMENTSTOOL` | Delete a tag. |
| `paperless_ngx_get_document` | `DOCUMENTSTOOL` | Retrieve a single document's metadata. |
| `paperless_ngx_get_document_metadata` | `DOCUMENTSTOOL` | Retrieve raw parsed metadata (EXIF, media filename, archive checksum…). |
| `paperless_ngx_get_document_notes` | `DOCUMENTSTOOL` | List the notes attached to a document. |
| `paperless_ngx_get_remote_version` | `GRANULARTOOL` | Latest available Paperless-ngx version (``GET /api/remote_version/``). |
| `paperless_ngx_get_schema` | `GRANULARTOOL` | Retrieve the live OpenAPI schema (``GET /api/schema/``, drf-spectacular). |
| `paperless_ngx_get_statistics` | `GRANULARTOOL` | Document/inbox statistics (``GET /api/statistics/``). |
| `paperless_ngx_get_system_status` | `GRANULARTOOL` | Backend/service health & version info (``GET /api/status/``). |
| `paperless_ngx_get_task` | `GRANULARTOOL` | Retrieve a single task by id (``GET /api/tasks/?task_id=...``). |
| `paperless_ngx_get_ui_settings` | `GRANULARTOOL` | Current user's UI settings and permissions (``GET /api/ui_settings/``). |
| `paperless_ngx_global_search` | `GRANULARTOOL` | Run a global search across documents, correspondents, tags, etc. |
| `paperless_ngx_list_correspondents` | `DOCUMENTSTOOL` | List correspondents. |
| `paperless_ngx_list_custom_fields` | `DOCUMENTSTOOL` | List custom fields. |
| `paperless_ngx_list_document_types` | `DOCUMENTSTOOL` | List document types. |
| `paperless_ngx_list_documents` | `DOCUMENTSTOOL` | List/search documents. ``query`` is full-text search; ``filters`` accepts |
| `paperless_ngx_list_saved_views` | `DOCUMENTSTOOL` | List saved views. |
| `paperless_ngx_list_storage_paths` | `DOCUMENTSTOOL` | List storage paths. |
| `paperless_ngx_list_tags` | `DOCUMENTSTOOL` | List tags. |
| `paperless_ngx_list_tasks` | `GRANULARTOOL` | List background/consumption tasks (``GET /api/tasks/``). |
| `paperless_ngx_post_document` | `DOCUMENTSTOOL` | Upload a new document for consumption via ``POST /api/documents/post_document/``. |
| `paperless_ngx_update_correspondent` | `DOCUMENTSTOOL` | Update a correspondent (PATCH). |
| `paperless_ngx_update_document` | `DOCUMENTSTOOL` | Partially update a document (PATCH) — title, tags, correspondent, etc. |
| `paperless_ngx_update_tag` | `DOCUMENTSTOOL` | Update a tag (PATCH). |

</details>

_4 action-routed tool(s) · 36 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Install

```bash
uvx --from "paperless-ngx-mcp[mcp]" paperless-ngx-mcp
```

Use the `[agent]` extra only when running the A2A agent entry point. Agent Utilities
supplies the full Epistemic Graph runtime on the current dependency line.

## AgentConfig boundary

The checked-in MCP catalog contains references only:

```json
{
  "mcpServers": {
    "paperless-ngx-mcp": {
      "command": "uvx",
      "args": ["--from", "paperless-ngx-mcp[mcp]", "paperless-ngx-mcp"],
      "env": {
        "PAPERLESS_URL": "env://PAPERLESS_URL",
        "PAPERLESS_TOKEN": "env://PAPERLESS_TOKEN",
        "PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY": "env://PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY",
        "TLS_PROFILE": "env://TLS_PROFILE",
        "TLS_PROFILES_REF": "env://TLS_PROFILES_REF",
        "WORKSPACE_PATH": "env://WORKSPACE_PATH",
        "MCP_TOOL_MODE": "intent",
        "LANGFUSE_CAPTURE_CONTENT": "false"
      }
    }
  }
}
```

GraphOS reads this catalog through `AgentConfig.MCP_CONFIG`. Map the runtime aliases to
approved `env://`, `vault://`, or `secret://` runtime sources with
`AgentConfig.MCP_FLEET_SECRET_REFS`. The connector has no packaged URL or credential
default and requires HTTPS.

TLS is resolved by `resolve_configured_tls_profile("paperless")`. Select system trust or
a runtime profile with `TLS_PROFILE` / `TLS_PROFILES_REF`; do not add a verification
boolean or commit trust material.

Validate the reference boundary without displaying resolved values:

```bash
agent-utilities-doctor --only config transport_security mcp_fleet_secrets mcp_fleet
```

## Privacy-preserving graph synchronization

`paperless_ingestion_projection` transforms provider records in memory into keyed opaque
references and structural relationships. `paperless_ingest_projection` commits that
same projection through Agent Utilities' governed ChangeEnvelope path.

The durable projection excludes OCR text, titles, notes, names, filenames, storage
locations, timestamps, URLs, raw bytes, and provider identifiers. It requires a
deployment-owned pseudonymization key of at least 32 bytes. Activation remains blocked
until the central capability compiler produces and validates the reviewed signed bundle;
this repository intentionally does not manufacture signed release artifacts.

## Documentation

- [Configuration](docs/configuration.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Architecture](docs/overview.md)
- [Concepts](docs/concepts.md)

## Security

- No arbitrary REST escape hatch or password-to-token action is exposed.
- Pagination is same-origin and bounded; redirects do not carry provider credentials.
- HTTP errors omit response bodies, connection values, parameters, and record content.
- Tool handlers do not echo malformed JSON or provider exception text.
- Uploads are constrained to a configured workspace root and a fixed size ceiling.
- Telemetry examples default to content capture disabled.

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `PAPERLESS_URL` | — | HTTPS provider URL projected at runtime |
| `PAPERLESS_TOKEN` | — | Runtime secret projection; never commit a token |
| `PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY` | — | Deployment-owned secret, at least 32 bytes |
| `TLS_PROFILE` | — | Shared mandatory-verification transport profile selector |
| `TLS_PROFILES_REF` | — | Runtime reference to the shared transport profile catalog |
| `WORKSPACE_PATH` | — | AgentConfig upload boundary; never commit a local path |
| `MCP_TOOL_MODE` | `intent` | Current intent-first tool surface |
| `DOCUMENTSTOOL` | `True` | Enable document operations |
| `SYSTEMTOOL` | `True` | Enable system operations |
| `KGTOOL` | `True` | Enable privacy-preserving governed projection tools |
| `TRANSPORT` | `stdio` | Local MCP transport |
| `HOST` | `127.0.0.1` | Loopback bind for HTTP transports |
| `PORT` | `8000` | Bind port for HTTP transports |
| `ENABLE_OTEL` | `False` | Enable trace export only after configuring an approved collector |
| `LANGFUSE_CAPTURE_CONTENT` | `False` | Never capture provider record content |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_TYPE` | `none` | Authorization mode: `none` \| `embedded` \| `remote` |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` | Embedded Eunomia policy file |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_15 package + 19 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->

Licensed under the MIT License.


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `paperless-ngx-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "paperless-ngx-mcp[mcp]"`, then run `paperless-ngx-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `paperless-ngx-mcp` |
| Immutable container | deploy `registry.example.invalid/paperless-ngx-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
