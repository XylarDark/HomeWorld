# Task: Character touching the ground

**Goal:** The character stands on the ground (no floating or sinking).

## Context

- The default pawn uses UE’s **Character** movement: `AHomeWorldCharacter` extends `ACharacter`, which uses `UCharacterMovementComponent`. The capsule and movement component handle collision and grounding.
- See [CONVENTIONS.md](../CONVENTIONS.md) and default pawn setup in [SETUP.md](../SETUP.md).

## Steps

1. **Check capsule size**
   - Open the default pawn Blueprint (or C++ class defaults). Select the **Capsule** (root) component. Ensure **Capsule Half Height** and **Capsule Radius** are sensible (e.g. 88 and 42 for a human-sized character). Extreme values can cause odd contact with the floor.

2. **Check collision preset**
   - On the **Capsule** component, set **Collision Preset** to **Pawn** (or a custom preset that collides with WorldStatic / WorldDynamic). Ensure the level floor (Landscape, plane, or floor mesh) has collision enabled and a preset that blocks Pawn (e.g. BlockAll or custom).

3. **Ensure the level has a floor**
   - The level must have a surface with collision (Landscape, BSP, or static mesh with collision). If the character spawns in the void, add a floor or Landscape and ensure the **game start** or **player start** is above it.

4. **Spawn height (optional)**
   - If the character spawns floating: move the **Player Start** (or **Game Mode** spawn) so its Z is at or just above the floor. Alternatively, in Blueprint or C++ `BeginPlay()`, you can trace downward from the character and set actor location to the hit Z (plus half capsule height) so the character is placed on the ground once at start. For most levels, placing the Player Start correctly is enough.

5. **Avoid custom gravity**
   - Do not override gravity or use custom movement unless required. `CharacterMovementComponent` handles gravity and ground contact; custom code can cause floating or sinking if it conflicts.

## Reference

- Default pawn and game mode: [SETUP.md](../SETUP.md#building-c) and [SETUP.md](../SETUP.md#validation).
- CONVENTIONS: [Code-first checklist](../CONVENTIONS.md#code-first-checklist).
