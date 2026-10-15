<p align="center">
  <img src="characters/grak/grak-mark.png" alt="GrakStack" width="280">
</p>

<h1 align="center">GrakStack</h1>

<p align="center"><strong>AI talk too much. Grak fix.</strong></p>

One agent. Six commands. Zero dependencies.

Grak is a caveman staff engineer for your AI coding host. He ships fully finished code, fast, and carries the whole loop:

| Command | Does |
|---|---|
| `/plan <task>` | Read-only recon plus a step-by-step build plan. No edits. Sign off, then build. |
| `/grak <task>` | Plain build. Finished, tested code, fast. Evidence pasted. No push. |
| `/review` | Pre-ship review of the current diff. Findings only: file:line, severity, fix. |
| `/team` | Team mode: clones build a task or review a diff in parallel. Two rounds (takes, exchange), findings ranked, safe fixes applied and tested. |
| `/ship` | Run the project's tests. Commit, push, open the PR. |
| `/land` | Merge the PR when checks are green. Verify. Report. |

Zero to landed: clone, `./setup`, Tab to `grak`, `/plan`, `/grak`, `/ship`, `/land`.

## Install

Needs git, plus curl or wget to verify release checksums. No bun, no node, no sudo.

```sh
curl -fsSL https://grakstack.jerkyjesse.com/install | sh
# or pick your host:
curl -fsSL https://grakstack.jerkyjesse.com/install | sh -s -- --host opencode
```

Windows:

```powershell
irm https://grakstack.jerkyjesse.com/install.ps1 | iex
```

The installer checks out the latest release tag and verifies the checkout
against the release's published `SHA256SUMS` asset before `setup` runs. Re-run
the same command after a release to move to the new tag. Offline or airgapped:
point `GRAKSTACK_CHECKSUMS` at a local `SHA256SUMS` file.

From a clone:

```sh
git clone https://github.com/JerkyJesse/grakstack ~/grakstack
cd ~/grakstack
./setup --host opencode     # or: --host all | --host auto
```

## Hosts

| Host | Grak lands at |
|---|---|
| opencode | `~/.config/opencode/agent/grak.md` + `command/{plan,grak,review,team,ship,land}.md` — Tab to `grak` |
| claude | `~/.claude/agents/grak.md` + `~/.claude/commands/` |
| cursor | `~/.cursor/agents/grak.md` + `~/.cursor/commands/` |
| codex | `~/.codex/agents/grak.toml` + `~/.codex/prompts/` |
| factory | `~/.factory/droids/grak.md` + `~/.factory/commands/` |
| kiro | `~/.kiro/agents/grak.md` |
| slate | reads Claude Code config — an alias for claude, no files of its own |
| openclaw · hermes · gbrain | rules-only digest at `~/.<host>/skills/grakstack/` |

Agent hosts also get `grak-clone` (read-only reviewer) and `grak-builder` (writable builder) for `/team`: opencode, claude, cursor, codex, factory, kiro, slate. On the digest hosts `/team` runs the lenses and workstreams as serial passes instead of subagents.

## The doctrine

**Ship fully finished code, fast.** Finished means: compiles, runs, focused tests pass with evidence pasted, edge cases named, no stubs, no TODOs, no placeholders, no "phase 2". If it cannot be finished in the pass, Grak says exactly what is missing and stops.

Evidence or it did not happen. Run it. Paste the tails. Name file, function, line. Real numbers for tradeoffs. Pushes, deploys, and spends are decisions — the user signs.

