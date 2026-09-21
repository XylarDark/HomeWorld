# GC-A — Site→RES map + flint/grass flavor

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE GC-A`**, 2026-09-21 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/22_GATHER_CRAFT_IMPL.md](../22_GATHER_CRAFT_IMPL.md) |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Site kind enum + resolve | `Source/HomeWorld/HomeWorldGatherSiteTypes.h/.cpp` |
| Pile harvest | `AHomeWorldResourcePile::GatherSiteKind`, infer `GC_Site_*` tags / `GP_RS_*` labels |
| Normalize aliases | `Flint`→`RES_STONE`, `Grass`→`RES_FIBER` in `HomeWorldInventoryTypes.cpp` |
| GC tags helper | `Content/Python/homeworld_gc_site_setup.py` |
| Planet triad | `place_vs_mvp_rs_material_sites.py` — `GP_RS_Tree` / `GP_RS_Rock` / `GP_RS_Flower` |
| Homestead piles | `place_vs_mvp_resource_piles.py` — `GP_Gather_WOOD` / `STONE` / `FIBER` (+ berry/seed) |

---

## Done criteria

- [ ] Day/body interact at `GP_RS_*` or `GP_Gather_*` piles yields inventory + logs
- [ ] Output Log greps include **`GATHER: RES_WOOD`**, **`GATHER: RES_STONE`**, **`GATHER: RES_FIBER`**
- [ ] Optional flavor greps: **`GATHER: RES_STONE (flint)`**, **`GATHER: RES_FIBER (grass)`**
- [ ] Flowers site alternates **`RES_HERB`** on second harvest (same pile)
- [ ] `hw.Gather.Seed` still grants **`RES_SEED`** (unchanged)
- [ ] No 7th `RES_*` id introduced

---

## DESKTOP runbook (Conductor parent)

```text
.\Tools\Safe-Build.ps1
# Editor: execute_python_script
place_vs_mvp_markers.py
place_vs_mvp_resource_piles.py
place_vs_mvp_rs_material_sites.py
# File → Save Current Level (KEEP-LOCAL)
# PIE: day/body, face pile within ~280cm, Interact (E)
```

**Expected greps (Output Log):**

```text
GATHER: RES_WOOD
GATHER: RES_STONE
GATHER: RES_FIBER
GATHER: RES_STONE (flint)
GATHER: RES_FIBER (grass)
```

**Cheat fallback (inventory only, not site proof):**

```text
hw.Gather.Ore 1    → RES_STONE + flint flavor line
hw.Gather.Seed 1   → RES_SEED
```

---

## CLOUD evidence (this PR)

- C++ compiles on CI header pairing / validate workflow
- Code review: harvest path uses `ResolveHarvestResourceId()` before `TryAddResource`
- Python placement sets `GC_Site_*` tags for explicit mapping

---

## Gate

Lead **`APPROVE GC-A`** in chat — **GRANTED** unlocks **GC-B** (campfire + tent + `PROGRESS:COTTAGE_UNLOCK`). Do not stamp in PR.
