# Docs/12b — NP-B Lookdev Apply

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE NP-B`** |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Prerequisite** | Lead **`APPROVE NP-A`** — **GRANTED**; [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) |
| **Script** | `Content/Python/assign_vs_mvp_materials.py` |
| **Mapping module** | `Content/Python/homeworld_vs_mvp_material_rules.py` |
| **Evidence base** | Windows DESKTOP-21CT3H0 at repo **HEAD `82c7eb2`** |

**Gate:** Lead **`APPROVE NP-B`** after evidence review in [handoffs/NP_B_LOOKDEV.md](handoffs/NP_B_LOOKDEV.md).

---

## What you'll do

Assign the **ten Docs/02 masters** onto every `DRESS_*` StaticMesh actor in `L_VS_MVP_Markers`, optionally smoke NightMix on `MPC_HomeWorld_Time`, and save the level **locally on Windows** (no `.uasset`/`.umap` commit).

Hard rules: Docs/07 CLOSED; FALLBACK armed; no free-flight; exactly 10 masters; no V3–V8; no binary commits.

---

## 0. Preconditions (Windows DESKTOP-21CT3H0)

Run in order if assets are missing after `git pull`:

1. `batch_import_asset_creation.py` — meshes under `/Game/HomeWorld/Meshes/...`
2. `create_master_materials.py` — ten masters under `/Game/HomeWorld/Materials/Masters/M_*`
3. `place_vs_mvp_markers.py` — level + `MPC_HomeWorld_Time`
4. `place_vs_mvp_dress.py` — `DRESS_*` kit actors in `VS_MVP/Dress`

See [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) for host inventory at prior HEAD.

---

## 1. Run material assign

1. Open Unreal Editor 5.7 from repo root (`HomeWorld.uproject`).
2. **Tools → Execute Python Script** → `Content/Python/assign_vs_mvp_materials.py`  
   Or via MCP: `execute_python_script("assign_vs_mvp_materials.py")`
3. Output Log prefix: `assign_vs_mvp_materials:`

**Idempotent:** Re-run skips slots already using the resolved MI/master path; only missing or wrong assignments are updated.

**Flags:**

| Flag | Effect |
|------|--------|
| (default) | NightMix smoke: MPC scalar `NightMix` → `0.0` then `0.85` |
| `--no-nightmix-smoke` | Skip MPC smoke |

---

## 2. Mesh → master cite matrix (automation)

Rules follow [02_MATERIAL_SHEET.md](02_MATERIAL_SHEET.md) §3 and [04_EXPORT_TABLE.md](04_EXPORT_TABLE.md) §4. First matching rule wins.

| Mesh family (basename patterns) | Master |
|--------------------------------|--------|
| `*Glow*`, `*Spirit*`, `*Wound*` | M_SpiritUnlit |
| `SM_Beast*` | M_BeastStylized |
| `*RES_STONE*` | M_CliffRock |
| `*RES_WOOD*`, `*RES_FUEL*` | M_WoodWild |
| `*RES_SEED*`, `*RES_CROP*` | M_Nurtured |
| Other `*RES_*` | M_GatherHerb |
| `*Foliage*`, `*Needle*`, `*Canopy*`, `*Card*`, `*_Leaves*` | M_FoliageCard |
| `*Pine*` (trunk default) | M_WoodWild |
| `SM_Cliff*`, `SM_Islet*`, `*ValleyLip*`, `*Chunk_Torn*` | M_CliffRock |
| `SM_IslandTop`, `SM_Planet_GroundPlate`, `*Grass*`, `*Soil*`, `*GardenBed*` | M_StylizedGrass |
| `*PathStone*`, `*Path_Planet*`, `*LandingCircle*`, `SM_Lookout_Pad` | M_PathStone |
| `*Gather*`, `*Herb*`, `*Berry*`, `*Bush*`, `*Fern*`, `*Vine*`, `*Flax*`, `*Planter*` | M_GatherHerb |
| `SM_Cabin*`, `SM_Glider_Perch`, `*Roof_Hamlet*`, `*Perch*` | M_WoodCabin |
| `*Shrine*` (non-glow) | M_WoodCabin |
| `*Nurture*`, `*Crop*` | M_Nurtured |

Material resolution order per master: `/Game/HomeWorld/Materials/Instances/MI_<ShortName>` → `M_*_Inst` → `/Game/HomeWorld/Materials/Masters/M_*`.

---

## 3. Verify (Windows)

- [x] Output Log: `assign_vs_mvp_materials: Done` with `actors` = **78**, `missing_master` = 0
- [x] `slots_assigned` = **78** on first run; `slots_skipped` = 0
- [ ] NightMix smoke lines: **FAILED** — `KismetMaterialLibrary` missing in UE 5.7 Python (non-blocking; C++ PIE path OK)
- [x] Viewport: island grass, cabin wood, path/landing stone, shrine glow accents (host spot-check)
- [x] Level saved on disk — `L_VS_MVP_Markers` **local only**, not committed
- [x] FALLBACK reminder logged (CRUMB glide + portal; no free-flight)

---

## 4. Windows run result (2026-09-17, DESKTOP-21CT3H0)

**HEAD:** `82c7eb2`

```
assign_vs_mvp_materials: Done {
  actors: 78,
  slots_assigned: 78,
  slots_skipped: 0,
  missing_master: 0,
  unmapped: 0,
  masters_used: [M_CliffRock, M_FoliageCard, M_GatherHerb, M_PathStone, M_SpiritUnlit, M_StylizedGrass, M_WoodCabin, M_WoodWild]
}
```

| Master | Applied | Notes |
|--------|---------|-------|
| M_CliffRock | yes | |
| M_FoliageCard | yes | |
| M_GatherHerb | yes | |
| M_PathStone | yes | |
| M_SpiritUnlit | yes | shrine glow accents |
| M_StylizedGrass | yes | island / ground plate |
| M_WoodCabin | yes | cabin / shrines |
| M_WoodWild | yes | |
| M_BeastStylized | no | **PRESENT** on host; no beast DRESS meshes — expected |
| M_Nurtured | no | **PRESENT** on host; no nurture/crop DRESS meshes — expected |

**NightMix smoke:** script path failed (`unreal.KismetMaterialLibrary`); assign pass **not affected**. Residual for NP-C or follow-up.

Full handoff: [handoffs/NP_B_LOOKDEV.md](handoffs/NP_B_LOOKDEV.md).

---

## 5. Explicit non-goals

- V3–V8 SYS verbs (NP-D / NP-E)
- Free-flight / combat / Lumen / Nanite gates
- `.uasset` / `.umap` in git
- Reopening Docs/07

---

## 6. Related

- Inventory: [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md)
- Dress runbook: [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md)
- Handoff evidence: [handoffs/NP_B_LOOKDEV.md](handoffs/NP_B_LOOKDEV.md)
- Strategy gates: [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md)

---

*Windows lookdev apply complete 2026-09-17 ET. Awaiting Lead **`APPROVE NP-B`**.*
