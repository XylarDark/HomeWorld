# SM_Shrine_Homestead.md — homestead shrine portal socket

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP  
**Status:** PUBLISHED name + portal socket contract  
**Graybox:** `SM_Shrine_Homestead` volume 1.5 × 1.5 × 2.0 m @ (−2.0, 3.5, 0.0)  
**Shot:** Shot 5 — spirit portal (homestead side)  
**Canon:** Spirit/night: homestead shrine ↔ planet shrine only

---

## Mesh contract

| Field | Spec |
|---|---|
| Name | `SM_Shrine_Homestead` |
| Type | Static mesh (`SM_`) + named sockets |
| Size | ~1.2–1.5 m wide × ~1.8–2.2 m tall (fits graybox) |
| Origin | Ground contact under stone/wood base |
| Materials | Base / posts: **M_WoodCabin** and/or **M_CliffRock**; portal glow / spirit cue: **M_SpiritUnlit** |
| Shape language | Soft handmade spirit shrine — stone+wood vernacular; **not** tech gate, neon ring, or dungeon mouth (art bible §2) |

Readable landmark on homestead loop (cabin → garden → lookout → shrine → cabin). Night: soft unlit emissive; day: landmark only, portal locked.

---

## Portal socket contract (MVP)

| Socket / volume | Spec |
|---|---|
| `SOCKET_Portal` | Center of shrine opening / focus ~1.0–1.4 m above ground; facing toward usable approach |
| `SOCKET_Interact` | Player Use attach; night/spirit only for V5 |
| `SOCKET_Arrive` | Spawn / exit pose for arrivals from planet shrine |
| `VOL_PortalOverlap` | Soft cylinder ~1.2 m radius × 2.0 m height (BP later) |

**Link rule:** Homestead `SOCKET_Portal` ↔ planet return shrine portal (same two places). Channel + transit ~3–6 s each way (GDD V5). No third map. No night flight.

**States**

| Mode | Visual | Interact |
|---|---|---|
| Day/body | Landmark; glow low / NightMix-driven | Locked or “at night” prompt |
| Night/spirit | **M_SpiritUnlit** readable; hopeful soft bloom | Use → portal to linked planet shrine |

Hurt/healed spirit language is for wisps (CHA), not a second shrine mesh family — shrine glow stays soft spirit cue.

---

## Planet return shrine — stub for WAVE_3

PROP **does not** hero-author the planet return shrine in this wave. ENV-P / PROP in WAVE_3 finalizes it. Socket contract stub so SYS/GP can wire both ends:

| Stub name | Notes |
|---|---|
| `SM_Shrine_Return` | Graybox volume already @ (6.0, −75.0, −95.0) — planet side |
| `SM_Shrine_Planet` | Brief Phase 4 alias; treat as same portal family as return shrine when ENV-P publishes |
| Required sockets (mirror) | `SOCKET_Portal`, `SOCKET_Interact`, `SOCKET_Arrive`, `VOL_PortalOverlap` |
| Materials | Same masters: wood/rock + **M_SpiritUnlit** |
| Link | Bidirectional with `SM_Shrine_Homestead` only |

Do not invent a sci-fi gate or a third shrine location.

---

## Rejects

- Neon / hard sci-fi portal tech
- Grimdark void mouth
- Combat shrine / loot altar
- Unique portal shader outside **M_SpiritUnlit**
- Moving graybox origin without WLD
