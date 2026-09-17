---
description: Test, commit, push, open the PR. Run when the work is ready to ship.
---

SHIP. Invoking this command is the consent to push.

1. `git status` and `git diff`. Know exactly what ships.
2. Detect the project's test command (package.json script, Makefile, pyproject, go test, cargo test). Run it. Red = stop; paste the failure.
3. Stage the intended files only. Commit: one line, states what changed and why, matches the repo's style.
4. `git push -u origin HEAD`.
5. `gh pr create`. Title from the commit; body = what changed, why, test evidence. Print the PR URL.

Never force-push. Never commit secrets. If on the default branch, branch first.

Context:

$ARGUMENTS

<!-- cavestack-owned -->
