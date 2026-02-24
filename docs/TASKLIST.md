# HomeWorld – Task list (master)

Current focus tasks. Each item links to a doc with step-by-step instructions for the remaining work.

> **MCP note:** With `execute_python_script` available via MCP, steps marked **(MCP)** can be run directly from Cursor without opening the Editor's script dialog.

| # | Task | Doc | Status | Remaining work |
|---|------|-----|--------|----------------|
| 1 | Fix character animation | [CHARACTER_ANIMATION.md](tasks/CHARACTER_ANIMATION.md) | Mostly done | Rebuild C++, populate AnimBP AnimGraph (manual), test in PIE |
| 2 | Fix character orientation while moving | [CHARACTER_ORIENTATION.md](tasks/CHARACTER_ORIENTATION.md) | PIE checked | Manual WASD test needed; adjust `MeshForwardYawOffset` if mesh faces wrong way |
| 3 | Character touching the ground | [CHARACTER_GROUND.md](tasks/CHARACTER_GROUND.md) | **Verified** | On ground, MOVE_WALKING, not falling. Walk around varied terrain to confirm. |
| 4 | Apply PCG forest to the map | [PCG_FOREST_ON_MAP.md](tasks/PCG_FOREST_ON_MAP.md) | **Verified** | 1161 actors in scene. Visual check recommended. |

Week 1 scope aligns with [ROADMAP.md](../ROADMAP.md) Phase 1.

---

## What was completed programmatically

- **C++ AnimInstance:** `UHomeWorldAnimInstance` exposes `Speed`, `bIsInAir`, `bIsMoving` — drives AnimBP data with zero EventGraph work.
- **AnimBP asset:** `ABP_HomeWorldCharacter` created via `setup_animation_blueprint.py` with correct skeleton.
- **Character BP:** `BP_HomeWorldCharacter` created with skeletal mesh (`SK_Man_Full_01`) and AnimBP assigned.
- **Enhanced Input:** `IA_Move`, `IA_Look`, `IMC_Default` assets created.
- **Orientation:** `bOrientRotationToMovement`, `RotationRate = 720`, collision preset Pawn — all in C++.
- **Ground contact:** Capsule size (42r, 88h), Pawn collision, BeginPlay ground trace — all in C++.
- **PCG Forest:** Landscape-sized volume (403m x 342m), dynamic village exclusion zones, Stylized Provencal trees/rocks.
- **Bootstrap:** `bootstrap_project.py` runs all setup scripts in order (Enhanced Input → AnimBP → Character BP → Project Settings → Level Setup).

## Remaining steps (summary)

### Task 1 — Character animation

1. **Rebuild C++** — Close Editor, build project, reopen. Then re-run: `execute_python_script("setup_animation_blueprint.py")` to set the C++ parent class on the AnimBP.
2. **(Manual)** Open `ABP_HomeWorldCharacter` → AnimGraph → Add State Machine → Idle/Walk states → use `Speed` variable from C++ parent for transitions.
3. **Test in PIE** — WASD to move, verify idle/walk/run animations play.

### Task 2 — Character orientation (verify only)

1. **Test in PIE** — Move with WASD, confirm character faces movement direction.
2. **Adjust offset (if needed)** — Set `MeshForwardYawOffset` on the BP if mesh faces sideways/backward.

### Task 3 — Character ground ✓

Automated PIE check passed (2026-02-22): `MOVE_WALKING`, not falling, capsule 42r/88h.
- **Manual follow-up:** Walk over varied terrain elevations.

### Task 4 — PCG forest ✓

Automated PIE check passed (2026-02-22): 1161 static mesh actors in scene.
- **Manual follow-up:** Visual check that trees cover landscape and village area is clear.

---

**See also:** [SETUP.md](SETUP.md), [CONVENTIONS.md](CONVENTIONS.md), [ROADMAP.md](../ROADMAP.md), [KNOWN_ERRORS.md](KNOWN_ERRORS.md).
