# Security agent prompt examples

## Safe bug fix

```text
Read CLAUDE.md and use /bug-fix.

Bug: The target normalizer treats duplicate hostnames with different case as separate entries.
Expected: Hostnames should deduplicate case-insensitively.
Reproduction: Add a fixture test with Example.com and example.com.
Constraints: Do not perform network lookups.
Verification: ./scripts/check.sh
```

## Passive enrichment design

```text
Read CLAUDE.md and use /osint-scope.

Objective: Design a passive enrichment interface for owned domains.
Authorized scope: examples/osint-targets/authorized-scope.example.txt
Collection mode: passive-only
Outputs: JSONL records and a markdown summary.
Constraints: No live third-party scans. No secrets in repo. Tests must use fixtures.
```

## MCP integration

```text
Read CLAUDE.md and use /mcp-tooling.

Goal: Add a template for a local-only target normalization MCP tool.
Tool type: local-only
Secrets: none
Safety: Validate file paths, reject absolute paths outside the workspace, and keep output deterministic.
```

