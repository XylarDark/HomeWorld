# RS-D — Humanoid camp

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE RS-D`**, 2026-09-19 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/21_REAP_SOW.md](../21_REAP_SOW.md) |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Placement script | [Content/Python/place_vs_mvp_rs_humanoid_camp.py](../../Content/Python/place_vs_mvp_rs_humanoid_camp.py) |
| Day camp | `GP_RS_HumanoidCamp` — visit landmark |
| Day collect | `GP_RS_HumanoidCamp_Collect` — post-recruit collect stub |
| Night dream | `GP_RS_HumanoidCamp_Dream` — convert/recruit via `hw.Conversion.Test` (placeholder GA deferred) |
| Level | `L_VS_MVP_Markers` — KEEP-LOCAL save after run |

---

## DESKTOP runbook (Conductor parent)

```text
place_vs_mvp_markers.py
place_vs_mvp_rs_humanoid_camp.py
# File → Save Current Level (KEEP-LOCAL)
```

**Night:** At `GP_RS_HumanoidCamp_Dream` → `hw.Conversion.Test` → `Foe converted (strip sin → loved)` / ConvertedFoesThisNight.

**Day:** Visit `GP_RS_HumanoidCamp` / `GP_RS_HumanoidCamp_Collect` (markers; inventory collect interact deferred).

Editor MCP offline at stamp — DESKTOP PIE deferred accept under Lead **`APPROVE RS-D`**.

---

## Gate

Lead **`APPROVE RS-D`**, 2026-09-19 ET — **GRANTED**. Unlocks **RS-E** (special cross-bonus site).
