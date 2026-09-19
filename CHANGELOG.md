# Changelog

## [3.6.0.0] - 2026-09-18 — The rock memory release

### Added

- **Rock memory** — `characters/grak/rock_memory.py` + `ROCK_MEMORY.sha256`: a sha256 manifest over every shipped source. `--write` regenerates it; `--check` verifies the repo and reports the installed record (`~/.cavestack/ROCK_RECEIPT`) current or stale. `setup --check` runs the deep check when python3 is present.
- **Provenance stamp** — every installed copy (agent, clones, commands, digest) carries `cavestack v<version> :: <manifest-hash>`; the install receipt records the same version and hash, so a stale install is named, not assumed.
- **Paper parity** — `exam.py --check` now requires every bank paper to map to a `GRAK_CREDENTIALS.md` paper, both directions, 20/20.

### Changed

- `setup` / `setup.ps1`: both installers read `VERSION` + the manifest hash, write `ROCK_RECEIPT`, stamp every composed file, run the deep source check, and remove the receipt on uninstall.
- CI: rock-memory and paper-parity checks added to both jobs; the smoke install asserts the stamp and the current record.
- `VERSION`: 3.5.0.0 -> 3.6.0.0.

### Fixed

- `rock_memory.py`: source digests normalize CRLF to LF and the manifest is written LF, so `--check` verifies on any checkout (CI caught the Windows-committed CRLF drift).

## [3.5.0.0] - 2026-09-18 — The build team release

### Added

- **`/team build <task>`** — team mode writes code: the lead freezes interfaces and assigns exactly one owner per file, `grak-builder` clones work disjoint workstreams in parallel, the lead integrates and runs the full suite, then a read-only `grak-clone` verifies the built diff. Unpartitionable work falls back to a single builder; no fake parallelism.
- **`grak-builder` subagent** — `characters/grak/builder-mission.md`, composed by both installers with the full `grak-agent.md` body. Contract-bound, owned files only, focused test evidence, one report, no commit, no push. Write dialects: opencode subagent, claude/factory inherit all tools, cursor default, codex TOML `sandbox_mode = "workspace-write"`, kiro name/description.

### Changed

- `setup` / `setup.ps1`: `install_companion` replaces `install_clone` — one composition path with a read-only / read-write switch drives `grak-clone` and `grak-builder`; uninstall, `--check`, summary, and the nine-host parity diff cover both.
- `team.md` gains explicit REVIEW and BUILD sections; `$ARGUMENTS` starting with `build` selects build.
- CI: smoke install and uninstall assert `grak-builder`, its subagent dialect, and its duty; the dash-path install asserts it too.
- README, site, `AGENTS.md`, `GRAK.md`, digest, in-repo skill: team builds and reviews.
- `VERSION`: 3.4.0.0 -> 3.5.0.0.

## [3.4.0.0] - 2026-09-18 — The team release

### Added

- **`/team` command** — clone Grak into a team of subagents: one read-only clone per lens (correctness, security, performance, simplicity), findings ranked with an evidence command, safe fixes auto-applied and verified, unmeasured optimizations left as proposals.
- **`grak-clone` subagent** — `characters/grak/clone-mission.md`, composed by both installers with the full `grak-agent.md` body so the clone keeps Grak's voice and laws. Per-host dialects: opencode `mode: subagent` + edit deny, claude read-only tools, cursor `readonly: true`, codex TOML `sandbox_mode = "read-only"`, factory `tools: read-only`, kiro name/description.
- **Serial fallback** — hosts without a subagent mechanism (openclaw, hermes, gbrain) run the team lenses as serial fresh passes; the report says serial, never parallel.

### Changed

- `setup` / `setup.ps1`: `team` joins the command set, clones install and uninstall under the same ownership cage, `--check` asserts the new sources, the summary reports clones.
- CI: smoke install and uninstall assert the team command, the clone agent, and the clone dialect; so does the dash-path install.
- README, site, `AGENTS.md`, `GRAK.md`, digest, in-repo skill: five commands and the clone line.
- `VERSION`: 3.3.1.0 -> 3.4.0.0.

## [3.3.1.0] - 2026-09-18 — The hardening release

### Fixed

- **Install through `sh` on dash** — `docs/install` now execs `bash "$DEST/setup"` and preflights bash; stock `sh` on Debian and Ubuntu is dash, which rejects `set -o pipefail`, so the documented `curl ... | sh` path could die before setup ran.
- **Ownership gate resolves links** — `setup` / `setup.ps1` own a symlink only when it resolves into this repo, matching the stated cage rule. Foreign symlinks and files are kept and reported. A write replaces an owned link instead of following it into its target.
- **Digest has one source** — the openclaw/hermes/gbrain digest lives at `characters/grak/digest.md`; both installers copy it.
- **Windows curl installer default host** — `docs/install.ps1` defaults to `claude`, matching `./setup` and `docs/install`.

### Changed

- Loop copy: the "Five commands" count is gone (README, GRAK.md, site); the listed path was six steps.
- CI: the Linux job adds the dash-path install, ownership-gate checks, and a bash-vs-PowerShell installer parity diff over nine hosts; the Windows job adds `exam.py --self-test` and an uninstall smoke.
- `VERSION`: 3.3.0.0 -> 3.3.1.0.

## [3.3.0.0] - 2026-09-17 — The lore wiring release

### Added

