# AgentRoles.ps1 - Single source of truth for the agent role cards.
#
# Run from project root:
#   .\Tools\AgentRoles.ps1            # check only (read-only, default)
#   .\Tools\AgentRoles.ps1 -Check     # same thing, explicit
#   .\Tools\AgentRoles.ps1 -Sync      # regenerate the derived copies
#
# WHY: the same 15 role cards are kept in three places:
#   .cursor/agents/<name>.md   <- SOURCE OF TRUTH
#   swarm/agents/<name>.md     <- derived; normalized content must match the source
#   .codex/agents/<name>.toml  <- derived, same content in Codex's TOML shape
#
# These were hand-maintained with no generator, and they had already drifted:
# swarm/agents/ was missing verifier.md. This script makes the drift visible
# instead of letting it accumulate.
#
# -Check writes nothing and exits 1 when the derived copies disagree with the
# source. -Sync rewrites them from the source; it never edits the source.
#
# Exit codes: 0 = in sync (or -Sync completed); 1 = drift found (check only);
#             2 = bad input (unreadable source, or a body containing ''' which
#             cannot be represented in the TOML literal multiline form).

param(
    [switch]$Check,
    [switch]$Sync
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

$SrcDir  = Join-Path $Root '.cursor\agents'
$SwarmDir = Join-Path $Root 'swarm\agents'
$CodexDir = Join-Path $Root '.codex\agents'

if ($Check -and $Sync) { Write-Error 'Use either -Check or -Sync, not both.'; exit 2 }
if (-not $Sync) { $Check = $true }   # read-only is the default

# Parse the two-line frontmatter the role cards use.
function Read-RoleCard {
    param([string]$Path)
    $lines = [System.IO.File]::ReadAllLines($Path)
    if ($lines.Count -lt 3 -or $lines[0] -ne '---') {
        throw "no frontmatter: $Path"
    }
    $name = $null; $desc = $null
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -eq '---') { break }
        if ($lines[$i] -match '^name:\s*(.+)$')      { $name = $Matches[1].Trim() }
        if ($lines[$i] -match '^description:\s*(.+)$') { $desc = $Matches[1].Trim() }
    }
    if (-not $name) { throw "no name in frontmatter: $Path" }
    # Body starts after the closing --- and the blank line. The committed .toml
    # cards begin straight at the first body line, so the blank line is dropped.
    $bodyStart = $i + 1
    while ($bodyStart -lt $lines.Count -and $lines[$bodyStart] -eq '') { $bodyStart++ }
    [pscustomobject]@{
        Name = $name
        Desc = $desc
        Body = (($lines[$bodyStart..($lines.Count - 1)] -join "`n").TrimEnd("`n"))
        Raw  = [System.IO.File]::ReadAllText($Path)
    }
}

