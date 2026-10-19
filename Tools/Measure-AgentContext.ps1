# Measure the standing agent-context catalogs.
# Prints skill and agent counts, description bytes / 4, continuity-file bytes,
# and rule bytes whose globs hit Tools, Content/Python, or docs.
# Does not read the Cursor context inspector. Record that separately on an empty chat.
# Run this after a rule glob or a skill description changes.
# Baseline snapshot is the comment block below, taken before the 2026-10-19 cuts.
#
# Inspector: not readable from this session. standingTok is the baseline.
# Baseline 2026-10-19 before cuts:
#   skills=237 skillTok=7814 agents=79 agentTok=3523 standingTok=11337
#   user .cursor/skills 72 skills / 1366 tok
#   user .agents/skills 98 skills / 2764 tok
#   user .cursor/skills-cursor 26 skills / 1404 tok
#   user .codex/skills 5 skills / 401 tok
#   project .agents/skills 27 skills / 1580 tok
#   project .cursor/skills 9 skills / 299 tok
#   user .cursor/agents 64 agents / 3066 tok
#   project .cursor/agents 15 agents / 457 tok
#   docs/SESSION_SUMMARY.md 152103 bytes
#   rule buckets Tools=16698 Python=18393 Docs=2837
# After 2026-10-19 cuts:
#   skills=130 skillTok=4157 agents=15 agentTok=457 standingTok=4614
#   drop vs baseline standingTok: 59% (11337 -> 4614)
#   SESSION_NOW.md 450 bytes; handoff + queue + SESSION_NOW = 9227 bytes
#   rule buckets Tools=0 Docs=0
#   user .agents/skills and .cursor/agents parked beside those folders
#   cursor/thirdPartyExtensibilityEnabled=false in state.vscdb (restart Cursor)
# After next-context cuts:
#   Cpp bucket 14719 -> 3804 (unreal-cpp.mdc only)
#   user .cursor/skills 0 (parked at ~/.cursor/skills-parked-2026-10-19)
#   standingTok 4614 -> 3238
# After harness-check (2026-10-19):
#   project .agents/skills 27 -> 28 (1013 tok)
#   standingTok 3248 -> 3275
param(
    [string]$RepoRoot = ""
)

$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}

function Get-FrontmatterDescription {
    param([string]$Path)
    $lines = Get-Content -LiteralPath $Path -TotalCount 40 -ErrorAction SilentlyContinue
    if (-not $lines) { return "" }
    $text = ($lines -join "`n")
    $match = [regex]::Match($text, '(?s)^---\s*\r?\n(.*?)\r?\n---')
    if (-not $match.Success) { return "" }
    $block = $match.Groups[1].Value
    $folded = [regex]::Match($block, '(?s)description:\s*>-?\s*\r?\n(.*?)(?:\r?\n[A-Za-z0-9_-]+:|\z)')
    if ($folded.Success -and $folded.Groups[1].Value.Trim().Length -gt 0) {
        $value = (($folded.Groups[1].Value -split '\r?\n') | ForEach-Object { $_.Trim() }) -join " "
        return $value.Trim()
    }
    $desc = [regex]::Match($block, '(?m)^description:\s*(.+)$')
    if (-not $desc.Success) { return "" }
    return $desc.Groups[1].Value.Trim().Trim('"')
}

$script:EmptyFolds = @()

function Test-EmptyFold {
    param([string]$Path)
    $lines = Get-Content -LiteralPath $Path -TotalCount 40 -ErrorAction SilentlyContinue
    if (-not $lines) { return }
    $text = ($lines -join "`n")
    $match = [regex]::Match($text, '(?s)^---\s*\r?\n(.*?)\r?\n---')
    if (-not $match.Success) { return }
    $block = $match.Groups[1].Value
    $isFold = [regex]::IsMatch($block, '(?m)^description:\s*[>|]')
    if (-not $isFold) { return }
    $desc = Get-FrontmatterDescription -Path $Path
    if ([string]::IsNullOrWhiteSpace($desc)) {
        $script:EmptyFolds += $Path
    }
}

function Measure-SkillTree {
    param([string]$Path)
    $result = [ordered]@{
        Path = $Path
        Exists = (Test-Path -LiteralPath $Path)
        Skills = 0
        DescriptionBytes = 0
    }
    if (-not $result.Exists) { return [pscustomobject]$result }
    $files = @(Get-ChildItem -LiteralPath $Path -Recurse -Filter SKILL.md -File -ErrorAction SilentlyContinue)
    $result.Skills = $files.Count
    $bytes = 0
    foreach ($file in $files) {
        Test-EmptyFold -Path $file.FullName
        $desc = Get-FrontmatterDescription -Path $file.FullName
        $bytes += [System.Text.Encoding]::UTF8.GetByteCount($desc)
    }
    $result.DescriptionBytes = $bytes
    return [pscustomobject]$result
}

function Measure-AgentTree {
    param([string]$Path)
    $result = [ordered]@{
        Path = $Path
        Exists = (Test-Path -LiteralPath $Path)
        Agents = 0
        DescriptionBytes = 0
    }
    if (-not $result.Exists) { return [pscustomobject]$result }
    $files = @(Get-ChildItem -LiteralPath $Path -Recurse -Filter *.md -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne "README.md" })
    $result.Agents = $files.Count
    $bytes = 0
    foreach ($file in $files) {
        $desc = Get-FrontmatterDescription -Path $file.FullName
        $bytes += [System.Text.Encoding]::UTF8.GetByteCount($desc)
    }
    $result.DescriptionBytes = $bytes
    return [pscustomobject]$result
}

