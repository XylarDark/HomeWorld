# Planetoid map to reality: checklist, in-editor work, and world-builder plan

**Purpose:** Single doc that answers: (1) What do we need to make the planetoid map a reality? (2) How much is in-Editor vs automated? (3) How to assemble everything automatically so you can go into the world and craft it? (4) Should we plan a world builder? (5) Tools for player biome/planetoid customization (modifiers for next planetoid) and other dual-purpose (dev + game) tools.

**Sources:** [VISION.md](workflow/VISION.md), [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md), [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md), [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md), [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md), [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), Days 16–20 (DAYS_16_TO_30.md), existing Python scripts in Content/Python. **Full manual-only tutorial:** [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md).

---

## 1. What it takes to make the planetoid map a reality

### 1.1 High-level checklist (MVP planetoid — Pride)

| # | Item | Status / script | Notes |
|---|------|-----------------|-------|
| 1 | **Planetoid level exists** | `ensure_planetoid_level.py` | Creates from template if `template_level_path` set; else one-time: File → New Level → Empty Open World → Save As Planetoid_Pride. |
| 2 | **Portal on DemoMap** | `ensure_demo_portal.py` → `place_portal_placeholder.py`, `ensure_portal_blueprint.py` | Places BP_PortalToPlanetoid at config position; LevelToOpen = Planetoid_Pride (CDO). |
| 3 | **Landscape in planetoid level** | Manual one-time | New Empty Open World includes default Landscape; no script creates Landscape. |
| 4 | **PCG Volume + graph on planetoid** | `setup_planetoid_pcg.py` | Tags Landscape, places volume, assigns Planetoid_POI_PCG, sets Get Landscape Data, triggers Generate. |
| 5 | **Get Landscape Data By Tag + mesh/template** | Partial / manual | Script cannot set Get Landscape Data actor selector or Actor Spawner template from Python (PCG_VARIABLES_NO_ACCESS). One-time: In graph set By Tag = PCG_Landscape; Actor Spawner Template = BP_Shrine_POI (or desired POI). |
| 6 | **POI / harvest / dungeon placement** | `place_resource_nodes.py`, `place_dungeon_entrance.py` | Config-driven; run with planetoid level open. |
| 7 | **Pride terrain (canyons, valleys, mountains, spires)** | Manual / future | Landscape Sculpt + Erosion + Noise per PLANETOID_PRIDE_MVP; spires as static meshes. No full-auto terrain gen today. |
| 8 | **Homestead plateau + glide** | Manual / future | Plateau = spawn/homestead location; glide = GAS or movement mode (designed, not yet built). |
| 9 | **Per-biome content (harvest, camps, dungeon camp, quest giver)** | Config + scripts | resource_nodes_per_biome, planetoid_monsters, planetoid_dungeons; placement scripts can use biome from config; full per-biome layout is script + hand-craft. |
| 10 | **Day/night on planetoid** | Existing | TimeOfDaySubsystem, phase; same as DemoMap. |

### 1.2 Delivered vs missing

- **Delivered:** Level create-if-missing, portal placement (Blueprint default LevelToOpen), planetoid PCG setup (volume, graph assign, tag, generate), POI graph, resource/dungeon config and placement scripts, biome/alignment types in C++ and config.
- **Missing for “full” Pride MVP:** (a) Terrain shaped as canyons/valleys/mountains/spires (manual or dedicated terrain pipeline). (b) Explicit biome regions on the map (today we have one planetoid level; biome segmentation is design, not yet layout). (c) Homestead plateau and glide ability. (d) Per-biome harvest/camps/dungeon/quest placement driven by a single “planetoid config” (scripts exist but are not yet wired to a single “Pride layout” config).

---

## 2. In-Editor work: how much and where

### 2.1 One-time (do once, then scripts reuse)

