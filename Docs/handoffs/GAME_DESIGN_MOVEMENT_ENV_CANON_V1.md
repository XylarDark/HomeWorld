# GAME_DESIGN_MOVEMENT_ENV_CANON_V1

**Pointers only. Seats do not ingest books. Cite EXIT `GAME_DESIGN_MOVEMENT_ENV_V1`.**  
**Status:** ACTIVE · CAP product **PARKED** · T0 SCOPE floor unchanged · greybox OK  
**Pins:** DET `0a27306` · map `Maps/VS_MVP` · A–E blob `107a5118c95c1bf0b1b3d1755796632bff41b535` (cite only)

---

## Movement — KEEP / CANDIDATE / PARK

| Status | Source | Why for T0 (≤2 lines) |
|--------|--------|------------------------|
| **KEEP** | Steve Swink, *Game Feel* (2008); “Game Feel: The Secret Ingredient” (Game Developer, 2007) | Control + simulated space. Sub-~100 ms input→motion; weight / not-floaty language for DONE-WHEN — not a juice checklist. |
| **KEEP** | Nintendo BotW GDC 2017; TotK GDC 2024 physics / multiplicative design | Glide = fall cushion, not aircraft. Multiplicative verbs. Matches CUT free-flight + seamless home↔planet. |
| **KEEP** | HomeWorld Movement bible LOCKED · Docs/24 MV-A · FALLBACK FLIGHT armed | In-repo law. Industry cites interpret; do not reopen. Eject-home / fallback = mid-transit degrade (A–E E). |
| **KEEP** | Camera-truth cluster (Swink response+context; predictable follow-cam) | Camera tells travel direction; no free-fly prove cam. Polish = Lead-later. |
| **CANDIDATE** | Fasterholdt jump-metrics · SMB physics writeups | Numeric walk/sprint/glide rates when a later bite freezes them. |
| **CANDIDATE** | Third-person camera GDC cluster | Follow-cam for glider/portals — Lead taste until bible says otherwise. |
| **CANDIDATE** | `#234` feel/juice library (when ACCEPTED) | Cross-link only; not movement law. |
| **PARK** | Fighting-game netcode · flight-sim energy · AAA anim-graph tomes as T0 | Wrong genre / conflicts glide-as-fall / polish-before-verbs. |

**T0 mapping:** Glider = height as currency (`NODE_GLIDER` → field AABB). `EJECT_HOME` = scripted degrade, not combat. Portals = deep module (A–E B); fail → eject/home (A–E E).

---

## Environment — KEEP / CANDIDATE / PARK

| Status | Source | Why for T0 (≤2 lines) |
|--------|--------|------------------------|
| **KEEP** | Totten, *An Architectural Approach to Level Design* | Prospect/refuge, arrivals, weenies. Homestead hub · field prospect · camp edge. Works in greybox. |
| **KEEP** | Lynch, *The Image of the City* (via Totten) | Landmarks / paths / nodes / edges. T0 `NODE_*` = Lynch-nodes; paths walkable without UI crumbs. |
| **KEEP** | *The Level Design Book* — Blockout | Playtest blockout, not GDD. Matches greybox + math-first Arrange. |
| **KEEP** | Norman affordance (conceptual) | Interactables read at **day** contrast by silhouette/height. Night = Lead taste, not bot PASS. |
| **CANDIDATE** | Schell lenses (Essential Experience / Spaces / Curiosity) | Thin questions only — no 100-lens dump. |
| **CANDIDATE** | BotW triangle landmarking | Occluder + peek of destination; do not rebuild VS_MVP this turn. |
| **CANDIDATE** | Alexander *A Pattern Language* (via Schell) | Thin cite only; PARK full book. |
| **PARK** | AAA biome dress as prove · night-mood as env proof · shooter cover metrics | Greybox longer; bright/day bot prove; camp = eject / avoid+soothe. |

### T0 envelopes (greybox)

| Envelope | Verb | Greybox tell |
|----------|------|--------------|
| Homestead interior → stoop | Wake, kettle, backpack, bed | Intimate; silhouette; door = arrival |
| Near-outside plant slot | Plant / nurture | Short walk from stoop; not in flight path |
| Perch / glider | Leave home | Height + field weenie |
| Open field | Gather + rune | Path nodes; rune landmark before bed |
| Day camp edge | Eject-not-kill | Edge + threat volume; no kill metrics |
| Night camp (Lead) | Avoid 1 / soothe 2 | Same volume; lighting taste later |