function Get-RuleGlobs {
    param([string]$Path)
    $lines = Get-Content -LiteralPath $Path -TotalCount 20
    $text = ($lines -join "`n")
    $match = [regex]::Match($text, '(?m)^globs:\s*(.+)$')
    if (-not $match.Success) { return "" }
    return $match.Groups[1].Value.Trim().Trim('"')
}

$userProfile = $env:USERPROFILE
$trees = @(
    (Join-Path $userProfile ".cursor\skills"),
    (Join-Path $userProfile ".agents\skills"),
    (Join-Path $userProfile ".cursor\skills-cursor"),
    (Join-Path $userProfile ".codex\skills"),
    (Join-Path $RepoRoot ".agents\skills"),
    (Join-Path $RepoRoot ".cursor\skills")
)
$agentTrees = @(
    (Join-Path $userProfile ".cursor\agents"),
    (Join-Path $RepoRoot ".cursor\agents")
)

Write-Host "REPO $RepoRoot"
Write-Host "SKILLS"
$skillTokens = 0
$skillCount = 0
foreach ($tree in $trees) {
    $row = Measure-SkillTree -Path $tree
    $tokens = [math]::Round($row.DescriptionBytes / 4.0, 0)
    $skillTokens += $tokens
    $skillCount += $row.Skills
    "{0,6} skills  {1,7} desc-bytes  {2,6} tok  {3}" -f $row.Skills, $row.DescriptionBytes, $tokens, $row.Path
}

Write-Host "AGENTS"
$agentTokens = 0
$agentCount = 0
foreach ($tree in $agentTrees) {
    $row = Measure-AgentTree -Path $tree
    $tokens = [math]::Round($row.DescriptionBytes / 4.0, 0)
    $agentTokens += $tokens
    $agentCount += $row.Agents
    "{0,6} agents  {1,7} desc-bytes  {2,6} tok  {3}" -f $row.Agents, $row.DescriptionBytes, $tokens, $row.Path
}

Write-Host "CONTINUITY"
$continuity = @(
    "docs\SESSION_NOW.md",
    "docs\SESSION_SUMMARY.md",
    "docs\history\SESSION_LOG.md",
    "Docs\context\SESSION_START.md",
    "Docs\handoffs\SESSION_HANDOFF_TUTORIAL_DAY.md",
    "Docs\qa\TUTORIAL_PLAYTEST_QUEUE.md"
)
foreach ($rel in $continuity) {
    $path = Join-Path $RepoRoot $rel
    if (Test-Path -LiteralPath $path) {
        $len = (Get-Item -LiteralPath $path).Length
        "{0,8} bytes  {1}" -f $len, $rel
    } else {
        " MISSING  {0}" -f $rel
    }
}

function Test-CppSourceGlob {
    param([string]$Globs)
    foreach ($part in ($Globs -split ',')) {
        $g = $part.Trim().Trim('"').Trim("'")
        if ($g -eq '**/*.cpp') { return $true }
        if ($g -match 'Source/\*\*') { return $true }
    }
    return $false
}

Write-Host "RULES"
$rulesDir = Join-Path $RepoRoot ".cursor\rules"
$buckets = [ordered]@{ Tools = 0; Python = 0; Docs = 0; Cpp = 0 }
Get-ChildItem -LiteralPath $rulesDir -Filter *.mdc -File | ForEach-Object {
    $globs = Get-RuleGlobs -Path $_.FullName
    $hit = @()
    if ($globs -match 'Tools') { $buckets.Tools += $_.Length; $hit += "Tools" }
    if ($globs -match 'Content/Python') { $buckets.Python += $_.Length; $hit += "Python" }
    if ($globs -match 'docs/\*\*|Docs/\*\*') { $buckets.Docs += $_.Length; $hit += "Docs" }
    if (Test-CppSourceGlob -Globs $globs) { $buckets.Cpp += $_.Length; $hit += "Cpp" }
    if ($hit.Count -gt 0) {
        "{0,7} bytes  {1,-28} {2}" -f $_.Length, ($hit -join ","), $_.Name
    }
}
"bucket Tools={0} Python={1} Docs={2} Cpp={3}" -f $buckets.Tools, $buckets.Python, $buckets.Docs, $buckets.Cpp

Write-Host "STANDING"
$standing = $skillTokens + $agentTokens
"skills={0} skillTok={1} agents={2} agentTok={3} standingTok={4}" -f $skillCount, $skillTokens, $agentCount, $agentTokens, $standing

$failed = $false
if ($script:EmptyFolds.Count -gt 0) {
    Write-Host "FAIL empty folded description:"
    $script:EmptyFolds | ForEach-Object { Write-Host "  $_" }
    $failed = $true
}
$nowPath = Join-Path $RepoRoot "docs\SESSION_NOW.md"
if ((Test-Path -LiteralPath $nowPath) -and ((Get-Item -LiteralPath $nowPath).Length -gt 4000)) {
    Write-Host "FAIL docs/SESSION_NOW.md is over 4000 bytes"
    $failed = $true
}
if ($failed) { exit 1 }
