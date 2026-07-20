# Deployment

## GraphOS-managed child

Register the checked-in reference-only catalog with `AgentConfig.MCP_CONFIG`. Map its
aliases through `AgentConfig.MCP_FLEET_SECRET_REFS`, select the TLS profile, and run the
doctor gate before GraphOS launches the child. This keeps connection values and trust
material outside the source tree and process arguments.

Use stdio for a GraphOS-owned local child. For a network transport, apply the Agent
Utilities authentication, authorization, TLS, and egress controls and expose only the
MCP route required by the client.

## Containers

The Dockerfile supplies separate `mcp` and `agent` targets. Compose examples consume an
external runtime environment and default telemetry content capture off. Build and image
publication are deployment responsibilities; the source package does not encode a
registry account or provider instance.

## A2A agent

The `paperless-ngx-agent` entry point uses the current Agent Utilities parser and server
factory. Supply the MCP catalog through AgentConfig and use secret references for model,
OIDC, telemetry, and provider credentials. Do not place resolved values on a command
line.

## Release activation

Provider installation is not graph-ingestion authorization. Enable the source preset
only after the central compiler has generated and verified the current signed capability
bundle and the deployment has supplied tenant, policy, and pseudonymization state.
