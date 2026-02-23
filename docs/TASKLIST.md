# HomeWorld – Task list (master)

Current focus tasks. Each item links to a doc with step-by-step instructions for the remaining manual work.

| # | Task | Doc | Status | Manual work |
|---|------|-----|--------|-------------|
| 1 | Fix character animation | [CHARACTER_ANIMATION.md](tasks/CHARACTER_ANIMATION.md) | In progress | 6 steps: run 2 Python scripts, create AnimBP, assign to mesh, set GameMode pawn, test |
| 2 | Fix character orientation while moving | [CHARACTER_ORIENTATION.md](tasks/CHARACTER_ORIENTATION.md) | Done (C++) | Verify in PIE; adjust `MeshForwardYawOffset` if mesh faces wrong way |
| 3 | Character touching the ground | [CHARACTER_GROUND.md](tasks/CHARACTER_GROUND.md) | Done (C++) | Verify collision preset is Pawn; test in PIE |
| 4 | Apply PCG forest to the map | [PCG_FOREST_ON_MAP.md](tasks/PCG_FOREST_ON_MAP.md) | Ready | 1 step: run `create_demo_map.py` in Editor, then verify |

Week 1 scope aligns with [ROADMAP.md](../ROADMAP.md) Phase 1.

---

## Remaining manual steps (summary)

### Task 1 — Character animation (most work remaining)

1. **Run Enhanced Input setup** — Editor: **Tools > Execute Python Script** → `Content/Python/setup_enhanced_input.py`
2. **Configure skeletal mesh** — Edit `Content/Python/character_blueprint_config.json`, set `skeletal_mesh` path
3. **Run Character BP setup** — Editor: **Tools > Execute Python Script** → `Content/Python/setup_character_blueprint.py`
4. **Create Animation Blueprint** — Content Browser: Right-click → Animation → Animation Blueprint → set up Idle/Locomotion state machine driven by velocity
5. **Assign AnimBP** — Open `BP_HomeWorldCharacter` → Mesh component → set Anim Class → compile/save
6. **Set GameMode pawn** — Open `BP_GameMode` → set Default Pawn Class to `BP_HomeWorldCharacter` → save

### Task 2 — Character orientation (verify only)

1. **Test in PIE** — Move with WASD, confirm character faces movement direction
2. **Adjust offset (if needed)** — Set `MeshForwardYawOffset` on the BP if mesh faces sideways/backward

### Task 3 — Character ground (verify only)

1. **Check collision** — Open `BP_HomeWorldCharacter` → Capsule → confirm Collision Preset is Pawn
2. **Test in PIE** — Confirm character stands on ground, not floating

### Task 4 — PCG forest (one script run)

1. **Open Main level** — `Content/HomeWorld/Maps/Main`
2. **Run script** — Editor: **Tools > Execute Python Script** → `Content/Python/create_demo_map.py`
3. **Verify** — 50–100+ trees, empty center exclusion zone, no errors in Output Log

---

**See also:** [SETUP.md](SETUP.md), [CONVENTIONS.md](CONVENTIONS.md), [ROADMAP.md](../ROADMAP.md), [KNOWN_ERRORS.md](KNOWN_ERRORS.md).
