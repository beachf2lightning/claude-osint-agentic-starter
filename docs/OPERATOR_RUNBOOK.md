# Operator runbook

Day-to-day, command-first reference for using this repository on Kali Linux with Claude Code. Complements `README.md` (project intro), `docs/USING_CLAUDE_CODE.md` (prompt patterns), and `docs/playbooks/kali-operator-notes.md` (general Kali notes). When in doubt about scope or safety, defer to `CLAUDE.md` and `SECURITY.md`.

This repository is for **authorized defensive work only**. Do not point any tooling derived from it at systems you are not explicitly authorized to assess.

## Startup checks

Run these at the top of every session.

```bash
pwd                          # repo root
git status                   # clean working tree, expected branch
git status --short           # no stray scope files or scan output staged
python3 --version            # 3.11 or newer
git --version
docker --version             # optional, only if you plan to use the lab
ls -d .venv                  # virtualenv exists; if not, see next section
```

If `git status` shows untracked output files (e.g. `*.jsonl`, `findings/`), move them out of the working tree before continuing — they should live under an ignored local directory, never in commits.

## Activating the venv

```bash
source .venv/bin/activate
which python                 # should resolve inside ./.venv/
```

First-time setup (or if `.venv/` is missing or broken):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Running validation

The canonical check is the combined script:

```bash
./scripts/check.sh           # ruff check + mypy + pytest
```

While iterating, run the narrower commands directly:

```bash
python -m pytest
python -m ruff check .
python -m ruff format .
python -m mypy src
```

All commands assume the venv is active and you are at the repo root.

## Using the CLI scope command

The `osint-agentic-starter` script is installed by `pip install -e ".[dev]"`. It is offline: no DNS, no network calls.

Normalize a string into a stable identifier:

```bash
osint-agentic-starter normalize "Hello, World"
# hello-world
```

Load an authorized-scope file (text output):

```bash
osint-agentic-starter scope examples/osint-targets/authorized-scope.example.txt
```

JSONL output for piping into other tools:

```bash
osint-agentic-starter scope examples/osint-targets/authorized-scope.example.txt --format jsonl
```

Confine reads to a trusted directory so the loader rejects symlink escapes and absolute paths outside it:

```bash
osint-agentic-starter scope ./scope/targets.txt --allowed-root ./scope
```

Errors (missing file, directory instead of file, validation failure) exit with code `2` and print to stderr.

## Safe public-repo hygiene

This repository is public-shaped. Treat every commit as if it were already pushed.

- **Never commit**: real client scope files, scan output, `.env`, API tokens, private keys, anything under `findings/` or similar local output paths.
- Use only the fixtures under `examples/osint-targets/*.example.txt` for tests and demos.
- Stage explicitly with `git add <path>` rather than `git add -A` — Kali working trees often pick up stray tool output.
- Before staging, run a quick secret sniff:

  ```bash
  git diff --cached | grep -iE 'api[_-]?key|secret|token|password|-----BEGIN'
  ```

  This is a sanity check, not a substitute for reviewing the diff.
- Run `./scripts/check.sh` before every commit.
- Cross-reference: the safety scope in `CLAUDE.md` and disclosure guidance in `SECURITY.md`.

## Committing and pushing

```bash
git switch -c feat/<short-name>
# ...make changes, run ./scripts/check.sh...
git add <specific files>
git commit -m "<concise message>"
git push -u origin feat/<short-name>
```

Optional: open a pull request from the CLI if `gh` is installed and authenticated:

```bash
gh pr create --fill
```

Keep commits small and focused. Mirror the style of existing entries in `git log`.

## Troubleshooting

### `ruff`, `mypy`, or `pytest` not found

The venv is not active, or dev extras are not installed.

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pip show ruff      # confirm it resolves inside .venv
```

### Corrupt zsh history

After a Kali crash or forced reboot you may see `zsh: corrupt history file /home/<user>/.zsh_history`.

```bash
mv ~/.zsh_history ~/.zsh_history.bak
strings ~/.zsh_history.bak > ~/.zsh_history
fc -R
```

If you do not need the prior history, just delete the backup after confirming the new shell starts cleanly.

### Claude Code `--resume` segfaults

If `claude --resume` crashes immediately, the stored session for this project is likely corrupted. Move the project-specific session directory aside (do not delete blindly) and start a fresh session:

```bash
mv ~/.claude/projects/<this-project-slug> ~/.claude/projects/<this-project-slug>.bak
claude
```

The slug is derived from the repository's absolute path; `ls ~/.claude/projects/` will show the matching directory. This loses in-progress conversation state but does not touch the repository.

### `pip install -e` fails

Check the interpreter the venv is using:

```bash
python -V                    # must be 3.11+
```

On Kali, ensure base packages are present:

```bash
sudo apt install -y python3-venv python3-pip
```

### Permission errors on a VM shared folder

Move the repository into `~` (your home directory). Shared folders frequently break virtualenvs, Docker bind mounts, and pytest caches due to permission and inode quirks.

### `./scripts/check.sh: Permission denied`

```bash
chmod +x scripts/check.sh
```
