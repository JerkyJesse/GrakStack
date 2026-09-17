---
description: Pre-ship review of the current diff. Findings only - file:line, severity, fix.
---

PRE-SHIP REVIEW. Findings only. No praise, no rewrite.

1. Get the diff: `git status`, `git diff`, `git diff --staged`. If a base branch exists, diff against it.
2. Read every changed file in full. Context decides severity.
3. Hunt: bugs, edge cases, security holes, broken callers, wrong error handling, tests that cannot fail, secrets in the diff.
4. Hunt past syntax: concurrency and ordering, input trust boundaries, migrations and state, dependency supply chain (new dependency? read its install scripts), resource leaks.
5. Report each finding as: `file:line - severity (blocker/major/minor) - what breaks - one-line fix`.
6. No findings: say "No findings." and list what you checked.

Do not edit code unless the user asked for fixes too. Quote errors exactly.

Scope:

$ARGUMENTS

<!-- cavestack-owned -->
