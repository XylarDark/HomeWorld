# Start-AllAgents-InNewWindow.ps1 - Launch the agent company in a separate terminal window.
# Use this so the automation never runs in the chat/integrated terminal; it always runs in its own window.
# Output is captured to Saved/Logs/automation_terminal_capture.log; the window stays open until you close it.
#
# Usage: From project root, .\Tools\Start-AllAgents-InNewWindow.ps1 [same params as Start-AllAgents.ps1]
# All parameters are passed through to Run-AutomationWithCapture.ps1 (which runs Start-AllAgents.ps1 with tee + pause).

param(
    [int]$MaxFixRounds = 3,
    [switch]$NoRetryAfterFix,
    [switch]$NoPauseOnComplete,
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$scriptRoot = $PSScriptRoot
$commonScript = Join-Path $scriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")

$captureScript = Join-Path $scriptRoot "Run-AutomationWithCapture.ps1"
if (-not (Test-Path -LiteralPath $captureScript)) {
    Write-Error "Run-AutomationWithCapture.ps1 not found at $captureScript"
    exit 1
}

# Build PowerShell command; quote paths for cmd
$processArgs = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$captureScript`"",
    "-ProjectRoot", "`"$ProjectRoot`"",
    "-MaxFixRounds", $MaxFixRounds
)
if ($NoRetryAfterFix) { $processArgs += "-NoRetryAfterFix" }
if ($NoPauseOnComplete) { $processArgs += "-NoPauseOnComplete" }
if ($PromptFile) { $processArgs += "-PromptFile", "`"$PromptFile`"" }
if ($NoLaunchEditor) { $processArgs += "-NoLaunchEditor" }
if ($Model) { $processArgs += "-Model", $Model }
if ($AgentPath) { $processArgs += "-AgentPath", "`"$AgentPath`"" }
if ($SkipInstall) { $processArgs += "-SkipInstall" }
if ($Verbose) { $processArgs += "-Verbose" }

# Single-instance guard: avoid starting a second loop (two CLIs fighting over task list and Editor)
if (Test-AutomationLoopRunning) {
    Write-Host "Another automation loop is already running (Saved/Logs/automation_loop.lock). Close that window or wait for it to finish before starting a new one." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting agents in a new window. Output is captured to Saved/Logs/automation_terminal_capture.log; window stays open until you close it."
# Use cmd /k so that even if PowerShell crashes, the window stays open and you can see errors
$psCmd = "powershell " + ($processArgs -join " ")
$cmdArg = "cd /d `"$ProjectRoot`" && $psCmd"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", $cmdArg -WorkingDirectory $ProjectRoot
exit 0
