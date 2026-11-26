---
name: paperless-ngx-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the paperless-ngx-mcp connector. Use this
  skill when changing the connector's API mappings, MCP tools, packaging,
  documentation, or repository gates.
license: MIT
tags: [paperless-ngx-mcp, development, connector, test, gates]
tier: repository
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# paperless-ngx-mcp development

This repository owns the Paperless-ngx transport, mappings, MCP tools, and
agent entry points. Shared connector contracts and transports belong to
`scion-sdk`; admission, serving, and durable graph state belong to
their owning repositories. Read `AGENTS.md` before changing code and keep
provider credentials and endpoints out of source, logs, and skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend
  that spec before adding new requirement text.
- Reuse existing SDK clients, transport policies, and tool factories. Do not
  create a second implementation of a connector capability.
- Keep changes scoped to this connector. A change owned by the SDK, Arbora,
  or the knowledge graph belongs in that repository instead.
- Every delivered requirement needs a bound test. Generated `status.json`
  files are produced by `pipelines-hook spec-status`; never hand-edit them.
- One logical change per commit, with `Spec: <ID>` and the assisting agent
  trailer adjacent in the final paragraph.

## Steps

1. Find the owning spec row with `git grep -n "<term>" -- specs`.
   Verify a row matches before editing code, and extend it rather than adding new requirement text.
2. Make the change in `paperless_ngx_mcp/` reusing the existing SDK clients and tool factories.
   Verify no second implementation of a connector capability was added.
3. Bind the change to a test and run `uv run pytest -q`.
   Verify the focused test passes.
4. Run the shared gates with `pre-commit run --all-files`.
   Verify every hook reports Passed.
5. Stage reviewed paths with `git add -- <path>` and check `git diff --cached --name-status`.
   Verify only intended files are listed, then commit with `Spec:` and the agent trailer adjacent.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| A hook fails | Formatting, spelling or a repository gate was violated | Read the hook output, fix the named file, and rerun `pre-commit run --all-files` |
| `status.json` shows as modified | A generated file was hand-edited | Restore it with `git checkout -- <path>` for that file, and let `pipelines-hook spec-status` regenerate it |
| No spec row matches the change | The behavior is not yet specified | Extend the closest row in `specs` first, and cite its id in the `Spec:` trailer |
