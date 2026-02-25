# HomeWorld – Task list (master)

Current focus tasks. Each links to a doc with remaining steps and in-depth manual guides where work is Editor-only. Task 1 (Animation), Task 2 (Orientation), and Task 3 (Character on ground) completed this round; terrain/walk-on-surface deferred.

| # | Task | Doc | Status | Remaining |
|---|------|-----|--------|-----------|
| 1 | Fix character animation | [CHARACTER_ANIMATION.md](tasks/CHARACTER_ANIMATION.md) | ✓ Completed | Done |
| 2 | Fix character orientation | [CHARACTER_ORIENTATION.md](tasks/CHARACTER_ORIENTATION.md) | ✓ Completed | Done |
| 3 | Character on ground | [CHARACTER_GROUND.md](tasks/CHARACTER_GROUND.md) | ✓ Completed | Done |
| 4 | PCG forest on map | [PCG_FOREST_ON_MAP.md](tasks/PCG_FOREST_ON_MAP.md) | ✓ Verified | Optional: visual spot-check |
| 5 | Family agents (Mass + State Tree) | [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md) | Not started | Week 2: MEC, State Tree, spawner, ZoneGraph, Smart Objects |
| 6 | Agentic building (Mass + Smart Objects) | [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md) | Not started | Week 2; extends Task 5. Build orders, SO, State Tree BUILD, resource piles. |

Week 1 scope aligns with [ROADMAP.md](../ROADMAP.md) Phase 1. Week 2 scope: family agents per [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md).

---

## Remaining work (summary)

### Task 1 — Animation ✓
Complete. C++ AnimInstance, ABP_HomeWorldCharacter, AnimGraph Locomotion (Idle/WalkRun with Speed), and PIE verification done for this round.

### Task 2 — Orientation ✓
Complete. Mesh forward yaw offset default -90 in C++ so mesh faces movement direction; verified in PIE.

### Task 3 — Ground ✓
Complete. Character on ground verified (MOVE_WALKING, capsule 42r/88h). Next focus was Task 3; closed. Terrain / walk-on-surface deferred to later.

### Task 4 — PCG forest ✓
1161 actors generated. Optional: visual check that trees cover landscape and village is clear.

### Task 5 — Family agents (Mass + State Tree) — Week 2
Enable Week 2 plugins (Mass Entity, Mass AI, StateTree, ZoneGraph, SmartObjects); create MEC_FamilyGatherer, ST_FamilyGatherer, Mass Spawner, ZoneGraph lanes, Smart Objects; PIE test. See [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md).

### Task 6 — Agentic building (Mass + Smart Objects) — Week 2
Extends Task 5. Create BP_BuildOrder_Wall (from AHomeWorldBuildOrder), BP_WoodPile (from AHomeWorldResourcePile), SO_WallBuilder and HarvestWood Smart Objects, State Tree BUILD branch, MP_WoodInventory; PIE test. See [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md).

**Latest PIE run (Editor open):** 5/7 checks passed — PIE active, character spawned, on ground, capsule 88/42, PCG 1161 actors. Skeletal mesh/AnimInstance can show false negatives from Python in PIE.

---

**See also:** [SETUP.md](SETUP.md), [CONVENTIONS.md](CONVENTIONS.md), [ROADMAP.md](../ROADMAP.md), [KNOWN_ERRORS.md](KNOWN_ERRORS.md).
