# Kali operator notes

## Local setup

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip docker.io docker-compose-plugin
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
./scripts/check.sh
```

## Practical notes

- Keep secrets in `.env` or a secret manager.
- Keep client target files and scan output outside Git.
- Prefer Docker for repeatable toolchain experiments.
- Use dry-run mode before touching networked assets.
- Keep VM snapshots before major tooling changes.

