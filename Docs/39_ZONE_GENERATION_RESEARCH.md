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

### Loading — decide the edges, generate the biome on discovery

Lead 2026-10-07: biomes generate from their seeds, and the camp is placed from
the forest spec only when the player discovers that forest. The field generates
first. Each edge's neighbor kind is decided and the edge assets are placed in
the field. The bounds of those assets are the discovery boundary. Reaching a
`pine_forest` boundary places the camp. Standing in the meadow does not.

Cost, in this order:

1. **Stream from where the player is standing.** While they are on the
   homestead, the field streams in and nothing past it does. While they are on
   the field, a neighbor streams only if it can be walked into from the ground
   — the two pine forests. Those forests generate from their seeds without the
   camp. The camp pins when the player reaches that edge's placed assets. The
   other forest stays streamed and camp-free. Going back to the homestead
   unloads the zones; returning restores the chosen camp from the same seed.
2. **Special traversal is not ground streaming.** The cliff edge is the
   upgraded glider. The river edge is the boat. Neither streams from merely
   standing on the field. Each starts streaming when that traversal begins and
   the upgrade is unlocked. Locked, the edge stays unloaded.
3. **Night spirit is not a traversal rule yet.** Day is the lock above. Canon
   already has spirit-stealth in the camp at night, a day eject home from the
   camp, and a night flight buff for spreading over the field. Whether spirit
   form can enter a forest, take the glider, or take the boat is still open.
4. **Do not convert `L_VS_MVP_Markers` to World Partition for this.** That map
   stores actors inline. Conversion creates a second map, and unloaded cells
   hide the ground. See `docs/KNOWN_ERRORS.md`.
5. **When a discovered forest has to stream as meshes,** put that zone on one
   runtime Data Layer and activate it at the boundary. Runtime Data Layers load
   and unload at runtime from Blueprints or C++
   ([Data Layers, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/world-partition---data-layers-in-unreal-engine)).
   Assets assigned to too many runtime data layers degrade streaming, so the
   layer is the zone, not each prop.
6. **Level Instances do not stream by themselves** outside a World Partition
   world. Level Streaming mode adds a level per instance and is a poor fit for
   a dense set of biomes
   ([Level Instancing, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/level-instancing-in-unreal-engine)).
7. **Dressing stays later.** PCG runtime generation, scoped to a source at the
   discovered forest, is still the density pass. It is not the loader for the
   camp.

The World Partition overview on Epic's site is still titled as the 5.7
documentation. The two 5.8 pages above are the ones this note uses.

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
  Reaching the placed edge-asset boundary instantiates (or re-activates) the
  neighbor from its template, and a forest boundary is what places the camp.
  Until that discovery the neighbor is a seed. Unchosen edges keep their
  neighbor dormant, which preserves FIELD's
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
- **No static placeholder** (Lead 2026-10-07, Q1 answered: *"straight to
  generation"*): skip the throwaway layout and build entry-triggered
  generation directly — whichever forest edge the player crosses instantiates
  the forest zone. The spec for it is `Lib/02_Zones/combat/FOREST.json`
  (entry-relative slots, no fixed world origin).

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

1. **T0 forest edge:** — **answered 2026-10-07: "straight to generation."**
   No static forest placement; entry-triggered generation is the first
   implementation. (Questions 2–3 below remain open.)
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
