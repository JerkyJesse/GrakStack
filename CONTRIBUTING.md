# Contributing

grakstack is a single-maintainer project. Issues are enabled; pull requests are
welcome when they are small and provable.

## Before you open a PR

Run the gates from the repo root:

```sh
bash setup --check
python3 characters/grak/rock_memory.py --check --no-receipt
python3 characters/grak/credentials/exam.py --check
python3 tools/version_check.py
```

- One change per PR. No new dependencies, no build step, no new hosts without a
  maintainer decision in an issue first.
- Every shipped-source change needs `python3 characters/grak/rock_memory.py
  --write` and the regenerated `ROCK_MEMORY.sha256` in the same PR.
- Paste the command output that proves the change in the PR body.

## What gets merged

Bug fixes with evidence, host dialect fixes that cite the host's documented
format, and small doctrine fixes. Features are out of scope unless agreed in an
issue first.

## Security

Do not report vulnerabilities in public issues. See [SECURITY.md](SECURITY.md).
