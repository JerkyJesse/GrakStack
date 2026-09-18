#requires -version 5.1
<#
cavestack setup (Windows native) - install the Grak agent and the /grak, /review,
/ship, /land commands into supported AI coding hosts. No network, no bun, no node,
no admin. Same contract as ./setup.

The cage rule: never delete or edit a target without proof that we own it.
A target is ours when it is a reparse point (symlink) resolving into this repo, or
a file carrying the cavestack-owned marker (the legacy cavestack-managed marker
also counts). Everything else is skipped and reported, never touched.
#>
[CmdletBinding()]
param(
  [string]$TargetHost = "claude",
  [switch]$Uninstall,
  [switch]$Check,
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$OwnRegex = "cavestack-(owned|managed)"
$AgentSrc = Join-Path $Root "characters\grak\grak-agent.md"
$CmdSrc = Join-Path $Root "characters\grak\commands"
$Commands = @("grak", "review", "ship", "land")
$SupportDir = Join-Path $HOME ".cavestack"
$SupportMarker = ".cavestack-owned"
$SupportFiles = @(
  @{ Src = Join-Path $Root "characters\grak\GRAK.md";                          Dst = "GRAK.md" },
  @{ Src = Join-Path $Root "characters\grak\credentials\GRAK_CREDENTIALS.md"; Dst = "GRAK_CREDENTIALS.md" },
  @{ Src = Join-Path $Root "characters\grak\credentials\exam.py";             Dst = "exam.py" },
  @{ Src = Join-Path $Root "characters\grak\credentials\mcq_bank.json";       Dst = "mcq_bank.json" }
)
$AllHosts = @("claude", "cursor", "codex", "factory", "opencode", "kiro", "slate", "openclaw", "hermes", "gbrain")
$AutoHosts = @("claude", "cursor", "codex", "factory", "opencode", "kiro", "openclaw", "hermes", "gbrain")

$script:Counters = @{ Agents = 0; Commands = 0; Digests = 0; Support = 0; Removed = 0; Skipped = 0 }

function Write-Log([string]$Message) { if (-not $Quiet) { Write-Host $Message } }
function Die([string]$Message) { Write-Host "Error: $Message" -ForegroundColor Red; exit 1 }

function Write-Utf8NoBom([string]$Path, [string]$Text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

function Get-Body([string]$Path) {
  $text = [System.IO.File]::ReadAllText($Path)
  $m = [regex]::Match($text, "(?s)\A---\r?\n.*?\r?\n---\r?\n")
  if ($m.Success) { return $text.Substring($m.Length) }
  return $text
}

function Get-FmValue([string]$Path, [string]$Key) {
  $text = [System.IO.File]::ReadAllText($Path)
  $m = [regex]::Match($text, "(?m)^" + [regex]::Escape($Key) + ":\s*(.+)$")
  if ($m.Success) { return $m.Groups[1].Value.Trim().Trim('"') }
  return ""
}

function Test-Owned([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return $false }
  $item = Get-Item -LiteralPath $Path -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { return $true }
  return (([System.IO.File]::ReadAllText($Path)) -match $OwnRegex)
}

function Get-HostConfigDir([string]$HostName) {
  switch ($HostName) {
    "claude"   { Join-Path $HOME ".claude" }
    "cursor"   { Join-Path $HOME ".cursor" }
    "codex"    { if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" } }
    "factory"  { Join-Path $HOME ".factory" }
    "opencode" { Join-Path $HOME ".config\opencode" }
    "kiro"     { Join-Path $HOME ".kiro" }
    "openclaw" { Join-Path $HOME ".openclaw" }
    "hermes"   { Join-Path $HOME ".hermes" }
    "gbrain"   { Join-Path $HOME ".gbrain" }
    default    { "" }
  }
}

function Get-HostAgentsDir([string]$HostName) {
  switch ($HostName) {
    "claude"   { Join-Path $HOME ".claude\agents" }
    "cursor"   { Join-Path $HOME ".cursor\agents" }
    "codex"    { if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "agents" } else { Join-Path $HOME ".codex\agents" } }
    "factory"  { Join-Path $HOME ".factory\droids" }
    "opencode" { Join-Path $HOME ".config\opencode\agent" }
    "kiro"     { Join-Path $HOME ".kiro\agents" }
    default    { "" }
  }
}

function Get-HostCommandsDir([string]$HostName) {
  switch ($HostName) {
    "claude"   { Join-Path $HOME ".claude\commands" }
    "cursor"   { Join-Path $HOME ".cursor\commands" }
    "codex"    { if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "prompts" } else { Join-Path $HOME ".codex\prompts" } }
    "factory"  { Join-Path $HOME ".factory\commands" }
    "opencode" { Join-Path $HOME ".config\opencode\command" }
    default    { "" }
  }
}

function Get-HostDigestDir([string]$HostName) {
  switch ($HostName) {
    "openclaw" { Join-Path $HOME ".openclaw\skills\cavestack" }
    "hermes"   { Join-Path $HOME ".hermes\skills\cavestack" }
    "gbrain"   { Join-Path $HOME ".gbrain\skills\cavestack" }
    default    { "" }
  }
}

function Install-Agent([string]$HostName) {
  $dir = Get-HostAgentsDir $HostName
  if (-not $dir) { return }
  New-Item -ItemType Directory -Force -Path $dir | Out-Null

  if ($HostName -eq "codex") {
    $target = Join-Path $dir "grak.toml"
    if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
      Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
      $script:Counters.Skipped++; return
    }
    $desc = $script:AgentDesc.Replace('"', '\"')
    $content = "name = ""grak""`n" + "description = ""$desc""`n" + "developer_instructions = '''`n" + (Get-Body $AgentSrc) + "'''`n"
    Write-Utf8NoBom $target $content
    $script:Counters.Agents++
    Write-Log "Installed agent: $target"
    return
  }

  $target = Join-Path $dir "grak.md"
  if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
    Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
    $script:Counters.Skipped++; return
  }
  switch ($HostName) {
    "opencode" {
      Copy-Item -LiteralPath $AgentSrc -Destination $target -Force
    }
    "claude" {
      Write-Utf8NoBom $target ("---`nname: grak`ndescription: " + $script:AgentDesc + "`nmodel: inherit`n---`n" + (Get-Body $AgentSrc))
    }
    "factory" {
      Write-Utf8NoBom $target ("---`nname: grak`ndescription: " + $script:AgentDesc + "`nmodel: inherit`n---`n" + (Get-Body $AgentSrc))
    }
    "cursor" {
      Write-Utf8NoBom $target ("---`nname: grak`ndescription: " + $script:AgentDesc + "`n---`n" + (Get-Body $AgentSrc))
    }
    "kiro" {
      Write-Utf8NoBom $target ("---`nname: grak`ndescription: " + $script:AgentDesc + "`n---`n" + (Get-Body $AgentSrc))
    }
  }
  $script:Counters.Agents++
  Write-Log "Installed agent: $target"
}

