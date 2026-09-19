#requires -version 5.1
<#
cavestack setup (Windows native) - install the Grak agent, the grak-clone and
grak-builder subagents, and the /grak, /review, /team, /ship, /land commands
into supported AI coding hosts. No network, no bun, no node, no admin. Same
contract as ./setup.

The cage rule: never delete or edit a target without proof that we own it.
A target is ours when it is a reparse point (symlink) resolving into this repo,
when it carries the full provenance stamp (cavestack v<version> :: <hash12>), or
when it carries an exact cavestack-owned / cavestack-managed marker line. A mere
mention of the marker text elsewhere in a file is not proof. Everything else is
skipped and reported, never touched.
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
$OwnStampRegex = "cavestack v[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ :: [0-9a-f]+"
$OwnMarkerRegex = "(?m)^\s*(<!--\s*cavestack-(owned|managed)(\s*|:[^>]*?)-->\s*$|#\s*cavestack-(owned|managed)(\s*|:.*?)$)"
$AgentSrc = Join-Path $Root "characters\grak\grak-agent.md"
$CmdSrc = Join-Path $Root "characters\grak\commands"
$DigestSrc = Join-Path $Root "characters\grak\digest.md"
$CloneMissionSrc = Join-Path $Root "characters\grak\clone-mission.md"
$BuilderMissionSrc = Join-Path $Root "characters\grak\builder-mission.md"
$Commands = @("grak", "review", "team", "ship", "land")
$SupportDir = Join-Path $HOME ".cavestack"
$SupportMarker = ".cavestack-owned"
$SupportFiles = @(
  @{ Src = Join-Path $Root "characters\grak\GRAK.md";                          Dst = "GRAK.md" },
  @{ Src = Join-Path $Root "characters\grak\credentials\GRAK_CREDENTIALS.md"; Dst = "GRAK_CREDENTIALS.md" },
  @{ Src = Join-Path $Root "characters\grak\credentials\exam.py";             Dst = "exam.py" },
  @{ Src = Join-Path $Root "characters\grak\credentials\mcq_bank.json";       Dst = "mcq_bank.json" }
)

$VersionPath = Join-Path $Root "VERSION"
$script:Version = (Get-Content -LiteralPath $VersionPath -Raw).Trim()
$script:ManifestPath = Join-Path $Root "characters\grak\ROCK_MEMORY.sha256"
$script:ManifestHash = (Get-FileHash -LiteralPath $script:ManifestPath -Algorithm SHA256).Hash.ToLower()
$script:Hash12 = $script:ManifestHash.Substring(0, 12)

$AllHosts = @("claude", "cursor", "codex", "factory", "opencode", "kiro", "slate", "openclaw", "hermes", "gbrain")
$AutoHosts = @("claude", "cursor", "codex", "factory", "opencode", "kiro", "openclaw", "hermes", "gbrain")

$script:Counters = @{ Agents = 0; Clones = 0; Builders = 0; Commands = 0; Digests = 0; Support = 0; Removed = 0; Skipped = 0 }

# Every file this run lands is recorded and hashed into the install receipt
# after the payload, so a later --check can prove the installed state itself.
$script:Installed = New-Object System.Collections.Generic.List[string]
function Add-Installed([string]$Path) { $script:Installed.Add($Path) | Out-Null }

function Write-Receipt {
  $lines = New-Object System.Collections.Generic.List[string]
  $lines.Add("cavestack $($script:Version)")
  $lines.Add("sha256 $($script:ManifestHash)")
  foreach ($f in $script:Installed) {
    if (Test-Path -LiteralPath $f) {
      $h = (Get-FileHash -LiteralPath $f -Algorithm SHA256).Hash.ToLower()
      $lines.Add("file $h $f")
    }
  }
  Write-Utf8NoBom (Join-Path $SupportDir "ROCK_RECEIPT") (($lines -join "`n") + "`n")
}

function Write-Log([string]$Message) { if (-not $Quiet) { Write-Host $Message } }
function Die([string]$Message) { Write-Host "Error: $Message" -ForegroundColor Red; exit 1 }

