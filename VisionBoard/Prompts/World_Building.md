# World Building — Vision Board

Use this when generating prompts or design for biomes, harvestables, dungeons, planetoid structure, and content placement. Source: [../Planetoid/PLANETOID_DESIGN.md](../Planetoid/PLANETOID_DESIGN.md), [../Planetoid/PLANETOID_BIOMES.md](../Planetoid/PLANETOID_BIOMES.md), [../Planetoid/PLANETOID_PRIDE_MVP.md](../Planetoid/PLANETOID_PRIDE_MVP.md), [../Core/VISION.md](../Core/VISION.md).

---

## Map shape and biome segmentation

- **Shape:** The planetoid **map shape is a sphere**. Playable surface is the sphere’s exterior; orientation and streaming follow the spherical layout (“align to planet up” for gravity and placement).
- **Biome segmentation:** The **entire area of the planetoid** is **divided into biomes**. We have four biomes at the start: **desert, forest, marsh, canyon**. Each region of the sphere’s surface is assigned to one of these so the player explores distinct harvest, combat, and dungeon content per biome.

---

## Per-biome structure (content per biome)

Each biome on the planetoid contains a **consistent set of content**:

| Content | Description |
|--------|-------------|
| **Harvest place** | Dedicated area(s) where the player can gather that biome’s harvestables (trees, herbs, rocks, water, spirits). |
| **Monster camps** | A couple of camps of monsters (corrupted, per-biome type) for combat and conversion. |
| **Dungeon camp** | One camp outside a dungeon — a monster camp at or near the dungeon entrance for that biome. |
| **Side quest giver** | A side quest giver in the biome for objectives and rewards. |

---

## Resource node types

Planetoids support these **resource node** categories (harvestable by the player):

| Type | Description | Example use |
|------|-------------|-------------|
| **Trees** | Wood, lumber, shade | Building, fuel, crafting |
| **Flowers / herbs** | Botanicals, medicine, dyes | Healing, buffs, cooking |
| **Rocks** | Stone, ore, crystals | Building, tools, crafting |
| **Water** | Water sources, wells, springs | Drinking, crafting, spirits |
| **Spirits** | Spirit nodes (astral / spiritual) | Empowerment, buffs, conversion |

Spirits are a resource node in the sense of a place or entity the player can interact with to gain empowerment (positive zones) or to fight/convert (corrupted zones).

---

## Four biomes (initial)

| Biome | Harvestable focus | Monster type (corrupted) | Dungeon type |
|-------|-------------------|---------------------------|--------------|
| **Desert** | Rocks, sparse herbs, water (oasis) | Desert-themed corrupted | Tomb / crypt |
| **Forest** | Trees, flowers/herbs, some water | Forest-themed corrupted | Ancient grove / dark wood |
| **Marsh** | Herbs, water, spirits (fen) | Marsh-themed corrupted | Swamp dungeon / bog shrine |
| **Canyon** | Rocks, crystals, sparse herbs | Canyon-themed corrupted | Mine / cavern |

---

## Biome alignment (corrupted / neutral / positive)

Each biome can appear in three **alignments**:

- **Corrupted** — Where you fight (monsters, conversion).
- **Neutral** — Where you harvest (resources, no combat focus).
- **Positive** — Where you empower yourself (buffs, spirits, safe zones).

Resource nodes and spirit nodes are placed per biome and alignment; implementation is task-list driven.

---

## Pride planetoid (first MVP) — terrain character

- **Canyons** — Deep cuts, gorges, ravines; vertical relief and narrow passages.
- **Valleys** — Lower ground between heights; corridors and basins.
- **Mountains** — High elevation, peaks, ridges; large-scale vertical variation.
- **Large spires** — Tall, prominent rock formations; landmarks and vertical drama.

Pride’s **overall surface character** is canyon–valley–mountain–spire. Sub-regions or named areas: e.g. Pride_Canyons, Pride_Valleys, Pride_Mountains, Pride_Spires. **Homestead:** Plateau at the top of a mountain; player can **glide down** to the ground to explore.

---

## Principles (planetoid identity)

- **One identity per planetoid:** Each of the 7 levels is a single planetoid identity (Pride, Greed, Wrath, Envy, Gluttony, Lust, Sloth), with its own **biome set**, **palette**, and **proc-gen rules**. Do not reuse the same “planet type” across sin levels.
- **Surface + optional layers:** Surface = primary play area (PCG-on-Landscape or equivalent). Optional subsurface/cave or “second layer” regions with different placement rules and density.
- **Thematic consistency:** Each planetoid has a distinct **soil/ground color**, **foliage set**, and **prop set** aligned with the sin/virtue theme. Curated materials and meshes per level.

---

## Out of scope

- **Deformable / voxel terrain.** HomeWorld does not use diggable, mutable terrain. No runtime voxel deformation. Terrain is static or baked (Landscape, PCG on surfaces, or pre-authored meshes).
