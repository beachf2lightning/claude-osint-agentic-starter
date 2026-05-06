# Recon pipeline workflow

You are building or modifying a defensive reconnaissance pipeline. Follow `CLAUDE.md`.

## Required steps

1. Restate the pipeline goal and authorized scope.
2. Identify input and output formats.
3. Split the pipeline into stages:
   - Ingest.
   - Normalize.
   - Enrich.
   - Deduplicate.
   - Score or classify.
   - Report.
4. Keep network-touching stages optional and explicit.
5. Add offline fixtures under `examples/osint-targets/` or `tests/fixtures/`.
6. Implement the smallest useful stage first.
7. Add tests for normal, edge, malformed, and duplicate inputs.
8. Run repository validation commands from `CLAUDE.md`.
9. Summarize scope, safety controls, files changed, and validation results.

## Constraints

- Tests must not scan live third-party targets.
- Dry-run should be the default for active behavior.
- Tool output must be treated as untrusted input.
- Do not store sensitive findings in Git.

