# One kept front sheet in. A standing 2 m mesh out. Mixar opens it.
param(
    [Parameter(Mandatory = $true)]
    [string]$Image,
    [string]$Name = "mesh"
)

$ErrorActionPreference = "Stop"
$Tripo = "C:\dev\TripoSR"
$Python = Join-Path $Tripo ".venv\Scripts\python.exe"
$Mixar = "C:\Program Files\Mixar\mixar.exe"
$OutDir = Join-Path $Tripo "output\$Name"
New-Item -ItemType Directory -Force -Path (Join-Path $OutDir "0") | Out-Null

& $Python (Join-Path $Tripo "run.py") $Image `
    --output-dir $OutDir `
    --no-remove-bg `
    --chunk-size 4096 `
    --mc-resolution 128
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$Raw = Join-Path $OutDir "0\mesh.obj"
$Stood = Join-Path $OutDir "0\mesh_greybox.obj"
& $Python (Join-Path $PSScriptRoot "Stand-TripoSRMesh.py") $Raw $Stood
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Set-Content -Path (Join-Path $Tripo "output\latest.txt") -Value $Stood -Encoding ascii
& $Mixar --python (Join-Path $Tripo "open_latest_mesh.py")