function Write-Utf8NoBom([string]$Path, [string]$Text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

function Add-CaveStamp([string]$Target, [string]$Kind) {
  $stamp = if ($Kind -eq "toml") {
    "`n# cavestack v$($script:Version) :: $($script:Hash12)`n"
  } else {
    "`n<!-- cavestack v$($script:Version) :: $($script:Hash12) -->`n"
  }
  $text = [System.IO.File]::ReadAllText($Target) + $stamp
  Write-Utf8NoBom $Target $text
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

function Resolve-OwnedLink([string]$Path) {
  $p = $Path
  for ($i = 0; $i -lt 40; $i++) {
    if (-not (Test-Path -LiteralPath $p)) { return $null }
    $item = Get-Item -LiteralPath $p -Force
    if (-not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { break }
    $target = $item.Target
    if ($target -is [array]) { $target = $target[0] }
    if ([string]::IsNullOrWhiteSpace($target)) { return $null }
    $p = if ([IO.Path]::IsPathRooted($target)) { $target } else { Join-Path (Split-Path -Parent $p) $target }
  }
  try { return [IO.Path]::GetFullPath($p) } catch { return $null }
}

function Test-Owned([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return $false }
  $item = Get-Item -LiteralPath $Path -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    $resolved = Resolve-OwnedLink $Path
    if (-not $resolved) { return $false }
    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
    return $resolved.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase)
  }
  $text = [System.IO.File]::ReadAllText($Path)
  if ($text -match $OwnStampRegex) { return $true }
  return ($text -match $OwnMarkerRegex)
}

function Remove-LinkIfAny([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return }
  $item = Get-Item -LiteralPath $Path -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    Remove-Item -LiteralPath $Path -Force
  }
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
    Remove-LinkIfAny $target
    $content = "name = ""grak""`n" + "description = ""$desc""`n" + "developer_instructions = '''`n" + (Get-Body $AgentSrc) + "'''`n"
    Write-Utf8NoBom $target $content
    Add-CaveStamp $target "toml"
    Add-Installed $target
    $script:Counters.Agents++
    Write-Log "Installed agent: $target"
    return
  }

  $target = Join-Path $dir "grak.md"
  if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
    Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
    $script:Counters.Skipped++; return
  }
  Remove-LinkIfAny $target
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
  Add-CaveStamp $target "md"
  Add-Installed $target
  $script:Counters.Agents++
  Write-Log "Installed agent: $target"
}

function Install-Companion([string]$HostName, [string]$Name, [string]$MissionSrc, [string]$Mode) {
  $dir = Get-HostAgentsDir $HostName
  if (-not $dir) { return $false }
  New-Item -ItemType Directory -Force -Path $dir | Out-Null

  $desc = Get-FmValue $MissionSrc "description"
  $body = (Get-Body $AgentSrc) + "`n" + (Get-Body $MissionSrc)

  if ($HostName -eq "codex") {
    $target = Join-Path $dir "$Name.toml"
    if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
      Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
      $script:Counters.Skipped++; return $false
    }
    $sandbox = if ($Mode -eq "rw") { "workspace-write" } else { "read-only" }
    $escaped = $desc.Replace('"', '\"')
    Remove-LinkIfAny $target
    $content = "name = ""$Name""`n" + "description = ""$escaped""`n" + "sandbox_mode = ""$sandbox""`n" + "developer_instructions = '''`n" + $body + "'''`n"
    Write-Utf8NoBom $target $content
    Add-CaveStamp $target "toml"
    Add-Installed $target
    Write-Log "Installed companion: $target"
    return $true
  }

  $target = Join-Path $dir "$Name.md"
  if ((Test-Path -LiteralPath $target) -and -not (Test-Owned $target)) {
    Write-Log "Not registered (a file you own already uses the name; left untouched): $target"
    $script:Counters.Skipped++; return $false
  }
  Remove-LinkIfAny $target
  $head = "---`nname: $Name`ndescription: $desc`n"
  switch ($HostName) {
    "opencode" {
      if ($Mode -eq "ro") { $front = "---`ndescription: $desc`nmode: subagent`npermission:`n  edit: deny`n---`n" }
      else { $front = "---`ndescription: $desc`nmode: subagent`n---`n" }
      Write-Utf8NoBom $target ($front + $body)
    }
    "claude" {
      if ($Mode -eq "ro") { $front = $head + "model: inherit`ntools: Read, Grep, Glob, Bash`n---`n" }
      else { $front = $head + "model: inherit`n---`n" }
      Write-Utf8NoBom $target ($front + $body)
    }
    "factory" {
      if ($Mode -eq "ro") { $front = $head + "model: inherit`ntools: read-only`n---`n" }
      else { $front = $head + "model: inherit`n---`n" }
      Write-Utf8NoBom $target ($front + $body)
    }
    "cursor" {
      if ($Mode -eq "ro") { $front = $head + "model: inherit`nreadonly: true`n---`n" }
      else { $front = $head + "model: inherit`n---`n" }
      Write-Utf8NoBom $target ($front + $body)
    }
    "kiro" {
      Write-Utf8NoBom $target ($head + "---`n" + $body)
    }
  }
  Add-CaveStamp $target "md"
  Add-Installed $target
  Write-Log "Installed companion: $target"
  return $true
}

