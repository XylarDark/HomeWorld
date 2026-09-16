# SM_LandingCircle.md — landing circle mesh (shared)

**ID:** P3_PROP_kit  
**Date:** 2026-09-16  
**Owner:** PROP  
**Status:** PUBLISHED name + mesh contract  
**Graybox alias:** `SM_Landing_Circle` volume @ (0.0, −70.0, −95.0), 8 × 8 × 0.2 m (`GRAYBOX_LAYOUT.md` §4)  
**Transit ref:** `Lib/08_Transit/SM_LandingCircle_REF.md`  
**Shot:** Shot 4 — planet landing clearing, day

---

## One mesh, used twice

**`SM_LandingCircle` is a single static mesh asset.** Place **two instances** (or one now + second in WAVE_3):

| Instance | Location | When | Dress owner |
|---|---|---|---|
| **A — Planet landing** | Planet clearing (graybox `SM_Landing_Circle`) | WAVE 2 publish + WAVE 3 ENV-P dress | PROP mesh / ENV-P place |
| **B — Reuse** | Optional second clear (e.g. islet crumb pad or future return clear) **or** mirrored read if needed | WAVE_3 (`HOMEWORLD_MVP_SWARM_BRIEF` Phase 4: “second `SM_LandingCircle`”) | Same mesh — **do not duplicate asset** |

**Reuse note:** Never fork a second landing mesh family. Scale/rotation instance only. Same **M_PathStone** ring + grass inset. Sci-fi pad / tech markings = hard reject.

---

## Mesh contract

| Field | Spec |
|---|---|
| Name | `SM_LandingCircle` |
| Type | Static mesh (`SM_`) |
| Footprint | ~6–8 m diameter walkable clear (fits 8×8 graybox) |
| Height | Ring stones ~0.1–0.2 m; center slightly inset / flat |
| Origin | Ground contact at circle center |
| Materials | Ring / stones: **M_PathStone**; center ground: **M_StylizedGrass** (lush day instance) |
| Read | Handmade stone ring in open pine clearing — hopeful day; open ground for arrival; **not** combat staging |

**Silhouette:** Soft irregular ring, readable from lookout (Shot 1 / lookout test) and at touchdown (Shot 4 / `CRUMB_Landing`).

---

## Sockets

| Socket | Local approx | Purpose |
|---|---|---|
| `SOCKET_Touchdown` | (0, 0, 0.15) | Glide / FALLBACK end attach; GP restore walk |
| `SOCKET_Interact` | (0, 0, 1.0) | Optional arrival prompt volume |
| `SOCKET_FX_Land` | (0, 0, 0.2) | Soft dust / leaf — handmade, not thruster |

---

## Gameplay hooks

- **V2 success:** Touchdown on this mesh / overlap → control to walk (GDD V2).
- Spline end crumb `CRUMB_Landing` (0.0, −70.0, −94.5) targets this circle — see `GLIDE_SPLINE.md` (PROP does not edit that file).
- Day/body only for glide arrival. Night portal uses shrines, not this circle.

---

## Rejects

- Sci-fi landing pad, chevrons, metal plates, neon
- Pancake disc island language on the ring
- Photoreal scanned cobble
- Combat cover / barricades
- Second unique mesh named differently for “planet vs islet”
