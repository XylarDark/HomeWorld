# CAM_Hero_LIT_NOTES (addendum)

**ID:** P3_LIT_night  
**Date:** 2026-09-16  
**Role:** LIT  
**Status:** ADDENDUM ONLY — does **not** overwrite `Lib/00_Core/CAM_Hero.md` (WLD-owned)  
**WLD source of truth:** `Lib/00_Core/CAM_Hero.md` + `Lib/00_Core/GRAYBOX_LAYOUT.md`

---

## 1. Framing gap assessment (Shot 1)

WLD `CAM_Hero` already matches shotlist intent: behind/above plateau, homestead left, lookout right, valley below, ~35 mm, pose `(−4.0, 4.5, 3.2)`.

**LIT finding:** No WLD framing rewrite required. Gaps are **lighting / sky object placement** relative to that frustum — owned here.

| Gap | Owner | Action |
|---|---|---|
| Huge warm moon upper-right | LIT | Place `LIT_Moon` per `LIT_Moon.md` |
| Window bloom left | LIT + ENV-H panes | `LIT_CabinWindows.md` |
| Under-cliff haze | LIT | `VOLUME_Haze.md` |
| Family silhouettes | ENV-H / PROP | Dark readable silhouettes on `SM_Lookout_Pad` |
| Peach clouds / stars / snow peak | LIT sky + ENV sky volumes | World shader / cards; `SM_Peak_Distant` already grayboxed |

---

## 2. Shot 1 — LIT checklist from this camera

From locked `CAM_Hero` pose, verify in lookdev:

1. Moon disc angular size ~16–20° upper-right (not speck)  
2. Cabin warm windows left — bloom on  
3. Path + garden mid; lookout edge right with three silhouettes readable  
4. `VOLUME_Haze` under cliff lip without erasing planet  
5. Sightline gate still holds: landing circle, 2–3 roofs, path, return shrine  
6. Warm-vs-cool contrast survives exposure  

Exposure tip: meter so windows bloom and moon glows but grass under NightMix 0.85 stays saturated spring green — not muddy mid-gray.

---

## 3. Shot 2 helper (no WLD overwrite)

Graybox already defines `CAM_CabinClose` at `(−4.0, −2.5, 1.6)`.

| Field | LIT note |
|---|---|
| Intent | Mid/close three-quarter on cabin face + raised beds |
| Lights | Same `PRESET_Homestead_Night`; prioritize window emissive + `LIT_CabinWarm` spill |
| Moon | Partial / out of frame OK — do not dolly out to Shot 1 |
| Reject | Dark windows; muddy/grim; photoreal wood |

If ENV needs a named alias: treat `CAM_CabinClose` ≡ shotlist Shot 2 / brief `CAM_CabinGarden`.

---

## 4. What LIT will not do

- Overwrite `CAM_Hero.md` pose table  
- Invent a 6th shot camera  
- Move planet slice masses to “fix” lighting  
