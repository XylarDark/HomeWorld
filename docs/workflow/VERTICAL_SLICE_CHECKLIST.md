# Vertical slice checklist (Days 26–30 buffer)

**Purpose:** Define and verify the **one moment** and **one beautiful corner** for the 30-day vertical slice. Use this when polishing for a short demo or stakeholder show. See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice) and [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).

---

## 1. Chosen moment (pick one and lock in PROTOTYPE_SCOPE)

| Option | Description | Verification |
|--------|-------------|---------------|
| **A. Claim homestead** | Player places first home asset (P) after exploring/fighting; "this is my base." | PIE: move → harvest (E) → place (P) at cursor; building spawns. |
| **B. First harvest** | Player interacts (E) with harvestable tree; wood granted. | PIE: face BP_HarvestableTree, press E; Output Log "Harvest succeeded - Wood +10"; inventory. |
| **C. Dungeon approach** | Player reaches Dungeon_POI / BP_DungeonEntrance; overlap opens dungeon level. | PIE: walk into trigger; level loads (or doc Level Streaming step). |
| **D. Planetoid POI** | Player lands on planetoid, approaches Shrine or Treasure POI; interact. | PIE: open planetoid via portal; E on Shrine_POI or Treasure_POI; log or reward. |

**Default for slice:** Option A (claim homestead) — aligns with "claim home as base for rescue" in VISION. Lock in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) when chosen.

---

## 2. Chosen corner (pick one and lock in PROTOTYPE_SCOPE)

| Option | Description | Verification |
|--------|-------------|---------------|
| **A. Homestead compound** | DemoMap (or Homestead) area with placed buildings, resource nodes, PCG trees. | Viewport: clear sightline to placed assets + trees; no obvious holes or floating meshes. |
| **B. Forest approach** | PCG forest with harvestable trees; player visible in frame. | Viewport: dense trees, character in frame; PIE walk-through. |
| **C. Planetoid POI cluster** | Planetoid level with PCG POI (Shrine/Treasure cubes); one framed shot. | Open planetoid level; PCG Generate; frame one POI-rich area. |
| **D. Dungeon entrance** | Dungeon_POI or BP_DungeonEntrance in level; clear "this is the dungeon" read. | Place entrance per DAYS_16_TO_30 Day 24; single hero shot. |

**Default for slice:** Option A (homestead compound) — one polished area showing explore → harvest → place. Lock in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) when chosen.

---

## 3. Pre-demo checklist (before recording or showing)

- [ ] **Level:** DemoMap (or Homestead) open; PCG generated; no "no surfaces" or empty volume.
- [ ] **Character:** BP_HomeWorldCharacter; Enhanced Input applied (movement + look); GAS abilities (LMB, Shift, E, P) granted.
- [ ] **Moment:** Chosen moment (1.A–D) playable in PIE; key action (place / harvest / trigger / interact) works.
- [ ] **Corner:** Chosen corner (2.A–D) visible in viewport; no critical LOD or lighting bugs.
- [ ] **Stability:** PIE run 2–5 min without crash; no repeated log errors.

**Automated support:** With PIE running, run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script). Results in `Saved/pie_test_results.json` cover: character spawn, on ground, capsule, placement API, PCG actor count. Use these to confirm Character and Level/PCG aspects of the checklist.

**Vertical slice lock (N1):** Moment (**Claim homestead**) and corner (**Homestead compound**) are locked in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md). Pre-demo checklist can be run as above; optional 1–3 min demo recording per §4 is user-led.

---

## 4. Demo recording steps (optional)

1. Open DemoMap (or chosen level); start PIE.
2. Establish shot: show the **corner** (e.g. homestead area).
3. Play the **moment** (e.g. walk up, harvest, then place building with P).
4. Optional: cut to planetoid or dungeon if showing scope.
5. Keep clip to 1–3 minutes for vertical slice.

---

## 5. After buffer (Days 26–30)

- Lock **Chosen moment** and **Chosen corner** in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- Update asset table in PROTOTYPE_SCOPE when free packs or placeholders are chosen.
- If Milady pipeline is advanced, add a bullet to [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md) "Programmatic work completed" and link from this checklist.

---

**See also:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) Days 26–30, [VISION.md](VISION.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
