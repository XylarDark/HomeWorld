# Docs/DAYNIGHT_BIBLE.md

**Status:** LOCKED (Lead interview 2026-09-20 ET)  
**Pointers:** `Docs/CAMERA_BIBLE.md`, `Docs/canon/VERBS.md`, `Docs/canon/SCHEMA.md`, `Docs/21_REAP_SOW.md`, `Docs/canon/FEEL.md`  
**Amends:** Older GDD “dusk auto-spirit at shrine” and “portal night-only” — this file wins for day/night/transit form rules.

---

HOMEWORLD DAY / NIGHT BIBLE — IMMERSION + SLEEP + TRANSIT

## One-line lock

Immersive dawn→day→dusk→night is a taste cornerstone. Spirit form is earned by **sleep** (bed or campsite), not by the clock alone. Glide is **down only**. Portals wake in **moonlight** and move body or spirit **between places and back up** to the HomeWorld island. Unprepared darkness without a torch is a **soft kidnap** home — rare preparedness fail, not a combat loop.

## Taste cornerstone

Immersion beats thin timer UI. Full phase progression (dawn, day, dusk, night) must be readable in light, audio, and NightMix — not a binary day/night toggle.

## Clock ownership

| Field | Spec |
|---|---|
| Owner | One GameState (or equivalent) phase / time float — sole source of day/night |
| Phases | `Dawn` → `Day` → `Dusk` → `Night` → (Rest/Dawn) |
| Dusk | Still **day-time for rules** (body verbs, no spirit yet). Buffer to reach a sleep spot |
| Lengths | **TODO** — set after playtest (propose later in `FEEL.md` / `DECISIONS.md`) |
| Cheat | Keep `hw.TimeOfDay.SetPhase` for prove; optional Rest/Dawn cheat TBD |

## Form rules — sleep to spirit

| Trigger | Result |
|---|---|
| Sleep in **homestead bed** | Body → spirit when night is allowed / after sleep confirm; enter night loop |
| Sleep at **campsite** | Same — spirit entry from planet campsite |
| Clock hits night **without** sleep | You do **not** auto-become spirit. See darkness / torch fail below |
| Dawn while still spirit (not returned to body) | **Spirit sickness** — debuffs (magnitudes **TODO**; schema before numbers) |

**Forbidden:** Auto form-swap solely because dusk/night timer fired while standing around.

## Campsites (MVP framing)

Campsites exist when:
1. Player **clears a humanoid encampment** (Docs/21 camp site) and it becomes a usable sleep spot, **or**
2. Player **pitches own tent + campfire** (placeable — systems TBD; mark TODO for place/cost)

Homestead bed is always valid. Exact pitch costs / clear criteria → implement from this bible later; do not invent economies here.

## Transit

| Mode | Direction | Form / phase | Notes |
|---|---|---|---|
| **Glide** | Island → planet **only** (down) | Body; **not** during dusk; day (and pre-dusk) | FALLBACK scripted / constrained per canon. No free-flight. No dusk **start** |
| **Portal** | Between linked places **and up** to HomeWorld island | Body **or** spirit | Portals **come alive in moonlight** (night). Day: portals dormant / unusable |

Mid-glide if dusk would begin: **finish or land under day rules**; do not start a new glide after dusk starts. (Queue: dusk does not cancel an in-flight glide mid-air without Lead revisit — default **complete current glide**, then dusk buffer applies on ground.)

## Darkness / torch — soft kidnap (not combat)

| Condition | Result |
|---|---|
| Night (or deep darkness) **and** player has **no torch equipped** **and** exposed to darkness | Soft lose: **kidnapped** to **nearest shrine**, then teleported to **HomeWorld** homestead. Night loop **skipped** / cut short as preparedness fail |
| Torch equipped (or in lit safe volume / sleep spot) | No kidnap |

**Design intent:** Force preparedness. **Not** a common return path. **Not** HP combat, weapons, or aggro loops. Scripted soft fail only. Homestead remains non-combat.

**TODO:** Torch as equippable — may need a tiny equipment exception or held item outside 6-slot RES grid. Stamp item ID + rules in `SCHEMA.md` / `DECISIONS.md` before coding. Proposed: `ITEM_TORCH` held/offhand, not a 7th RES stack.

## Spirit sickness

| Trigger | Result |
|---|---|
| Still in spirit when dawn/day returns without rejoining body (sleep wake / body return flow) | Debuffs — **TODO** names/magnitudes/duration after playtest |

Return-to-body path: sleep wake / shrine-home / bed — **TODO** exact interact; must be explicit in impl prompt when coded.

## Activity × phase (summary)

| Phase | Body | Spirit | Glide start | Portals | Sleep→spirit |
|---|---|---|---|---|---|
| Dawn | Yes | Sickness if still out | No (landed) | Moonlight off | — |
| Day | Yes | No (unless sickness carry) | Yes (down) | Off | Prep only |
| Dusk | Yes (day rules) | No | **No** | Off | Race to bed/camp |
| Night | Body until sleep; darkness risk | After sleep | No | **On** (moonlight) | Bed or campsite |

Day reap / night sow verbs still follow `VERBS.md` + Docs/21 once form matches.

## Explicit out of scope

- Free-flight / night glide down
- Dedicated FP camera (see `CAMERA_BIBLE`)
- Kill/HP shadow combat as the kidnap resolution
- Auto-spirit at dusk without sleep
- Inventing day/night second lengths in code before playtest stamp

## Engine note (UE5)

One time/phase owner. Form flag from sleep interact. Portal actors gated on moonlight/night. Glide start blocked in dusk. Torch + darkness volume → soft kidnap to nearest shrine → homestead. Do not add a parallel day/night clock.

---

**Relationship to combat framing A:** Homestead never combat. Shadow kidnap is a **scripted soft fail**, not dream-combat and not hub combat. Dream-convert (Docs/21) remains separate night content after intentional sleep.
