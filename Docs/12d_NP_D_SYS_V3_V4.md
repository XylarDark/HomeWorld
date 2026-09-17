# Docs/12d — NP-D SYS V3–V4 (Gather + Tame)

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE NP-D`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Unlocked by** | Lead **`APPROVE NP-C`**, 2026-09-17 ET |
| **Canon** | [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) §2–5 |

---

## Deliverables

| Item | Path | Disposition |
|------|------|-------------|
| Six-slot inventory-lite | `Source/HomeWorld/HomeWorldInventorySubsystem.*` + `HomeWorldInventoryTypes.*` | **PRESENT** — RES_* only; stack max 9 |
| Legacy gather evolve | `TryHarvestInFront`, `AHomeWorldResourcePile::TryHarvest` | **PRESENT** — Wood/Ore/Flowers → RES_* |
| Beast tame SM | `Source/HomeWorld/HomeWorldBeastTameComponent.*` | **PRESENT** — wild→cautious→tamed→helper |
| Interact wiring | `HomeWorldInteractAbility`, `TryTameBeastInFront` | **PRESENT** — E key after portal, before gather |
| Beast pad script | `Content/Python/place_vs_mvp_beast_tame.py` | **PRESENT** — idempotent tame component on pad |
| Handoff | [handoffs/NP_D_SYS_V3_V4.md](handoffs/NP_D_SYS_V3_V4.md) | **PRESENT** |

---

## V3 — RES_* six-slot inventory

| Rule | Implementation |
|------|----------------|
| Exactly 6 slots | `HomeWorldInventory::SlotCount` |
| RES_WOOD … RES_SEED | `HomeWorldInventoryTypes.h` |
| Stack max 9 | `HomeWorldInventory::StackMax` |
| Gather +1 | `AmountPerHarvest` default 1 on `AHomeWorldResourcePile` |
| Fail if full | `TryAddResource` → `GATHER:` log |
| Day/body only | `TryHarvestInFront` checks night + spirit form |
| Node deplete until dawn | `bDepleteUntilDawn` on resource pile (default true) |
| Legacy names | Wood→RES_WOOD, Ore→RES_STONE, Flowers→RES_HERB |

**Console (PIE):**

```text
hw.Gather.Ore 1      → RES_STONE +1
hw.Gather.Flowers 1  → RES_HERB +1
hw.Goods             → logs all six RES_* counts
```

---

## V4 — Beast tame

| State | Enter | Log prefix |
|-------|-------|------------|
| wild | spawn | `TAME: component ready … state=wild` |
| cautious | pad proximity | `TAME: wild -> cautious` |
| tamed | offer + bond wait ~4s | `TAME: bond complete -> tamed` |
| helper | interact while tamed (day) | `TAME: tamed -> helper` |

| Rule | Implementation |
|------|----------------|
| Offer food | 1× RES_BERRY (prefer) or RES_HERB |
| Wrong item | soft reject — `TAME: soft reject` |
| Day/body only | blocked at night / spirit form |
| No combat | no damage APIs |

---

## Windows Safe-Build (C++ changed)

After merge:

```powershell
.\Tools\Safe-Build.ps1
```

Then (Editor):

```text
execute_python_script("place_vs_mvp_beast_tame.py")
```

Local `.umap` changes from placement are **not committed**.

---

## PIE runbook — gather + tame

**Prerequisites:** Safe-Build; `L_VS_MVP_Markers`; day phase (`hw.TimeOfDay.Phase 0`).

### V3 Gather

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | `hw.Gather.Ore 1` | `GATHER: RES_STONE +1` |
| 2 | Face harvest pile / tree; Interact (E) | `GATHER: RES_WOOD +1` (or mapped RES_*) |
| 3 | Repeat until stack 9 | `GATHER: fail stack full` |
| 4 | `hw.Goods` | Six RES_* counts printed |
| 5 | `hw.TimeOfDay.Phase 2` + Interact pile | `GATHER: blocked — night or spirit form` |

### V4 Tame

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | Run `place_vs_mvp_beast_tame.py` | Beast pad actor gets tame component |
| 2 | `hw.Gather.Flowers 1` (or berry gather) | RES_HERB or RES_BERRY in inventory |
| 3 | Walk to beast pad; Interact (E) | `TAME: offer accepted` |
| 4 | Stay in radius ~4s | `TAME: bond complete -> tamed` |
| 5 | Interact again (day) | `TAME: tamed -> helper` (optional) |
| 6 | Interact with no food | `TAME: soft reject` |

### NightMix smoke (residual)

`smoke_nightmix_phase.py` — fix only if trivial on Windows; not blocking NP-D gate.

---

## Gate

Lead **`APPROVE NP-D`** → unlock **NP-E** (SYS V6–V8 heal + nurture + dawn persist).

---

*NP-D delivered 2026-09-17 ET under Lead APPROVE NP-C.*
