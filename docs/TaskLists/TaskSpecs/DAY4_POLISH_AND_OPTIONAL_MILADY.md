# Day 4: Polish First Playable Loop + Optional Milady

**Goal:** Polish the explore → fight → build loop so it is ready for Day 5 playtest sign-off; optionally run Milady folder and pastel material scripts for content prep. No new systems; solidify existing behavior. See [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md) Day 4 and [VISION.md](../../../VisionBoard/Core/VISION.md).

**Status:** Complete. Day 4 checkboxes in 30_DAY_SCHEDULE and DAILY_STATE updated. Run polish playtest per checklist below as needed; Milady scripts were run via MCP.

---

## 1. Polish checklist (re-run Week 1 playtest)

Re-run the Week 1 playtest from [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) and fix any issues found.

### 1.1 Pre-playtest

- [ ] **Map:** DemoMap or Homestead open; PCG generated if you want trees/rocks.
- [ ] **GameMode:** Uses BP_HomeWorldCharacter (or default pawn with GAS).
- [ ] **Abilities:** Run `setup_gas_abilities.py` if not done; confirm **Left Mouse**, **Shift**, **E** are bound (Primary Attack, Dodge, Interact).
- [ ] **Build:** C++ built (Build-HomeWorld.bat with Editor closed); no errors in Output Log on load.

### 1.2 Playtest (in PIE)

- [ ] **Explore:** Move with **WASD**; look with **mouse**. Character stays on ground; no falling through floor.
- [ ] **Fight:** **Left Mouse** triggers Primary Attack; **Shift** triggers Dodge. Add VFX later if desired.
- [ ] **Interact:** **E** triggers Interact.
- [ ] **Placement (optional):** If you added a placement test (e.g. key **P** per Day 3 section 1.2), confirm trace/preview works.
- [ ] **Stability:** No crashes or repeated errors in Output Log during a short session (2–5 minutes).

### 1.3 Fix and document

- Fix any bugs or inconsistencies found (movement, ability triggers, placement API). Record new issues in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).
- Optional: Add a simple placement test (key **P** in Blueprint calling GetPlacementTransform and spawning a preview) per [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) section 1.2; or leave as "add VFX later" and only document.

---

## 2. Optional: Milady content prep

Run the two Python scripts to create Milady folders and a pastel material. Idempotent; safe to run multiple times.

### 2.1 Run scripts

1. **Ensure Milady folders:** Tools → Execute Python Script → `Content/Python/ensure_milady_folders.py` (or via MCP: `execute_python_script("ensure_milady_folders.py")`).
   - Creates `/Game/HomeWorld/Milady/Meshes`, `Materials`, `Animations`, `Blueprints`.
2. **Create pastel material:** Tools → Execute Python Script → `Content/Python/create_milady_pastel_material.py` (or via MCP: `execute_python_script("create_milady_pastel_material.py")`).
   - Creates `M_MiladyPastel` in `/Game/HomeWorld/Milady/Materials`; skips if already exists.

### 2.2 Verify

- In Content Browser, confirm folders under **Content → HomeWorld → Milady** and material **M_MiladyPastel** exist.
- No further Milady pipeline work required for Day 4. Full pipeline: [MILADY_IMPORT_ROADMAP.md](MILADY_IMPORT_ROADMAP.md), [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md).

---

## 3. Success criteria

- [ ] **Loop:** Explore → fight → build is playable without regressions; any issues from playtest fixed or documented.
- [ ] **Optional Milady:** If chosen, both scripts ran successfully and folders/material are present.

---

## 4. After Day 4

- Check off Day 4 in [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md).
- Update [DAILY_STATE.md](../../../VisionBoard/DAILY_STATE.md): Yesterday = Day 4 work; Today = Day 5 (playtest sign-off); Tomorrow = Day 6 (Homestead Phase 1); Current day = 5.
- Append [SESSION_LOG.md](../SESSION_LOG.md) with date, Day 4 summary (polish done, optional Milady if run), and any issues.

---

## References

- [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) — Week 1 playtest checklist and placement API.
- [VISION.md](../../../VisionBoard/Core/VISION.md) — Theme, Week 1 goal, success criteria.
- [GAS_SURVIVOR_SKILLS.md](GAS_SURVIVOR_SKILLS.md) — Day 2 abilities and verification.
- [MILADY_IMPORT_ROADMAP.md](MILADY_IMPORT_ROADMAP.md) — Milady pipeline; [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md) — setup.
