# PA-C — Blender rebuild / upgrade (Homestead kit)

| Field | Value |
|-------|-------|
| **Status** | Lead **`APPROVE PA-C`** **GRANTED** (chat, 2026-09-22 ET) · **IN PROGRESS** (optional island rim only) |
| **Tranche 1** | **COMPLETE** — cliffs (3) + pine foliage upgrade |
| **Tranche 2** | **COMPLETE** — cabin, path stones, planters, fence, glider perch |
| **Track** | Whole **PA track not CLOSED** — **PA-D OPEN** (import/place); PA-E evidence **LOCKED** until Lead **`APPROVE PA-E`** |
| **Host** | DESKTOP + Blender MCP (export) · CLOUD (mesh land + docs) |
| **Impl doc** | [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| **Prior** | [PA_A_GAP_AUDIT.md](PA_A_GAP_AUDIT.md) **APPROVED / CLOSED** — Lead **`APPROVE PA-A`**, 2026-09-22 ET |

**Do not** stamp **`APPROVE PA-D`**, whole **PA track CLOSED**, or **PA-E done** until Shot 1/2 evidence + Lead PA-E gate.

---

## Lead gate (record)

Lead typed in chat (2026-09-22 ET):

```text
APPROVE PA-C
```

Unlocks PA-C Blender work and **PA-D prep** on DESKTOP. Tranche 1–2 FBX landed in `AssetCreation/Exports/Homestead/`; no `.uasset` in cloud land.

---

## Tranche 1 — delivered meshes

| Asset | Action | Tris | Notes |
|-------|--------|-----:|-------|
| `SM_Cliff_LookoutFace` | CREATE | 864 | M_CliffRock; portable origin |
| `SM_Cliff_CabinFace` | CREATE | 648 | M_CliffRock |
| `SM_Cliff_Rear` | CREATE | 540 | M_CliffRock |
| `SM_Pine_Homestead` | UPGRADE | 472 | Foliage Z-stack fix; S/M/L names preserved |

Evidence: [PA_C_TRANCHE1.md](PA_C_TRANCHE1.md) · manifest rows in [MVP_EXPORT_MANIFEST.md](../../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md).

---

## Tranche 2 — delivered meshes

| Asset | Action | Tris | Notes |
|-------|--------|-----:|-------|
| `SM_Cabin` | UPGRADE | 1680 | Rustic log/gable; UCX 5.5×4.5×5.5 |
| `SM_PathStone_A` | CREATE | 24 | M_PathStone |
| `SM_PathStone_B` | CREATE | 20 | M_PathStone |
| `SM_PathStone_C` | CREATE | 28 | M_PathStone |
| `SM_Planter_A` | CREATE | 240 | Raised bed + soil/plant proxies |
| `SM_Planter_B` | CREATE | 336 | M_Nurtured plant slot |
| `SM_Planter_C` | CREATE | 240 | M_GatherHerb plant slot |
| `SM_Garden_Fence_Seg` | CREATE | 100 | Post-and-rail; M_WoodCabin |
| `SM_Glider_Perch` | UPGRADE | 132 | Plank platform + rails + perch |

Evidence: [PA_C_TRANCHE2.md](PA_C_TRANCHE2.md) · manifest rows in [MVP_EXPORT_MANIFEST.md](../../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md).

---

## PA-C queue status

| # | Item | Status |
|---|------|--------|
| 1 | Cliff modules | **DONE** (tranche 1) |
| 2 | Pines S/M/L | **DONE** (tranche 1) |
| 3 | Cabin | **DONE** (tranche 2) |
| 4 | Path stones | **DONE** (tranche 2) |
| 5 | Planters ×3 | **DONE** (tranche 2) |
| 6 | Fence segments | **DONE** (tranche 2) |
| 7 | Glider perch | **DONE** (tranche 2) |
| 8 | Optional island rim | **PENDING** (optional) |

**KEEP (no mesh unless polish):** IslandTop, Lookout pad, Soft shrine, Islets optional.

---

## UE placement note (PA-D)

Cliff assemblies export at **(0,0,0)** with geometry relative to graybox empty origins. Place in VS_MVP at:

- LookoutFace: `(7.5, -5.5, -4.0)`
- CabinFace: `(-7.0, -4.5, -3.0)`
- Rear: `(0.0, 5.0, -2.5)`

Cabin portable kit origin `(0,0,0)` — place at `SOCKET_Cabin` (−6, 1, 0) per tranche-2 report.

---

## DESKTOP chain (PA-D — OPEN)

```text
.\Tools\Safe-Build.ps1
execute_python_script("batch_import_asset_creation.py")
execute_python_script("place_vs_mvp_dress.py")
```

Cloud agents: land FBX + docs only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist

- [x] Lead **`APPROVE PA-C`** stamped (2026-09-22 ET)
- [x] Tranche 1 FBX in `AssetCreation/Exports/Homestead/`
- [x] Tranche 2 FBX in `AssetCreation/Exports/Homestead/`
- [x] Tranche 1 + 2 reports + this handoff
- [ ] Optional island rim (DESKTOP / Lead optional)
- [ ] PA-D import + master bind (DESKTOP) — **OPEN**, not Lead-approved
- [ ] PA-E Shot 1/2 evidence (DESKTOP + Lead)
