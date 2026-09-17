# Changelog

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
