# RS-B — Material triad (trees / rocks / flowers)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE RS-B`**, 2026-09-19 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/21_REAP_SOW.md](../21_REAP_SOW.md) |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Placement script | [Content/Python/place_vs_mvp_rs_material_sites.py](../../Content/Python/place_vs_mvp_rs_material_sites.py) |
| Day sites | `GP_RS_Tree` (RES_WOOD), `GP_RS_Rock` (RES_STONE), `GP_RS_Flower` (RES_HERB) — `AHomeWorldResourcePile` |
| Night sow markers | `GP_RS_Tree_Sow` / `GP_RS_Rock_Sow` / `GP_RS_Flower_Sow` — TargetPoints (nurture enum extension deferred) |
| Level | `L_VS_MVP_Markers` — KEEP-LOCAL save after run |

---

## DESKTOP runbook (Conductor parent)

```text
place_vs_mvp_markers.py
place_vs_mvp_resource_piles.py   # optional homestead piles
place_vs_mvp_rs_material_sites.py
# File → Save Current Level (KEEP-LOCAL)
```

**Expected day greps:** `GATHER: RES_WOOD` / `RES_STONE` / `RES_HERB` or `GATHER: harvest ok` facing `GP_RS_*` (~280 cm, day/body).

**Night sow:** Markers only this phase — full `NURTURE:` on material sites needs nurture-target enum extension (follow-on). Lead **`APPROVE RS-B`** accepted CLOUD script + early unlock without DESKTOP PIE table (Editor MCP unavailable at stamp time).

---

## Gate

Lead **`APPROVE RS-B`**, 2026-09-19 ET — **GRANTED**. Unlocks **RS-C** (animal den).
