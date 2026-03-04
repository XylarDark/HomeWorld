# Append-AgentRunRecord.ps1 - Appends one NDJSON record to Saved/Logs/agent_run_history.ndjson
# for strategy refinement and rule updates. Merge in agent_feedback_this_run.json if present.
#
# Usage: .\Tools\Append-AgentRunRecord.ps1 -ProjectRoot <path> -Role main|fix|loop_breaker -Round <n> -ExitCode <code> [-ErrorSummary <text>] [-TriggerExitCode <code>]
#   -SuggestedRuleUpdate / -SuggestedStrategy: optional; also read from Saved/Logs/agent_feedback_this_run.json when Role is fix or loop_breaker.

param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][ValidateSet("main","fix","loop_breaker")][string]$Role,
    [Parameter(Mandatory=$true)][int]$Round,
    [Parameter(Mandatory=$true)][int]$ExitCode,
    [string]$ErrorSummary = "",
    [Nullable[int]]$TriggerExitCode = $null,
    [string]$SuggestedRuleUpdate = "",
    [string]$SuggestedStrategy = ""
)

$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$LogsDir = Join-Path (Join-Path $ProjectRoot "Saved") "Logs"
$HistoryPath = Join-Path $LogsDir "agent_run_history.ndjson"
$FeedbackPath = Join-Path $LogsDir "agent_feedback_this_run.json"

if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }

# Merge agent-written feedback when present (fix and loop_breaker runs)
if ($Role -in "fix","loop_breaker" -and (Test-Path -LiteralPath $FeedbackPath)) {
    try {
        $fb = Get-Content -Path $FeedbackPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($fb.PSObject.Properties["suggested_rule_update"] -and $fb.suggested_rule_update) { $SuggestedRuleUpdate = $fb.suggested_rule_update.ToString().Trim() }
        if ($fb.PSObject.Properties["suggested_strategy"] -and $fb.suggested_strategy) { $SuggestedStrategy = $fb.suggested_strategy.ToString().Trim() }
    } catch {}
    Remove-Item -LiteralPath $FeedbackPath -Force -ErrorAction SilentlyContinue
}

# Keep one line per record: collapse newlines in text fields
$ErrorSummary = ($ErrorSummary -replace "[\r\n]+", " ").Trim()
if ($ErrorSummary.Length -gt 800) { $ErrorSummary = $ErrorSummary.Substring(0, 800) }
$SuggestedRuleUpdate = ($SuggestedRuleUpdate -replace "[\r\n]+", " ").Trim()
if ($SuggestedRuleUpdate.Length -gt 500) { $SuggestedRuleUpdate = $SuggestedRuleUpdate.Substring(0, 500) }
$SuggestedStrategy = ($SuggestedStrategy -replace "[\r\n]+", " ").Trim()
if ($SuggestedStrategy.Length -gt 500) { $SuggestedStrategy = $SuggestedStrategy.Substring(0, 500) }

$ts = Get-Date -Format "o"
$record = @{
    ts = $ts
    role = $Role
    round = $Round
    exit_code = $ExitCode
    error_summary = if ($ErrorSummary) { $ErrorSummary } else { $null }
    trigger_exit_code = if ($TriggerExitCode -ne $null) { $TriggerExitCode } else { $null }
    suggested_rule_update = if ($SuggestedRuleUpdate) { $SuggestedRuleUpdate } else { $null }
    suggested_strategy = if ($SuggestedStrategy) { $SuggestedStrategy } else { $null }
}
$line = $record | ConvertTo-Json -Compress
Add-Content -Path $HistoryPath -Value $line -Encoding UTF8
