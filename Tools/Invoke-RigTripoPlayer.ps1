# Rig the stood Tripo player, store Idle and Walk, and open the result in Mixar.
$ErrorActionPreference = "Stop"
$Mixar = "C:\Program Files\Mixar\mixar.exe"
$Script = Join-Path $PSScriptRoot "Rig-TripoPlayer.py"
$Frame = Join-Path $PSScriptRoot "Frame-PlayerRig.py"
$Blend = "C:\dev\TripoSR\output\player\0\SM_Player_Rig.blend"

& $Mixar --background --python $Script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not (Test-Path $Blend)) { throw "Rig blend was not written: $Blend" }

Start-Process -FilePath $Mixar -ArgumentList $Blend, "--python", $Frame
