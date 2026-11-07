# CONN-PAPERLESS-NGX-MCP-SDK — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `paperless-ngx-mcp` delivers the rows of `CONN-PAPERLESS-NGX-MCP-SDK`. The live caller is the `paperless-ngx-mcp` console script. The owner is the `paperless_ngx_mcp` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 5 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `paperless_ngx_mcp/mcp_server.py` (existing)
- `paperless_ngx_mcp/api/api_client_documents.py` (existing)
- `paperless_ngx_mcp/api/api_client_base.py` (existing)
- `tests/test_api_client.py` (existing)
- `pyproject.toml` (existing)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

### Summary

This plan states how `paperless-ngx-mcp` delivers the rows of `CONN-PAPERLESS-NGX-MCP-SDK`. The live caller is the `paperless-ngx-mcp` console script. The owner is the `paperless_ngx_mcp` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 5 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `paperless_ngx_mcp/mcp_server.py` (existing)
- `paperless_ngx_mcp/api/api_client_documents.py` (existing)
- `paperless_ngx_mcp/api/api_client_base.py` (existing)
- `tests/test_api_client.py` (existing)
- `pyproject.toml` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `paperless-ngx-mcp` delivers the rows of `CONN-PAPERLESS-NGX-MCP-SDK`. The live caller is the `paperless-ngx-mcp` console script. The owner is the `paperless_ngx_mcp` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 5 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `paperless_ngx_mcp/mcp_server.py` (existing)
- `paperless_ngx_mcp/api/api_client_documents.py` (existing)
- `paperless_ngx_mcp/api/api_client_base.py` (existing)
- `tests/test_api_client.py` (existing)
- `pyproject.toml` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `paperless-ngx-mcp` delivers the rows of `CONN-PAPERLESS-NGX-MCP-SDK`. The live caller is the `paperless-ngx-mcp` console script. The owner is the `paperless_ngx_mcp` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 5 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `paperless_ngx_mcp/mcp_server.py` (existing)
- `paperless_ngx_mcp/api/api_client_documents.py` (existing)
- `paperless_ngx_mcp/api/api_client_base.py` (existing)
- `tests/test_api_client.py` (existing)
- `pyproject.toml` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `paperless-ngx-mcp` delivers the rows of `CONN-PAPERLESS-NGX-MCP-SDK`. The live caller is the `paperless-ngx-mcp` console script. The owner is the `paperless_ngx_mcp` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 5 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `paperless_ngx_mcp/api/api_client_base.py` (existing)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Existing system and reuse

The SDK owns every capability named in the rows. paperless-ngx-mcp adds no module that repeats one. Each row deletes connector code and calls the SDK module.

### Live call path

`ApiClientBase.__init__` in `paperless_ngx_mcp/api/api_client_base.py` calls `create_http_client`. Every domain client and MCP tool calls `ApiClientBase.request`

### Compatibility

Tool names, arguments, and results stay identical. The SDK floor is `scion-sdk>=0.3.11`.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain


### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-PAPERLESS-NGX-MCP-SDK-R001`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R002`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R003`: the installer and the `dependency-readiness` pre-commit gate read `[project] dependencies` in `pyproject.toml`.
- `CONN-PAPERLESS-NGX-MCP-SDK-R004`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R005`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-PAPERLESS-NGX-MCP-SDK-R001`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R002`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R003`: the installer and the `dependency-readiness` pre-commit gate read `[project] dependencies` in `pyproject.toml`.
- `CONN-PAPERLESS-NGX-MCP-SDK-R004`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R005`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-PAPERLESS-NGX-MCP-SDK-R001`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R002`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R003`: the installer and the `dependency-readiness` pre-commit gate read `[project] dependencies` in `pyproject.toml`.
- `CONN-PAPERLESS-NGX-MCP-SDK-R004`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R005`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Adoption of scion-sdk 0.10.0 (CONN-PAPERLESS-NGX-MCP-SDK-R006)

- Owner. This repository, the import lines named in `CONN-PAPERLESS-NGX-MCP-SDK-R006`. The paths belong to scion-sdk.
- Cohesion. The import edits, the pin and the lock change together and sit in one change.
- Dependency direction. The connector imports public modules of the SDK units; no import points to a private module.
- Interface depth. The connector uses the public surface only.
- Special cases. None. Every removed path takes the same replacement, with no alias.
- State. None.
- Environment. None. The pin is package metadata, not environment code.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-PAPERLESS-NGX-MCP-SDK-R001`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R002`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R003`: the installer and the `dependency-readiness` pre-commit gate read `[project] dependencies` in `pyproject.toml`.
- `CONN-PAPERLESS-NGX-MCP-SDK-R004`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).
- `CONN-PAPERLESS-NGX-MCP-SDK-R005`: an MCP tool of `paperless_ngx_mcp/mcp_server.py` calls a domain client such as `ApiClientDocuments` (`paperless_ngx_mcp/api/api_client_documents.py`), which calls `ApiClientBase.request` (`paperless_ngx_mcp/api/api_client_base.py:150`); the session was built by `create_http_client` (`paperless_ngx_mcp/api/api_client_base.py:73`).

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.
