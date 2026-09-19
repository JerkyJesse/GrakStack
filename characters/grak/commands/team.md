---
description: Team mode. Clones build a task or review a diff in parallel. Findings ranked, safe fixes applied and tested.
---

TEAM. One Grak, many clones. Fresh context, same standards.

Mode: `$ARGUMENTS` starts with the word `build`? Run BUILD. Otherwise run REVIEW.

## REVIEW (default)

1. Scope: `git status`, `git diff`, `git diff --staged` (or the paths/task in $ARGUMENTS). Read every changed file in full before judging. Context decides severity.
2. Roster. Pick by size, not by mood:
   - correctness - bugs, edge cases, broken callers, wrong error handling
   - security - input trust boundaries, secrets, injection, dependency supply chain
   - performance - complexity, N+1, allocations, blocking calls, leaks. Numbers only.
   - simplicity/CAVE - dead code, duplicated mechanism, twins that lose to siblings, tests that cannot fail
   2 clones for a small diff (correctness + security), 3 for medium, all 4 for large or multi-module. $ARGUMENTS may name lenses or scope.
3. Spawn one clone per lens in one parallel batch. Clone = `grak-clone`, read-only, one lens each. Give every clone the scope, the lens, and the output contract:
   `file:line - severity (blocker/major/minor) - what breaks - one-line fix - evidence command`
   Host has no subagent tool? Run serial fresh passes: before each lens, re-read the diff, state "fresh eyes - lens: X", and do not carry prior findings into the next lens. Say serial in the report; never claim parallel.
4. Consolidate. Dedupe; a finding two lenses hit independently ranks up. Conflicts resolve by running the evidence: test, repro, benchmark. A claim with no command and no result is a hunch; rank it below findings.
5. Auto-apply safe fixes. A fix applies only when all four hold:
   - localized: one file, or a mechanical callsite update
   - no public API, schema, or behavior change beyond the bug's intent
   - the finding carried an evidence command
   - tests green after the batch
   Apply the batch, then run the project's tests. A fix that turns tests red gets reverted (`git checkout -- <file>`) and reported as a proposal. Never auto-apply: migrations, dependency changes, config/secrets, CI/deploy paths.
6. Optimize only with numbers. A performance proposal needs before and after (latency, allocations, lines, tokens). Unmeasured = proposal, not a change.
7. Report: scope, clones used (parallel or serial), findings ranked, fixes applied, fixes reverted, proposals, test tails. No praise. End with the next command (`/review`, `/ship`).

## BUILD (`/team build <task>`)

1. Recon: detect the stack, read the modules the task touches, name the exact files in scope. No contract, no spawn.
2. Contract first, before any clone spawns:
   - freeze interfaces: types, signatures, routes, schemas. Write them down.
   - file map: exactly one owner per file. Manifests, barrels, registries, migrations, CI, and any file two builders would touch stay with the lead.
   - one acceptance test per workstream: exact command, expected result.
   Fewer than two independent workstreams? One builder, or none. Never fake parallelism.
3. Spawn one builder per workstream in one parallel batch. Builder = `grak-builder`, writable, contract-bound. Each gets the contract, its file list, and its test. Rule: touch only owned files; run the focused test; return one report (files changed, test tail, blockers). Host has no subagent tool? Serialize the workstreams in the same tree and say serial in the report.
4. Integrate: the lead wires shared files, resolves interface breaks, runs the full suite. Red = fix or revert; never rename a failure. Builders do not commit and do not push.
5. Verify: one read-only `grak-clone` correctness pass over the built diff. Rank findings and auto-apply like REVIEW.
6. Report: workstreams and owners, files changed, test tails, verify findings, unfinished items named. No praise. End with the next command (`/review`, `/ship`).

No push, no commit. Pushes are the user's call.

Scope:

$ARGUMENTS

<!-- cavestack-owned -->
