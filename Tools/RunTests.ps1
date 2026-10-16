# RunTests.ps1 - Run UE automation tests for this project.
# Run from project root: .\Tools\RunTests.ps1 [-Filter HomeWorld] [-ValidateAssets] [-IncludePythonTests]
# The filter is a test-name prefix; it defaults to HomeWorld, which is what this project's tests
# are named. UE "groups" match nothing here - a Group: selector ran zero tests, and a run that
# completes zero tests is an error - so the prefix is the selector, not the group. The Editor.Python
# tests are excluded from the verdict by default because they fail in-editor by construction; they
# are gated in validate.yml under host Python.
# Requires UE 5.8: a set-but-wrong $env:UE_EDITOR (this machine had 5.7) is replaced with the
# locked engine from the registry, and an unset one is resolved from it. Set it to point elsewhere
# only on a project that is not engine-locked.

param(
    [string]$Filter = "HomeWorld",
    [switch]$ValidateAssets,
    # Opt in to the Editor.Python tests. They fail in-editor by construction (see below) and one of
    # them fails on its own assertions under host Python, so they are excluded by default.
    [switch]$IncludePythonTests
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot + "\.."
$PythonScript = Join-Path $ProjectRoot "Content\Python\run_ue_automation.py"

if (-not (Test-Path $PythonScript)) {
    Write-Error "run_ue_automation.py not found at $PythonScript"
    exit 1
}

if ($LockDir = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\EpicGames\Unreal Engine\5.8' -Name InstalledDirectory -ErrorAction SilentlyContinue).InstalledDirectory) {
    $LockedEditor = Join-Path $LockDir "Engine\Binaries\Win64\UnrealEditor.exe"
    if (-not $env:UE_EDITOR) {
        # The runner refuses an editor that is not the locked engine (it caught 5.7 here), so resolve
        # the lock instead of guessing: same HKLM key Start-RiderMcp.ps1 preflights.
        $env:UE_EDITOR = $LockedEditor
        Write-Host "UE_EDITOR not set; resolved to $env:UE_EDITOR"
    } elseif ($env:UE_EDITOR -notlike "$LockDir*") {
        # A set-but-wrong UE_EDITOR only produces the runner's refusal, so prefer the lock and say so.
        Write-Warning "UE_EDITOR points at '$env:UE_EDITOR', not the locked UE 5.8 ('$LockDir'). run_ue_automation refuses it; using $LockedEditor instead."
        $env:UE_EDITOR = $LockedEditor
    }
} elseif (-not $env:UE_EDITOR) {
    Write-Error "UE_EDITOR is not set and UE 5.8 is not registered at HKLM:\SOFTWARE\EpicGames\Unreal Engine\5.8. Set UE_EDITOR to UnrealEditor.exe and re-run."
    exit 1
}

Push-Location $ProjectRoot
try {
    if ($ValidateAssets) {
        Write-Host "Asset validation runs in Editor; use Tools > Execute Python Script validate_assets.py, or run orchestrator with --task."
    }
    # UE runs Content/Python/tests/*.py as Editor.Python.* tests with __name__ == "__main__", so
    # their unittest.main() guard executes, discovers nothing, raises SystemExit, and UE reports
    # Fail - while the same suite is really gated in validate.yml under host Python (where
    # test_polish_readiness currently fails 5 assertions of its own). Keep it out of this verdict
    # unless asked for it; -IncludePythonTests needs pytest in the engine Python.
    $RunArgs = @('--filter', $Filter)
    if ($Filter -notlike 'Editor.Python*' -and -not $IncludePythonTests) {
        $RunArgs += @('--exclude', 'Editor.Python')
    }
    & python $PythonScript @RunArgs
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
