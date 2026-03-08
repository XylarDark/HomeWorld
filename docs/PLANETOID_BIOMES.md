# Planetoid biomes and resources (vision)

**Purpose:** Define planetoid biomes, resource node types, and the corrupted/neutral/positive alignment system. Each biome has distinct harvestables, monster types, and dungeon types. **This is the first of a 4-list planetoid focus;** implementation is spread across task lists 36–39.

**Source:** Vision update (2026-03-06). See [workflow/VISION.md](workflow/VISION.md) for campaign and sin/virtue context; [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md) for proc-gen philosophy.

---

## 1. Resource node types

Planetoids support these **resource node** categories (harvestable by the player; can be placed by PCG or scripts):

| Type | Description | Example use |
|------|-------------|-------------|
| **Trees** | Wood, lumber, shade | Building, fuel, crafting |
| **Flowers / herbs** | Botanicals, medicine, dyes | Healing, buffs, cooking |
| **Rocks** | Stone, ore, crystals | Building, tools, crafting |
| **Water** | Water sources, wells, springs | Drinking, crafting, spirits |
| **Spirits** | Spirit nodes (astral / spiritual) | Empowerment, buffs, conversion |

Spirits are a **resource node** in the sense of a place or entity the player can interact with to gain empowerment (positive zones) or to fight/convert (corrupted zones). Exact implementation (actor, POI, or subsystem) is task-list driven.

### 1.1 Resource-node-to-biome mapping

Which resource node types appear in which biomes (for placement, PCG, or scripts):

| Resource node   | Desert | Forest | Marsh | Canyon |
|-----------------|--------|--------|-------|--------|
| **Trees**       | —      | ✓ primary | (optional) | — |
| **Flowers / herbs** | sparse | ✓ primary | ✓ primary | sparse |
| **Rocks**       | ✓ primary | (some) | (some) | ✓ primary (incl. crystals) |
| **Water**       | ✓ (oasis) | ✓ (some) | ✓ primary | — |
| **Spirits**     | —      | (optional) | ✓ primary (fen) | — |

- **✓ primary** = core harvestable/focus for that biome. **sparse** = present but not the main focus. **(some)** / **(optional)** = can be added for variety in later lists.
- Per-biome harvestable lists can be expanded in list 37+ (e.g. specific tree or rock variants). **Config:** `Content/Python/resource_nodes_per_biome.json` — keys are biome names (Desert, Forest, Marsh, Canyon); each entry lists `node_type`, `role`, and `variants` for PCG or placement scripts. **Placement:** `Content/Python/place_resource_nodes.py` reads this config and uses it when deciding which resource node types to place in a biome (optional `biome` in `demo_map_config.json`; default Forest). Code may reference `EBiomeType` from `HomeWorldPlanetoidTypes.h`.

### 1.2 Per-biome harvestable variants (list 38)

Concrete variant names/IDs per biome for PCG or placement scripts. Asset paths are placeholders until meshes/materials exist; code can resolve by type name or ID.

| Biome | Node type | Variant IDs / type names (placeholders) | Notes |
|-------|-----------|----------------------------------------|-------|
| **Desert** | Rocks | `sandstone_rock`, `iron_ore`, `desert_boulder` | Primary harvestable |
| **Desert** | Flowers/Herbs | `sparse_sage`, `desert_herb` | Sparse |
| **Desert** | Water | `oasis_well`, `desert_spring` | Oasis only |
| **Forest** | Trees | `oak_tree`, `pine_tree`, `birch_tree` | Primary |
| **Forest** | Flowers/Herbs | `wildflower`, `forest_herb`, `berry_bush` | Primary |
| **Forest** | Water | `river_water`, `forest_pond`, `stream` | Some |
| **Forest** | Rocks | `forest_stone`, `moss_rock` | Some |
| **Forest** | Spirits | `forest_spirit_node` | Optional |
| **Marsh** | Flowers/Herbs | `fen_herb`, `marsh_flower`, `bog_plant` | Primary |
| **Marsh** | Water | `fen_pool`, `bog_water`, `marsh_spring` | Primary |
| **Marsh** | Spirits | `fen_spirit_node`, `bog_spirit` | Primary (fen) |
| **Marsh** | Rocks | `marsh_stone` | Some |
| **Marsh** | Trees | `marsh_tree` | Optional |
| **Canyon** | Rocks | `canyon_rock`, `crystal_node`, `ore_vein` | Primary (incl. crystals) |
| **Canyon** | Flowers/Herbs | `canyon_herb`, `sparse_flower` | Sparse |

**Config:** The same variants are listed in `Content/Python/resource_nodes_per_biome.json` under a `variants` key per node entry so placement scripts can read them. See §1.1 for the config path and `EBiomeType` in `HomeWorldPlanetoidTypes.h`.

---

## 2. Biomes (initial four)

At the start we have **four biomes**. Each has a distinct **harvestable focus**, **monster type**, and **dungeon type**.

