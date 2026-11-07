# CONN-PAPERLESS-NGX-MCP-SDK — Implementation tasks

Governing spec: [spec.md](spec.md). Design: [plan.md](plan.md). Rows: [requirements.md](requirements.md).

Each task line reads `- [ ] T001 [P] [US1] <ID>-R012.4 description`. Tasks run producer first; a checked task has landed.

- [x] T001 [US1] CONN-PAPERLESS-NGX-MCP-SDK-R001 Requests use the governed SDK client.
- [x] T002 [US2] CONN-PAPERLESS-NGX-MCP-SDK-R002 Retries come from the SDK retry policy.
- [x] T003 [US3] CONN-PAPERLESS-NGX-MCP-SDK-R003 SDK floor and dependency set.
- [x] T004 [US4] CONN-PAPERLESS-NGX-MCP-SDK-R004 Production wiring.
- [x] T005 [US5] CONN-PAPERLESS-NGX-MCP-SDK-R005 Hot-path proof.
- [ ] T006 [US1] CONN-PAPERLESS-NGX-MCP-SDK-R006 Adopt scion-sdk 0.10.0 import paths. Size: S, 1 PR, 30 minutes.
