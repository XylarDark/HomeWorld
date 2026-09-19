# RS-C — Animal den

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE RS-C`**, 2026-09-19 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/21_REAP_SOW.md](../21_REAP_SOW.md) |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Placement script | [Content/Python/place_vs_mvp_rs_animal_den.py](../../Content/Python/place_vs_mvp_rs_animal_den.py) |
| Day den | `GP_RS_AnimalDen` — `AHomeWorldBeastPad` + tame component (`TAME:` greps) |
| Night dream stub | `GP_RS_AnimalDen_Dream` — TargetPoint; placeholder recruit via `hw.Conversion.Test` |
| Level | `L_VS_MVP_Markers` — KEEP-LOCAL save after run |

---

## DESKTOP runbook (Conductor parent)

```text
place_vs_mvp_markers.py
place_vs_mvp_beast_tame.py          # optional NP pad
place_vs_mvp_rs_animal_den.py
# File → Save Current Level (KEEP-LOCAL)
```

**Day:** Face `GP_RS_AnimalDen` with RES_BERRY/HERB → Interact → `TAME: offer accepted` / bond.

**Night dream stub:** Approach `GP_RS_AnimalDen_Dream`; console `hw.Conversion.Test` → convert/recruit hook logs (full dream combat deferred).

Editor MCP offline at stamp — DESKTOP PIE deferred accept under Lead **`APPROVE RS-C`**.

---

## Gate

Lead **`APPROVE RS-C`**, 2026-09-19 ET — **GRANTED**. Unlocks **RS-D** (humanoid camp).
