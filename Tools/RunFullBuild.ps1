# RunFullBuild.ps1 - Full build via RunUAT BuildGraph or fallback to Build-HomeWorld.bat.
# Run from project root: .\Tools\RunFullBuild.ps1 [-Clean] [-Platform Win64] [-Test]
# Requires: UE 5.7 at default path or set $env:UE_ENGINE (e.g. "C:\Program Files\Epic Games\UE_5.7")

param(
    [switch]$Clean,
    [string]$Platform = "Win64",
    [switch]$Test
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot + "\.."
$UProject = Join-Path $ProjectRoot "HomeWorld.uproject"
$EnginePath = $env:UE_ENGINE
if (-not $EnginePath) { $EnginePath = "C:\Program Files\Epic Games\UE_5.7" }
$RunUAT = Join-Path $EnginePath "Engine\Build\BatchFiles\RunUAT.bat"
$BuildGraphScript = Join-Path $ProjectRoot "Tools\BuildGraph.xml"

if (-not (Test-Path $UProject)) {
    Write-Error "HomeWorld.uproject not found at $UProject. Run from project root."
    exit 1
}

# If RunUAT and BuildGraph exist, use them; else fall back to Build-HomeWorld.bat
if ((Test-Path $RunUAT) -and (Test-Path $BuildGraphScript)) {
    $args = @("BuildGraph", "-Script=`"$BuildGraphScript`"", "-Project=`"$UProject`"")
    if ($Clean) { $args += "-Clean" }
    $args += "-Platform=$Platform"
    if ($Test) { $args += "-RunEditorTests" }
    Write-Host "RunUAT $($args -join ' ')"
    & $RunUAT $args
    exit $LASTEXITCODE
}

# Fallback: Build-HomeWorld.bat
$BuildBat = Join-Path $ProjectRoot "Build-HomeWorld.bat"
if (Test-Path $BuildBat) {
    Write-Host "Using Build-HomeWorld.bat (RunUAT/BuildGraph not used)"
    & $BuildBat
    exit $LASTEXITCODE
}

Write-Error "Neither RunUAT nor Build-HomeWorld.bat found."
exit 1
