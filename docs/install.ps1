# cavestack installer (Windows)
#   irm https://cavestack.jerkyjesse.com/install.ps1 | iex
#
# Pinned and verified: checks out the released tag, then verifies the checkout
# against the release's published SHA256SUMS asset before setup runs. Needs git;
# no bun, no node, no admin.
#
# Overrides: CAVESTACK_REPO, CAVESTACK_HOME (clone destination),
# CAVESTACK_HOST, CAVESTACK_VERSION (release tag), CAVESTACK_CHECKSUMS (path or
# URL of SHA256SUMS), CAVESTACK_RELEASE_BASE (release download base).
$ErrorActionPreference = "Stop"

function Die([string]$Message) {
  Write-Host "cavestack: $Message" -ForegroundColor Red
  exit 1
}

$repo = if ($env:CAVESTACK_REPO) { $env:CAVESTACK_REPO } else { "https://github.com/JerkyJesse/cavestack.git" }
$dest = if ($env:CAVESTACK_HOME) { $env:CAVESTACK_HOME } else { Join-Path $HOME "cavestack" }
$hostArg = if ($env:CAVESTACK_HOST) { $env:CAVESTACK_HOST } else { "claude" }
$version = if ($env:CAVESTACK_VERSION) { $env:CAVESTACK_VERSION } else { "v3.6.0.0" }
$releaseBase = if ($env:CAVESTACK_RELEASE_BASE) { $env:CAVESTACK_RELEASE_BASE } else { "https://github.com/JerkyJesse/cavestack/releases/download" }
$checksums = if ($env:CAVESTACK_CHECKSUMS) { $env:CAVESTACK_CHECKSUMS } else { "$releaseBase/$version/SHA256SUMS" }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Die "git is required"
}

if (Test-Path (Join-Path $dest ".git")) {
  Write-Host "cavestack: updating $dest to $version"
  git -C $dest fetch --depth 1 --quiet origin "refs/tags/${version}:refs/tags/${version}"
  if ($LASTEXITCODE -ne 0) { Die "git fetch failed ($LASTEXITCODE)" }
  git -C $dest checkout --quiet --detach "refs/tags/$version"
  if ($LASTEXITCODE -ne 0) { Die "git checkout failed ($LASTEXITCODE)" }
} else {
  Write-Host "cavestack: cloning $version into $dest"
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
  git clone --depth 1 --branch $version --quiet $repo $dest
  if ($LASTEXITCODE -ne 0) { Die "git clone failed ($LASTEXITCODE)" }
}

$actualCommit = (& git -C $dest rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { Die "git rev-parse failed ($LASTEXITCODE)" }

if ($checksums -match '^https?://') {
  $sumsFile = Join-Path ([IO.Path]::GetTempPath()) "cavestack-checksums-$PID"
  try {
    Invoke-WebRequest -UseBasicParsing -Uri $checksums -OutFile $sumsFile
  } catch {
    Die "cannot fetch release checksums for ${version}: $checksums"
  }
} else {
  $sumsFile = $checksums
  if (-not (Test-Path -LiteralPath $sumsFile)) { Die "checksums file not found: $sumsFile" }
}

$expectedCommit = $null
$expectedManifest = $null
foreach ($line in Get-Content -LiteralPath $sumsFile) {
  $trimmed = $line.Trim()
  if (-not $trimmed -or $trimmed.StartsWith("#")) { continue }
  $parts = $trimmed -split '\s+', 2
  if ($parts.Count -eq 2 -and $parts[1] -eq $version) { $expectedCommit = $parts[0] }
  if ($parts.Count -eq 2 -and $parts[1] -eq "ROCK_MEMORY.sha256") { $expectedManifest = $parts[0] }
}
if (-not $expectedCommit) { Die "SHA256SUMS has no commit line for $version" }
if (-not $expectedManifest) { Die "SHA256SUMS has no ROCK_MEMORY.sha256 line" }

if ($actualCommit -ne $expectedCommit) {
  Die "commit mismatch - expected $expectedCommit, actual $actualCommit"
}
$manifestPath = Join-Path $dest "characters\grak\ROCK_MEMORY.sha256"
$actualManifest = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLower()
if ($actualManifest -ne $expectedManifest.ToLower()) {
  Die "manifest mismatch - expected $expectedManifest, actual $actualManifest"
}

Write-Host "cavestack: verified $version ($actualCommit)"
& (Join-Path $dest "setup.ps1") -TargetHost $hostArg
