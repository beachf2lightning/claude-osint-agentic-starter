# Using Claude Code with this repository

Use this guide when you want Claude to handle defensive cybersecurity and OSINT coding work with enough context to act autonomously while still producing reviewable changes.

## Session setup

Start from the repository root:

```bash
claude
```

Then give Claude a short, explicit instruction:

```text
Read CLAUDE.md. Confirm the validation commands, then wait for my task.
```

## Strong task format

Use this structure for agentic tasks:

```text
Goal: Build or fix <defensive capability>.
Acceptance criteria:
- <observable outcome>
- <test coverage expectation>
Constraints:
- Scope: passive-only, lab-only, or explicitly authorized targets only.
- Preserve <public API or compatibility rule>.
Verification:
- Run python -m pytest
- Run python -m ruff check .
```

## OSINT scope prompt

```text
Use /osint-scope.

Objective: <what you want to learn or automate>
Authorized scope: <domains, IP ranges, lab targets, or fixture files>
Collection mode: passive-only unless explicitly stated otherwise
Outputs: <CSV, JSONL, markdown report, graph data, etc.>
Constraints: No secrets in repo, no live third-party scans, no exploitation.
```

## Bug fix prompt

```text
Use /bug-fix.

Bug: <describe observed behavior>
Expected: <describe expected behavior>
Reproduction: <command, failing test, issue link, or steps>
Constraints: Keep the fix minimal and add a regression test.
```

## Refactor prompt

```text
Use /refactor.

Target: <file, module, or function>
Goal: <clarity, performance, separation of concerns, typing, etc.>
Constraints: Preserve behavior and public API. Add characterization tests first if coverage is weak.
Verification: Run related tests, then python -m pytest.
```

## Feature prompt

```text
Use /feature-dev.

Feature: <feature name>
User story: As a <user>, I want <capability>, so that <outcome>.
Acceptance criteria:
- <criterion 1>
- <criterion 2>
Out of scope:
- <non-goal>
Verification:
- <tests and commands>
```

## Recon pipeline prompt

```text
Use /recon-pipeline.

Pipeline goal: <normalize targets, enrich DNS, parse tool output, dedupe findings, etc.>
Input: <fixture path or authorized target file>
Output: <expected artifact or data structure>
Safety: Keep tests offline. Any network-touching behavior must be behind an explicit flag and dry-run by default.
Verification:
- python -m pytest
- python -m ruff check .
- python -m mypy src
```

## MCP tooling prompt

```text
Use /mcp-tooling.

Goal: Add or update an MCP server/tool configuration for <tool>.
Tool type: local-only, passive network, active authorized-scope, or reporting-only.
Secrets: Use environment variables only.
Safety: Include dry-run behavior where practical and document confirmation requirements.
```

## Review checklist

Before accepting Claude's changes, check:

- Does the diff match the requested scope?
- Are tests meaningful and not overfit to implementation details?
- Did Claude remove or weaken existing tests?
- Did Claude update docs and examples where needed?
- Did validation commands run successfully?
- Are secrets, tokens, or local paths absent from the diff?
- Is target scope explicit for any recon-related code?
- Are tests offline or fixture-based unless explicitly marked otherwise?
