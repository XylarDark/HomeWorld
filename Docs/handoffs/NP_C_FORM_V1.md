# Handoff — NP-C Form + V1 Polish

| Field | Value |
|-------|-------|
| **Phase** | NP-C |
| **Status** | COMPLETE — awaiting **`APPROVE NP-C`** |
| **Lead stamp** | NP-B **APPROVED** (Luke Thompson, 2026-09-17 ET) |
| **Deliverable** | [12c_NP_C_FORM_V1.md](../12c_NP_C_FORM_V1.md) |

---

## What shipped

1. **`place_vs_mvp_gp.py`** — `GP_PlayerStart` TargetPoint + `PlayerStart` at cabin/homestead hub on `L_VS_MVP_Markers`.
2. **Form swap** — `AHomeWorldCharacter::ApplyFormForPhase` driven by `UHomeWorldTimeOfDaySubsystem::OnPhaseChanged`; logs `FORM:`.
3. **Soft bounds** — `UHomeWorldSoftBoundsComponent`; config `Content/Python/vs_mvp_walk_bounds.json`; navmesh deferred.
4. **Runbook** — PIE checklist for V2 glide + V5 portal in Docs/12c.
5. **NightMix smoke** — `smoke_nightmix_phase.py` (MaterialLibrary API).

---

## Windows follow-up (required for C++)

```powershell
.\Tools\Safe-Build.ps1
```

Then in Editor (MCP or Execute Python Script):

- `place_vs_mvp_gp.py`
- `place_fallback_glide_markers.py` (if not in bootstrap chain)
- PIE runbook § in [12c_NP_C_FORM_V1.md](../12c_NP_C_FORM_V1.md)

---

## Evidence to capture

- Output Log: `FORM:` lines on phase toggle
- Output Log: `FALLBACK:` glide + portal lines
- Optional: `Saved/pie_test_results.json` after `pie_test_runner.py`

---

## Next gate

Lead **`APPROVE NP-C`** → unlock NP-D.
