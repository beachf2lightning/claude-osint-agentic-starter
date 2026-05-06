# Bug fix workflow

You are fixing a bug in this repository. Follow `CLAUDE.md`.

## Required steps

1. Restate the bug and expected behavior.
2. Find the smallest relevant area of code.
3. Reproduce the bug with a failing test or clear command.
4. Explain the likely root cause.
5. Implement the smallest safe fix.
6. Add or update regression tests.
7. Run targeted tests first.
8. Run the repository validation commands from `CLAUDE.md`.
9. Summarize:
   - Root cause.
   - Files changed.
   - Tests added or updated.
   - Commands run and results.

## Constraints

- Do not broaden scope without asking.
- Do not delete failing tests unless they are demonstrably invalid.
- Do not change public behavior beyond the bug fix unless asked.

