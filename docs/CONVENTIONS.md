# HomeWorld – Conventions

## Programmatic by default

HomeWorld is developed **programmatically by default**: as much work as possible is done in C++ so that behavior is in code, versionable, and reviewable.

- **C++** is used for:
  - Gameplay systems (movement, input, camera, combat, building logic)
  - Core logic and reusable behavior
  - Anything that should be consistent across maps and Blueprint children

- **Blueprint** is used for:
  - Content (meshes, materials, level placement)
  - Designer-facing overrides and one-off behavior
  - Subclassing C++ classes to assign assets (e.g. character mesh, input assets)

When adding new features, prefer C++ for the core implementation; use Blueprint for data, overrides, and content integration.

---

## Code-first checklist

- **New systems:** Implement in C++; expose designer-facing APIs with `UFUNCTION(BlueprintCallable)` or `BlueprintNativeEvent` where designers need to drive or extend behavior from Blueprint.
- **C++ systems (current):** Movement, input, camera, game mode, default pawn. GAS: `AHomeWorldCharacter` owns `UAbilitySystemComponent` and `UHomeWorldAttributeSet`; base ability class `UHomeWorldGameplayAbility`. New attributes go in `UHomeWorldAttributeSet` (or a second attribute set if needed).
- **Blueprint:** Content (meshes, materials, input assets), level layout, one-off logic, and Blueprint children of C++ classes for asset assignment (e.g. character mesh, IA_Move/IA_Look/IMC_Default).

---

## Input setup (Enhanced Input)

The default pawn is **AHomeWorldCharacter** (C++). Movement and look are driven by Enhanced Input. To have working WASD and mouse look:

1. In the Editor, create Input Actions and a Mapping Context (once):
   - **IA_Move** (Value Type: Axis2D) — for WASD
   - **IA_Look** (Value Type: Axis2D) — for mouse
   - **IMC_Default** — map W/S/A/D to Move and Mouse XY to Look
2. Assign **MoveAction**, **LookAction**, and **DefaultMappingContext** on the default pawn:
   - Either on the **AHomeWorldCharacter** class defaults (Editor), or
   - On a **Blueprint child** of `HomeWorldCharacter` that you set as the default pawn (e.g. to also set the character mesh).

If these are not set, the character will spawn and the camera will work, but movement and look input will do nothing until the assets are created and assigned.

---

## Camera & controls

The default pawn uses a **third-person** setup:

- **Camera:** A spring arm and follow camera are attached to the character capsule. The camera orbits with the mouse (Look) and stays behind the character. Pitch is clamped so the camera does not flip.
- **Movement:** Movement is **camera-relative** — W moves toward where the camera looks, and the character orients to movement direction.
- **Input:** IA_Move, IA_Look, and IMC_Default must be created in the Editor and assigned to the default pawn (or a Blueprint child) for movement and look to work. Camera settings (arm length, FOV, pitch limits, sensitivity) are exposed on the character for tuning.
