# PA-C — Blender rebuild / upgrade (Homestead kit)

| Field | Value |
|-------|-------|
| **Status** | Lead **`APPROVE PA-C`** **GRANTED** (chat, 2026-09-22 ET) · **IN PROGRESS** |
| **Tranche 1** | **COMPLETE** — cliffs (3) + pine foliage upgrade landed in `AssetCreation/Exports/Homestead/` |
| **Track** | Whole **PA track not CLOSED** — PA-D import / PA-E evidence still **LOCKED** until remaining PA-C queue + Lead PA-E gate |
| **Host** | DESKTOP + Blender MCP (export) · CLOUD (mesh land + docs) |
| **Impl doc** | [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| **Prior** | [PA_A_GAP_AUDIT.md](PA_A_GAP_AUDIT.md) **APPROVED / CLOSED** — Lead **`APPROVE PA-A`**, 2026-09-22 ET |

**Do not** stamp whole **PA track CLOSED** or **PA-E done** until Shot 1/2 evidence.

---

## Lead gate (record)

Lead typed in chat (2026-09-22 ET):

```text
APPROVE PA-C
```

Unlocks continued PA-C Blender work and PA-D prep on DESKTOP. **Tranche 1** meshes are review-ready on branch; no `.uasset` in this land.

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

## PA-C queue status

| # | Item | Status |
|---|------|--------|
| 1 | Cliff modules | **DONE** (tranche 1) |
| 2 | Pines S/M/L | **DONE** (tranche 1) |
| 3 | Cabin | **PENDING** |
| 4 | Path stones | **PENDING** |
| 5 | Planters ×3 | **PENDING** |
| 6 | Fence segments | **PENDING** |
| 7 | Glider perch | **PENDING** |
| 8 | Optional island rim | **PENDING** |

**KEEP (no mesh unless polish):** IslandTop, Lookout pad, Soft shrine, Islets optional.

---

## UE placement note (PA-D)

Cliff assemblies export at **(0,0,0)** with geometry relative to graybox empty origins. Place in VS_MVP at:

- LookoutFace: `(7.5, -5.5, -4.0)`
- CabinFace: `(-7.0, -4.5, -3.0)`
- Rear: `(0.0, 5.0, -2.5)`

---

## DESKTOP chain (next)

```text
# Remaining PA-C queue in Blender MCP + STYLE_GUIDE
# AssetCreation/Blender/export_to_asset_creation.py
.\Tools\Safe-Build.ps1
execute_python_script("batch_import_asset_creation.py")
execute_python_script("place_vs_mvp_dress.py")
```

Cloud agents: land FBX + docs only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist

- [x] Lead **`APPROVE PA-C`** stamped (2026-09-22 ET)
- [x] Tranche 1 FBX in `AssetCreation/Exports/Homestead/`
- [x] Tranche report + this handoff
- [ ] Tranche 2+ Blender exports (DESKTOP)
- [ ] PA-D import + master bind (DESKTOP)
- [ ] PA-E Shot 1/2 evidence (DESKTOP + Lead)
