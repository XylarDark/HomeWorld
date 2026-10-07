# docs/39_ZONE_GENERATION_RESEARCH.md

## Zone generation — PoE-style maps for the plains and the forest

**Status:** RESEARCH + PROPOSAL — Lead directive 2026-10-07, not yet canon.
**Directive:** the homestead island and its assets stay custom, hand-made. The
field (plains) and the forest become generative zones, like a Path of Exile
map: a vague preset shape that changes with random generative variables. The
plains and the forest are the first two use cases. As the player explores,
zones generate based on the direction they travel, and the specs must
accommodate that. The camp is custom content inserted into a generated forest
— it must never land in the field.

---

## 1. What Path of Exile actually does (ExileCon 2019 dev talk + community notes)

PoE area generation is two phases over a per-area template:

1. **Layout skeleton.** Each area declares a *vague shape* — an overall extent,
   a target room/segment count, and a set of special anchors (entrance, exit,
   boss room). The generator picks segments from that area's authored pool,
   places them roughly on a grid with weighted randomness, then connects them
   with corridors so the graph is fully connected (entrance reaches exit, boss
   hangs off a leaf). Segments are pre-authored tile pieces; the *choice,
   orientation and connection* of pieces is what randomizes, not the pieces
   themselves.
2. **Dressing.** Props, enemies and decorations scatter inside placed segments
   with weighted rules and density budgets. Predictability comes from anchors
   (exit generally opposite entrance), uniqueness from set-piece segments the
   generator can drop in.

Key properties worth stealing:

- **Determinism from a seed.** Same seed → same map. A party shares one
  instance; a save only needs the seed plus what changed.
- **Preset shape, variable interior.** The map *type* is recognizable every
  time; the interior, connections and contents vary.
- **Content mods on top of layout.** Random variables ("map mods") change what
  spawns, not the geometry contract.
- **Hand-authored segments are the unit of quality.** The generator never
  invents geometry, it *arranges* authored geometry. Quality scales with the
  segment library, which is why PoE feels designed even when random.

## 2. How generated zones stop feeling generated (industry consensus)

- **Layer authored over random.** Keep a curated pool of authored rooms/
  set pieces the generator stitches between; the random base only supplies
  connectivity and filler. (Classic fix, cited everywhere from roguelikedev to
  shipped AAA.)
- **Guaranteed anchors/landmarks.** One or two authored points of interest per
  zone that the player can navigate by and remember — Hades' authored reward
  rooms behind random doors, Dead Cells' set-piece rooms inside random biome
  layouts, PoE's boss/unique rooms.
- **Constrained randomness, not free randomness.** Rules that forbid dull or
  unfair results (connectivity checks, density budgets, minimum/maximum
  spacing, "no man-made markers in an untouched meadow"). Randomness is only
  felt when it breaks a rule the player subconsciously learned.
- **Zone identity and clear boundaries.** Distinct zones with readable edges
  read as designed; a mush of continuous noise reads as generated.
- **Weighted scatter with adjacency rules.** Our FIELD scatter rule (common
  ~30 m, 25 % duals, 5 % triples) is already this pattern — it just needs a
  seeded driver instead of an authored list.

## 3. UE 5.8 runtime options in this project

| Option | What it gives us | Status here |
|---|---|---|
| **PCG framework, Runtime Generation** | Graph-driven scatter that generates/cleans up near PCG Generation Sources at runtime (editor, PIE, standalone); On-Demand for edit, On-Load for ship; needs a PCGWorldActor | Tooling exists but is legacy/quarantined: `ForestIsland_PCG`, `Planetoid_POI_PCG` (docs/08), known no-access automation gaps (`docs/PCG/PCG_VARIABLES_NO_ACCESS.md`), helpers `pcg_settings_introspect.py` / `create_pcg_forest.py` |
| **C++ seeded generator** | `FRandomStream` skeleton + scatter + slot insertion, fully unit-testable (budgets, connectivity, "camp never in field" as automation) | No precedent yet, but every placement rule already lives in our `Lib/**/*.json` specs, which the tests already read |
| **Hybrid (recommended)** | C++ owns the zone skeleton, edge contracts and custom-content slots; PCG or HISM scatter owns grass/trees/decor density | Matches Arch B: existing specs and systems, no parallel canon |

Streaming note: the playable level is a single map (`L_VS_MVP_Markers`), no
World Partition. "Unload a zone" for now means returning its actors to a pool —
fine at the 420 m scale; revisit only if the world grows past a handful of
live zones.

## 4. Proposed architecture — zone = seeded map instance

```
ZoneSpec (our existing JSON, extended)        ZoneInstance (runtime)
--------------------------------------        ----------------------
template shape (vague ellipse/blob)     -->   seeded skeleton (size/edge jitter
edge contracts (neighbor kind, band)          within preset bounds)
content budget (counts, spacing)        -->   FRandomStream scatter (rules above)
custom-content slots (camp, wound...)   -->   authored pieces pinned into slots
rejects (no paths, no markers, ...)     -->   generator assertions + tests
```

