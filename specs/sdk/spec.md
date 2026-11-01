# CONN-PAPERLESS-NGX-MCP-SDK — Shared SDK capabilities in paperless-ngx-mcp

**Owner:** paperless-ngx-mcp.

See [`requirements.md`](requirements.md) for each row and [`status.json`](status.json) for its generated state.

## Purpose

paperless-ngx-mcp must use the scion-sdk capability for each concern the SDK centralizes. A connector copy of a centralized capability splits policy across the fleet.

## Why a new spec

Search: `git grep -n "SDK" -- specs` found no row that owns SDK capability use in paperless-ngx-mcp. The SDK index spec `SCION-CENTRALIZED-CAPABILITIES` owns the capabilities. This spec owns the connector side of each one.

## Delivery mapping

Component: paperless-ngx-mcp connector

Code: ../../paperless_ngx_mcp/__init__.py

## User Scenarios & Testing

### User Story 1 - Requests use the governed SDK client (Priority: P1)

The fleet operator and the engine rely on this behaviour of `paperless-ngx-mcp`: paperless-ngx-mcp must send every vendor request through the SDK governed HTTP client with its TLS profile. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `paperless-ngx-mcp` connector built from the default branch, **When** `tests/test_api_client.py::test_client_is_governed_with_token_auth` runs, **Then** a unit test shows the API client holds a governed client with redirects off and token auth.

### User Story 2 - Retries come from the SDK retry policy (Priority: P1)

The fleet operator and the engine rely on this behaviour of `paperless-ngx-mcp`: paperless-ngx-mcp must delete its own backoff loop. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `paperless-ngx-mcp` connector built from the default branch, **When** `tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client` runs, **Then** a unit test sends 503 then 200 through a mock transport and sees one result.

### User Story 3 - SDK floor and dependency set (Priority: P1)

The fleet operator and the engine rely on this behaviour of `paperless-ngx-mcp`: The package must require scion-sdk 0.6.4 or later. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `paperless-ngx-mcp` connector built from the default branch, **When** `tests/test_api_client.py::test_dependencies_carry_sdk_floor_and_no_requests_pin` runs, **Then** pyproject.toml shows the floor and no requests pin.

### User Story 4 - Production wiring (Priority: P2)

The fleet operator and the engine rely on this behaviour of `paperless-ngx-mcp`: `ApiClientBase.__init__` in `paperless_ngx_mcp/api/api_client_base.py` calls `create_http_client`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `paperless-ngx-mcp` connector built from the default branch, **When** `tests/test_api_client.py::test_client_is_governed_with_token_auth` runs, **Then** a test enters at the production entry point and reaches the wired call site.

### User Story 5 - Hot-path proof (Priority: P2)

The fleet operator and the engine rely on this behaviour of `paperless-ngx-mcp`: A test builds `ApiClientDocuments` and calls a list operation. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `paperless-ngx-mcp` connector built from the default branch, **When** `tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client` runs, **Then** the named integration test passes.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Requests use the governed SDK client. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R001`.
- **FR-002**: Retries come from the SDK retry policy. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R002`.
- **FR-003**: SDK floor and dependency set. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R003`.
- **FR-004**: Production wiring. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R004`.
- **FR-005**: Hot-path proof. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R005`.

## Success Criteria

- **SC-001**: A unit test shows the API client holds a governed client with redirects off and token auth. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R001`.
- **SC-002**: A unit test sends 503 then 200 through a mock transport and sees one result. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R002`.
- **SC-003**: pyproject.toml shows the floor and no requests pin. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R003`.
- **SC-004**: A test enters at the production entry point and reaches the wired call site. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R004`.
- **SC-005**: The named integration test passes. Rows: `CONN-PAPERLESS-NGX-MCP-SDK-R005`.

## Assumptions

- The `paperless-ngx-mcp` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-PAPERLESS-NGX-MCP-SDK-R001` | plan.md Production caller chain | T-001 | tests/test_api_client.py::test_client_is_governed_with_token_auth |
| FR-002 | `CONN-PAPERLESS-NGX-MCP-SDK-R002` | plan.md Production caller chain | T-002 | tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client |
| FR-003 | `CONN-PAPERLESS-NGX-MCP-SDK-R003` | plan.md Production caller chain | T-003 | tests/test_api_client.py::test_dependencies_carry_sdk_floor_and_no_requests_pin |
| FR-004 | `CONN-PAPERLESS-NGX-MCP-SDK-R004` | plan.md Production caller chain | T-004 | tests/test_api_client.py::test_client_is_governed_with_token_auth |
| FR-005 | `CONN-PAPERLESS-NGX-MCP-SDK-R005` | plan.md Production caller chain | T-005 | tests/test_api_client.py::test_transient_status_is_retried_by_the_sdk_client |
