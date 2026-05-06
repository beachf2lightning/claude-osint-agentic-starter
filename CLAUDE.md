# CLAUDE.md

This file gives Claude Code the project context, guardrails, and workflows it needs to act as a reliable coding agent for defensive cybersecurity and OSINT automation. Keep it current as the repository changes. Claude should read this before making changes.

## Project overview

This is a starter repository for building defensive OSINT and reconnaissance automation with Claude Code in VS Code, Cursor, Kali Linux, Docker, and MCP-oriented workflows. It is intentionally small, testable, and documented so Claude can safely handle bug fixes, refactors, and feature work without drifting into unsafe activity.

## Repository map

- `src/agentic_starter/` - application package code.
- `tests/` - unit tests and regression tests.
- `docs/` - human-readable engineering notes, Claude workflow instructions, and security playbooks.
- `docker/` - Dockerfile and compose scaffold for repeatable lab execution.
- `mcp/` - MCP server configuration placeholders and tool manifest examples.
- `examples/osint-targets/` - safe, explicitly authorized target files for demos and tests.
- `.claude/commands/` - reusable Claude Code slash-command prompts.
- `.github/` - GitHub issue templates and CI workflow.
- `.vscode/` - VS Code settings and recommended extensions.
- `.cursor/rules/` - Cursor project rules mirroring key Claude guidance.
- `scripts/` - local helper scripts.

## Default development commands

Run commands from the repository root.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m ruff format .
python -m mypy src
```

If a command fails because dependencies are missing, install the development dependencies first. If a command fails because the repository changed, update this section in the same pull request.

## Agent operating principles

1. Prefer small, reviewable changes.
2. Read relevant files before editing.
3. Make a short plan for multi-file work.
4. Add or update tests for every behavior change.
5. Run the narrowest useful tests first, then the broader suite.
6. Do not remove tests to make a failure disappear.
7. Do not commit secrets, tokens, private keys, API keys, client data, target lists, or scan output containing sensitive findings.
8. Do not introduce new tools or dependencies unless there is a clear benefit and the reason is documented.
9. Preserve public APIs and CLI flags unless the task explicitly asks for a breaking change.
10. Update documentation when behavior, setup, commands, threat model, or architecture changes.

## Cybersecurity safety scope

This repository is for authorized defensive work only.

Allowed:

- OSINT collection against owned assets, lab targets, or explicitly authorized scopes.
- Passive reconnaissance and metadata enrichment.
- Defensive vulnerability triage using public advisories and benign checks.
- Building MCP integrations that orchestrate local tools safely.
- Parsing, normalizing, deduplicating, and reporting recon data.

Not allowed:

- Credential theft, phishing, persistence, malware, evasion, or exploitation guidance.
- Instructions to bypass authentication, rate limits, monitoring, or access controls.
- Running scans or tools against targets without explicit authorization.
- Storing secrets, live tokens, private keys, or customer-sensitive output in the repo.

If the user asks for a risky workflow, pause and provide a safe defensive alternative.

## Preferred workflow for bug fixes

1. Reproduce the bug with a failing test or a minimal command.
2. Explain the suspected cause.
3. Make the smallest fix that addresses the cause.
4. Run the failing test again.
5. Run related tests.
6. Summarize the root cause, fix, and verification.

## Preferred workflow for refactoring

1. Confirm the intended behavior is already covered by tests.
2. Add characterization tests before refactoring if coverage is weak.
3. Refactor in small steps.
4. Keep behavior unchanged unless explicitly requested.
5. Run tests after each meaningful step.
6. Summarize what changed and why it is safer or clearer.

## Preferred workflow for feature development

1. Restate the feature request and acceptance criteria.
2. Identify touched modules and tests.
3. Implement the smallest vertical slice first.
4. Add tests for expected behavior, edge cases, and errors.
5. Update docs or examples.
6. Run linting, type checks, and tests.
7. Summarize usage, limitations, and verification.

## Code style

- Python version: 3.11 or newer.
- Formatting: Ruff formatter.
- Linting: Ruff.
- Typing: mypy with strict settings where practical.
- Tests: pytest.
- Keep functions focused and descriptive.
- Prefer explicit names over clever abbreviations.
- Prefer dependency injection over hidden global state.
- Use standard library features before adding packages.

## Security expectations

- Treat all user input as untrusted.
- Avoid shell invocation unless absolutely necessary.
- If shell commands are required, avoid string interpolation with untrusted input.
- Never log secrets.
- Validate file paths before reading or writing.
- Keep examples benign and defensive.
- If a request could enable harm, pause and ask for clarification or provide a safe alternative.
- Make target scope explicit before any recon logic is run.
- Prefer dry-run mode for commands that would touch networks or external systems.
- Keep network timeouts, retries, and rate limits conservative.
- Store generated findings under ignored local output directories unless the user explicitly asks otherwise.

## Kali and Docker expectations

- Kali is a useful operator environment, but application tests must also run in a clean Python environment.
- Prefer Docker for repeatable labs and toolchain isolation.
- Do not assume privileged containers are available.
- Do not mount host secrets into containers unless documented and explicitly required.
- Keep Docker defaults safe: no host networking, no privileged mode, no broad host mounts.

## MCP expectations

- MCP server configs in `mcp/` are templates only.
- Do not hardcode API keys or tokens in MCP config files.
- Prefer environment variables named in `.env.example`.
- Tool descriptions should state whether a tool is passive, active, local-only, or network-touching.
- Claude should ask for confirmation before enabling active network-touching tools.

## Git and pull request expectations

- Work on a feature branch.
- Keep commits focused.
- Before opening a pull request, run:

```bash
python -m pytest
python -m ruff check .
python -m mypy src
```

- Pull request summaries should include:
  - What changed.
  - Why it changed.
  - How it was tested.
  - Any risks or follow-up work.

## When to ask for help

Ask the user before proceeding if:

- Requirements are ambiguous and multiple implementations would be reasonable.
- A change would delete user data or make a breaking API change.
- A task requires credentials, external accounts, or private infrastructure.
- Tests reveal unrelated failures that would require broader changes.

## Useful Claude prompts

Use the slash commands in `.claude/commands/` for repeatable workflows:

- `/bug-fix`
- `/feature-dev`
- `/refactor`
- `/test-plan`
- `/security-review`
- `/osint-scope`
- `/recon-pipeline`
- `/mcp-tooling`
- `/docker-lab`
- `/pr-description`
- `/commit-ready`
