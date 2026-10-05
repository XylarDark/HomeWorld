# Docs/03_GAMEPLAY_MVP.md

## 1. Status: DONE (P5 / WAVE 4)

Date: 2026-09-16  
Owner: GP  
Inputs (read-only): `Docs/00_CANON.md`, `Docs/01_GDD_MVP.md`, `Docs/03_SYSTEMS_MVP.md`, `Lib/08_Transit/GLIDE_SPLINE.md`  
Consumers: WLD (volumes/crumbs already placed), LIT (NightMix drive), SYS (form flag for spends), CHA/PROP (demo markers owned elsewhere)

Movement and transit reference. The active V2 behavior is the freely steered cloud descent described in `Docs/01_GDD_MVP.md` §9 and `Docs/context/HOMEWORLD_ROUTE.md`. The fixed-crumb sequence below is a separate scripted fallback. **No general-purpose flight model.** **No combat.** **No inventory rules** (SYS).

---

## 2. Eight verbs — GP vs SYS split

| Verb | GP owns | SYS owns |
|---|---|---|
| V1 Walk homestead | Nav / walk volumes, camera-readable move | — |
| V2 Glide island → planet | Freely steered cloud descent; fixed-crumb `FALLBACK` remains separate | — |
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

## 4. Spirit form — sleep and rune gates

| Trigger | Result |
|---|---|
| Sleep gate and rune gate are both met | Body → spirit; `NightMix` → 1; spirit layer visible; gather/beast idle |
| Dawn / Rest complete (V8) | Spirit → body; `NightMix` → 0; spirit layer off; day gather/beast available |

Mid-day shrine is **landmark only** (portal locked). No night flight.

---

## 5. Existing scripted FALLBACK along CRUMB_* / GLIDE_SPLINE (V2)

This section describes the existing fixed-crumb `FALLBACK` implementation. It does not implement the active steered cloud descent recorded in [`HOMEWORLD_ROUTE.md`](context/HOMEWORLD_ROUTE.md).

| Mode | Spec |
|---|---|
| FALLBACK | Scripted cinematic / locked traverse of the crumb sequence; no steering beyond camera follow; day/body |

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
| Fail | Leave perch without confirm → idle; night → unavailable |
| Duration | FALLBACK default 32 s, clamped to 25–40 s; see [`09_FALLBACK_GLIDE.md`](09_FALLBACK_GLIDE.md) |
| Fallback-only | Fixed-crumb scripted route; does not define active cloud descent steering |
| Forbidden | General-purpose flight model, flight HUD/energy meter, night glide |

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
| `GP_GlideStart` | V2 launch / perch start | `SM_Glider_Perch` / lookout | `verb=V2`; `path=CLOUD_DESCENT`; `steering=UNRESTRICTED`; `demo_order=2` |
| `GP_PortalA` | V5 homestead portal interact | `SM_Shrine_Homestead` | `verb=V5`; `link=GP_PortalB`; `mesh=SM_Shrine_Homestead`; `demo_order=5` |
| `GP_PortalB` | V5 planet portal interact | `SM_Shrine_Return` | `verb=V5`; `link=GP_PortalA`; `mesh=SM_Shrine_Return`; `demo_order=5` |

**Suggested camera-demo path (first-run order):**

1. `GP_PlayerStart` → walk lookout (V1) — `CAM_Hero`
2. `GP_GlideStart` → freely steer through the cloud descent and land in the field (V2) — `CAM_GlideDepart` → `CAM_LandingDay`
3. Landing / path — gather + beast pads camera-readable (V3/V4; SYS data)
4. Dusk form swap at homestead shrine (time float → NightMix)
5. `GP_PortalA` ↔ `GP_PortalB` (V5) — `CAM_PortalNight`
6. Spirit wound site heal ×3 (V6); portal home; nurture ×2 (V7); dawn (V8)

---

## 9. Explicit out-of-scope

- General-purpose free-flight controller / flight HUD (the active cloud descent remains freely steered)
- Combat
- Inventory / RES tables (SYS — see `Docs/03_SYSTEMS_MVP.md`)
- Extra maps, extra biomes, night flight
- Editing `.blend` this wave (CHA/PROP owns Blender)
- Editing `.blend` without the owning art task

---

## Appendix — Ownership

| System | Owner | Source |
|---|---|---|
| Walk, form swap, active cloud descent + separate FALLBACK, portal A↔B, time→NightMix + spirit vis | GP | This file |
| Inventory, tame SM, heal, nurture spends | SYS | `Docs/03_SYSTEMS_MVP.md` |
| Cloud/wisp placements, field landing; fallback CRUMB_* placements | WLD | `Docs/context/HOMEWORLD_ROUTE.md`; `Lib/08_Transit/GLIDE_SPLINE.md` |
| Shrine / gather meshes | PROP / ENV | Lib kits |

End of GAMEPLAY MVP (P5).

---

## Current transit direction

Body/day V2 is the freely steered cloud descent. The fixed-crumb implementation is retained only as a separate `FALLBACK`; its steering lock and timing do not apply to V2. Night/spirit transit remains the shrine portal route.

## Implementation status — cloud descent (2026-10-05)

The direction above is the target. The code does not yet deliver all of it. Read this before assuming a capability exists.

| Route requirement | State |
|---|---|
| Launch at `GP_GlideStart`, day/body only, within 450 cm | Implemented — `AHomeWorldCharacter::TryStartCloudDescent` |
| Steering unrestricted (no rail, corridor, or artificial bound) | Implemented — full air control, no steering clamp |
| Island soft bounds suppressed during descent, restored after | Implemented — `Landed` restores movement state |
| Collect a cloud wisp and keep it while descending | Implemented — `AHomeWorldCloudWisp` + carried count on the character |
| **A glider descent** (standard glide speed, descent-rate feel) | **Not implemented.** The descent currently sets `MOVE_Falling` with full air control. There is no glide-speed or sink-rate model in the codebase. Route wording requires it remain a glider descent rather than a new flight mode, so the fall is not yet the accepted behavior. |
| **Clouds to descend through** | **Not implemented.** No cloud actor, generator, or placement exists under `Source/` or `Content/`. Cloud size, spacing, and layer counts are recorded placeholders pending human testing. |
| Landing in the existing field, walk control returns | Implemented in `Landed`, but **not covered by automation** — only reachable in PIE. |

Two further facts an agent should not have to rediscover:

- `AHomeWorldCloudWisp` exists as C++ only. No Blueprint derives from it and none is placed in any map or asset, so the pickup cannot be exercised until WLD places one.
- `TryStartFallbackGlide` currently has **no caller**. `UHomeWorldInteractAbility` now enters the cloud descent first, so the scripted fallback is reachable only by an explicit Blueprint call. Whether the fallback keeps a player-facing trigger is an open Steer question.