| Biome | Harvestable focus | Monster type (corrupted) | Dungeon type |
|-------|-------------------|---------------------------|--------------|
| **Desert** | Rocks, sparse herbs, water (oasis) | Desert-themed corrupted | Tomb / crypt |
| **Forest** | Trees, flowers/herbs, some water | Forest-themed corrupted | Ancient grove / dark wood |
| **Marsh** | Herbs, water, spirits (fen) | Marsh-themed corrupted | Swamp dungeon / bog shrine |
| **Canyon** | Rocks, crystals, sparse herbs | Canyon-themed corrupted | Mine / cavern |

Per-biome harvestable, monster, and dungeon lists can be expanded in later task lists (e.g. specific tree or rock variants per biome).

### 2.1 Monster types per biome (config)

Per-biome **corrupted** monster types (for spawn or AI) are defined in config so that placement scripts or spawn logic can look up which monster type IDs to use in each biome:

| Biome | Monster type (corrupted) | Config |
|-------|---------------------------|--------|
| Desert | Desert-themed corrupted | `Content/Python/planetoid_monsters.json` |
| Forest | Forest-themed corrupted | `Content/Python/planetoid_monsters.json` |
| Marsh | Marsh-themed corrupted | `Content/Python/planetoid_monsters.json` |
| Canyon | Canyon-themed corrupted | `Content/Python/planetoid_monsters.json` |

**Config:** `Content/Python/planetoid_monsters.json` — keys are biome names (Desert, Forest, Marsh, Canyon); each entry lists `monster_type_id`, `display_name`, and optional `notes` for future spawn or AI. Expand with additional rows per biome in later lists (e.g. elite or variant IDs).

### 2.2 Dungeon types per biome (config)

Per-biome **dungeon types** (for level/POI naming and placement) are defined in config so that placement scripts or level streaming can look up which dungeon type IDs to use in each biome:

| Biome | Dungeon type | Config |
|-------|--------------|--------|
| Desert | Tomb / crypt | `Content/Python/planetoid_dungeons.json` |
| Forest | Ancient grove / dark wood | `Content/Python/planetoid_dungeons.json` |
| Marsh | Swamp dungeon / bog shrine | `Content/Python/planetoid_dungeons.json` |
| Canyon | Mine / cavern | `Content/Python/planetoid_dungeons.json` |

**Config:** `Content/Python/planetoid_dungeons.json` — keys are biome names (Desert, Forest, Marsh, Canyon); each entry lists `dungeon_type_id`, `display_name`, and optional `notes` for level/POI naming and placement. **Placement:** `Content/Python/place_dungeon_entrance.py` loads this config when placing dungeon entrances; optional `biome` in `dungeon_map_config.json` selects the dungeon type for the current biome. Expand with additional dungeon variants per biome in later lists.

---

## 3. Alignment: corrupted, neutral, positive

Each biome can appear in **three alignments**. These define what the player does there:

| Alignment | Role | Player activity |
|-----------|------|------------------|
| **Corrupted** | **Fight** | Combat, conversion; strip sin, convert foes. Dangerous; where you fight. |
| **Neutral** | **Harvest** | Gather resources (trees, herbs, rocks, water); no combat focus. Safe to harvest. |
| **Positive** | **Empower** | Buffs, spirits, restoration; where you empower yourself (buffs, spirit nodes). |

- **Corrupted** = bad/corrupted version of the biome → combat and conversion.
- **Neutral** = neutral version → harvest and gather.
- **Positive** = positive/virtue-aligned version → empower (buffs, spirits, safety).

This gives 4 biomes × 3 alignments = **12 planetoid “flavours”** (e.g. Corrupted Forest, Neutral Desert, Positive Marsh). Implementation can start with one biome and one alignment and expand.

### 3.1 Alignment-based behavior (for code/config branching)

What happens in each alignment so code can branch on `GetCurrentZoneAlignment()` (see [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) for `hw.Planetoid.ZoneAlignment` and `hw.Planetoid.ZoneInfo`). **Pre-demo verification entry point:** For the step-by-step run sequence (§3) and all console commands in one place, use [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) — it links to [Vertical Slice Checklist §3](workflow/VERTICAL_SLICE_CHECKLIST.md) and lists every `hw.*` command.

| Alignment   | Spawn / combat | Harvest | Empower / conversion |
|-------------|----------------|---------|----------------------|
| **Corrupted** | Spawn corrupted monsters; combat; dangerous. | Disabled or minimal (zone is dangerous). | Conversion: strip sin, convert foes to loved version (vendors, helpers, quest givers). |
| **Neutral**   | No combat focus; safe. | Full harvest (trees, herbs, rocks, water per biome). | None. |
| **Positive**  | No hostile spawns; safe. | Optional / safe harvest. | Buffs, spirit nodes, restoration; empower self. |

**Config:** `Content/Python/planetoid_alignments.json` — keys are alignment names (Corrupted, Neutral, Positive); each entry has `spawn_rule`, `harvest_rule`, `empower_rule` (or equivalent) for placement scripts or C++/Blueprint branching. See `EPlanetoidAlignment` in `HomeWorldPlanetoidTypes.h`.

### 3.2 Alignment content summary (what content/systems per alignment)

Short at-a-glance summary for designers and list 39: which content or systems apply to each alignment.

