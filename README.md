# Claude OSINT Agentic Starter

A GitHub-ready starter repository for using Claude Code as an agentic assistant for defensive cybersecurity, OSINT automation, and reconnaissance tooling in VS Code, Cursor, Kali Linux, Docker, and MCP-oriented workflows.

The template includes:

- A root `CLAUDE.md` optimized for defensive security automation, bug fixes, refactoring, and feature development.
- Reusable Claude Code command prompts in `.claude/commands/`.
- OSINT and recon workflow prompts with explicit authorization guardrails.
- Kali-friendly setup notes.
- Docker and MCP scaffolding.
- Cursor project rules.
- VS Code settings and extension recommendations.
- GitHub issue templates and CI.
- A tiny typed Python package with offline-safe target normalization tests so the repo works out of the box.

## Quick start

```bash
git init
git add .
git commit -m "Initial Claude OSINT agentic starter"
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

## Command-line usage

After install, the `osint-agentic-starter` script exposes two subcommands.

Normalize a string into a stable identifier:

```bash
osint-agentic-starter normalize "Hello, World"
# hello-world
```

Load and normalize an authorized-scope file (offline; no DNS or network):

```bash
osint-agentic-starter scope examples/osint-targets/authorized-scope.example.txt
osint-agentic-starter scope path/to/scope.txt --format jsonl
```

The `source` field in `--format jsonl` reflects the loaded file's resolved absolute path; callers using `load_targets_from_file` programmatically can override it via the `source` keyword.

Use `--allowed-root` to confine reads to a trusted directory and reject symlink escapes or absolute paths outside it:

```bash
osint-agentic-starter scope ./scope/targets.txt --allowed-root ./scope
```

The bare form (no subcommand) is preserved for backward compatibility and behaves the same as `normalize`:

```bash
osint-agentic-starter "Hello, World"
```

## Use with Claude Code in VS Code

1. Open this folder in VS Code.
2. Install the recommended extensions when prompted.
3. Open an integrated terminal.
4. Run `claude` from the repository root.
5. Ask Claude to read `CLAUDE.md` and follow the workflow for your task.

Example prompts:

```text
Read CLAUDE.md, then inspect the failing tests and fix the smallest bug that explains them.
```

```text
Use /recon-pipeline to add a passive subdomain normalization stage. Keep it offline-testable, add fixtures, and run validation.
```

```text
Use /mcp-tooling to design a safe MCP tool manifest for passive DNS enrichment. Use environment variables for secrets and mark network-touching tools clearly.
```

## Use with Cursor

1. Open this folder in Cursor.
2. Keep `.cursor/rules/claude-agentic-starter.mdc` enabled.
3. Use Agent mode for multi-file tasks.
4. Point Cursor at `CLAUDE.md` when starting larger work.
5. Ask for a plan before broad edits, then have the agent implement and test incrementally.

Example Cursor prompt:

```text
Follow CLAUDE.md and the Cursor project rules. Implement the defensive OSINT feature described in docs/feature-brief.md, add tests, and summarize the verification commands.
```

## Kali Linux quick start

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git docker.io docker-compose-plugin
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
./scripts/check.sh
```

If you use Kali in a VM, keep this repository inside your home directory rather than a shared folder when possible. Shared folders can create file permission issues for Python virtual environments, Docker bind mounts, and test caches.

For day-to-day operator workflow on Kali, see [`docs/OPERATOR_RUNBOOK.md`](docs/OPERATOR_RUNBOOK.md).

## Docker quick start

```bash
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml run --rm osint-agent ./scripts/check.sh
```

The Docker scaffold is intentionally non-privileged and offline-friendly by default.

## MCP quick start

Start with `mcp/server-template.json` and replace placeholder commands with your actual local MCP server entry points. Keep secrets in `.env`, not in JSON config files.

## Make Claude agentic safely

For reliable autonomous coding sessions:

- Give Claude a clear goal, success criteria, and verification command.
- Keep tasks small enough to review.
- Ask Claude to write or update tests before changing behavior.
- Let Claude run local tests and linters.
- Review generated diffs before merging.
- Keep secrets out of the repository and out of prompts.
- State whether recon logic must be passive-only, lab-only, or authorized-scope-only.
- Use fixtures under `examples/osint-targets/` rather than live third-party targets in tests.

## Suggested first tasks

- Replace the sample package with your real application code.
- Update `CLAUDE.md` with your stack-specific commands.
- Add architecture notes under `docs/`.
- Add authorized scope templates for your own lab domains or ranges.
- Add MCP server configs for local-only security tools.
- Add project-specific slash commands under `.claude/commands/`.
- Tighten CI to match your production standards.
