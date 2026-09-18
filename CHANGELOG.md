# Changelog

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
