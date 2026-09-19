# RS-E — Special cross-bonus site

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE RS-E`**, 2026-09-19 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/21_REAP_SOW.md](../21_REAP_SOW.md) |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Placement | [place_vs_mvp_rs_special_site.py](../../Content/Python/place_vs_mvp_rs_special_site.py) |
| Landmark | `GP_RS_SpecialSite` (+ `GP_RS_Special_DayBonus` / `GP_RS_Special_NightBonus`) |
| Cross-buff pipe | PlayerState `bHasRSDayBonusForNight` / `bHasRSNightBonusForDay`; cleared at dawn |
| Console | `hw.RS.CollectDayBonus` · `hw.RS.CollectNightBonus` · `hw.RS.CrossBonusStatus` |
| Greps | `RS: day_bonus` · `RS: night_bonus` · `RS: day→night cross_buff` · `RS: night→day cross_buff` · `RS: status` |

---

## DESKTOP prove (Conductor parent)

```text
.\Tools\Safe-Build.ps1
# Editor + MCP
place_vs_mvp_markers.py
place_vs_mvp_rs_special_site.py
# Save KEEP-LOCAL
```

PIE:

1. Day: `hw.RS.CollectDayBonus` → `RS: day_bonus collected; night_buff=1`
2. `hw.RS.CrossBonusStatus` → `day_bonus_for_night=1`
3. `hw.TimeOfDay.Phase 2` then `hw.RS.CollectNightBonus` → `RS: night_bonus collected; day_buff=1`
4. `hw.RS.CrossBonusStatus` → both flags (or night→day after dawn cycle as desired)

---

## Gate

Lead **`APPROVE RS-E`**, 2026-09-19 ET — **GRANTED**. Docs/21 Reap & Sow **CLOSED / COMPLETE**.
