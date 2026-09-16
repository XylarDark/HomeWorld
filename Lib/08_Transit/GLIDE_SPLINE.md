# Lib/08_Transit/GLIDE_SPLINE.md

**ID:** P1_WLD_graybox  
**Date:** 2026-09-16  
**Role:** WLD  
**Inputs:** `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`

---

## Rule

**Glide is a spline / crumb path — NOT free flight.**

Canon hard reject: free-flight sim. Shot 3 reject: free-flight sim framing.

**FALLBACK = scripted glide** (canon §8: scripted glide down + portal both ways). If SYS cannot ship interactive spline follow, play the same crumb sequence as a scripted cinematic / locked traverse. Portal night island ↔ planet remains the spirit/night transit (separate from this day body glide).

---

## Route

`SM_Lookout_Pad` / `SM_Glider_Perch` → islets → `SM_Landing_Circle`

Body/day transit only (canon topology).

---

## Control points (crumbs)

World space, meters. Player / glider follows crumbs in order. No lateral free roam off spline.

| # | Crumb name | Position (X, Y, Z) | Notes |
|---|---|---|---|
| 0 | CRUMB_Depart_Lookout | (7.5, −4.5, 1.5) | At `SM_Glider_Perch`; start |
| 1 | CRUMB_Air_01 | (7.0, −10.0, −8.0) | Leave cliff; sell vertical drop |
| 2 | CRUMB_Islet_01 | (6.0, −18.0, −23.0) | Pass `SM_Islet_01` |
| 3 | CRUMB_Air_02 | (4.5, −25.0, −36.0) | Air current mid |
| 4 | CRUMB_Islet_02 | (3.0, −32.0, −46.0) | Pass `SM_Islet_02` |
| 5 | CRUMB_Air_03 | (2.0, −40.0, −60.0) | Descent continues |
| 6 | CRUMB_Islet_03 | (1.0, −48.0, −70.0) | Pass `SM_Islet_03` |
| 7 | CRUMB_Approach | (0.5, −60.0, −88.0) | Align to clearing |
| 8 | CRUMB_Landing | (0.0, −70.0, −94.5) | Touchdown at `SM_Landing_Circle` |

Approx. spline arc length: ~110–120 m. Scripted glide duration target: **25–40 s** (readable drop; not a flight sim).

---

## Explicit non-goals

- No free-flight model, HUD, or energy meter
- No new transit biome or vehicles
- No combat staging at landing
- Pancake island edge at departure is a reject — use `SM_Cliff_LookoutFace`

---

## Handoff notes

- ENV dresses islets and landing clearing; do not move crumb order without WLD.
- SYS/GPL: implement as spline follow **or** FALLBACK scripted glide using the same crumbs.
- Spirit/night shrine portal is not this spline.
