# EA-LOOKLOCK — Environment Art look-lock inventory

| Field | Value |
|-------|-------|
| **Status** | **GATE READY** — pending Lead **`APPROVE EA-LOOKLOCK`** |
| **Host** | CLOUD (this doc) · Lead (taste gate) · **no DESKTOP Act** |
| **Source brief** | [ENV_ART_DIRECTOR_BRIEF.md](ENV_ART_DIRECTOR_BRIEF.md) (PR #212 — merge if still open) |
| **Canon parent** | [Docs/00_CANON.md](../00_CANON.md) **LOCKED** — inventory **⊆** canon ∩ brief; no new product track |
| **CAP** | CAP-002 Do **HELD** — this packet is look-lock docs only |
| **Cite** | Architecture Trade-Offs A–E (canon blob `107a511`) · HomeWorld Co ops · CAPTURE_REDUNDANCY · ONE_SHOT_BITES |

---

## Lead gate

```text
APPROVE EA-LOOKLOCK
```

Unlocks **docs-only** next: Conductor may open Implement SCOUT for *labeled* lookdev/kit work that cites this inventory — **not** CAP Do, **not** a new Docs/N phase number without Lead naming the track.

---

## Non-goals (locked)

- No CAP-001/002 product Do
- No Content/Python/Source/.uasset/.umap in this bite
- No invent Docs/34+ phase row
- No unlock of CANON hard-reject **extra biomes** as MVP scope
- No DESKTOP MCP prove / PASS/FAIL from Design
- No alwaysApply / AGENTS dump / pin bump

---

## 1. Spatial contract → canon map (labels only)

| Brief layer | Inventory label | Canon map (00_CANON §2) | MVP status |
|-------------|-----------------|-------------------------|------------|
| SKY HUB | `LAYER_SKY_HUB` | HERO ISLAND (cabin, garden, path, pines, lookout, shrine, glider perch) | **IN** |
| DESCENT CORRIDOR | `LAYER_DESCENT` | TRANSIT (lookout → air / islets / glider → landing; night portal) | **IN** |
| SURFACE SLICE | `LAYER_SURFACE` | PLANET SLICE (forest path 2–4 min, gather, 1 beast, spirit-wound, landing, return shrine) | **IN** |

**Generation method (brief → inventory):** Path-of-Exile tileset language is **kit grammar**, not open-world noise. MVP uses existing VS_MVP / homestead + planet forest kit; PCG invent of new biome continents is **OUT** until Lead names a track.

| Graph node label | Meaning | MVP world intersection |
|------------------|---------|------------------------|
| `NODE_ENTRANCE` | Glide/landing or biome gate in | Landing circle / lookout lip |
| `NODE_THROUGHLINE` | Readable spine path | Forest/homestead path stones |
| `NODE_SIDE_A` / `NODE_SIDE_B` | Optional pockets | Gather / den / blight-shaped damage |
| `NODE_SLEEP` | Sleep/shrine candidate | Homestead shrine / return shrine / tree-bowl read |
| `NODE_LANDMARK` | Visible from prior node | Island silhouette, pine landmark, shrine stack |

Reject layouts (inventory flags — Implement must not ship): even prop scatter; no spine; mechanic-as-particles-only.

---

## 2. Day / night = same map (dress pass)

| Label | Day read | Night read | Canon hook |
|-------|----------|------------|------------|
| `TOD_DAY` | Body-work: gather, tame dens, planted rows, damaged soil | — | Verbs walk/gather/tame/nurture |
| `TOD_NIGHT` | — | Spirit-work: healed veins, shrine corridors, residual sow/tame shapes | Portal + heal; NightMix 0–1 on masters |
| `MAP_SAME` | Geometry shared | Second dress + light only | **No second continent** |

Hard reject: horror night, neon cyberpunk, white blowout emissives.

---

## 3. Style lock (intersection)

**Target:** Nintendo surface readability + classic WoW zone color sentence + low-poly cartoon construction.

| Steal-from | Inventory keep |
|------------|----------------|
| Nintendo | Atmospheric perspective; floating underside silhouette; vista = mid + far + sky; TOD as color script |
| Classic WoW | One biome = one color sentence; landmark-first; chunky forms; vertex-color thinking |
| Low-poly | Clear planes/bevels; few mats; even texture density; icon/toy/diorama distances |

Union hard rejects (brief ∪ CANON §7): photoreal / megascan grit; Fortnite gloss; anime chrome spam; soulslike grey-brown default; generic pine pack; sci-fi hex/UI magic; horror night; pancake islands; tiny white moons; dark cabin windows; combat; free-flight sim; worker self-approve.

---

## 4. Palette sentences (schema; MVP vs future)

CANON locks **one** planet forest slice. Brief biomes A/B/C are **palette role labels** — only **A** maps to MVP surface default; B/C stay **FUTURE** until Lead Taste Gate unlocks extra biomes.

| ID | Color sentence (≤5 words) | Role | MVP |
|----|---------------------------|------|-----|
| `PAL_A_MEADOW` | warm green, cream stone, honey path | Living terrace / meadow-wood | **IN** (planet + homestead warm) |
| `PAL_A_DAMAGED` | olive-grey, dust-yellow blight fans | Day wound shapes | **IN** (spirit-wound / blight as shape, not noise) |
| `PAL_A_HEALED_NIGHT` | teal shadow, soft gold shrine | Healed night of A | **IN** (NightMix + shrine emissive) |
| `PAL_B_CANYON` | slate teal, terracotta banks | River-canyon / root-cliff | **FUTURE** |
| `PAL_C_ASH` | charcoal soil, copper grass | Ash-garden wound | **FUTURE** |

Lighting law (inventory): authored skylight + fog; short local lights; night = moon fill + shrine + healed-vein emissive only; tinted shadows; matte ground.

---

## 5. Verb advertising (labels ⊆ inventory ∩ world)

Map brief verbs → CANON eight MVP verbs (no new verbs).

| Brief verb | Inventory label | Canon verb | World proof cue |
|------------|-----------------|------------|-----------------|
| GLIDE | `VERB_GLIDE` | Glide/fly island → planet | Launch lip, wind/cloud lane, surface color mass + landmark spike |
| WALK | `VERB_WALK` | Walk homestead (+ planet path) | Path value-contrast vs wild; consistent slope language |
| GATHER / TAME | `VERB_GATHER` / `VERB_TAME` | Gather 6 RES / Encounter 1 beast | Nodes in rooms; dens with entrance scale; blight = shaped fan |
| SLEEP | `VERB_SLEEP` | Return / dawn cycle (safe hollow) | Readable from ~80 m: roof / light / shrine knot / tree-bowl |
| HEAL | `VERB_HEAL` | Heal 3 spirits | Same silhouette as day wound; material + light change |
| NURTURE | `VERB_NURTURE` | Nurture 2 homestead targets | Planted rows / cared micro-scenes |

Camera assumption freeze: design for **wide pastoral / mid-distance third-person** first (`CAM_ASSUME_WIDE`). Tight cinematic-only spaces = rebuild.

---

## 6. Prove cam catalog (look-at / AABB / TOD freeze — Arrange before Act)

Schema only. No new actors until Lead **`APPROVE EA-LOOKLOCK`** and Conductor opens a named Implement bite. Prefer **reuse** existing `CAM_*` labels from PS/MVP inventory; new `EA_*` labels only if missing.

| Cam ID | Intent | Prefer reuse | TOD | Look-at target (label ⊆ §1–5) | AABB / framing note |
|--------|--------|--------------|-----|-------------------------------|---------------------|
| `EA_SKY_HUB_LIP` | Homestead lip vista | `CAM_Hero` / lookout family | `TOD_DAY` golden | `LAYER_SKY_HUB` + far `LAYER_SURFACE` color mass | Wide; player tiny; three-point vista |
| `EA_DESCENT_GLIDE` | Mid-glide underside | `CAM_GlideDepart` | `TOD_DAY` | Island underside + surface beacon | Cloud lane readable |
| `EA_SURFACE_APPROACH` | Path → landmark | path / landing family | `TOD_DAY` | `NODE_LANDMARK` + `VERB_WALK` path | Mid-distance; side pocket optional |
| `EA_SLEEP_DUSK` | Sleep shrine read | shrine / cabin family | dusk → `TOD_NIGHT` | `NODE_SLEEP` | Readable ~80 m silhouette |
| `EA_HEAL_NIGHT` | Day-wound healed | `CAM_PortalNight` family or night shrine | `TOD_NIGHT` | Same wound silhouette as day | Cool teal + gold vein; no horror fog |

**Arrange DONE-WHEN (docs gate — not DESKTOP score):** each cam row has TOD + look-at label from this inventory; no orphan look-at; FUTURE palettes not required for MVP cams.

**Pass tests (brief § finished environment — taste / Lead, not auto metrics):**

1. Silhouette @128px: island + descent target + one surface landmark  
2. Saturation −30%: path / hazard / rest / wild still separate  
3. Same camera day vs night = same place  
4. Three care objects visible  
5. (PCG) two kit rolls still same region — **N/A until PCG bite named**  
6. Pace: stand-still place without objective marker  

---

## 7. Material / production constraints (cite only; no new masters)

CANON: **exactly 10** masters. Brief “one foliage/rock/shrine/soil master” maps onto existing ten — **do not add masters**.

| Brief constraint | Inventory decision |
|------------------|--------------------|
| Nanite for hero rocks/island underside | Optional later; style stays authored low-mid poly |
| PCG places from artist kit | Kit sockets: path, cliff, water, grove, blight, shrine, nest — **labels only** until Lead track |
| World Partition | One surface slice + one sky island |
| Water / glide air | Graphic plane + large readable cloud shapes |

---

## 8. A–E 15-q (boundary invented: brief → look-lock inventory quantum)

Invented boundary: **docs quantum** `EA-LOOKLOCK` = frozen label inventory + prove cam schema. Writer = Design. Consumers = Conductor / Implement (later) / AD. No Source API.

| # | Answer |
|---|--------|
| 1 Quantum | Yes — docs-only deployable via PR; no shared DB/schema drag. Real quantum = this handoff file + brief. |
| 2 Integrators | Keep with CANON (integrator: shared language). Do not split a second “art bible” quantum. |
| 3 Data ownership | Design writes inventory labels; world labels must ⊆ inventory ∩ existing level actors when Act opens. Freshness = at APPROVE stamp. |
| 4 3Cs | Sync docs handoff; consistency = Lead APPROVE; coordination = Conductor ball. No saga. |
| 5 Contract | Explicit tables §1–6 + gate string. Implicit “make it pretty” rejected. |
| 6 Depth | One inventory file hides brief prose; interface = labels + DONE-WHEN + APPROVE. |
| 7 Leakage | Biome B/C marked FUTURE so CANON “no extra biomes” does not leak as unlocked MVP. |
| 8 Errors | Undefined FUTURE palette in MVP Act = closed_fail design bounce, not soft invent. |
| 9 Obviousness | Labels prefixed `LAYER_` / `PAL_` / `VERB_` / `EA_` / `TOD_`. |
| 10 Strategic residue | Cite CANON + brief; fitness = labels ⊆ inventory ∩ world at Arrange. |
| 11 Data physics | N/A — no replication. Derived: cam rows from inventory (source = this file). |
| 12 Consistency | Strongest = Lead gate before Implement SCOUT. |
| 13 Team | Stream-aligned Design owns; Implement consumes X-as-a-Service via this handoff path. |
| 14 Integration | No remote calls. Degrade = hold Act if labels missing. |
| 15 Steady state | No unbounded retries; one unknown; CAP stays HELD. |

---

## DONE-WHEN (EA-LOOKLOCK)

- [x] Brief → canon layer map (§1)
- [x] Day/night same-map dress rule (§2)
- [x] Style + reject union (§3)
- [x] Palette sentences with MVP vs FUTURE (§4) — **no extra-biome unlock**
- [x] Verb advertising mapped to CANON eight (§5)
- [x] Prove cam catalog with look-at / TOD freeze schema (§6)
- [x] Ten-master constraint restated (§7)
- [x] A–E 15-q for inventory quantum (§8)
- [ ] Lead **`APPROVE EA-LOOKLOCK`**
- [ ] Brief on `main` (`Docs/handoffs/ENV_ART_DIRECTOR_BRIEF.md` via #212 merge if needed)

---

## Next (after Lead gate — Conductor owns)

1. Conductor: set `ball:` / optional PHASE_BOARD note — **no new Docs/N without Lead name**
2. Implement: only if Lead names a SCOUT bite citing this inventory paths
3. CAP-002 remains **HELD** unless Lead flips product

---

## References

- Brief: `Docs/handoffs/ENV_ART_DIRECTOR_BRIEF.md`
- Canon: `Docs/00_CANON.md`
- Prior inventory pattern: `Docs/handoffs/PS_A_INVENTORY.md`
- Ops: CAPTURE_REDUNDANCY · ONE_SHOT_BITES · homeworld-co-ops
