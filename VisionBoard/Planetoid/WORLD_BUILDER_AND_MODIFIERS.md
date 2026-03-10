# World builder and planetoid modifiers (plan and config schema)

**Purpose:** Define the **world-builder** plan (config-driven assembly + Editor crafting) and the **planetoid modifier** config schema so that (1) we can generate planetoids programmatically from config, and (2) player choices at the spaceship (post-MVP) can drive "next planetoid" via the same schema. See [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md) for the full checklist and in-editor vs automated work.

---

## 1. World builder (dev tool)

**Goal:** One config (or preset) drives level create, portal, PCG, and placement; you then open the level and craft terrain and key locations in Editor.

**Current entry point:** Run **`Content/Python/assemble_planetoid_from_config.py`** with Editor open. It runs: ensure_demo_portal → setup_planetoid_pcg. Manual follow-up: Get Landscape Data By Tag, Actor Spawner Template, terrain (Pride: canyons/valleys/mountains/spires), homestead plateau.

**Planned extension (config schema below):** A **world_builder_config.json** (or extended planetoid_map_config) with:

- `planetoid_id` — e.g. Pride, Greed.
- `terrain_preset` — e.g. Pride (canyons/valleys/mountains/spires); references documented manual steps or future terrain pipeline.
- `biomes` — list of biome IDs enabled on this planetoid (Desert, Forest, Marsh, Canyon).
- `per_biome` — optional overrides per biome: harvest_place, monster_camps (count), dungeon_camp, side_quest_giver (boolean or count).
- `bounds`, `poi_density` — already in planetoid_map_config (volume_extent, poi_points_per_squared_meter).

Scripts (existing + future) read this and run in order; same pipeline can be used for "next planetoid" when the player has chosen modifiers at the spaceship.

---

## 2. Planetoid modifiers (player customization — post-MVP)

**Vision:** Conquering a planetoid/biome unlocks items; at the **spaceship** the player uses them to **choose which biomes appear on the next planetoid**. So the same config that drives our world builder should be writable (or selectable) from player choices.

**Schema (for future implementation):**

```json
{
  "enabled_biomes": ["Forest", "Canyon"],
  "seed": 12345,
  "terrain_preset": "Pride",
  "per_biome_overrides": {
    "Forest": { "harvest": true, "camps": 2, "dungeon": true, "quest_giver": true },
    "Canyon": { "harvest": true, "camps": 2, "dungeon": true, "quest_giver": true }
  }
}
```

- **enabled_biomes** — Biomes that appear on the next planetoid (player selection at spaceship).
- **seed** — Optional; for reproducible layout when generating from modifiers.
- **terrain_preset** — Which sin/theme (Pride, Greed, …); determines terrain style and palette.
- **per_biome_overrides** — Per-biome toggles/counts (harvest place, monster camps, dungeon camp, side quest giver). Defaults from [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md) § Per-biome structure; overrides allow tuning or unlocking.

**Use:** Dev: edit config and run assemble (or future "generate from modifiers" script). Game (post-MVP): spaceship UI sets enabled_biomes (and optionally seed/preset); next planetoid load uses this as input to assembly/generation.

---

## 3. Tools that serve both dev and game

| Tool | Dev | Game / player |
|------|-----|----------------|
| Biome set in config | Iterate planetoid content | Player picks biomes for next planetoid |
| Seed / modifier | Reproducible tests | Themed or difficulty-driven layout |
| Per-biome toggles | Tune content per biome | Unlocks (e.g. "Forest harvest unlocked") |
| World-builder preset | Pride, Greed, etc. | Themed planetoid (sin theme) |
| Orchestrator script | assemble_planetoid_from_config.py | Future: runtime or dedicated "planetoid gen" uses same schema |

---

## 4. References

- [PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md](PLANETOID_TO_REALITY_AND_WORLD_BUILDER.md) — Checklist, in-editor work, orchestrator, world-builder plan.
- [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md) — Map shape, per-biome structure, post-MVP chunk/biome and spaceship biome selection.
- [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md) — Four biomes, resource nodes, alignments.
- [VISION.md](workflow/VISION.md) — Planetoid structure and progression (biome-selection unlock loop).
