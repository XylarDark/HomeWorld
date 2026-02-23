# Task: Character touching the ground

**Goal:** The character stands on the ground (no floating or sinking).

**Status:** Done (C++) — verify in Editor.

---

## What's already done (programmatic)

- Capsule size set in C++ constructor: **Radius 42**, **Half-Height 88** (human-sized).
- `BeginPlay()` performs a downward line trace and snaps the character to the ground surface on spawn.
- Player Start verified at **(-3700, -530, 742)** which is above the landscape.
- `UCharacterMovementComponent` handles gravity and ground contact automatically.

All ground-contact logic is handled in C++ in [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp).

## Context

- The default pawn uses UE's **Character** movement: `AHomeWorldCharacter` extends `ACharacter`, which uses `UCharacterMovementComponent`. The capsule and movement component handle collision and grounding.
- See [CONVENTIONS.md](../CONVENTIONS.md) and default pawn setup in [SETUP.md](../SETUP.md).

---

## Remaining manual steps

### Step 1 — Verify collision preset

1. Open `BP_HomeWorldCharacter` in the Editor.
2. Select the **Capsule** (root) component.
3. In Details, confirm **Collision Preset** is set to **Pawn** (or a custom preset that collides with WorldStatic/WorldDynamic).
4. If not set, change it to **Pawn** and save.

### Step 2 — Verify the level has a floor with collision

1. Open the Main level.
2. Confirm a Landscape or floor mesh exists and has collision enabled.
3. The landscape should use a collision preset that blocks Pawn (e.g. BlockAll).

### Step 3 — Test in PIE

1. Press **Play** (Alt+P).
2. The character should spawn standing on the ground, not floating or falling through.
3. Walk around — the character should stay on the terrain surface.

### Step 4 — Adjust spawn height (if needed)

If the character still floats after spawning:

1. Select the **Player Start** actor in the level.
2. Move its Z position so it is just above the ground surface.
3. The `BeginPlay()` ground trace will snap the character down, but the Player Start must be close enough for the trace to hit.

---

## Reference

- Default pawn and game mode: [SETUP.md](../SETUP.md#building-c) and [SETUP.md](../SETUP.md#validation).
- CONVENTIONS: [Code-first checklist](../CONVENTIONS.md#code-first-checklist).
