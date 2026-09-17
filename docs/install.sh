#!/bin/sh
# cavestack installer
#   curl -fsSL https://cavestack.jerkyjesse.com/install | sh
#   curl -fsSL https://cavestack.jerkyjesse.com/install | sh -s -- --host opencode
# No network beyond git; no bun, no node, no sudo.
set -e

REPO_URL="${CAVESTACK_REPO:-https://github.com/JerkyJesse/cavestack.git}"
DEST="${CAVESTACK_HOME:-$HOME/cavestack}"

command -v git >/dev/null 2>&1 || {
  echo "cavestack: git is required" >&2
  exit 1
}

if [ -d "$DEST/.git" ]; then
  echo "cavestack: refreshing $DEST"
  git -C "$DEST" pull --ff-only --quiet
else
  echo "cavestack: cloning into $DEST"
  mkdir -p "$(dirname "$DEST")"
  git clone --depth 1 --quiet "$REPO_URL" "$DEST"
fi

exec sh "$DEST/setup" "$@"
