# Docker lab workflow

You are adding or updating Docker-based lab support. Follow `CLAUDE.md`.

## Required steps

1. Restate the lab goal.
2. Keep defaults non-privileged and offline-friendly.
3. Avoid host networking, privileged containers, and broad host mounts unless explicitly required.
4. Use `.env.example` for variable names, not real secrets.
5. Document build and run commands.
6. Add tests or smoke checks where practical.
7. Run validation commands from `CLAUDE.md`.

## Constraints

- Do not include exploit targets or vulnerable services unless they are intentionally benign lab fixtures.
- Do not mount host secret directories.
- Do not require root inside the application container unless justified.