function ConvertTo-CodexToml {
    param($Card, [string]$Path)
    # Literal multiline strings (''') keep backslashes as characters. Basic
    # strings (""") treat \b as backspace and reject \P, which corrupts a
    # Windows path such as C:\Program Files\... or .\Tools\Safe-Build.ps1.
    if ($Card.Body.Contains("'''")) {
        throw "body contains a triple single-quote and cannot be emitted as a TOML literal: $Path"
    }
    $desc = if ($Card.Desc) { $Card.Desc } else { '' }
    $desc = $desc.Replace('\', '\\').Replace('"', '\"')
    $name = $Card.Name.Replace('\', '\\').Replace('"', '\"')
    $q = '"'
    $lit = "'"
    $out = New-Object System.Text.StringBuilder
    # LF only, no BOM, with a trailing newline.
    [void]$out.Append('name = ' + $q + $name + $q + "`n")
    [void]$out.Append('description = ' + $q + $desc + $q + "`n")
    [void]$out.Append('developer_instructions = ' + ($lit * 3) + "`n")
    [void]$out.Append($Card.Body)
    [void]$out.Append(($lit * 3) + "`n")
    $out.ToString()
}

# A drift check should answer "has the CONTENT drifted", not "does the
# whitespace match". Normalising both sides means legacy formatting quirks in
# the committed cards do not read as false drift, while a real edit to a role
# card still trips the check.
function Get-Normalized {
    param([string]$Text)
    if ($null -eq $Text) { return '' }
    $t = $Text -replace "`r`n", "`n" -replace "`r", "`n"
    $t = ($t -split "`n" | ForEach-Object { $_.TrimEnd() }) -join "`n"
    return $t.Trim("`n")
}

if (-not (Test-Path $SrcDir)) { Write-Error "source dir missing: $SrcDir"; exit 2 }

$Cards = @(Get-ChildItem -Path $SrcDir -Filter '*.md' -File |
           Where-Object { $_.Name -ne 'README.md' } |
           Sort-Object Name)

if ($Cards.Count -eq 0) { Write-Error "no role cards found in $SrcDir"; exit 2 }

$Drift = New-Object System.Collections.ArrayList

foreach ($card in $Cards) {
    $parsed = $null
    try { $parsed = Read-RoleCard -Path $card.FullName }
    catch { Write-Error $_.Exception.Message; exit 2 }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($card.Name)

    # 1. swarm must match the source once line endings and trailing spaces are folded
    $swarmPath = Join-Path $SwarmDir "$base.md"
    if (-not (Test-Path $swarmPath)) {
        [void]$Drift.Add("swarm/agents/$base.md  MISSING")
    } else {
        $swarmRaw = [System.IO.File]::ReadAllText($swarmPath)
        if ((Get-Normalized $swarmRaw) -cne (Get-Normalized $parsed.Raw)) {
            [void]$Drift.Add("swarm/agents/$base.md  DIFFERS from source")
        }
    }

    # 2. codex must be the TOML rendering of the same card
    $codexPath = Join-Path $CodexDir "$base.toml"
    if (-not (Test-Path $codexPath)) {
        [void]$Drift.Add(".codex/agents/$base.toml  MISSING")
    } else {
        $expected = $null
        try { $expected = ConvertTo-CodexToml -Card $parsed -Path $codexPath }
        catch { Write-Error $_.Exception.Message; exit 2 }
        $actual = [System.IO.File]::ReadAllText($codexPath)
        if ((Get-Normalized $actual) -cne (Get-Normalized $expected)) {
            [void]$Drift.Add(".codex/agents/$base.toml  DIFFERS from source")
        }
    }
}

if ($Sync) {
    foreach ($card in $Cards) {
        $parsed = Read-RoleCard -Path $card.FullName
        $base = [System.IO.Path]::GetFileNameWithoutExtension($card.Name)
        foreach ($dir in @($SwarmDir, $CodexDir)) {
            if (-not (Test-Path $dir)) { [void](New-Item -ItemType Directory -Path $dir -Force) }
        }
        $swarmPath = Join-Path $SwarmDir "$base.md"
        $codexPath = Join-Path $CodexDir "$base.toml"
        if (-not (Test-Path $swarmPath) -or
            [System.IO.File]::ReadAllText($swarmPath) -cne $parsed.Raw) {
            [System.IO.File]::WriteAllText($swarmPath, $parsed.Raw, (New-Object System.Text.UTF8Encoding($false)))
            "synced swarm/agents/$base.md"
        }
        $expected = ConvertTo-CodexToml -Card $parsed -Path $codexPath
        if (-not (Test-Path $codexPath) -or
            [System.IO.File]::ReadAllText($codexPath) -cne $expected) {
            [System.IO.File]::WriteAllText($codexPath, $expected, (New-Object System.Text.UTF8Encoding($false)))
            "synced .codex/agents/$base.toml"
        }
    }
    "sync complete: $($Cards.Count) role cards from .cursor/agents"
    exit 0
}

if ($Drift.Count -gt 0) {
    "Agent role trees have DRIFTED from .cursor/agents ($($Drift.Count) problem(s)):"
    foreach ($d in $Drift) { "  $d" }
    ""
    "Run .\Tools\AgentRoles.ps1 -Sync to regenerate the derived copies."
    "Check only. Nothing was written."
    exit 1
}

"Agent role trees are in sync: $($Cards.Count) cards, source .cursor/agents"
exit 0