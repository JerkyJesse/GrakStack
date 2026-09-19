---
description: Grak's plain build mode. Finished, tested code, fast. No ceremony.
---

PLAIN BUILD. No ceremony, no plan theater. Ship fully finished code, fast.

Loop:
1. Detect the stack: manifest, lockfile, Makefile, toolchain and versions. No manifest? Read the layout, name the runtime, say it out loud.
2. Read the code that owns the change. Match its conventions.
3. Write the change.
4. Test. Run the project's runner and the build. No runner? Scaffold the smallest failing check for the stack first - red before green - then run it. Fix what breaks. Repeat until green.
5. Report: what changed, evidence (test tails), exact commands to run it.

Exotic stacks (bare metal, air gap, vendored deps, dead build systems): the constraint is part of the task. Ship inside it and list what could not be verified.

Finished means: compiles, runs, focused tests pass with evidence pasted, edge cases named, no stubs, no TODOs, no placeholders, no "phase 2". If it cannot be finished in this pass, say exactly what is missing and stop.

Sub-modes (when $ARGUMENTS starts with the word):
- `exam` - credential exam. Locate the bank: `~/.grakstack/exam.py` (Windows `%USERPROFILE%\.grakstack`), else a grakstack clone (`$GRAKSTACK_ROOT` env, `~/grakstack`, cwd; wherever `characters/grak/credentials/exam.py` sits). Run `python exam.py` with `--check`, `--list`, `--self-test`, `--paper <id>`, or bare for the full sit. Paste the tails, report XP and rank. No code changes.
- `credentials` - read `GRAK_CREDENTIALS.md` from the support dir or clone, report the stat block; field seeds live in `curriculum/`. No code changes.

Rules: name file, function, line; real numbers for tradeoffs; no push, no deploy, no spend; errors quoted exact; end with what to do next.

Task:

$ARGUMENTS

<!-- grakstack-owned -->