| Step | What | Why in-Editor | Doc |
|------|------|-----------------------|-----|
| Create planetoid level | File → New Level → Empty Open World → Save As Planetoid_Pride | If no template in config; script can’t create level from nothing | ensure_planetoid_level.py, DAYS_16_TO_30 Day 16 |
| Landscape tag + PCG graph nodes | Get Landscape Data → By Tag = PCG_Landscape; Actor Spawner → Template = BP_Shrine_POI (or POI BP) | Python can’t set these node properties (PCG_VARIABLES_NO_ACCESS) | PCG_VARIABLES_NO_ACCESS.md |
| Portal LevelToOpen | Only if not using BP_PortalToPlanetoid (CDO already set) | C++ UPROPERTY on spawned actor not writable from Python | AUTOMATION_GAPS (Gap 1); ensure_portal_blueprint avoids this |
| Terrain (Pride) | Sculpt / Erosion / Noise / spires | No script for heightmap sculpt; spires = meshes | PLANETOID_PRIDE_MVP.md §3 |
| Homestead plateau location | Place spawn / home actor or volume | Designer choice | VISION, PLANETOID_PRIDE_MVP |

### 2.2 Repeat / optional (each new map or iteration)

| Step | What | Why | Mitigation |
|------|------|-----|------------|
| Generate PCG | Click Generate on PCG Volume | Script can call Generate after setup | setup_planetoid_pcg.py already triggers Generate |
| Paint / place props | Materials, foliage, landmarks | Creative; no full auto | World-builder config can drive *where* scripts place; you polish in Editor |
| Tune POI density / bounds | volume_extent, poi_points_per_squared_meter | Design iteration | Config in planetoid_map_config.json; script reads it |
| Per-biome boundaries | Mark regions (e.g. layers, volumes, or tags) | Biome segmentation is design | Future: biome_volumes or splines in config; scripts place content per biome |

### 2.3 Summary count (MVP planetoid)

- **One-time in-Editor:** ~3–5 steps: (1) Create level (if no template), (2) In Planetoid_POI_PCG set Get Landscape Data By Tag and Actor Spawner Template, (3) Optionally set LevelToOpen on portal if not using BP_PortalToPlanetoid, (4) Terrain blockout (Pride: canyons, valleys, mountains, spires), (5) Homestead plateau placement.
- **Repeat in-Editor:** Mostly creative (paint, place, tune). Config-driven placement (resources, dungeons, POIs) is scripted; you run scripts then craft in-world as you see fit.

---

## 3. Assemble everything automatically, then craft in-world

### 3.1 Goal

Run **one entry point** (or a short ordered list) so that level, portal, PCG, and config-driven placement are done; then you open the map and do terrain + layout + polish in the Editor.

### 3.2 Single orchestrator script

Use **`assemble_planetoid_from_config.py`** (see §6 and Content/Python):

- Reads **planetoid_map_config.json** (and optionally pride-specific or per-planetoid config).
- **Order:** (1) ensure_planetoid_level, (2) ensure_demo_portal (or ensure_portal_blueprint + place_portal_placeholder with DemoMap open), (3) open planetoid level, (4) setup_planetoid_pcg, (5) place_resource_nodes (if config has resource placement for planetoid), (6) place_dungeon_entrance (if config has dungeon placement).
- Logs what was done and what remains **manual** (Get Landscape Data By Tag, Actor Spawner Template, terrain, plateau).
- Idempotent: safe to run multiple times; create-if-missing, update-in-place per game-development-principles.

### 3.3 What stays manual (documented in one place)

After the orchestrator runs:

1. **In Planetoid_POI_PCG:** Get Landscape Data → Actor Selector → **By Tag**, tag **PCG_Landscape**; Actor Spawner → **Template** = desired POI Blueprint (e.g. BP_Shrine_POI). See PCG_VARIABLES_NO_ACCESS.
2. **Terrain (Pride):** Sculpt / Erosion / Noise / spires per PLANETOID_PRIDE_MVP §3.
3. **Homestead plateau:** Place spawn or homestead actor; later glide start.
4. **Optional:** If portal was placed without BP_PortalToPlanetoid, set LevelToOpen in Details.

So: **automation assembles level, portal, PCG, and placement; you then go into the world and craft terrain and key locations.**

