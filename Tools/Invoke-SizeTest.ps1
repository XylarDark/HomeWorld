# Build the whole-meter greybox set, then tell the editor script where it landed.
$ErrorActionPreference = "Stop"
$Mixar = "C:\Program Files\Mixar\mixar.exe"
$Script = Join-Path $PSScriptRoot "Build-SizeTestWorld.py"
$Out = "C:\dev\HomeWorld\AssetCreation\SizeTest"

& $Mixar --background --python $Script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$fbx = Get-ChildItem $Out -Filter *.fbx
if ($fbx.Count -lt 20) { throw "Size-test export is short: $($fbx.Count) FBX files in $Out" }
Write-Host "Exported $($fbx.Count) FBX files to $Out"
