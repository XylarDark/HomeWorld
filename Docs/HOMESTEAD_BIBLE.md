# Docs/HOMESTEAD_BIBLE.md

**Status:** LOCKED (Lead interview 2026-09-20 ET)  
**Pointers:** `Docs/DAYNIGHT_BIBLE.md`, `Docs/CAMERA_BIBLE.md`, `Docs/canon/VERBS.md`, `Docs/canon/DO_NOT.md`, `Docs/00_CANON.md`  
**Amends:** “No crafting trees” → **limited named homestead recipes only** (not a generic skill/crafting web). Co-op on hub deferred — **NPC family** instead.

---

HOMEWORLD HOMESTEAD BIBLE — SAFE HEARTH + EDGE GLIDE

## One-line lock

The floating HomeWorld island is the family’s **safe hearth**: NPC family life, sleep, store, nurture, limited crafting, and wholesome hub activities. You bring gifts from the planet home to use and to grow the base. You leave only by **glide down** (any edge path) or **moonlight portals** — never by void-fall or invisible walls.

## Purpose

| Role | Spec |
|---|---|
| Safety | **No combat** on homestead — ever (pillars / combat framing A) |
| Family | **NPC family** presence and wholesome activities — **no co-op MVP** |
| Economy loop | Bring planet gathers home → store / craft / research-prep → go out stronger |
| Taste | Warm, readable, handmade, hopeful — immersion on the hub |

## Activity set (hub)

Wholesome **safe-space** activities that belong on the island (not as planet combat pressure):

| Activity | MVP framing |
|---|---|
| Walk / chores / presence | Yes — Galaxy orbit TP (`CAMERA_BIBLE`) |
| Sleep / bed → spirit | Yes — `DAYNIGHT_BIBLE` |
| Family (NPC) play / presence | Yes — NPCs; beats/TODO as needed |
| Family eating / meal | Yes as hub fantasy — interact TBD (**TODO** meal rules) |
| Store transfer | Yes — existing RES store |
| Nurture ×2 | Yes — night spirit |
| Fishing | Hub activity allowed — spot/interact **TODO** |
| Fitness / exercise | Hub activity allowed — beat **TODO** |
| Research / “more to do on base” | Fantasy lock — board/unlocks **TODO** (no invented tech tree) |
| Crafting | **Limited named recipes only** (below) |
| Iso building / pens / crops planning | Camera systems mode when placing/layout (`CAMERA_BIBLE`) |

## Crafting (limited — not a skill tree)

Homestead crafting may create **only** these MVP outputs unless Lead appends `DECISIONS.md`:

| Output | Purpose |
|---|---|
| **Tent** | Campsite pitch (with campfire) — `DAYNIGHT` campsite |
| **Torch** | Darkness preparedness — soft-kidnap gate |
| **Taming consumables** | Spendables for tame offer (beyond raw RES if needed) |
| **Healing consumables** | Spendables for heal (beyond raw RES if needed) |
| **Fishing consumables / gear** | Enable hub fishing loop |

**Forbidden:** Generic crafting web, weapon/armor smithing, infinite recipe pages, combat gear on hub.

Recipe costs / station props = **TODO** in `SCHEMA.md` before coding (schema before data rows).

## Placeables

**Limited placeables** — not freebuild. Prefer authored homestead kit + small placeable set (tent/campfire family, store, nurture targets). Do not ship a full base-builder MVP.

## Leaving the island

| Method | Spec |
|---|---|
| **Glide** | **Any path off the island** can start glide **down** to the planet map. You **cannot** glide off HomeWorld into empty void — trajectory must hit the playable map below. Dusk: **no new glide start** (`DAYNIGHT_BIBLE`). |
| **Portal** | Moonlight / night — body or spirit — between places **and up** to island (`DAYNIGHT_BIBLE`). |

**No invisible wall collisions** as the default language of bounds — anywhere in the game. Rare mid-map blockers only if needed, and they must have an **immersive** read (geometry, vines, spirit barrier VFX, etc.), never a naked clip plane.

Walking toward an edge ≠ soft pushback into a wall; it **commits to glide** (when phase allows) toward the planet.

## Sacred hub props (do not silent-delete)

Cabin, **bed**, garden / N1 nurture, store racks, shrine, lookout / glider perch / edge glide starts, path, NPC family anchors (when placed). Treat as sacred systems under `DO_NOT.md`.

## Explicit do-not (homestead)

- Combat / weapons / aggro / shadow kidnap combat resolution on hub  
- Co-op drop-in as MVP requirement (NPC family instead)  
- Free-flight or night glide-down from hub  
- Invisible walls as primary bounds  
- Generic crafting skill tree  
- Void death loop off the island rim  
- Second movement component / parallel hub controller  

## Engine note (UE5)

Hub GameMode/volume: no-damage. Edge volumes → glide start (day/phase gated), not blocking walls. Portal + bed + store + nurture + craft station ownership clear. Iso camera when in build/place mode. Read `DAYNIGHT_BIBLE` + `CAMERA_BIBLE` before adding parallel systems.

---

**Relationship to older canon:** Gather→store→spend remains valid; homestead crafting is a **narrow recipe list**, not a reopened crafting MMO. Vertical-slice “no crafting trees” means no web — these named recipes are Lead-allowed exceptions.
