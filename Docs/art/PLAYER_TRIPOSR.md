# Player mesh from TripoSR

One front sheet goes in. TripoSR invents the unseen side. Mixar cleans the result. This is not a Steam mesh and it is not the cottage sheet.

## Input

`Docs/art/player/SM_Player_front_v2.jpg`

Front, A-pose, plain gray ground. Dark coat. No shoulder spirit. No scarf.

Do not attach `player_expression_sheet.jpg`. The scarf there belongs to the partner. Do not attach a homestead or field scene.

## Run

From the repo root:

```powershell
.\Tools\Invoke-TripoSR.ps1 -Image "C:\dev\HomeWorld\Docs\art\player\SM_Player_front_v2.jpg" -Name player
```

That runs TripoSR, stands the mesh on its feet, scales the height to 2 m, and opens the result in Mixar. The raw file stays `mesh.obj`. The stood file is `mesh_greybox.obj`.

`--no-remove-bg` stays, because the ground is already plain gray.

## After the mesh

Look at it texture-off. The silhouette has to match the front. The back is a guess. A face or a bending arm stays a hand mesh. Do not copy the file into `Content/`.

## Rig

The stood mesh can take a skeleton with an idle and a walk:

```powershell
.\Tools\Invoke-RigTripoPlayer.ps1
```

That writes `C:\dev\TripoSR\output\player\0\SM_Player_Rig.blend` and opens it. Playback starts on the walk. Idle is the other action on the rig. These clips are a size-check motion. Do not copy the file into `Content/`.