function Install-Commands([string]$HostName) {
  $dir = Get-HostCommandsDir $HostName
  if (-not $dir) { return }
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  foreach ($name in $Commands) {
    $src = Join-Path $CmdSrc "$name.md"
    $target = Join-Path $dir "$name.md"
    if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
      Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
      $script:Counters.Skipped++; continue
    }
    $desc = Get-FmValue $src "description"
    if ($HostName -eq "opencode") {
      Write-Utf8NoBom $target ("---`ndescription: " + $desc + "`nagent: grak`n---`n" + (Get-Body $src))
    } else {
      Write-Utf8NoBom $target ("---`ndescription: " + $desc + "`n---`n" + (Get-Body $src))
    }
    $script:Counters.Commands++
    Write-Log "Installed command: $target"
  }
}

function Install-Digest([string]$HostName) {
  $dir = Get-HostDigestDir $HostName
  if (-not $dir) { return }
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $target = Join-Path $dir "SKILL.md"
  if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
    Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
    $script:Counters.Skipped++; return
  }
  $digest = @'
# cavestack (Grak) - digest

You are Grak. Terse like smart caveman. All technical substance stays; only fluff dies.
Ship fully finished code, fast. Finished means: compiles, runs, tests pass with
evidence, edge cases named, no stubs, no TODOs, no "phase 2". Evidence or it did not
happen: run it, paste the tails.
Credential rail: rank is flavor; a claim carries issuer and proof artifact; no artifact,
no claim. Domain task? Check the paper seed in the record first.
Record: ~/.cavestack/ (GRAK.md lore, GRAK_CREDENTIALS.md papers, exam.py).

