# HomeWorld – Planetoid Generation Design (Astroneer-Inspired)

Planetoid and procedural-generation philosophy for the 7 sin-themed levels. **Inspired by Astroneer’s** distinct planets, per-planet biomes and layers, and procedural-placement approach—**but we do not use deformable or voxel terrain**; terrain is static or baked (Landscape, PCG on surfaces, or pre-authored meshes).

---

## Principles

**1. One identity per planetoid**

- Treat each of the 7 levels as a **single planetoid identity** (Pride, Greed, Wrath, Envy, Gluttony, Lust, Sloth), with its own **biome set**, **palette**, and **proc-gen rules**.
- Do not reuse the same “planet type” across sin levels: each sin has its own modifiers and placement logic (similar to Astroneer’s per-planet models).

**2. Surface + optional layers**

- **Pride (first MVP planetoid):** Biome focus = **canyons, valleys, mountains, large spires**. Surface area TBD; use Astroneer-like (medium) scale as reference. See [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md) for vision and implementation research.
- **Surface:** Primary play area (PCG-on-Landscape or equivalent). Define at least one named surface biome per planetoid (e.g. Pride_Highlands, Greed_Mines).
- **Layers:** Optional subsurface/cave or “second layer” regions with different placement rules and density (e.g. Pride_Depths, Greed_Caverns). Can be separate PCG graphs or sublevels that stream in.

**3. Placement philosophy**

- **Radius / density:** Control how close or far props, foliage, and points of interest spawn (similar to Astroneer’s Radius and Max Projection Distance).
- **Orientation:** If planetoids remain flat (current World Partition + Landscape), “surface up” is world Z; if spherical planetoids are added later, adopt “align to planet up” so objects and PCG align to the local surface normal.
- **Per-planetoid graphs:** Each sin-themed level has its own PCG graph(s) or graph parameters (like Astroneer’s per-planet modifiers), rather than one global graph for all levels.

**4. Thematic consistency**

- **Palette and props:** Each planetoid has a distinct **soil/ground color**, **foliage set**, and **prop set** aligned with the sin/virtue theme. A curated set of materials and meshes per level, not a single shared set.
- **Difficulty / intensity:** Map “hardness” or danger to depth or biome (e.g. deeper layers = harder encounters) via encounter tables or GAS difficulty, not voxel hardness.

---

## Out of scope

- **Deformable / voxel terrain.** HomeWorld does not adopt Astroneer’s diggable, mutable terrain. No runtime voxel deformation.

---

## Post-MVP: Chunk/biome loading and progression (vision)

**Not MVP.** Per [workflow/VISION.md](workflow/VISION.md) § Campaign summary (Planetoid structure and progression):

- **Chunk shape and biomes:** A shape/method will be used to create **chunks that load as biomes**, so different sections of a planetoid can host different content (desert, forest, marsh, canyon, etc.) and stream or load independently.
- **Destroyable vs persistent:** **Only harvestables** (trees, rocks, flowers/herbs, etc.) are destroyable; all other world content is persistent.
- **Below ground = dungeon:** Anything **below ground** (subsurface) is a **portal to a dungeon map** — entering leads to a separate dungeon level.
- **Progression:** Conquering the planetoid and each biome **unlocks items**. Those items are used **at the spaceship (back home)** to **choose which biomes appear on the next planetoid**. This loop runs throughout the game.

Implementation of chunking, biome loading, and spaceship biome-selection is post-MVP.

---

## References

- **Campaign:** The 7 levels and their sin themes are defined in [workflow/VISION.md](workflow/VISION.md).
- **Pride (first MVP):** [PLANETOID_PRIDE_MVP.md](PLANETOID_PRIDE_MVP.md) — canyons, valleys, mountains, large spires; Astroneer-like scale; UE5 implementation approach.
- **Biomes and resources:** Four biomes, resource node types, and corrupted/neutral/positive alignment are in [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md).
- **Tech:** PCG and World Partition are in [STACK_PLAN.md](STACK_PLAN.md) (Layer 2 – World and Procedural Content).
- **Astroneer modding (Procedural Generation):** [astroneermodding.readthedocs.io](https://astroneermodding.readthedocs.io/en/latest/guides/proceduralGeneration.html) (Procedural Placement, Procedural Modifier, biome/layer metadata, per-planet models).
