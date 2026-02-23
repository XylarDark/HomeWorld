# Task: Fix character orientation while moving

**Goal:** The character mesh faces the movement direction (and turns smoothly when changing direction).

## Context

- [AHomeWorldCharacter](../../Source/HomeWorld/HomeWorldCharacter.h) already exposes:
  - **RotationRateYaw** (deg/s) – how fast the character rotates toward movement direction (default 720).
  - **MeshForwardYawOffset** (degrees) – offset applied to the mesh so its “forward” matches movement (use 90 or -90 if the mesh faces the wrong axis).
- Movement is camera-relative (W = move toward where the camera looks). See [CONVENTIONS.md](../CONVENTIONS.md#camera--controls).

## What the code does

In [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp):

- `bUseControllerRotationYaw = false` so the character doesn’t snap to camera yaw.
- `CharacterMovementComponent->bOrientRotationToMovement = true` so the character rotates toward its movement direction.
- `RotationRate = FRotator(0, RotationRateYaw, 0)` sets the turn speed.
- In `BeginPlay()`, the mesh’s relative rotation is set with `MeshForwardYawOffset` so the mesh forward aligns with movement.

## Steps

1. **Confirm rotation is applied**
   - Run PIE and move in different directions. The character (capsule) should turn toward movement. If it never turns, check that the default pawn class is HomeWorldCharacter (or a Blueprint child) and that no Blueprint or project setting overrides `bOrientRotationToMovement` or `RotationRate` on the character movement component.

2. **Fix mesh facing the wrong way**
   - If the capsule turns but the mesh faces sideways or backward, set **MeshForwardYawOffset** on the character (Blueprint or C++ defaults):
     - **90** or **-90** if the mesh is 90° off.
     - **180** if the mesh faces backward.
   - The offset is applied in C++ in `BeginPlay()`, so changing it in the Editor and restarting PIE is enough.

3. **Tune turn speed**
   - **RotationRateYaw** (deg/s): higher = snappier (e.g. 720–1080), lower = smoother (e.g. 360). Edit on the character Blueprint or C++ defaults and test in PIE.

## Reference

- CONVENTIONS: [Camera & controls](../CONVENTIONS.md#camera--controls).
