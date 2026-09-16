# SM_LandingCircle_REF.md — transit pointer (PROP)

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP (ref only)  
**Do not overwrite:** `Lib/08_Transit/GLIDE_SPLINE.md`

---

## Landing circle

| Field | Value |
|---|---|
| Published mesh | **`SM_LandingCircle`** |
| Spec | `Lib/03_Gatherables/SM_LandingCircle.md` |
| Graybox volume | `SM_Landing_Circle` @ (0.0, −70.0, −95.0) |
| Spline end | `CRUMB_Landing` → this mesh (`GLIDE_SPLINE.md`) |
| Reuse | **One mesh asset**, second instance in WAVE_3 (ENV-P) — no fork |

Route reminder (unchanged): `SM_Lookout_Pad` / `SM_Glider_Perch` → islets → **`SM_LandingCircle`**.

---

## Glider perch (name expect — not PROP mesh)

| Name | Owner | Notes |
|---|---|---|
| `SM_Glider_Perch` | **ENV-H** | Graybox @ (7.5, −4.5, 0.0); departure for Shot 3 / V2 |
| `CRUMB_Depart_Lookout` | WLD | (7.5, −4.5, 1.5) at perch — see `GLIDE_SPLINE.md` |

PROP does not author perch geometry in this kit. ENV-H dresses lookout + perch; PROP supplies shared landing mesh only.
