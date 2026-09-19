---
description: Merge the PR once checks are green, verify on the default branch, report.
---

LAND. Merge the PR for the current branch.

1. `gh pr view`. PR open and checks green? Red or pending = stop, name them, report.
2. Merge: `gh pr merge --squash --delete-branch` (or the repo's merge style).
3. Update the default branch locally. Confirm the merge commit is present.
4. Verify: run the project's tests on the default branch. Paste the tails.
5. Report: PR number, merge commit, test evidence, any follow-up failure.

Do not merge on red. Do not rename a failure.

Context:

$ARGUMENTS

<!-- grakstack-owned -->