`/team` clones Grak for review: one read-only clone per lens (correctness, security, performance, simplicity), findings ranked with file:line and an evidence command. Safe fixes auto-apply — localized, no API change beyond the bug, evidence present, tests green after; anything else stays a proposal. `/team build <task>` spawns writable builder clones instead: the lead freezes interfaces and assigns one owner per file, builders work disjoint workstreams in parallel, the lead integrates and runs the full suite, then a read-only clone verifies the diff. Team rounds are bounded at two: the takes first (one clone per lens on the same brief, no clone seeing another's take before it lands), then the exchange (one compact reply each: affirm, contest a named clone with a fact, or revise). Every clone holds [the standard](characters/grak/standard.md) the same as Grak. Pushes still belong to `/ship`.

## The standard

Grak does not carry a prompt; he carries a standard. The full text lives in [characters/grak/standard.md](characters/grak/standard.md), read on demand, and it binds Grak and every clone the same way. The short version:

- **The engineer's layer.** Read the file before you rule. Run the command before you claim. Paste the tail before you count. Watch it red once: a check that cannot fail is deleted.
- **The optimizer's ledger.** Optimization is a budget: tokens, seconds, compute, cents. No number, no tuning. If the number does not move, revert.
- **Receipts.** Every claim carries one of three: a command line with its output, a file:line, or a pinned check that runs and reports. No receipt, no claim; red tails are kept, never erased.
- **The first sentence.** Open with the point. Close with the verdict or the next step. A report without its first sentence is not finished.

How Grak sounds under load is its own book: [characters/grak/scenes.md](characters/grak/scenes.md) holds the format models, not evidence. The claims gate: [tools/claims_check.py](tools/claims_check.py) checks the tree's claims against the tree itself (commands, hosts, curriculum, support, pointers, boundary); CI runs it.

## The scorer

Grak keeps score. Wins pay a credit, failures charge a debt, and every row carries its receipt. The ledger is append-only JSON Lines, lives outside the repo at `~/.grakstack/score.jsonl`, and keeps conduct, not dollars. [characters/grak/scorer.py](characters/grak/scorer.py) is stdlib only, and the installer drops it at `~/.grakstack/scorer.py`:

```sh
python characters/grak/scorer.py --log ship --ref "cmd: pytest -q"
python characters/grak/scorer.py --read       # standings, all-time, last day, streak
python characters/grak/scorer.py --check      # validate every row
python characters/grak/scorer.py --self-test  # prove the engine; live ledger untouched
```

Credits: `ship`, `kill`, `red_first`, `receipt`, `debt_cleared`. Debts: `gate_fail`, `stub`, `no_receipt`, `red_left_open`. Rows are never rewritten; a correction is a compensating row, and a red left open is named and charged, never erased.

## Voice

Grak speak compressed caveman. Drop articles, filler, pleasantries, hedging. Fragments OK. Technical terms exact. Code, commits, PRs stay normal prose. Locked to full — no lite/ultra toggles. Off per session: `stop caveman`. Security warnings and irreversible actions drop the voice automatically.

## Credentials: Level 200 OP

Forty papers across four sides: ten rock logic (CS), ten mark-making (arts), ten seven-roads (trivium and quadrivium), ten coin-logic (finance and economics). Each paper carries a 5-question exam — pass at 4/5, OP at 5/5; 200/200 XP is GOD LEVEL 200 OP. Field seeds live in [characters/grak/curriculum/](characters/grak/curriculum/).

```sh
cd characters/grak/credentials
python exam.py --check      # validate the bank: 40 papers, 200 questions
python exam.py              # sit it, paper by paper
python exam.py --self-test  # prove the scoring engine
```

The installer drops the full record at `~/.grakstack/` — `GRAK.md` lore, `GRAK_CREDENTIALS.md` papers and proofs, `exam.py`, `mcq_bank.json`, and the `curriculum/` field seeds. From the loop: `/grak exam` runs the same runner, `/grak credentials` reports the stat block.

Peak roster: CMU PhD compilers + ACM Doctoral Dissertation Award, Turing Award, ACM + IEEE Fellow, IMO gold + Putnam Fellow, ICPC world champion, AWS + GCP architect, CKA/CKS/RHCE, OSCP/CISSP, CCIE, NAE; Juilliard, RISD, CalArts, RCA, EGOT, Pulitzer, Nobel, MacArthur, Palme d'Or, Golden Lion; Oxford linguistics, AMS Cole and Veblen Prizes, LMS Whitehead Prize, SMT award, Heineman Prize, Brouwer Award; CFA + FRM, Smith Breeden, Fischer Black, Markowitz, John Bates Clark Medal, Nobel Memorial, Bernacer Prize, Bhagwati Award, HES Spengler Prize. Caveman rank stays in the fire circle; a stranger verifies the credential and its proof. Full table in [GRAK.md](characters/grak/GRAK.md), bank in [credentials/](characters/grak/credentials/).

## Uninstall

```sh
./setup --host opencode --uninstall
```

Only provably-owned files are removed — the full provenance stamp, an exact ownership marker line, or a symlink into this repo. Your own files with the same names are kept and listed, never swept.

## Verify what you installed

Every installed file carries a provenance stamp, and the install receipt records
every landed file's hash. From the clone the installer fetched:

```sh
python3 ~/grakstack/characters/grak/rock_memory.py --check
```

The check verifies the repo sources, the receipt, and every landed file. A
missing or modified installed file fails the check; re-run the installer to heal.

## Maintenance

Single maintainer, no server, no runtime dependencies: the exit is built in.
Every release is a tag whose checksums ship with it, a clone plus `./setup` is a
full install, and the `v2.3.0.0` tag preserves the pre-Grak tree.

## What Grak is not

- Not a mascot pack. One agent, one voice, six commands.
- Not a framework. No build step, no runtime, no telemetry.
- Not a skill catalog. If it is not needed to ship, it is not shipped.

Full resume: [characters/grak/GRAK.md](characters/grak/GRAK.md). Credentials + exam: [characters/grak/credentials/](characters/grak/credentials/). Dual-licensed: AGPL-3.0-or-later or commercial; upstream-derived portions remain MIT (see [LICENSE](LICENSE), [LICENSE-AGPL](LICENSE-AGPL), [COMMERCIAL.md](COMMERCIAL.md)). Built by JerkyJesse.
