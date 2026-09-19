#!/usr/bin/env python3
"""make_checksums.py - build the release SHA256SUMS asset.

usage: python3 tools/make_checksums.py v3.6.0.0 > SHA256SUMS

The file carries the two values the installers verify before setup runs: the
sha256 of ROCK_MEMORY.sha256 and the tag's commit sha. Attach the output to the
GitHub release; docs/install and docs/install.ps1 fetch it from there.

Stdlib only. No network. No deps.
"""

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv):
    if len(argv) != 2:
        print("usage: make_checksums.py <tag>", file=sys.stderr)
        return 2
    tag = argv[1]
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "refs/tags/%s^{commit}" % tag],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("make_checksums: tag not found: %s" % tag, file=sys.stderr)
        return 1
    commit = result.stdout.strip()
    manifest = ROOT / "characters/grak/ROCK_MEMORY.sha256"
    manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()
    print("# grakstack release checksums")
    print("%s  ROCK_MEMORY.sha256" % manifest_hash)
    print("%s  %s" % (commit, tag))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