---

## 4. World builder: should we plan it?

**Yes.** Plan a **world builder** as a **config-driven assembly layer** plus **Editor crafting**:

- **Config-driven:** One or more JSON (or similar) configs define: planetoid id (e.g. Pride), level path, terrain preset (e.g. “Pride”: canyons/valleys/mountains/spires), biome list and per-biome content (harvest, camps, dungeon, quest giver), default bounds, POI density, resource/dungeon placement rules. Scripts create/update level, PCG, and place actors from config.
- **Editor crafting:** You open the level after assembly; sculpt terrain, paint materials, place spires and landmarks, tune spawn points and quest giver locations. The world builder doesn’t replace authoring; it gives a consistent, repeatable base so you spend time on shape and feel, not repetitive setup.
- **Same pipeline for “next planetoid”:** When the player applies **biome modifiers** (post-MVP: choose which biomes appear on the next planetoid), the same config schema can drive generation: e.g. `next_planetoid_biomes: [Forest, Canyon]` and seed; world-builder scripts (or runtime equivalent) use that to assemble the next world. So the world builder is both a **dev tool** (fast iteration) and the **backend for player-customized planetoids**.

**Concrete next steps:**

- Add **world_builder_config.json** (or extend planetoid_map_config) with: planetoid_id, terrain_preset (e.g. Pride), biomes[], per_biome: { harvest_place, monster_camps, dungeon_camp, side_quest_giver }, bounds, density. Document in PLANETOID_DESIGN or a short WORLD_BUILDER.md.
- Orchestrator reads this and calls existing scripts (ensure level, portal, setup PCG, place resources/dungeons) in order; later, add “terrain preset” as a documented manual step or a future terrain pipeline (e.g. heightmap export/import or Landscape layer workflow).

---

## 5. Player customization: biome modifiers for next planetoid

**Vision (post-MVP):** Conquering a planetoid/biome unlocks items; at the spaceship the player uses them to **choose which biomes appear on the next planetoid**. So the same tools that let **us** generate planetoids programmatically should support **player-driven** planetoid composition.

### 5.1 Tools to implement (useful for both dev and game)

| Tool | Dev use | Player/game use | Implementation idea |
|------|---------|------------------|----------------------|
| **Biome set for planetoid** | Config: biomes: [Forest, Canyon] for Pride | Player choices → same config (e.g. next_planetoid_biomes) | Config key `biomes` or `enabled_biomes`; placement and PCG respect it. |
| **Planetoid modifier / seed** | Reproducible layouts for testing | Seed or “modifier” from player choices (e.g. difficulty, theme) | Config: seed, difficulty_preset; placement scripts use seed. |
| **Per-biome content toggles** | Turn on/off harvest, camps, dungeon, quest per biome | Unlocks enable content (e.g. “Forest harvest unlocked”) | Config: per_biome: { harvest: true, camps: 2, dungeon: true, quest_giver: true }. |
| **World-builder “preset”** | Pride, Greed, etc. | Themed planetoid (sin theme) | terrain_preset + palette + biome set; one config per sin. |

### 5.2 Config schema (for future implementation)

- **planetoid_modifiers.json** (or section in world_builder_config):  
  `enabled_biomes`, `seed`, `terrain_preset`, `per_biome_overrides` (harvest, camps, dungeon, quest_giver).  
  At spaceship, player choices write (or select) a modifier set; next planetoid load uses it to drive assembly (dev scripts now; runtime or dedicated “planetoid gen” later).

### 5.3 Other dual-purpose tools

| Tool | Dev | Game / design |
|------|-----|----------------|
| **Console / cheat: load planetoid by id** | Quick test of Pride vs Greed | — |
| **Console: set zone biome/alignment** | Test harvest vs combat vs empower | — |
| **Placement validation script** | Check “every biome has harvest + 2 camps + dungeon + quest” | QA / design checklist |
| **POI density / bounds in config** | Iterate without Editor | Same config for shipped “planetoid templates” |
| **Glide ability (GAS)** | Test plateau → ground | Core loop (homestead → glide → explore) |
| **Spaceship “biome selector” UI** | — | Player picks biomes for next planetoid (post-MVP) |

