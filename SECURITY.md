# Security Policy

## Supported versions

Only the latest tagged release is supported. Installs are pinned to a release
tag and verified against the release's published `SHA256SUMS` asset before
`setup` runs; `python3 ~/grakstack/characters/grak/rock_memory.py --check`
verifies the installed state.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting:

https://github.com/JerkyJesse/grakstack/security/advisories/new

Do not open a public issue for a security problem.

## Scope

In scope:

- the installers: `setup`, `setup.ps1`, `docs/install`, `docs/install.ps1`
- the rock memory, receipt, and ownership checks
- anything that could cause code execution, file deletion outside the install
  set, or configuration corruption on a user's machine

Out of scope:

- the behavior of third-party AI coding hosts
- generated agent output and its content

## Response

Single-maintainer project. You will get an acknowledgment within 7 days and a
fix or a written statement within 30.
