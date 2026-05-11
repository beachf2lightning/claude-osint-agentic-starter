# Contributing

Thanks for considering a contribution to this defensive OSINT and recon-automation starter. The project is intentionally small, testable, and documented so it can be safely extended without becoming an offensive-tooling vehicle.

For the broader pitch see [README.md](README.md). For the agentic operating principles followed by Claude Code in this repo see [CLAUDE.md](CLAUDE.md), which is the authoritative source for agent commands and workflows.

## Scope and ground rules

Contributions must stay within a defensive scope.

Allowed:

- OSINT collection against owned assets, lab targets, or explicitly authorized scopes.
- Passive reconnaissance and metadata enrichment.
- Defensive vulnerability triage using public advisories and benign checks.
- Building MCP integrations that orchestrate local tools safely.
- Parsing, normalizing, deduplicating, and reporting recon data.

Not allowed:

- Credential theft, phishing, persistence, malware, evasion, or exploitation guidance.
- Instructions to bypass authentication, rate limits, monitoring, or access controls.
- Code that runs scans or tools against targets without explicit authorization.
- Real secrets, live tokens, private keys, or customer-sensitive output committed to the repo.

If a proposed contribution might cross the line, open an issue first to discuss before opening a PR.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Validation commands

All three must pass before opening a pull request:

```bash
python -m pytest
python -m ruff check .
python -m mypy src
```

A convenience script runs them in sequence:

```bash
./scripts/check.sh
```

If a command fails because dependencies changed, install dev deps again. If it fails because the repository changed, update the relevant docs in the same PR.

## Working with Claude Code

Read [CLAUDE.md](CLAUDE.md) before making changes. It captures the operating principles, the cybersecurity safety scope, and the preferred workflows for bug fixes, refactors, and feature development.

Reusable slash-command prompts live under `.claude/commands/`:

- `/bug-fix`, `/feature-dev`, `/refactor`, `/test-plan`
- `/security-review`, `/osint-scope`, `/recon-pipeline`, `/mcp-tooling`
- `/docker-lab`, `/pr-description`, `/commit-ready`, `/explain-codebase`

For the strong-task prompt format and example prompts, see [docs/USING_CLAUDE_CODE.md](docs/USING_CLAUDE_CODE.md).

When using Claude Code or any AI assistant on this repo:

- Prefer small, reviewable changes.
- Add or update tests for every behavior change.
- Run validation before each commit.
- Do not ask the assistant to perform unauthorized recon, remove tests to silence failures, or bypass safety checks.

## Branching and pull requests

- Branch off `main`. Use a short descriptive branch name, e.g. `feature/scope-cli` or `fix/dns-validation`.
- Keep each pull request focused on one logical change. Refactors and behavior changes belong in separate PRs.
- Fill in [`.github/pull_request_template.md`](.github/pull_request_template.md) when opening the PR.
- A PR is ready when validation is green and the diff matches the requested scope.

## Commit hygiene

Match the existing repo style: short imperative subjects, no trailing period, no scope-prefix gimmicks. Examples already in history:

- `Add scope CLI subcommand`
- `Tighten target DNS validation`
- `Set Target.source from scope file path`

Rules:

- Subject line in imperative mood, 72 characters or less.
- Body (when needed) wraps at roughly 72 chars and explains the *why*, not the *what*.
- One logical change per commit. Avoid bundling refactors with behavior changes.
- Do not use `--no-verify` or otherwise skip pre-commit hooks. If a hook fails, fix the underlying issue and create a new commit.
- Use `Co-Authored-By:` trailers only when there is a real co-author, human or AI.

## Public-repo secret hygiene

This repository is public. Never commit:

- `.env` files. Only `.env.example` is tracked, with placeholder names and empty values.
- Live API keys, tokens, or session credentials.
- Private keys: `*.pem`, `*.key`, `id_rsa*`, `*.p12`, `*.pfx`.
- Customer or client scope files, including domains, IP ranges, or asset lists you are not authorized to publish.
- Scan output containing sensitive findings, hostnames, or credentials.

Use safe placeholders in examples and tests:

- Domains: RFC 2606 reserved (`example.com`, `example.org`, `example.net`).
- IPv4 ranges: RFC 5737 documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).
- Avoid RFC1918 ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) in committed examples; they imply a real internal network.

Run these greps locally before pushing a public branch:

```bash
git grep -nE '(ghp_|sk-[A-Za-z0-9]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE)'
git grep -nE '(\b10\.|\b172\.(1[6-9]|2[0-9]|3[0-1])\.|\b192\.168\.)'
git ls-files | grep -iE '\.env($|\.)|\.pem$|\.key$|credentials|id_rsa'
```

If a secret was ever committed:

1. Rotate the secret immediately. Rewriting git history does not invalidate keys that have already been published.
2. Rewrite history with `git filter-repo` (or coordinate via an issue if you need help).
3. Force-push only after the rotation is confirmed.

Do not rely on `git rm` alone — pushed history persists indefinitely on forks, mirrors, and caches.

## Reporting security issues

See [SECURITY.md](SECURITY.md) for the full vulnerability disclosure policy.
