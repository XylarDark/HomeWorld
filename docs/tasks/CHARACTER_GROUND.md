# Task: Character touching the ground

**Goal:** The character stands on the ground (no floating or sinking).

**Status:** Verified in PIE — character stands on ground correctly.

---

## What's already done (programmatic)

- Capsule size set in C++ constructor: **Radius 42**, **Half-Height 88** (human-sized).
- Collision preset set to **Pawn** in C++ constructor (`SetCollisionProfileName("Pawn")`).
- `BeginPlay()` performs a downward line trace and snaps the character to the ground surface on spawn.
- `UCharacterMovementComponent` handles gravity and ground contact automatically.

All ground-contact logic is handled in C++ in [HomeWorldCharacter.cpp](../../Source/HomeWorld/HomeWorldCharacter.cpp).

---

## Remaining manual steps

### Step 1 — Test in PIE ✓

PIE automated check (2026-02-22):
- `BP_HomeWorldCharacter_C` spawns at ground level (Z ≈ 681).
- `MovementMode = MOVE_WALKING`, `IsFalling = false`.
- Capsule: Half-height 88, Radius 42 (as configured in C++).

**Manual follow-up:** Walk around with WASD to confirm the character stays on terrain over varied elevation.

### Step 2 — Adjust spawn height (if needed)

If the character still floats after spawning:

1. Select the **Player Start** actor in the level.
2. Move its Z position so it is just above the ground surface.
3. The `BeginPlay()` ground trace will snap the character down, but the Player Start must be close enough for the trace to hit.

---

## Reference

- Default pawn and game mode: [SETUP.md](../SETUP.md).
- Capsule and collision are set in `AHomeWorldCharacter` constructor — no Editor configuration needed.