The loop: /grak build, /review check, /ship push + PR, /land merge.
Full source and install: https://github.com/JerkyJesse/cavestack

<!-- cavestack-owned -->
'@
  $content = "---`nname: cavestack`ndescription: Grak - caveman build agent digest. Ultra-terse voice, finished code, four commands.`n---`n`n" + $digest
  Write-Utf8NoBom $target $content
  $script:Counters.Digests++
  Write-Log "Installed digest: $target"
}

function Install-Support {
  $marker = Join-Path $SupportDir $SupportMarker
  if ((Test-Path -LiteralPath $SupportDir) -and -not (Test-Path -LiteralPath $marker)) {
    if (Get-ChildItem -LiteralPath $SupportDir -Force -ErrorAction SilentlyContinue) {
      Write-Log "Not registered (a directory you own already uses the path; left untouched): $SupportDir"
      $script:Counters.Skipped++; return
    }
  }
  New-Item -ItemType Directory -Force -Path $SupportDir | Out-Null
  foreach ($f in $SupportFiles) {
    Copy-Item -LiteralPath $f.Src -Destination (Join-Path $SupportDir $f.Dst) -Force
  }
  Write-Utf8NoBom $marker "<!-- cavestack-owned -->`n"
  $script:Counters.Support++
  Write-Log "Installed record: $SupportDir (GRAK.md, GRAK_CREDENTIALS.md, exam.py, mcq_bank.json)"
}

function Uninstall-Support {
  $marker = Join-Path $SupportDir $SupportMarker
  if (-not (Test-Path -LiteralPath $marker)) {
    if (Test-Path -LiteralPath $SupportDir) {
      Write-Log "Kept (not ours): $SupportDir"
      $script:Counters.Skipped++
    }
    return
  }
  foreach ($f in $SupportFiles) {
    $t = Join-Path $SupportDir $f.Dst
    if (Test-Path -LiteralPath $t) { Remove-Item -LiteralPath $t -Force; $script:Counters.Removed++ }
  }
  Remove-Item -LiteralPath $marker -Force
  if (-not (Get-ChildItem -LiteralPath $SupportDir -Force -ErrorAction SilentlyContinue)) {
    Remove-Item -LiteralPath $SupportDir -Force
  }
  Write-Log "Removed record: $SupportDir"
}

function Uninstall-File([string]$Target) {
  if (-not (Test-Path -LiteralPath $Target)) { return }
  if (Test-Owned $Target) {
    Remove-Item -LiteralPath $Target -Force
    $script:Counters.Removed++
    Write-Log "Removed: $Target"
  } else {
    Write-Log "Kept (not ours): $Target"
    $script:Counters.Skipped++
  }
}

function Uninstall-Host([string]$HostName) {
  $adir = Get-HostAgentsDir $HostName
  if ($adir) {
    if ($HostName -eq "codex") { Uninstall-File (Join-Path $adir "grak.toml") }
    else { Uninstall-File (Join-Path $adir "grak.md") }
  }
  $cdir = Get-HostCommandsDir $HostName
  if ($cdir) {
    foreach ($name in $Commands) { Uninstall-File (Join-Path $cdir "$name.md") }
  }
  $ddir = Get-HostDigestDir $HostName
  if ($ddir) {
    Uninstall-File (Join-Path $ddir "SKILL.md")
    if ((Test-Path -LiteralPath $ddir) -and -not (Get-ChildItem -LiteralPath $ddir -Force)) {
      Remove-Item -LiteralPath $ddir -Force
    }
  }
}

