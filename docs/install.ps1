# cavestack installer (Windows)
#   irm https://cavestack.jerkyjesse.com/install.ps1 | iex
# Override with env vars: CAVESTACK_REPO, CAVESTACK_HOME, CAVESTACK_HOST.
# No network beyond git; no bun, no node, no admin.
$ErrorActionPreference = "Stop"

$repo = if ($env:CAVESTACK_REPO) { $env:CAVESTACK_REPO } else { "https://github.com/JerkyJesse/cavestack.git" }
$dest = if ($env:CAVESTACK_HOME) { $env:CAVESTACK_HOME } else { Join-Path $HOME "cavestack" }
$hostArg = if ($env:CAVESTACK_HOST) { $env:CAVESTACK_HOST } else { "auto" }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "cavestack: git is required" -ForegroundColor Red
  exit 1
}

if (Test-Path (Join-Path $dest ".git")) {
  Write-Host "cavestack: refreshing $dest"
  git -C $dest pull --ff-only --quiet
} else {
  Write-Host "cavestack: cloning into $dest"
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
  git clone --depth 1 --quiet $repo $dest
}

& (Join-Path $dest "setup.ps1") -TargetHost $hostArg
