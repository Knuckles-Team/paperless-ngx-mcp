# Configuration, trust, and privacy

## Configuration boundary

The connector reads deployment values only after the shared AgentConfig/XDG loader has
projected them. Its checked-in `mcp_config.json` uses `env://` aliases; GraphOS resolves
those aliases from `MCP_FLEET_SECRET_REFS` at the child-process boundary.

| Reference | Purpose | Durable package value |
| --- | --- | --- |
| `PAPERLESS_URL` | HTTPS base for the selected provider instance | None |
| `PAPERLESS_TOKEN` | Fixed service token when delegation is disabled | None |
| `PAPERLESS_INGESTION_PSEUDONYMIZATION_KEY` | Key for opaque graph identifiers | None |
| `TLS_PROFILE` | Shared transport profile selector | None |
| `TLS_PROFILES_REF` | Runtime trust-profile catalog reference | None |
| `WORKSPACE_PATH` | AgentConfig upload boundary | None |

Map runtime references to approved `env://`, `vault://`, or `secret://` sources in AgentConfig.
Do not replace the checked-in references with resolved values. The pseudonymization key
must be deployment-owned, at least 32 bytes, scoped to the intended correlation domain,
and rotated under a migration policy.

`MCP_TOOL_MODE` selects `intent` (default), `condensed`, `verbose`, or `both`.
`DOCUMENTSTOOL`, `SYSTEMTOOL`, and `KGTOOL` may disable their corresponding domains, but
enabling a domain never grants provider permissions by itself.

## Authentication

With OIDC delegation enabled, the request-scoped user token is exchanged through the
shared RFC 8693 implementation and the resulting provider client is not cached. Without
delegation, the projected fixed token is required. No MCP action accepts a username and
password or returns a newly minted credential.

Logs expose only the authentication mode and bounded exception class. They never emit a
token, subject, identity, connection value, provider error body, or record value.

## TLS trust

Peer and hostname verification are mandatory. The client uses
`resolve_configured_tls_profile("paperless")`; no boolean verification option exists.
System trust works without a profile. A deployment that uses private trust, mTLS, or an
outbound proxy selects a runtime profile through `TLS_PROFILE` or `TLS_PROFILES_REF`.
Certificate material and filesystem locations stay in the runtime trust boundary.

## Graph governance

The connector contributes a data-only source preset and a provider-native zero-PII
ontology. Release tooling derives and commits its exact local schema fingerprint,
signed manifest, SHACL shapes, neutral mapping and fixture, migration ledger, and
offline source attestation. Those artifacts contain no deployment records, mapping
customizations, source content, or external-live claim.

Before activation, require a verified tenant, ACL, classification, retention, legal-hold
policy, pseudonymization key, current tool-schema fingerprint, and signed capability
bundle. Missing state fails closed.

## Observability

Keep `LANGFUSE_CAPTURE_CONTENT=false`. Trace only opaque run/tenant/actor references,
action names, status, counts, timing, and bounded error classes. Provider inputs and
outputs, document content, filenames, local locations, and resolved configuration are
not trace attributes.

## Doctor

Validate configuration without printing resolved values:

```bash
agent-utilities-doctor --only config transport_security mcp_fleet_secrets mcp_fleet
```

Use live doctor checks only when bounded access to the configured provider and telemetry
services is explicitly authorized.
