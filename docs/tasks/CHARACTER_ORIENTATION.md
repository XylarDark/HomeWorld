# Task: Fix character orientation while moving

**Goal:** The character mesh faces the movement direction (and turns smoothly when changing direction).

**Status:** Done (C++) — verify in Editor and tune if needed.

---

## What's already done (programmatic)

- `bUseControllerRotationYaw = false` set in C++ constructor so the character doesn't snap to camera yaw.
- `bOrientRotationToMovement = true` set on `CharacterMovementComponent` so the character rotates toward movement direction.
- `RotationRate = FRotator(0, RotationRateYaw, 0)` set in C++ (default 720 deg/s).
- `MeshForwardYawOffset` exposed as UPROPERTY (default 0.0); applied to mesh relative rotation in `BeginPlay()`.

All orientation logic is handled in C++ in [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp). No Blueprint or Editor configuration is strictly required.

## Context

- [AHomeWorldCharacter](../../Source/HomeWorld/HomeWorldCharacter.h) exposes:
  - **RotationRateYaw** (deg/s) – how fast the character rotates toward movement direction (default 720).
  - **MeshForwardYawOffset** (degrees) – offset applied to the mesh so its "forward" matches movement (use 90 or -90 if the mesh faces the wrong axis).
- Movement is camera-relative (W = move toward where the camera looks). See [CONVENTIONS.md](../CONVENTIONS.md#camera--controls).

---

## Remaining manual steps

### Step 1 — Test orientation in PIE

1. Press **Play** (Alt+P) in the Editor.
2. Move in different directions with WASD.
3. Confirm the character (capsule and mesh) turns to face the movement direction.

### Step 2 — Fix mesh facing the wrong way (if needed)

If the capsule turns correctly but the mesh faces sideways or backward:

1. Open `BP_HomeWorldCharacter` (or the C++ class defaults).
2. Set **MeshForwardYawOffset**:
   - **90** or **-90** if the mesh is 90° off.
   - **180** if the mesh faces backward.
   - **0** (default) for standard forward-facing meshes.
3. Restart PIE to see the change (the offset is applied in `BeginPlay()`).

### Step 3 — Tune turn speed (optional)

- **RotationRateYaw** (deg/s): higher = snappier (720–1080), lower = smoother (360).
- Edit on the character Blueprint or C++ defaults and test in PIE.

---

## Reference

- CONVENTIONS: [Camera & controls](../CONVENTIONS.md#camera--controls).
