# Handoff — NP-C Form + V1 Polish

| Field | Value |
|-------|-------|
| **Phase** | NP-C |
| **Status** | **COMPLETE — awaiting `APPROVE NP-C`** (Windows place done) |
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

## Windows evidence (DESKTOP-21CT3H0)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **HEAD** | `16f7afe` |
| **Capture** | UnrealMCP Editor run, 2026-09-17 ET |

| Step | Result | Notes |
|------|--------|-------|
| Safe-Build | **PASS** | At `16f7afe` (include-order + `GetSpiritIdForDeath` fixes merged) |
| `place_vs_mvp_gp.py` | **PASS** | `GP_PlayerStart` TargetPoint + `PlayerStart_VS_MVP` at **(-400, -150, 100)**; level saved |
| `place_fallback_glide_markers.py` | **PASS** | `GP_GlideStart` **(750, 450, 150)**; `GP_PortalA`, `GP_PortalB`; level saved |
| Marker probe | **PASS** | `GP_PlayerStart`, `GP_GlideStart`, `GP_PortalA/B`, `CRUMB_*` present — **15 labeled** actors |
| `smoke_nightmix_phase.py` | **EXECUTED** | Result not captured in this handoff — confirm `OK phase=… NightMix=…` lines in Output Log |
| PIE `FORM:` / `FALLBACK:` | **NOT RUN** | Optional Lead visual; not blocking **`APPROVE NP-C`** gate |

Local `.umap` changes from placement scripts are **not committed** (project policy).

---

## Next gate

Lead **`APPROVE NP-C`** → unlock NP-D.
