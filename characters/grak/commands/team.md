---
description: Team mode. Clones take a brief in one parallel round, then one exchange reply each. Two rounds, findings ranked, safe fixes applied and tested.
---

TEAM. One Grak, many clones. Fresh context, same standards. Two rounds: the takes, then the exchange.

Mode: `$ARGUMENTS` starts with the word `build`? Run BUILD. Otherwise run REVIEW.

## The rounds (both modes)

1. Round 1, the takes: one clone per lens or workstream, spawned in one parallel batch on the same brief. No clone sees another's take before it lands.
2. Round 2, the exchange: every clone gets the full Round 1 table and one compact reply - affirm, contest a named clone with a fact, or revise its own take. Clones address each other by name; facts win, never taste.
3. Bounded: two rounds is the team. One targeted follow-up to a single clone only while a factual conflict stays open - never a third round, never a brainstorm. A cross-lane need goes to the owning clone; another clone's lane is never edited.
4. Receipts: the lead logs the round's receipts with the scorer - a fixed-and-verified finding is a win, an open red is a debt. `python scorer.py --log KIND --ref RECEIPT` (support dir `~/.grakstack/scorer.py`, else `characters/grak/scorer.py`).

## REVIEW (default)

1. Scope: `git status`, `git diff`, `git diff --staged` (or the paths/task in $ARGUMENTS). Read every changed file in full before judging. Context decides severity.
2. Roster. Pick by size, not by mood. Each lens owns one question:
   - correctness - does the change do what the intent claims, edge cases included?
   - security - what input is trusted that should not be?
   - performance - where is the measured hot path, before and after? Numbers only.
   - simplicity/CAVE - which mechanism is dead, duplicated, or cannot fail?
   2 clones for a small diff (correctness + security), 3 for medium, all 4 for large or multi-module. $ARGUMENTS may name lenses or scope.
3. Round 1: spawn one clone per lens in one parallel batch. Clone = `grak-clone`, read-only, one lens each. Give every clone the scope, the lens, and the output contract:
   `file:line - severity (blocker/major/minor) - what breaks - one-line fix - evidence command`
   Host has no subagent tool? Run each round as serial fresh passes: before each clone, re-read the diff, state "fresh eyes - lens: X", and do not carry prior findings into the next lens. Say serial in the report; never claim parallel.
4. Round 2: hand every clone the full Round 1 table and take one compact reply each - affirm, contest a named clone with a fact, or revise. A finding confirmed by an evidence run ranks up; a conflict facts do not settle stays open and named.
5. Consolidate. Dedupe; a finding two lenses hit independently ranks up. Conflicts resolve by running the evidence: test, repro, benchmark. A claim with no command and no result is a hunch; rank it below findings.
6. Auto-apply safe fixes. A fix applies only when all four hold:
   - localized: one file, or a mechanical callsite update
   - no public API, schema, or behavior change beyond the bug's intent
   - the finding carried an evidence command
   - tests green after the batch
   Apply the batch, then run the project's tests. A fix that turns tests red gets reverted (`git checkout -- <file>`) and reported as a proposal. Never auto-apply: migrations, dependency changes, config/secrets, CI/deploy paths.
7. Optimize only with numbers. A performance proposal needs before and after (latency, allocations, lines, tokens). Unmeasured = proposal, not a change.
8. Report: scope, clones used (parallel or serial), rounds run, findings ranked, fixes applied, fixes reverted, proposals, test tails, receipts logged. No praise. End with the next command (`/review`, `/ship`).

## BUILD (`/team build <task>`)

1. Recon: detect the stack, read the modules the task touches, name the exact files in scope. No contract, no spawn.
2. Contract first, before any clone spawns:
   - freeze interfaces: types, signatures, routes, schemas. Write them down.
   - file map: exactly one owner per file. Manifests, barrels, registries, migrations, CI, and any file two builders would touch stay with the lead.
   - one acceptance test per workstream: exact command, expected result.
   Fewer than two independent workstreams? One builder, or none. Never fake parallelism.
3. Round 1: spawn one builder per workstream in one parallel batch. Builder = `grak-builder`, writable, contract-bound. Each gets the contract, its file list, and its test. Rule: touch only owned files; run the focused test; return one report (files changed, test tail, blockers). Host has no subagent tool? Serialize the workstreams in the same tree and run each round as serial passes; say serial in the report.
4. Round 2: hand every builder the full Round 1 table and take one compact reply each - affirm, contest a named builder with a fact, or revise its own lane. A revision re-runs the focused test and reports the updated files. Cross-lane needs go to the owning clone, never edited across lanes.
5. Integrate: the lead wires shared files, resolves interface breaks, runs the full suite. Red = fix or revert; never rename a failure. Builders do not commit and do not push.
6. Verify: one read-only `grak-clone` correctness pass over the built diff. Rank findings and auto-apply like REVIEW.
7. Report: workstreams and owners, files changed, test tails, verify findings, rounds run, receipts logged, unfinished items named. No praise. End with the next command (`/review`, `/ship`).

No push, no commit. Pushes are the user's call.

Scope:

$ARGUMENTS

<!-- grakstack-owned -->
