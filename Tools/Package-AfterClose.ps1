# Package-AfterClose.ps1 - Run Shipping build + Package-HomeWorld.bat after closing Editor.
# Use when Stage failed with "files in use": close Unreal Editor (and any HomeWorld game) first, then run this script.
# Does NOT kill processes; exits with instructions if UnrealEditor or HomeWorld is still running.
#
# Usage: From project root, .\Tools\Package-AfterClose.ps1 [-CleanStagedBuilds]
#   -CleanStagedBuilds: Remove Saved\StagedBuilds before packaging for a clean stage.
#
# Exit code: 0 = packaging completed (check Package-HomeWorld.log for RunUAT exit 0); non-zero = blocked or build/package failed.

param(
    [switch]$CleanStagedBuilds
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $null
if ($env:HOMEWORLD_PROJECT -and (Test-Path -LiteralPath $env:HOMEWORLD_PROJECT)) {
    $ProjectRoot = $env:HOMEWORLD_PROJECT.TrimEnd("\", "/")
}
if (-not $ProjectRoot) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
$UProject = Join-Path $ProjectRoot "HomeWorld.uproject"
$PackageBat = Join-Path $ProjectRoot "Package-HomeWorld.bat"
$StagedBuilds = Join-Path $ProjectRoot "Saved\StagedBuilds"
$BuildLog = Join-Path $ProjectRoot "Build-HomeWorld.log"
$PackageLog = Join-Path $ProjectRoot "Package-HomeWorld.log"

$UE_ROOT = $env:UE_ROOT
if (-not $UE_ROOT) { $UE_ROOT = "C:\Program Files\Epic Games\UE_5.7" }
$BuildBat = Join-Path $UE_ROOT "Engine\Build\BatchFiles\Build.bat"
if (-not (Test-Path -LiteralPath $BuildBat)) {
    Write-Host "Package-AfterClose: Build.bat not found at $BuildBat. Set UE_ROOT if engine is elsewhere."
    exit 2
}

function Write-PkgLog { param([string]$Msg) Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Package-AfterClose: $Msg" }

# Check for processes that commonly lock Engine/project binaries
function Get-LockHoldingProcesses {
    $names = @("UnrealEditor", "HomeWorld", "HomeWorld-Win64-Shipping")
    $found = @()
    foreach ($n in $names) {
        $out = & tasklist /FI "IMAGENAME eq $n.exe" /NH 2>$null
        if ($out -match "\.exe") { $found += "$n.exe" }
    }
    return $found
}

$blockers = Get-LockHoldingProcesses
if ($blockers.Count -gt 0) {
    Write-PkgLog "The following processes are still running and may lock files during Stage: $($blockers -join ', ')"
    Write-Host "Close Unreal Editor and any running HomeWorld game, then run this script again."
    exit 1
}

if (-not (Test-Path -LiteralPath $UProject)) {
    Write-PkgLog "HomeWorld.uproject not found at $UProject. Run from project root."
    exit 2
}
if (-not (Test-Path -LiteralPath $PackageBat)) {
    Write-PkgLog "Package-HomeWorld.bat not found at $PackageBat."
    exit 2
}

if ($CleanStagedBuilds -and (Test-Path -LiteralPath $StagedBuilds)) {
    Write-PkgLog "Removing Saved\StagedBuilds for clean stage..."
    Remove-Item -Recurse -Force -LiteralPath $StagedBuilds -ErrorAction SilentlyContinue
}

Write-PkgLog "Building HomeWorld Win64 Shipping..."
& $BuildBat HomeWorld Win64 Shipping "-Project=$UProject" 2>&1 | Tee-Object -FilePath $BuildLog | Write-Host
if ($LASTEXITCODE -ne 0) {
    Write-PkgLog "Shipping build failed. See $BuildLog"
    exit $LASTEXITCODE
}

Write-PkgLog "Running Package-HomeWorld.bat..."
Push-Location $ProjectRoot
try {
    & cmd /c "`"$PackageBat`""
    $packExit = $LASTEXITCODE
} finally {
    Pop-Location
}
if ($packExit -ne 0) {
    Write-PkgLog "Packaging failed (exit $packExit). See $PackageLog"
    exit $packExit
}

Write-PkgLog "Done. Check $PackageLog for RunUAT exit code 0; smoke-test exe from Saved\StagedBuilds\...\HomeWorld.exe"
exit 0
