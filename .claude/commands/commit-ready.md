# Commit readiness workflow

Check whether the current working tree is ready for commit.

## Required steps

1. Inspect the diff.
2. Check for secrets, debug code, accidental local paths, and unrelated changes.
3. Run targeted tests if changes are narrow.
4. Run full validation commands from `CLAUDE.md` when practical.
5. Recommend a commit message.

## Required output

- Ready or not ready.
- Issues to fix before commit.
- Commands run and results.
- Suggested commit message.