---

## 6. Research applied: solutions in this repo

### 6.1 Orchestrator: `assemble_planetoid_from_config.py`

- **Location:** Content/Python/assemble_planetoid_from_config.py.
- **Behavior:** Load planetoid_map_config.json; run in order: ensure_planetoid_level → (open DemoMap) ensure_demo_portal → (open planetoid level) setup_planetoid_pcg → place_resource_nodes (if config/level allow) → place_dungeon_entrance (if config allows). Log manual follow-ups (Get Landscape Data, terrain, plateau).
- **Idempotent:** Each step is already create-if-missing or update-in-place; no delete-and-recreate.

### 6.2 Docs updated

- **PLANETOID_DESIGN.md:** Add reference to this doc (§ World builder and planetoid-to-reality) and to WORLD_BUILDER_AND_MODIFIERS.md (or inline §4/§5 above) for world-builder plan and biome-modifier config.
- **DAYS_16_TO_30.md:** Add “Single entry point” bullet: run assemble_planetoid_from_config.py then do manual steps in §2.1.

### 6.3 Manual steps (single checklist for you)

After running the orchestrator:

1. **PCG graph (Planetoid_POI_PCG):** Get Landscape Data → By Tag = PCG_Landscape; Actor Spawner → Template = BP_Shrine_POI (or chosen POI). Generate if needed.
2. **Terrain (Pride):** Sculpt / Erosion / Noise; add spire meshes. See PLANETOID_PRIDE_MVP §3.
3. **Homestead plateau:** Place spawn/homestead; later add glide.
4. **Portal:** If not BP_PortalToPlanetoid, set LevelToOpen = Planetoid_Pride in Details.

---

## 7. Summary

| Question | Answer |
|----------|--------|
| **What to do to make planetoid map a reality?** | Use §1.1 checklist: level, portal, PCG, POI/resource/dungeon placement; then terrain (manual) and plateau/glide (manual or future). |
| **Do you need in-Editor work?** | Yes: (1) One-time: create level (if no template), PCG graph By Tag + Template, optional portal LevelToOpen, terrain, plateau. (2) Repeat: creative polish (paint, place, tune). |
| **How much in-Editor for MVP?** | About 3–5 one-time steps above; rest is config-driven scripts + your crafting. |
| **Assemble automatically then craft?** | Yes: run **assemble_planetoid_from_config.py**; it does level, portal, PCG, placement. Then do the short manual checklist (§6.3) and craft terrain and key locations in Editor. |
| **Plan a world builder?** | Yes: config-driven assembly (planetoid id, terrain preset, biomes, per-biome content) + Editor crafting; same pipeline can drive player-customized “next planetoid” via biome modifiers. |
| **Tools for biome/planetoid customization?** | Config: enabled_biomes, seed, per_biome_overrides; world-builder and (later) spaceship UI feed same schema so we generate programmatically and players customize next planetoid. |
| **Other useful tools (dev + game)?** | Biome set in config, seed/modifier, per-biome toggles, world-builder presets, console load planetoid / set zone, placement validation script, glide ability, spaceship biome selector (post-MVP). |

---

## References

- [VISION.md](workflow/VISION.md) — MVP scope (day/night on planetoid), homestead plateau, glide, biomes, per-biome content.
- [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md) — Map shape (sphere), biome segmentation, per-biome structure, post-MVP chunk/biome loading and spaceship biome selection.
- [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md) — Pride terrain (canyons, valleys, mountains, spires), UE5 approach, Astroneer-like scale.
- [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md) — Four biomes, resource nodes, alignments, per-biome harvest/camps/dungeon/quest.
- [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) — Get Landscape Data, Actor Spawner template, manual steps.
- [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) — Portal LevelToOpen, State Tree, etc.
- [DAYS_16_TO_30.md](tasks/DAYS_16_TO_30.md) — Day 16–20 scripts and verification.
