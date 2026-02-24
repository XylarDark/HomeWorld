# Task: Fix character animation

**Goal:** The character uses correct animations (idle, walk/run) so it looks right in play.

**Status:** Mostly done — AnimBP active in PIE (`ABP_HomeWorldCharacter_C`), skeletal mesh rendering (`SK_Man_Full_01`). AnimGraph state machine needs manual setup for idle/walk transitions. C++ `UHomeWorldAnimInstance` parent class needs rebuild.

---

## What's already done (programmatic)

- `UHomeWorldAnimInstance` C++ class created ([HomeWorldAnimInstance.h](../../Source/HomeWorld/HomeWorldAnimInstance.h), [.cpp](../../Source/HomeWorld/HomeWorldAnimInstance.cpp)) — exposes `Speed`, `bIsInAir`, `bIsMoving` to the AnimGraph via `NativeUpdateAnimation()`.
- `ABP_HomeWorldCharacter` Animation Blueprint asset created at `/Game/HomeWorld/Characters/` via `setup_animation_blueprint.py`, with skeleton from `SK_Man_Full_01`.
- `BP_HomeWorldCharacter` Blueprint created (child of `AHomeWorldCharacter`) with skeletal mesh (`SK_Man_Full_01`) and AnimBP assigned.
- Enhanced Input assets created: `IA_Move`, `IA_Look`, `IMC_Default`.
- Project settings configured: GameMode, default map, DefaultPawnClass.
- Animation sequences available in `Content/Man/Demo/Animations/`: `ThirdPersonIdle`, `ThirdPersonWalk`, `ThirdPersonRun`, `ThirdPerson_Jump`.
- All setup scripts are idempotent — safe to re-run without duplicates.

## Context

- Movement and input are driven by C++ in [AHomeWorldCharacter](../../Source/HomeWorld/HomeWorldCharacter.h).
- Animation data (Speed, IsInAir) is computed in C++ by [UHomeWorldAnimInstance](../../Source/HomeWorld/HomeWorldAnimInstance.h) — no EventGraph wiring needed.
- The AnimBP's AnimGraph must be populated manually (UE5 does not expose AnimGraph node creation to Python or MCP).

---

## Remaining manual steps

### Step 0 — Rebuild C++ (required once)

After pulling the new `HomeWorldAnimInstance` files, rebuild the project:
- Close the Editor, run `Build-HomeWorld.bat`, then reopen the Editor.
- Or use Live Coding (Ctrl+Alt+F11) if the Editor is open and not in PIE.

After rebuild, re-run the AnimBP setup so the parent class gets set to `UHomeWorldAnimInstance`:
- **Via MCP:** `execute_python_script("setup_animation_blueprint.py")`
- Or delete `ABP_HomeWorldCharacter` in Content Browser and re-run the script.

### Step 1 — Populate the AnimBP AnimGraph

1. Open `ABP_HomeWorldCharacter` in the Editor (Content Browser → `/Game/HomeWorld/Characters/`).
2. Open the **AnimGraph** tab.
3. Right-click → **Add New State Machine** → name it `Locomotion`.
4. Double-click the state machine to open it.
5. Add two states:
   - **Idle** — assign `ThirdPersonIdle` animation (from `Content/Man/Demo/Animations/`).
   - **Walk/Run** — assign `ThirdPersonRun` animation.
6. Add transitions:
   - **Idle → Walk/Run:** condition = `Speed > 10` (drag `Speed` from the C++ parent — it's already exposed as BlueprintReadOnly).
   - **Walk/Run → Idle:** condition = `Speed < 10`.
7. Set **Idle** as the default state (right-click → Set as Default).
8. Connect the state machine output to the **Output Pose** node.
9. Compile and save.

### Step 2 — Test in PIE

PIE automated check (2026-02-22):
- `ABP_HomeWorldCharacter_C` AnimInstance is **active and running**.
- Skeletal mesh `SK_Man_Full_01` is assigned.
- Character spawns and is possessed by PlayerController.
- AnimGraph state machine not yet populated — character will T-pose until Step 1 is completed.

1. After completing Step 1, press **Play** (Alt+P).
2. Move with WASD — character should play walk/run animation.
3. Stand still — character should play idle animation.
4. If no animation plays, verify the AnimBP is assigned on BP_HomeWorldCharacter → Mesh → Anim Class.

---

## Reference

- **C++ locomotion data:** `UHomeWorldAnimInstance` computes `Speed` (horizontal velocity in cm/s), `bIsMoving` (Speed > 5), `bIsInAir` (CharacterMovement->IsFalling()) every tick.
- **Available animations:** `ThirdPersonIdle`, `ThirdPersonWalk`, `ThirdPersonRun`, `ThirdPerson_Jump` in `/Game/Man/Demo/Animations/`.
- **Scripts:** `setup_animation_blueprint.py` (creates AnimBP asset), `setup_character_blueprint.py` (assigns mesh + AnimBP), `bootstrap_project.py` (runs all setup).
