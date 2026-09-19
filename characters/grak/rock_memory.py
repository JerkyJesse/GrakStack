#!/usr/bin/env python3
"""rock_memory.py - Grak's rock memory: the hash manifest for the shipped sources.

--write   regenerate ROCK_MEMORY.sha256 over every file the installers ship
--check   verify the repo against the manifest; when an install receipt exists
          (~/.cavestack/ROCK_RECEIPT, CAVESTACK_HOME overrides), report the
          record current or stale (--no-receipt skips the record check)

Digests normalize CRLF to LF, so the manifest verifies on any checkout.

Stdlib only. No network. No deps.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MANIFEST = HERE / "ROCK_MEMORY.sha256"
RECEIPT = (
    Path(os.environ.get("CAVESTACK_HOME", str(Path.home() / ".cavestack")))
    / "ROCK_RECEIPT"
)

SOURCES = (
    "VERSION",
    "characters/grak/grak-agent.md",
    "characters/grak/clone-mission.md",
    "characters/grak/builder-mission.md",
    "characters/grak/digest.md",
    "characters/grak/GRAK.md",
    "characters/grak/rock_memory.py",
    "characters/grak/commands/grak.md",
    "characters/grak/commands/review.md",
    "characters/grak/commands/team.md",
    "characters/grak/commands/ship.md",
    "characters/grak/commands/land.md",
    "characters/grak/credentials/GRAK_CREDENTIALS.md",
    "characters/grak/credentials/exam.py",
    "characters/grak/credentials/mcq_bank.json",
)


def digest(path):
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def manifest_digest():
    return hashlib.sha256(MANIFEST.read_bytes()).hexdigest()


def read_version():
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def write_manifest():
    lines = []
    for rel in SOURCES:
        path = ROOT / rel
        if not path.is_file():
            print("rock-memory: missing source: %s" % rel, file=sys.stderr)
            return 1
        lines.append("%s  %s" % (digest(path), rel))
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print(
        "rock-memory: wrote %s (%d files, v%s)"
        % (MANIFEST.name, len(lines), read_version())
    )
    return 0


def check_manifest():
    if not MANIFEST.is_file():
        print("rock-memory: manifest missing: %s" % MANIFEST, file=sys.stderr)
        return 1
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            print("rock-memory: bad manifest line: %r" % line, file=sys.stderr)
            return 1
        expected[parts[1].strip()] = parts[0].strip()
    ok = True
    for rel in SOURCES:
        want = expected.get(rel)
        path = ROOT / rel
        if want is None:
            print("rock-memory: %s not in manifest" % rel, file=sys.stderr)
            ok = False
            continue
        if not path.is_file():
            print("rock-memory: missing file: %s" % rel, file=sys.stderr)
            ok = False
            continue
        got = digest(path)
        if got != want:
            print("rock-memory: changed: %s" % rel, file=sys.stderr)
            ok = False
    if ok:
        print("rock-memory: %d files verified against %s" % (len(SOURCES), MANIFEST.name))
    return 0 if ok else 1


def check_receipt():
    if not RECEIPT.is_file():
        print("record: none (%s)" % RECEIPT)
        return 0
    version = ""
    manifest_hash = ""
    for line in RECEIPT.read_text(encoding="utf-8").splitlines():
        if line.startswith("cavestack "):
            version = line.split(None, 1)[1].strip()
        elif line.startswith("sha256 "):
            manifest_hash = line.split(None, 1)[1].strip()
    current_version = read_version()
    current_hash = manifest_digest()
    if version == current_version and manifest_hash == current_hash:
        print("record: current (v%s)" % current_version)
        return 0
    print(
        "record: STALE - installed v%s, repo v%s; re-run setup"
        % (version or "?", current_version),
        file=sys.stderr,
    )
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Grak rock memory: the hash manifest for the shipped sources."
    )
    parser.add_argument("--write", action="store_true", help="regenerate ROCK_MEMORY.sha256")
    parser.add_argument("--check", action="store_true", help="verify the repo against the manifest")
    parser.add_argument(
        "--no-receipt",
        action="store_true",
        help="skip the installed-record check; repo sources only",
    )
    args = parser.parse_args()
    if args.write:
        return write_manifest()
    if args.check:
        if check_manifest() != 0:
            return 1
        if args.no_receipt:
            return 0
        return check_receipt()
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
