# Task: Fix character animation

**Goal:** The character uses correct animations (idle, walk/run) so it looks right in play.

## Context

- Movement and input are driven by C++ in [AHomeWorldCharacter](../../Source/HomeWorld/HomeWorldCharacter.h) and [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp), using Enhanced Input. See [CONVENTIONS.md](../CONVENTIONS.md) for input setup.
- Animation is driven on the **Blueprint side**: the character mesh, skeleton, and Animation Blueprint are assigned on the default pawn (either on the C++ class defaults or on a Blueprint child of `AHomeWorldCharacter`).

## Steps

1. **Ensure the default pawn has a mesh and skeleton**
   - In the Editor, open **Project Settings → Maps & Modes** and confirm **Default Pawn Class** is set to **HomeWorldCharacter** or a Blueprint child of it.
   - Open that Blueprint (or the C++ class defaults). In **Components**, ensure the **Mesh** component has a **Skeletal Mesh** and **Anim Class** (Animation Blueprint) assigned. The mesh must use a skeleton compatible with your animations.

2. **Create or assign an Animation Blueprint**
   - If you don’t have one: in Content Browser, **Right-click → Animation → Animation Blueprint**. Choose the same skeleton as the character mesh. Name it (e.g. `ABP_HomeWorldCharacter`).
   - Open the Animation Blueprint. Add a state machine with at least:
     - **Idle** (default state).
     - **Locomotion** (walk/run), driven by movement speed or velocity.
   - Use **Try Get Pawn Owner** (or the character reference) and **Get Velocity** (or **Get Movement Component → Get Max Speed** / current speed) to drive a blend or transition from Idle to Locomotion when the character is moving.

3. **Wire movement to the blend**
   - In the AnimGraph, blend between Idle and Locomotion based on **Speed** (e.g. from **Get Velocity → Vector Length** on XY, or from the character’s movement component). Threshold around 10–50 (Unreal units) is typical for “moving” vs “idle”.

4. **Assign and test**
   - Assign this Animation Blueprint as the **Anim Class** on the character’s Mesh component (Blueprint or class defaults).
   - Run **Play In Editor (PIE)**. Move with WASD and confirm: idle when still, walk/run when moving.

## Reference

- **C++ movement:** `AHomeWorldCharacter::Move()` adds movement input; `CharacterMovementComponent` handles velocity. Animation does not need to be changed in C++ for basic locomotion.
- **Input:** IA_Move, IA_Look, IMC_Default must exist and be assigned per [CONVENTIONS.md](../CONVENTIONS.md#input-setup-enhanced-input).