- **Lore rails** — `grak-agent.md`: the record wired as operating rules. Twelve shipped systems with mechanism + number, the record table, numbers-or-nothing citations, inventions as rules (TTHW, CAVE, Zero-Test-Drift, Test-Scaffold Gate, voice-verify, persist regardless of voice), scars stay named.
- **Credential rail** — rank is fire circle, never evidence; a claim carries issuer and proof artifact; no artifact demotes to training paper. No hymn credentials.
- **Domain consult** — a task in a shipped or credentialed domain reads the matching record seed first (lore or paper); record unreachable, the agent says so.
- **Exam surface** — `/grak exam` sits the credential exam, `/grak credentials` reports the stat block; the command locates the bank in `~/.cavestack/` or a clone.
- **Record install** — `setup` / `setup.ps1` drop `GRAK.md`, `GRAK_CREDENTIALS.md`, `exam.py`, `mcq_bank.json` at `~/.cavestack/`, marker-owned and removed by `--uninstall`; CI asserts the record and runs the exam on both runners. Digest hosts (openclaw/hermes/gbrain) get the rail and the record path in the rules digest.

### Changed

- `README.md` and site: record path (`~/.cavestack/`) and `/grak exam` lines.
- `VERSION`: 3.2.0.0 -> 3.3.0.0.

## [3.2.0.0] - 2026-09-17 — The level 100 OP credentials release

### Added

- **Level 100 OP credentials** — `characters/grak/credentials/GRAK_CREDENTIALS.md`: 20 papers, 10 rock logic (CS) and 10 mark-making (arts), each with the caveman rank, the real-world credential, its issuer, and the proof to demand. Peak roster: CMU PhD + ACM Doctoral Dissertation Award, Turing Award, ACM + IEEE Fellow, IMO gold + Putnam Fellow, ICPC world champion, AWS + GCP architect certs, CKA/CKS/RHCE, OSCP/CISSP, CCIE, NAE member; Juilliard, RISD, CalArts, RCA, EGOT, Pulitzer, Nobel, MacArthur, Palme d'Or, Golden Lion. Level 100 OP stat block and verification protocol.
- **Credential exam** — `characters/grak/credentials/mcq_bank.json` + `exam.py`: 100 multiple-choice prompts, 5 per paper. 4/5 passes a paper, 5/5 is OP, 100/100 XP is GOD LEVEL 100 OP. Stdlib only; `--check` validates the bank, `--self-test` proves the scoring engine and the OP rank.
- **Digest hooks** — the compressed credential record ships in `grak-agent.md`; `GRAK.md` carries the full table; the in-repo skill points at the bank.

### Changed

- `README.md`: credentials section with the exam run commands and the peak roster.
- GitHub Pages site (`docs/index.html`): credentials section with the rock-logic and mark-making rosters plus the exam runner; version bumped to 3.2.0.0; license section corrected to AGPL-3.0-or-later or commercial (upstream MIT).
- `VERSION`: 3.1.0.0 -> 3.2.0.0.

## [3.1.0.0] - 2026-09-17 — The god resume release

### Added

- **Full resume** — `characters/grak/GRAK.md`: record table, twelve shipped domains with mechanism and number, stack matrix, inventions with mechanism, exotic proofs, failure log. The credentials mirror in `grak-agent.md` stays a compressed digest; the full record lives in the resume.
- **Unknown-stack protocol** — agent behavior and the `/grak` loop: detect toolchain and versions first, scaffold the smallest failing check when no runner exists, name the exact missing piece when unfinishable, ship inside exotic constraints and list what was not verified.
- **Review hunt list** — `/review` now hunts past syntax: concurrency and ordering, input trust boundaries, migrations and state, dependency supply chain, resource leaks.

### Changed

- `VERSION`: 3.0.0.0 -> 3.1.0.0.

## [3.0.0.0] - 2026-09-17 — The Grak-only release

CaveStack is now one agent and four commands. Everything else retired.

### Added

- **Grak agent mode** — `characters/grak/grak-agent.md`: caveman voice locked to full, credentials, finish doctrine ("Ship fully finished code, fast"), installed per host by `setup` / `setup.ps1`.
- **Four commands** — `/grak` (plain build), `/review` (pre-ship findings), `/ship` (test, commit, push, PR), `/land` (merge, verify, report). Sources in `characters/grak/commands/`; setup composes per-host dialects from one source.
- **Dependency-free installer** — `setup` (bash) and `setup.ps1` (Windows native): `--host <name|all|auto>`, `--uninstall` (provenance-gated), `--check`. No bun, no node, no network beyond git.
- **Ten hosts** — claude, cursor, codex, factory, opencode, kiro, slate, openclaw, hermes, gbrain.
- **Grak logo** — used in the README and on cavestack.jerkyjesse.com (hero, favicon, OG card).
- **Site overhaul** — cavestack.jerkyjesse.com rebuilt around Grak: commands grid, install, hosts table, uninstall, doctrine. Cave aesthetic retained.
- **One CI workflow** — `verify.yml`: bash syntax, source check, smoke install + uninstall on Linux and Windows.

### Retired

- The 50+ skill pack, the multi-host skill installer, `browse`, `design`, `make-pdf`, extensions, and their test suites. The full v2.3.0.0 tree is preserved under the `v2.3.0.0` tag.

## [2.3.0.0] - 2026-09-17
Grak gets a name, a face, and his own mode. See the `v2.3.0.0` tag for the full history.
