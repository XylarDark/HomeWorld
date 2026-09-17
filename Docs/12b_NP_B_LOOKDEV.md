# Docs/12b — NP-B Lookdev Apply

| Field | Value |
|-------|-------|
| **Status** | **IN PROGRESS** — script + runbook delivered; Windows evidence pending |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (NP-B) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Prerequisite** | Lead **`APPROVE NP-A`** — **GRANTED**; [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) |
| **Script** | `Content/Python/assign_vs_mvp_materials.py` |
| **Mapping module** | `Content/Python/homeworld_vs_mvp_material_rules.py` |

**Gate:** Lead **`APPROVE NP-B`** after Conductor runs script on DESKTOP and fills [handoffs/NP_B_LOOKDEV.md](handoffs/NP_B_LOOKDEV.md) evidence.

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

- [ ] Output Log: `assign_vs_mvp_materials: Done` with `actors` > 0, `missing_master` = 0
- [ ] `slots_assigned` > 0 on first run; `slots_skipped` dominates on re-run
- [ ] NightMix smoke lines: `NightMix smoke set` for 0.0 and 0.85 (unless `--no-nightmix-smoke`)
- [ ] Viewport: island grass tone, cabin wood, path/landing stone, shrine glow accents readable
- [ ] Level saved on disk under `Content/.../L_VS_MVP_Markers.umap` — **not** committed
- [ ] FALLBACK reminder logged (CRUMB glide + portal; no free-flight)

---

## 4. Explicit non-goals

- V3–V8 SYS verbs (NP-D / NP-E)
- Free-flight / combat / Lumen / Nanite gates
- `.uasset` / `.umap` in git
- Reopening Docs/07

---

## 5. Related

- Inventory: [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md)
- Dress runbook: [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md)
- Handoff evidence: [handoffs/NP_B_LOOKDEV.md](handoffs/NP_B_LOOKDEV.md)
- Strategy gates: [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md)
