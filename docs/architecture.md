# Architecture notes

Use this file to give Claude durable context about the system.

## Current architecture

- `agentic_starter.cli` parses command-line arguments.
- `agentic_starter.normalizer` contains the core example behavior.
- `agentic_starter.targets` normalizes authorized scope entries without live lookups.
- `docker/` contains an optional non-privileged runtime scaffold.
- `mcp/` contains local MCP configuration templates.
- `examples/osint-targets/` contains safe target fixtures.

## Design principles

- Keep core logic independent from I/O.
- Test behavior through public functions.
- Prefer small modules with explicit responsibilities.
- Keep recon logic scoped, dry-run-friendly, and offline-testable.
- Separate passive enrichment, active checks, parsing, and reporting stages.
- Treat all tool output as untrusted input.

## Add your project context

Replace this section with:

- System boundaries.
- Data flow.
- External integrations.
- Security-sensitive areas.
- Performance-sensitive paths.
- Known trade-offs.
- Authorized target scope rules.
- Which tools are passive, active, local-only, or reporting-only.