- **Seed** = hash(zone kind, position in the world graph, direction of
  arrival). Deterministic: revisiting a zone regenerates the same map; a save
  stores seed + deltas (healed wisps, freed captive, tamed beasts, tended
  soil).
- **Edge contracts.** Every zone edge declares the neighbor kind it opens onto
  (field south/west edge → forest, east → river/future, north → cliff/dead).
  Crossing an edge instantiates (or re-activates) the neighbor from its
  template — this is the "generates based on the direction we travel" part.
  Unchosen edges keep their neighbor dormant, which preserves FIELD's
  "the unchosen forest is a road they did not take" rule with no extra work.
- **Identical-forest constraint stays structural.** FIELD's hard constraint
  (both forest edges must look identical from inside the field) is enforced by
  both edges pointing at the same template with the same silhouette budget —
  only the interior seed differs, and only after the player has entered.
- **Custom-content insertion is slot-driven.** The camp (5 modules + 4 actors),
  spirit wound, rune and shrine are authored pieces the forest template has
  slots for — PoE's "unique room" pattern. **The field template has zero such
  slots**, so "camp in the field" becomes structurally impossible rather than
  a placement mistake. Homestead island is not generated at all.
- **Feel less generative** = (a) one guaranteed anchor per zone from the slot
  pool, (b) budgets that keep the locked reads intact (untouched meadow: no
  paths, no markers; grass 0.9–1.2 m hides the dung), (c) seeded jitter of the
  vague shape so silhouette varies but edge *types* never do.

### First use cases

1. **Plains (FIELD)** — template already 90 % written: 420 × 420 ellipse-ish
   bounds, four typed edges, scatter rule, rejects list. What's missing is the
   seeded driver and shape jitter (size ± %, edge band positions) instead of
   fixed ±210 coordinates.
2. **Forest (CAMP lives here)** — needs a spec (see §5): blob template with a
   depth band, two entry points matching the field's two forest edges, camp /
   wound / shrine slots, pine density budget, identical-silhouette rule.

## 5. Zone separation — current defect and the fix

Checked against the specs and the blend today:

- FIELD origin `(0, -80, -95)`, bounds 420 × 420 → world x ∈ [-210, 210],
  y ∈ [-290, 130].
- CAMP origin `(20, -80, -95)` → **~20 m from the field centre — the camp is
  inside the field**, which also violates FIELD's own reject
  `camp_visible_from_the_field_centre`.
- The blend's `02_Forest` blob (x -37..47, y -166..-65) and my new `06_Camp`
  modules sit inside the field bounds too. Everything currently clusters on
  one datum.

The fix as a contract (Lead 2026-10-07: "the field and the forest are two
different zones and the camp work is not going in the field"):

- **FIELD** contains: meadow, four edges, beasts, scatter. It contains no
  forest interior and no camp — only the two identical forest *edge bands*.
- **FOREST** becomes its own zone spec with its own origin outside the field
  bounds (beyond one of the two forest edges), carrying camp, spirit wound,
  shrine-return and pine density. The camp origin moves with it.
- **T0 static placeholder:** one forest instance attached to one field edge
  while generation is being built. Which edge is the one open question (see
  §7) — after that, entry-triggered generation replaces the static choice.

## 6. Build order (proposal)

1. `FOREST.json` — new zone spec: template, edges, slots, budget, rejects
   (mirrors FIELD's structure).
2. Zone separation edits — FIELD/CAMP json contracts + move the blend camp and
   forest to the new origin (revertible, git-tracked).
3. Seeded zone generator (C++): skeleton jitter + scatter from specs, with
   tests asserting budgets, determinism (same seed → same output), and
   **field-has-no-camp-slots** as permanent automation.
4. Edge-crossing instantiation — direction-driven neighbor generation, seeded
   by arrival history; dormant neighbors for unchosen edges.
5. Custom-content insertion pass — camp/wound/rune/shrine slots into the
   forest instance; prove scripts (M8/M10–M14) then run against generated
   geometry, which is what unblocks GATE 3 evidence anyway.
6. Only then: PCG/HISM density dressing (grass, pines) under the locked
   art-bible reads.

## 7. Open questions for the Lead

1. **T0 forest edge:** which field edge hosts the first static forest+camp
   instance — south (EDGE_FOREST_A) or west (EDGE_FOREST_B)? (Player-choice
   generation comes later; T0 needs one concrete placement.)
2. **Shape variance:** how vague is "vague"? Proposal: ±15 % on zone extent,
   edge bands drift ±25 m, interior scatter fully seeded — silhouette-level
   variation only, edge types never change.
3. **Old forest/camp datum:** the move clears the field but re-positions
   shrine-return and the wound marker too — confirm they follow the forest.

## References

- ExileCon 2019, *Procedural World Generation in Path of Exile* (Rhys Abraham).
- UE docs, *Using PCG Generation Modes — Runtime Generation* (5.5+, applies to 5.8).
- Project state: `docs/08_AUDIT_SIGN_OFF.md` (legacy PCG assets, quarantined),
  `docs/PCG/PCG_VARIABLES_NO_ACCESS.md` (automation gaps),
  `Lib/02_Zones/gather/FIELD.json`, `Lib/02_Zones/combat/CAMP.json`.
