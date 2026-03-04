# CleanProject.ps1 - Remove Binaries, Intermediate, optional Saved/Logs for a clean rebuild.
# Run from project root: .\Tools\CleanProject.ps1 [-IncludeSaved] [-Confirm]
# Use -Confirm to prompt before deleting.

param(
    [switch]$IncludeSaved,
    [switch]$Confirm
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot + "\.."
$dirs = @(
    (Join-Path $ProjectRoot "Binaries"),
    (Join-Path $ProjectRoot "Intermediate"),
    (Join-Path $ProjectRoot "DerivedDataCache")
)
if ($IncludeSaved) {
    $dirs += (Join-Path $ProjectRoot "Saved\Logs")
}

$toRemove = $dirs | Where-Object { Test-Path $_ }
if (-not $toRemove) {
    Write-Host "Nothing to clean (dirs already absent)."
    exit 0
}

if ($Confirm) {
    $toRemove | ForEach-Object { Write-Host $_ }
    $r = Read-Host "Remove these? (y/N)"
    if ($r -ne "y" -and $r -ne "Y") { exit 0 }
}

foreach ($d in $toRemove) {
    Write-Host "Removing $d"
    Remove-Item -Recurse -Force $d
}
Write-Host "Clean done."
exit 0
