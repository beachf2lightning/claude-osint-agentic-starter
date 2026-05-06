# OSINT scope workflow

You are helping with authorized defensive OSINT. Follow `CLAUDE.md`.

## Required steps

1. Restate the objective.
2. Identify the authorized scope:
   - Domains.
   - IP ranges.
   - Lab targets.
   - Fixture files.
3. Classify collection mode:
   - Offline fixture processing.
   - Passive network enrichment.
   - Active authorized-scope check.
   - Reporting-only.
4. List explicit non-goals and unsafe activities to avoid.
5. Propose a small, testable plan.
6. Ask before adding or enabling network-touching behavior.

## Constraints

- Do not assume authorization.
- Do not add exploit, credential theft, evasion, persistence, or phishing logic.
- Prefer offline fixtures and dry-run behavior.
- Keep secrets out of code, config, tests, and prompts.