function Invoke-Check {
  $fail = 0
  $sources = @($AgentSrc) + ($Commands | ForEach-Object { Join-Path $CmdSrc "$_.md" }) + ($SupportFiles | ForEach-Object { $_.Src })
  foreach ($f in $sources) {
    if (-not (Test-Path -LiteralPath $f)) { Write-Host "missing source: $f" -ForegroundColor Red; $fail = 1 }
  }
  if ($fail -eq 0) {
    if (-not ((Get-Content -LiteralPath $AgentSrc -Raw) -match "cavestack-owned")) { Write-Host "agent source missing ownership marker" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $AgentSrc -Raw) -match "Ship fully finished code, fast")) { Write-Host "agent source missing finish doctrine" -ForegroundColor Red; $fail = 1 }
    foreach ($name in $Commands) {
      $f = Join-Path $CmdSrc "$name.md"
      if (-not (Get-FmValue $f "description")) { Write-Host "command $name missing description" -ForegroundColor Red; $fail = 1 }
      $raw = Get-Content -LiteralPath $f -Raw
      if (-not ($raw -match "cavestack-owned")) { Write-Host "command $name missing ownership marker" -ForegroundColor Red; $fail = 1 }
      if (-not ($raw -match "ARGUMENTS")) { Write-Host "command $name missing `$ARGUMENTS" -ForegroundColor Red; $fail = 1 }
    }
  }
  if ($fail -eq 0) { Write-Host "cavestack: check ok" }
  else { exit 1 }
}

# ---------------------------------------------------------------- main

if ($Check) { Invoke-Check; exit 0 }

if ($AllHosts -notcontains $TargetHost -and $TargetHost -ne "all" -and $TargetHost -ne "auto") {
  Die "unknown -TargetHost value: $TargetHost (expected claude, cursor, codex, factory, opencode, kiro, slate, openclaw, hermes, gbrain, all, auto)"
}

$script:AgentDesc = Get-FmValue $AgentSrc "description"
if (-not $script:AgentDesc) { Die "cannot read description from $AgentSrc" }

$hosts = @()
switch ($TargetHost) {
  "all" { $hosts = $AllHosts }
  "auto" { $hosts = $AutoHosts | Where-Object { Test-Path -LiteralPath (Get-HostConfigDir $_) } }
  default { $hosts = @($TargetHost) }
}
if (-not $hosts) { Die "no hosts selected (nothing to do)" }

if ($Uninstall) { Uninstall-Support } else { Install-Support }

foreach ($h in $hosts) {
  switch ($h) {
    "slate" {
      $verb = if ($Uninstall) { "uninstalling" } else { "installing" }
      Write-Log "Slate reads Claude Code config; $verb claude instead."
      if ($Uninstall) { Uninstall-Host "claude" } else { Install-Agent "claude"; Install-Commands "claude" }
    }
    { $_ -in @("openclaw", "hermes", "gbrain") } {
      if ($Uninstall) { Uninstall-Host $h } else { Install-Digest $h }
    }
    default {
      if ($Uninstall) { Uninstall-Host $h } else { Install-Agent $h; Install-Commands $h }
    }
  }
}

if ($Uninstall) {
  Write-Host "cavestack uninstall complete."
  Write-Host "  removed:            $($script:Counters.Removed)"
  Write-Host "  skipped (not ours): $($script:Counters.Skipped)"
} else {
  Write-Host "cavestack ready ($TargetHost)."
  Write-Host "  agents installed:   $($script:Counters.Agents)"
  Write-Host "  commands installed: $($script:Counters.Commands)"
  Write-Host "  digests installed:  $($script:Counters.Digests)"
  if ($script:Counters.Support -gt 0) { Write-Host "  record installed:   $SupportDir" }
  if ($script:Counters.Skipped -gt 0) { Write-Host "  skipped (not ours): $($script:Counters.Skipped)" }
  Write-Host "Open a new session. Tab to grak. Run /grak."
}