---

## Harness pointer rules

1. Movement/env DONE-WHEN name **`NODE_*`** + verb — not a camera path.  
2. “Feels floaty / pretty at night” = **Lead-only** — never bot `ok: true`.  
3. Transit prove: `NODE_GLIDER` → `NODE_FIELD_GATHER` without load hang; fail → `EJECT_HOME`.  
4. Arrange-before-Act; no stills to discover missing nodes. CAP **PARKED**.  
5. Soft vs closed: `ready:false` ≠ `closed_fail`. Soft = dress/TOD/unreadability Lead will polish. Closed = MUST node marked Present then missing after Act, or eject with no home degrade.  
6. Files-only: `hw.test_score_packet/v1` stamps; exists-only ≠ PASS.  
7. `#234` juice stays off this harness until that EXIT ACCEPTs.

**Blockout gate:** `T0_GAP_INVENTORY_WALK_V1` after Lead `APPROVE-PROTOTYPE-LIST`.

---

## Feel goals (early testers) — bot-proveable vs Lead-only

| # | Feel goal | Beat | bot-proveable / Lead-only |
|---|-----------|------|---------------------------|
| 1 | Wake = work-day start, not combat spawn | Wake | B day-start log · L staging |
| 2 | Tea sprint readable on/off | Kettle→sprint | B buff · L weight curve |
| 3 | Path invites plant-then-leave | Plant + glider | B two nodes in order · L invitation |
| 4 | Backpack = load-up, not menu trap | Backpack | B state · L UI |
| 5 | Glide = intentional fall, not floaty flight | Glider→field | B left perch / field AABB · L sink |
| 6 | Gather along a path | Gather | B path nodes · L scatter |
| 7 | Rune noticed before bed | Rune | B interact before bed-gate · L icon |
| 8 | Camp ejects home; you do not die | Eject | B eject + home · L cartoon |
| 9 | Night home w/o bed: no spirit | Night-home | B flags · L mood |
| 10 | Bed→spirit = threshold | Bed+rune | B gated · L ritual |
| 11 | Nurture = care on same plant slot | Nurture | B same `NODE_PLANT_SLOT` · L VFX |
| 12 | Portals = doors; avoid+soothe ≠ kill | Portals/camp | B portal pair + 1+2 · L stealth/night |

Example DONE-WHEN lines: `left NODE_GLIDER, arrived field AABB, no load hang` · `EJECT_HOME fired, player at home, not dead` · `NODE_PLANT_SLOT day plant == spirit nurture target`.

---

## Anti-patterns (short)

| Ruling | Pattern |
|--------|---------|
| **REJECT** | Art/NightMix before verbs walk · night as bot PASS · capture-first inventory · lethal defaults · free-flight · new MUST from this library · books in AGENTS · reopen Movement bible / MV-A · DESKTOP / `.uasset` from this canon |
| **PARK** | Fast-travel skipping perch→field in *feel* pass (prove cheat OK if a later bite names it) |

---

*End. Cite EXIT GAME_DESIGN_MOVEMENT_ENV_V1 · Lead greenlight 2026-09-27. Design cites for greybox PROP_INVENTORY / feel DONE-WHEN. No Implement movement. CAP PARKED.*

**Score note:** Arrange `ready:false` ⇒ soft_fail path; `closed_fail: false` until post-Act missing MUST / bad eject.


---

## Lead lock 2026-10-03, floor entry

Outside the island spec. Not a mesh edit.

- The level is finally seen by a short move through cover to a hidden vantage. Bushes are an example, not the technique. This stays even when the floor does not change.
- One floor is a preference until the cost is measured. Do not split the floor on a guess.
- The camp does not spawn on the forest edge. From the entry, the camp's own edge is visible, whichever way the player comes in, so they can see there is something to check.
- Other forest spawns are part of the first floor and do not wait on the camp.

## Lead lock 2026-10-03, camp size

Outside the island spec. Not a mesh edit. Sized by what has to fit, not by a walk-across time.

- The camp is a circle 7 m across.
- Inside it: one guard, two sleepers, the captive, a fire, and the camp portal. Nothing else.
- The fire is 2 m across.
- The guard, both sleepers, the captive, and the portal sit in one ring around the fire, 1.5 m out from the fire's edge. That ring is 5 m across, center to center through the fire.
- There is 1 m of ground past where they stand, all the way around. That is the camp's edge.
