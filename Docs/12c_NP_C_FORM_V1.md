# Docs/12c — NP-C Form + V1 Polish

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead **`APPROVE NP-C`**, 2026-09-17 ET |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Unlocked by** | Lead **`APPROVE NP-B`**, 2026-09-17 ET |
| **Scope** | V1 walk + form swap + V2/V5 verify runbook |

---

## Deliverables

| Item | Path | Disposition |
|------|------|-------------|
| GP_PlayerStart + PlayerStart | `Content/Python/place_vs_mvp_gp.py` | **PRESENT** — idempotent on `L_VS_MVP_Markers` |
| Form swap body↔spirit | `Source/HomeWorld/HomeWorldCharacter.*` + `HomeWorldTimeOfDaySubsystem.*` | **PRESENT** — `FORM:` logs; Night/Dusk → spirit; Day/Dawn → body |
| Soft walk bounds | `Source/HomeWorld/HomeWorldSoftBoundsComponent.*` + `vs_mvp_walk_bounds.json` | **PRESENT** — cylindrical pushback; navmesh **DEFER** |
| V2/V5 PIE runbook | This doc § Runbook | **PRESENT** |
| NightMix smoke | `Content/Python/smoke_nightmix_phase.py` | **PRESENT** — MaterialLibrary UE 5.7 API |
| Handoff | [handoffs/NP_C_FORM_V1.md](handoffs/NP_C_FORM_V1.md) | **PRESENT** |

---

## Form swap (Docs/03 §4, §7)

| Phase | Form | NightMix (C++) |
|-------|------|----------------|
| Day | body | 0.0 |
| Dusk | spirit | 0.35 |
| Night | spirit | 0.85 |
| Dawn | body | 0.15 |

- **No free-flight** — spirit uses same walk + soft bounds as body.
- **Log prefix:** `FORM:` on transition (grep Output Log).
- **Test:** `hw.TimeOfDay.Phase 2` → spirit; `hw.TimeOfDay.Phase 0` → body.

---

## V1 walk bounds

- **Implemented:** `UHomeWorldSoftBoundsComponent` on `AHomeWorldCharacter` — soft pushback toward island hub.
- **Config:** `Content/Python/vs_mvp_walk_bounds.json` (21 m graybox footprint).
- **Deferred:** Navmesh / blocking volumes — document only; use `check_level_bounds.py` on VS_MVP level for bounds reminder.

---

## Windows Safe-Build (C++ changed)

After merge, Conductor on **DESKTOP-21CT3H0** must run:

```powershell
.\Tools\Safe-Build.ps1
```

Then re-run Editor scripts: `place_vs_mvp_gp.py`, `place_fallback_glide_markers.py` (if level stale).

---

## PIE runbook — V2 glide + V5 portal

**Prerequisites:** Safe-Build complete; `L_VS_MVP_Markers` open; scripts run (`bootstrap_project.py` or individual place scripts).

### Setup

1. Open `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`.
2. PIE with `AHomeWorldGameMode` / `BP_HomeWorldCharacter`.
3. Confirm spawn at homestead hub (`GP_PlayerStart` / PlayerStart).

### V1 walk

| Step | Action | Expected log / result |
|------|--------|------------------------|
| 1 | Walk toward lookout | Movement OK; optional `BOUNDS: soft pushback` if near cliff edge |
| 2 | `hw.TimeOfDay.Phase 2` | `FORM: spirit form`; NightMix 0.85 on MPC |
| 3 | `hw.TimeOfDay.Phase 0` | `FORM: body form`; NightMix 0.0 |

### V2 FALLBACK glide (day/body only)

| Step | Action | Expected log / result |
|------|--------|------------------------|
| 1 | `hw.TimeOfDay.Phase 0` | Body form |
| 2 | Move to `GP_GlideStart` / `CRUMB_Depart_Lookout` | — |
| 3 | Interact (E) | `FALLBACK: TryStartFallbackGlide started`; CRUMB_* resolve logs |
| 4 | Wait traverse | `FALLBACK:` segment logs; landing restores walk |
| 5 | `hw.TimeOfDay.Phase 2` + Interact at glide start | `FALLBACK: StartGlide blocked — night phase` |

Optional: `execute_python_script("pie_test_runner.py")` → read `Saved/pie_test_results.json`.

### V5 portal (night/spirit only)

| Step | Action | Expected log / result |
|------|--------|------------------------|
| 1 | `hw.TimeOfDay.Phase 2` | Spirit form |
| 2 | Walk into `GP_PortalA` trigger (homestead shrine) | `FALLBACK: Portal` transit logs |
| 3 | Arrive at planet return shrine | Position near `ANCHOR_SM_Shrine_Return` |
| 4 | Walk into `GP_PortalB` | Return to homestead shrine |
| 5 | `hw.TimeOfDay.Phase 0` + portal | Portal locked (day/body) — no transit |

### NightMix smoke (bonus)

```text
execute_python_script("smoke_nightmix_phase.py")
```

Expect four `OK phase=… NightMix=…` lines in Output Log.

---

## Gate

Lead **`APPROVE NP-C`** — **GRANTED** (Luke Thompson, 2026-09-17 ET) → **NP-D** unlocked.

---

*NP-C APPROVED 2026-09-17 ET. NP-D delivered same day.*
