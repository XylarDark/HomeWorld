# Docs/03_GAMEPLAY_MVP.md

## 1. Status: DONE (P5 / WAVE 4)

Date: 2026-09-16  
Owner: GP  
Inputs (read-only): `Docs/00_CANON.md`, `Docs/01_GDD_MVP.md`, `Docs/03_SYSTEMS_MVP.md`, `Lib/08_Transit/GLIDE_SPLINE.md`  
Consumers: WLD (volumes/crumbs already placed), LIT (NightMix drive), SYS (form flag for spends), CHA/PROP (demo markers owned elsewhere)

Movement and transit contract only. **No free-flight.** **No combat.** **No inventory rules** (SYS). No UE C++ this slice — docs + named demo markers. CHA/PROP own Blender this wave; GP documents empties here instead of editing the `.blend`.

---

## 2. Eight verbs — GP vs SYS split

| Verb | GP owns | SYS owns |
|---|---|---|
| V1 Walk homestead | Nav / walk volumes, camera-readable move | — |
| V2 Glide island → planet | Spline follow along `CRUMB_*` / FALLBACK scripted | — |
| V3 Gather ×6 | Interact prompt timing / day gate | Inventory + RES_* counts |
| V4 Encounter / tame | Proximity enter + day gate | Beast SM + food spend |
| V5 Portal night A ↔ B | Shrine link transit | — |
| V6 Heal ×3 | Night gate + channel timing | hurt→healed + herb/seed spend |
| V7 Nurture ×2 | Night gate + channel timing | `M_Nurtured` flags + spend |
| V8 Return / dawn | Portal home + dawn time float | Persist optional inventory/tame/nurture |

**Claim gate:** all eight executable or camera-demoable via markers + cameras below.

---

## 3. Body walk (V1)

| Field | Spec |
|---|---|
| Form | Body (day) or spirit (night) — same walk volumes; spirit has no flight |
| Domain | Hero Island navmesh / walk volumes: cabin, garden, path, pines, lookout, shrine, glider perch |
| Success | Reach named POI without leaving island bounds |
| Fail | Off-nav → soft pushback; no void death loop in MVP |
| Duration | Continuous; cabin→lookout ~15–25 s |

Demo: place player at `GP_PlayerStart`; walk toward lookout / shrine for Shot 1–2 framing.

---

## 4. Form swap — dusk / shrine (body ↔ spirit)

| Trigger | Result |
|---|---|
| Dusk at homestead (or return to shrine when cycle arms night) | Body → spirit; `NightMix` → 1; spirit layer visible; gather/beast idle |
| Dawn / Rest complete (V8) | Spirit → body; `NightMix` → 0; spirit layer off; day gather/beast available |

Mid-day shrine is **landmark only** (portal locked). No night flight.

---

## 5. Scripted glide along CRUMB_* / GLIDE_SPLINE (V2) — NOT free flight

**Rule:** Glide is a spline / crumb path. Canon hard reject: free-flight sim.

| Mode | Spec |
|---|---|
| Preferred | Constrained follow of crumbs in order; limited lateral influence only; day/body |
| FALLBACK | Scripted cinematic / locked traverse of the **same** crumb sequence; no steering beyond camera follow |

**Route:** `SM_Lookout_Pad` / `SM_Glider_Perch` → islets → `SM_Landing_Circle`

**Crumbs (from `Lib/08_Transit/GLIDE_SPLINE.md` — do not reorder without WLD):**

| # | Name |
|---|---|
| 0 | `CRUMB_Depart_Lookout` |
| 1 | `CRUMB_Air_01` |
| 2 | `CRUMB_Islet_01` |
| 3 | `CRUMB_Air_02` |
| 4 | `CRUMB_Islet_02` |
| 5 | `CRUMB_Air_03` |
| 6 | `CRUMB_Islet_03` |
| 7 | `CRUMB_Approach` |
| 8 | `CRUMB_Landing` |

Helper curve name in blend (visual only): `CRUMB_GlideSpline`. Follow **EMPTY crumb order**, not curve deformation.

| Field | Spec |
|---|---|
| Trigger | Day/body; enter lookout / glider perch interact + confirm (`GP_GlideStart`) |
| Success | Touchdown on landing circle; restore walk |
| Fail | Leave without confirm → idle; night → unavailable |
| Duration | Preferred ~20–40 s; FALLBACK ~12–25 s (WLD arc ~25–40 s readable) |
| Forbidden | Free-flight model, flight HUD/energy meter, night glide |

Cameras for demo: `CAM_GlideDepart`, `CAM_LandingDay` (WLD P4).

---

## 6. Portal — SM_Shrine_Homestead ↔ SM_Shrine_Return (V5)

