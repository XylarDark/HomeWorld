# Task: Fix character animation

**Goal:** The character uses correct animations (idle, walk/run) so it looks right in play.

**Status:** In progress — Blueprint scaffolding done, manual Editor work required.

---

## What's already done (programmatic)

- `BP_HomeWorldCharacter` Blueprint created (child of `AHomeWorldCharacter`) via MCP.
- C++ class handles movement, input binding, camera — no C++ changes needed.
- Python setup scripts exist: `setup_enhanced_input.py`, `setup_character_blueprint.py`.
- Config files ready: `character_blueprint_config.json`.

## Context

- Movement and input are driven by C++ in [AHomeWorldCharacter](../../Source/HomeWorld/HomeWorldCharacter.h) and [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp), using Enhanced Input. See [CONVENTIONS.md](../CONVENTIONS.md) for input setup.
- Animation is driven on the **Blueprint side**: the character mesh, skeleton, and Animation Blueprint are assigned on the default pawn (either on the C++ class defaults or on a Blueprint child of `AHomeWorldCharacter`).

---

## Remaining manual steps

### Step 1 — Run Enhanced Input setup script

In the Editor: **Tools > Execute Python Script** → `Content/Python/setup_enhanced_input.py`.

This creates `IA_Move`, `IA_Look`, and `IMC_Default` at `/Game/HomeWorld/Input/`.

### Step 2 — Configure and run Character Blueprint setup script

1. Edit `Content/Python/character_blueprint_config.json`:
   - Set `skeletal_mesh` to the asset path of your mesh (e.g. `/Game/Characters/Mannequins/Meshes/SKM_Manny`).
   - Leave `anim_blueprint` empty for now (you'll create it in Step 3).
2. In the Editor: **Tools > Execute Python Script** → `Content/Python/setup_character_blueprint.py`.
   - This assigns the input assets and skeletal mesh to `BP_HomeWorldCharacter`.

### Step 3 — Create an Animation Blueprint

1. In Content Browser: **Right-click → Animation → Animation Blueprint**.
2. Select the **same skeleton** as the mesh you assigned in Step 2.
3. Name it `ABP_HomeWorldCharacter`.
4. Open the Animation Blueprint and add a **State Machine** with at least:
   - **Idle** (default state) — plays an idle animation.
   - **Locomotion** (walk/run) — plays a walk or run animation.
5. Create a **Speed** variable. In the **Event Graph**, use **Try Get Pawn Owner → Get Velocity → Vector Length** to set it each tick.
6. In the **State Machine**, add transitions:
   - Idle → Locomotion: when **Speed > 10**.
   - Locomotion → Idle: when **Speed < 10**.

### Step 4 — Assign AnimBP to the character

1. Open `BP_HomeWorldCharacter` in the Editor.
2. Select the **Mesh** component in the Components panel.
3. In Details, set **Anim Class** to `ABP_HomeWorldCharacter`.
4. Compile and save the Blueprint.

### Step 5 — Set GameMode DefaultPawnClass

1. Open `BP_GameMode` in the Editor (Content Browser → `/Game/HomeWorld/GameMode/`).
2. In the **Classes** section, set **Default Pawn Class** to `BP_HomeWorldCharacter`.
3. Save the Blueprint.

> **Why manual?** MCP cannot find Blueprints stored outside `/Game/Blueprints/` and cannot set inherited C++ properties. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

### Step 6 — Test in PIE

1. Press **Play** (Alt+P) in the Editor.
2. Move with WASD and confirm: idle animation when still, walk/run when moving.
3. If the mesh has no visible animation, verify the AnimBP is assigned and the skeleton matches.

---

## Reference

- **C++ movement:** `AHomeWorldCharacter::Move()` adds movement input; `CharacterMovementComponent` handles velocity. Animation does not need to be changed in C++ for basic locomotion.
- **Velocity for AnimBP:** The Animation Blueprint can drive Idle/Locomotion from the pawn owner's **Get Velocity** (e.g. Vector Length on XY) or **Get Movement Component → Velocity**; no extra C++ API is required.
- **Input:** IA_Move, IA_Look, IMC_Default must exist and be assigned per [CONVENTIONS.md](../CONVENTIONS.md#input-setup-enhanced-input).
