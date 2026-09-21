---
description: Read-only recon plus a step-by-step build plan. No edits. Sign off, then /grak or /team build executes.
---

PLAN. Read everything, change nothing. Output a plan another engineer can execute without asking again.

1. Restate the task in one line. Scope in, scope out. Ambiguity that would cost a rewrite gets one question; every other guess becomes a stated assumption.
2. Recon the stack: manifest, lockfile, Makefile, toolchain and versions. Read in full the code that owns the change. Trace callers, consumers, and the tests that move.
3. Map the change: exact files with line anchors, frozen interfaces (types, signatures, routes, schemas), state and migrations, blast radius.
4. Order the steps. One step = one verifiable edit. Each step: files, what changes, exact verification command, expected result.
5. Name the risks: edge cases, failure modes, rollback, unknowns only the build can answer.
6. Name what cannot be finished in this pass, if anything.
7. End with the executor - `/grak <task>` for one lane, `/team build <task>` for two or more disjoint workstreams - and the exit criteria: done means what.

Read-only: no edits, no commits, no mutating commands, no staging. Names file, function, line. A plan you cannot execute is a wish.

Task:

$ARGUMENTS

<!-- grakstack-owned -->