function Install-Clone([string]$HostName) {
  if (Install-Companion $HostName "grak-clone" $CloneMissionSrc "ro") { $script:Counters.Clones++ }
}

function Install-Builder([string]$HostName) {
  if (Install-Companion $HostName "grak-builder" $BuilderMissionSrc "rw") { $script:Counters.Builders++ }
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
    Remove-LinkIfAny $target
    $desc = Get-FmValue $src "description"
    if ($HostName -eq "opencode") {
      Write-Utf8NoBom $target ("---`ndescription: " + $desc + "`nagent: grak`n---`n" + (Get-Body $src))
    } else {
      Write-Utf8NoBom $target ("---`ndescription: " + $desc + "`n---`n" + (Get-Body $src))
    }
    Add-CaveStamp $target "md"
    Add-Installed $target
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
  Remove-LinkIfAny $target
  Copy-Item -LiteralPath $DigestSrc -Destination $target -Force
  Add-CaveStamp $target "md"
  Add-Installed $target
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
    $t = Join-Path $SupportDir $f.Dst
    Copy-Item -LiteralPath $f.Src -Destination $t -Force
    Add-Installed $t
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
  $receipt = Join-Path $SupportDir "ROCK_RECEIPT"
  if (Test-Path -LiteralPath $receipt) { Remove-Item -LiteralPath $receipt -Force }
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
    if ($HostName -eq "codex") {
      Uninstall-File (Join-Path $adir "grak.toml")
      Uninstall-File (Join-Path $adir "grak-clone.toml")
      Uninstall-File (Join-Path $adir "grak-builder.toml")
    } else {
      Uninstall-File (Join-Path $adir "grak.md")
      Uninstall-File (Join-Path $adir "grak-clone.md")
      Uninstall-File (Join-Path $adir "grak-builder.md")
    }
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
  $docsInstall = Join-Path $Root "docs\install"
  $docsInstallPs = Join-Path $Root "docs\install.ps1"
  $sources = @($AgentSrc, $CloneMissionSrc, $BuilderMissionSrc, $DigestSrc, $docsInstall, $docsInstallPs) + ($Commands | ForEach-Object { Join-Path $CmdSrc "$_.md" }) + ($SupportFiles | ForEach-Object { $_.Src }) + @((Join-Path $Root "characters\grak\rock_memory.py"), $script:ManifestPath)
  foreach ($f in $sources) {
    if (-not (Test-Path -LiteralPath $f)) { Write-Host "missing source: $f" -ForegroundColor Red; $fail = 1 }
  }
  if ($fail -eq 0) {
    if (-not ((Get-Content -LiteralPath $AgentSrc -Raw) -match "cavestack-owned")) { Write-Host "agent source missing ownership marker" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $DigestSrc -Raw) -match "cavestack-owned")) { Write-Host "digest source missing ownership marker" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $CloneMissionSrc -Raw) -match "cavestack-owned")) { Write-Host "clone mission source missing ownership marker" -ForegroundColor Red; $fail = 1 }
    if (-not (Get-FmValue $CloneMissionSrc "description")) { Write-Host "clone mission source missing description" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $CloneMissionSrc -Raw) -match "one clone of Grak")) { Write-Host "clone mission source missing clone duty" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $BuilderMissionSrc -Raw) -match "cavestack-owned")) { Write-Host "builder mission source missing ownership marker" -ForegroundColor Red; $fail = 1 }
    if (-not (Get-FmValue $BuilderMissionSrc "description")) { Write-Host "builder mission source missing description" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $BuilderMissionSrc -Raw) -match "one builder clone of Grak")) { Write-Host "builder mission source missing builder duty" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $docsInstall -Raw) -match "exec bash")) { Write-Host "docs/install must exec bash (setup is a bash script, sh may be dash)" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $docsInstall -Raw) -match "CAVESTACK_VERSION")) { Write-Host "docs/install must pin the release tag (CAVESTACK_VERSION)" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $docsInstallPs -Raw) -match "CAVESTACK_VERSION")) { Write-Host "docs/install.ps1 must pin the release tag (CAVESTACK_VERSION)" -ForegroundColor Red; $fail = 1 }
    if (-not ((Get-Content -LiteralPath $AgentSrc -Raw) -match "Ship fully finished code, fast")) { Write-Host "agent source missing finish doctrine" -ForegroundColor Red; $fail = 1 }
    foreach ($name in $Commands) {
      $f = Join-Path $CmdSrc "$name.md"
      if (-not (Get-FmValue $f "description")) { Write-Host "command $name missing description" -ForegroundColor Red; $fail = 1 }
      $raw = Get-Content -LiteralPath $f -Raw
      if (-not ($raw -match "cavestack-owned")) { Write-Host "command $name missing ownership marker" -ForegroundColor Red; $fail = 1 }
      if (-not ($raw -match "ARGUMENTS")) { Write-Host "command $name missing `$ARGUMENTS" -ForegroundColor Red; $fail = 1 }
    }
  }
  if ($fail -eq 0) {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if ($py) {
      & python (Join-Path $Root "characters\grak\rock_memory.py") --check --no-receipt
      if ($LASTEXITCODE -ne 0) { $fail = 1 }
    } else {
      Write-Host "check: python is required for the deep source check" -ForegroundColor Red
      $fail = 1
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
if (-not (Get-FmValue $CloneMissionSrc "description")) { Die "cannot read description from $CloneMissionSrc" }
if (-not (Get-FmValue $BuilderMissionSrc "description")) { Die "cannot read description from $BuilderMissionSrc" }

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
      if ($Uninstall) { Uninstall-Host "claude" } else { Install-Agent "claude"; Install-Clone "claude"; Install-Builder "claude"; Install-Commands "claude" }
    }
    { $_ -in @("openclaw", "hermes", "gbrain") } {
      if ($Uninstall) { Uninstall-Host $h } else { Install-Digest $h }
    }
    default {
      if ($Uninstall) { Uninstall-Host $h } else { Install-Agent $h; Install-Clone $h; Install-Builder $h; Install-Commands $h }
    }
  }
}

if (-not $Uninstall) { Write-Receipt }

if ($Uninstall) {
  Write-Host "cavestack uninstall complete."
  Write-Host "  removed:            $($script:Counters.Removed)"
  Write-Host "  skipped (not ours): $($script:Counters.Skipped)"
} else {
  Write-Host "cavestack ready ($TargetHost)."
  Write-Host "  agents installed:   $($script:Counters.Agents)"
  Write-Host "  clones installed:   $($script:Counters.Clones)"
  Write-Host "  builders installed: $($script:Counters.Builders)"
  Write-Host "  commands installed: $($script:Counters.Commands)"
  Write-Host "  digests installed:  $($script:Counters.Digests)"
  if ($script:Counters.Support -gt 0) { Write-Host "  record installed:   $SupportDir" }
  if ($script:Counters.Skipped -gt 0) { Write-Host "  skipped (not ours): $($script:Counters.Skipped)" }
  Write-Host "Open a new session. Tab to grak. Run /grak."
}
