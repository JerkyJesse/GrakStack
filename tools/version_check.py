#!/usr/bin/env python3
"""version_check.py - one version story across every shipped surface.

The version declared in VERSION must agree with:

  CHANGELOG.md        the top release section
  docs/index.html     the JSON-LD softwareVersion
  docs/index.html     the footer label
  docs/install        the pinned release tag
  docs/install.ps1    the pinned release tag

Exit 0 when every surface agrees; exit 1 with each mismatch named.

Stdlib only. No network. No deps.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def first(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def main():
    version = read("VERSION").strip()
    if not version:
        print("version: VERSION is empty", file=sys.stderr)
        return 1
    index = read("docs/index.html")
    surfaces = (
        ("CHANGELOG.md top release", first(r"(?m)^## \[([0-9][0-9.]*)\]", read("CHANGELOG.md"))),
        ("docs/index.html softwareVersion", first(r'"softwareVersion":\s*"([^"]+)"', index)),
        ("docs/index.html footer", first(r"v([0-9][0-9.]*)\s*·\s*AGPL", index)),
        ("docs/install pin", first(r"CAVESTACK_VERSION:-v([0-9][0-9.]*)", read("docs/install"))),
        ("docs/install.ps1 pin", first(r'else \{ "v([0-9][0-9.]*)" \}', read("docs/install.ps1"))),
    )
    bad = False
    print("version: %s" % version)
    for name, value in surfaces:
        if value != version:
            print(
                "  MISMATCH %s: %s" % (name, value if value is not None else "not found"),
                file=sys.stderr,
            )
            bad = True
        else:
            print("  ok %s" % name)
    if bad:
        return 1
    print("version: all surfaces agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