| Field | Spec |
|---|---|
| Link | Homestead shrine `SM_Shrine_Homestead` ↔ planet return shrine `SM_Shrine_Return` **only** |
| Form | Night/spirit required both ways |
| Player action | Use shrine → short portal transit to linked shrine |
| Success | Arrive opposite shrine; spirit form retained |
| Fail | Day/body → locked (“at night”); no third map |
| Duration | Channel + transit ~3–6 s each way |

Demo markers: `GP_PortalA` at homestead shrine interact/arrive; `GP_PortalB` at planet return shrine. Camera: `CAM_PortalNight`.

Sockets expected on shrine kits (PROP/ENV): `SOCKET_Portal` / Interact / Arrive — GP reads them; does not remodel.

---

## 7. Time float → NightMix + spirit visibility (V8 support)

| Driver | Targets |
|---|---|
| GameState (or demo) **time float** / cycle phase | All ten masters' `NightMix` 0–1 |
| Same float / phase | Spirit layer visibility on; day gather/beast interact off when night |
| Dawn (V8 success) | `NightMix` → 0; spirit layer off; body form on homestead |

| Phase | time / NightMix intent | Spirit layer | Form |
|---|---|---|---|
| Day | ~0.0 | Off | Body |
| Dusk transition | 0 → 1 over ~4–8 s | Fading on | Swap to spirit |
| Night | ~0.85–1.0 (LIT Homestead_Night uses 0.85) | On | Spirit |
| Dawn transition | 1 → 0 over ~4–8 s | Fading off | Swap to body |

**Rules:** One float flips lights + NightMix + spirit visibility. Never author `_Night` texture sets. Windows stay warm emissive (LIT).

---

## 8. Named GP demo markers (document only — CHA/PROP place in Blender)

GP does **not** open or save the `.blend` this wave. The following empties are the verb demo path contract; CHA/PROP (or a later GP pass) create them in-scene with matching names + custom props.

| Empty name | Role | Suggested parent / near | Custom props (document on empty) |
|---|---|---|---|
| `GP_PlayerStart` | V1 walk spawn / dawn body start | Cabin path / homestead hub | `verb=V1`; `form=body`; `demo_order=1` |
| `GP_GlideStart` | V2 confirm volume / perch start | `SM_Glider_Perch` / `CRUMB_Depart_Lookout` | `verb=V2`; `path=CRUMB_*`; `free_flight=0`; `demo_order=2` |
| `GP_PortalA` | V5 homestead portal interact | `SM_Shrine_Homestead` | `verb=V5`; `link=GP_PortalB`; `mesh=SM_Shrine_Homestead`; `demo_order=5` |
| `GP_PortalB` | V5 planet portal interact | `SM_Shrine_Return` | `verb=V5`; `link=GP_PortalA`; `mesh=SM_Shrine_Return`; `demo_order=5` |

**Suggested camera-demo path (first-run order):**

1. `GP_PlayerStart` → walk lookout (V1) — `CAM_Hero`
2. `GP_GlideStart` → follow `CRUMB_*` to landing (V2) — `CAM_GlideDepart` → `CAM_LandingDay`
3. Landing / path — gather + beast pads camera-readable (V3/V4; SYS data)
4. Dusk form swap at homestead shrine (time float → NightMix)
5. `GP_PortalA` ↔ `GP_PortalB` (V5) — `CAM_PortalNight`
6. Spirit wound site heal ×3 (V6); portal home; nurture ×2 (V7); dawn (V8)

---

## 9. Explicit out-of-scope

- Free-flight controller / flight HUD
- Combat
- Inventory / RES tables (SYS — see `Docs/03_SYSTEMS_MVP.md`)
- Extra maps, extra biomes, night flight
- Editing `.blend` this wave (CHA/PROP owns Blender)
- UE C++ this wave
- Editing `PHASE_BOARD` or starting WAVE 5

---

## Appendix — Ownership

| System | Owner | Source |
|---|---|---|
| Walk, form swap, glide/FALLBACK, portal A↔B, time→NightMix + spirit vis | GP | This file |
| Inventory, tame SM, heal, nurture spends | SYS | `Docs/03_SYSTEMS_MVP.md` |
| CRUMB_* positions, islets, landing | WLD | `Lib/08_Transit/GLIDE_SPLINE.md` |
| Shrine / gather meshes | PROP / ENV | Lib kits |

End of GAMEPLAY MVP (P5).

---

## Transit cut — FALLBACK FLIGHT ARMED (2026-09-16)

Lead typed `FALLBACK FLIGHT`. Body/day transit is **scripted glide only** along `CRUMB_*` / `Lib/08_Transit/GLIDE_SPLINE.md`. Do **not** implement interactive constrained free-steer flight. Spirit/night transit remains **portal both ways** (`SM_Shrine_Homestead` ↔ `SM_Shrine_Return`). Conductor may apply this cut without a design meeting (canon).
