# MCP tooling workflow

You are adding or updating MCP-related tooling for defensive security automation. Follow `CLAUDE.md`.

## Required steps

1. Restate the MCP goal.
2. Classify each tool:
   - Local-only.
   - Passive network.
   - Active authorized-scope.
   - Reporting-only.
3. Identify required environment variables.
4. Keep secrets out of JSON, code, docs, and tests.
5. Add or update templates under `mcp/`.
6. Document setup and safety assumptions.
7. Add tests for any code changes.
8. Run validation commands from `CLAUDE.md`.

## Constraints

- Ask before enabling active network-touching tools.
- Prefer dry-run and read-only defaults.
- Avoid broad filesystem mounts or privileged execution.
- Do not hardcode local absolute paths unless clearly marked as examples.