| Alignment   | Content / systems that apply |
|-------------|------------------------------|
| **Corrupted** | Combat; conversion (strip sin, convert foes to loved version); corrupted monster spawns (per-biome from `planetoid_monsters.json`); dungeon entrances (per-biome from `planetoid_dungeons.json`). Harvest disabled or minimal. |
| **Neutral**   | Harvest only: trees, herbs, rocks, water per biome (from `resource_nodes_per_biome.json`). No combat focus; no empower systems. Safe gathering. |
| **Positive**  | Spirits, spirit nodes; buffs; restoration; optional safe harvest. No hostile spawns. Empowerment and virtue-aligned content. |

- **Corrupted** → fight, conversion, corrupted monsters, dungeons.
- **Neutral** → harvest-only content; no combat or empower.
- **Positive** → spirits, buffs, empowerment; safe.

### 3.3 How to test biome/alignment

- **Config (no PIE):** Run `Content/Python/test_biome_alignment_config.py` (e.g. via MCP `execute_python_script("test_biome_alignment_config.py")` or Tools → Execute Python Script). It loads `resource_nodes_per_biome.json` and `planetoid_alignments.json` and logs one entry per biome and per alignment to the Output Log.
- **PIE (zone alignment at runtime):** For step-by-step PIE test (run ZoneInfo, set alignment with optional arg, confirm GameMode state), see [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) § How to test zone alignment in PIE.

---

## 4. Per-biome summary (harvestable, monster, dungeon)

| Biome | Harvestable | Monster type | Dungeon type |
|-------|-------------|--------------|--------------|
| Desert | Rocks, herbs, water (oasis) | Desert corrupted | Tomb / crypt |
| Forest | Trees, flowers/herbs, water | Forest corrupted | Grove / dark wood |
| Marsh | Herbs, water, spirits | Marsh corrupted | Swamp / bog shrine |
| Canyon | Rocks, crystals, herbs | Canyon corrupted | Mine / cavern |

Each row is the **thematic identity** for that biome; alignment (corrupted/neutral/positive) then decides whether the zone is fight, harvest, or empower.

---

## 5. Task list linkage (4-list planetoid focus)

- **List 36:** Vision update, this doc (PLANETOID_BIOMES.md), VISION link, optional C++/config stub for biome and alignment.
- **List 37–39:** Resource nodes (trees, herbs, rocks, water, spirits) per biome; monster types per biome; dungeon types per biome; corrupted/neutral/positive implementation or content.

**Implementation stub (list 36):** C++ enums added in `Source/HomeWorld/HomeWorldPlanetoidTypes.h`: `EBiomeType` (Desert, Forest, Marsh, Canyon) and `EPlanetoidAlignment` (Corrupted, Neutral, Positive). Game code and later lists can include this header. Config or per-biome data (e.g. resource_nodes_per_biome) can be added in list 37.

**Alignment read at runtime (list 37):** `AHomeWorldGameMode` stores `CurrentZoneAlignment` (EPlanetoidAlignment) and `CurrentZoneBiome` (EBiomeType). Code and Blueprint can read them via `GetCurrentZoneAlignment()` and `GetCurrentZoneBiome()` for fight / harvest / empower branching. Set in PIE via **`hw.Planetoid.ZoneAlignment Corrupted|Neutral|Positive`**; log current state with **`hw.Planetoid.ZoneInfo`**. See [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md).

**See also:** [workflow/VISION.md](workflow/VISION.md), [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md), [docs/tasks/PLANETOID_HOMESTEAD.md](tasks/PLANETOID_HOMESTEAD.md).

### 5.1 4-list planetoid block complete (lists 36–39)

**Block complete.** The four task lists (36–39) delivered the planetoid design foundation. Future lists can start from "planetoid design done."

**Delivered:**

- **Biomes:** Four biomes (Desert, Forest, Marsh, Canyon) with C++ `EBiomeType` and config-driven harvestable, monster, and dungeon types.
- **Alignments:** Three alignments (Corrupted, Neutral, Positive) with C++ `EPlanetoidAlignment`; GameMode `GetCurrentZoneAlignment()` / `GetCurrentZoneBiome()`; console commands `hw.Planetoid.ZoneAlignment` and `hw.Planetoid.ZoneInfo`.
- **Configs:** `planetoid_alignments.json`, `resource_nodes_per_biome.json`, `planetoid_monsters.json`, `planetoid_dungeons.json` (Content/Python).
- **Placement wiring:** `place_resource_nodes.py` loads alignment config and branches (e.g. Corrupted skips harvest placement; Neutral/Positive place). `place_dungeon_entrance.py` loads dungeon config per biome.

**Suggested next steps:**

- **PIE on planetoid map:** Run DemoMap or planetoid level; use `hw.Planetoid.ZoneAlignment Corrupted|Neutral|Positive` and `hw.Planetoid.ZoneInfo` to confirm GameMode state (see [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md)).
- **Spawn by alignment:** Wire spawn logic or AI to alignment (e.g. spawn corrupted monsters only when alignment is Corrupted).
- **Content authoring:** Add harvestable variants, meshes, and per-biome assets; expand configs as needed.
