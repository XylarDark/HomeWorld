# RunTests.ps1 - Run UE automation tests and optional asset validation.
# Run from project root: .\Tools\RunTests.ps1 [-Group Smoke] [-ValidateAssets]
# Requires: $env:UE_EDITOR set to UnrealEditor.exe path; run with Editor closed for headless.

param(
    [string]$Group = "Smoke",
    [switch]$ValidateAssets
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot + "\.."
$PythonScript = Join-Path $ProjectRoot "Content\Python\run_ue_automation.py"

if (-not (Test-Path $PythonScript)) {
    Write-Error "run_ue_automation.py not found at $PythonScript"
    exit 1
}

Push-Location $ProjectRoot
try {
    if ($ValidateAssets) {
        Write-Host "Asset validation runs in Editor; use Tools > Execute Python Script validate_assets.py, or run orchestrator with --task."
    }
    & python $PythonScript --group $Group
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
