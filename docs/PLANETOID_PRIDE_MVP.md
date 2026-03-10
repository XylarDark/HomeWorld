# Pride planetoid (first MVP) — Vision and implementation research

**Purpose:** Define the **Pride** planetoid as the **first MVP planetoid**, with a **biome focus on canyons, valleys, mountains, and large spires**. Collect research on the best approach to implementing a map of this kind and on **Astroneer-like scale** for surface area (size TBD; start with Astroneer as reference).

**See also:** [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md), [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md), [workflow/VISION.md](workflow/VISION.md).

---

## 1. Vision update: Pride biome focus

**Pride** (first of the 7 sin-themed planetoids) is the **first MVP planetoid**. Its **biome focus** is:

- **Canyons** — Deep cuts, gorges, ravines; vertical relief and narrow passages.
- **Valleys** — Lower ground between heights; corridors and basins.
- **Mountains** — High elevation, peaks, ridges; large-scale vertical variation.
- **Large spires** — Tall, prominent rock formations; landmarks and vertical drama.

This gives Pride a **distinct identity**: vertical, dramatic terrain (canyons, valleys, mountains, spires) rather than flat plains or uniform forest. The existing **Canyon** biome in [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md) (rocks, crystals, sparse herbs; mine/cavern dungeon) aligns with this focus; Pride’s *overall* surface character is canyon–valley–mountain–spire, with sub-regions or named areas (e.g. Pride_Canyons, Pride_Valleys, Pride_Mountains, Pride_Spires) as needed.

**Surface area:** Not fixed yet. Use **Astroneer-like scale** as a starting reference (see §2). When locking size, consider play time to cross, density of POIs, and World Partition cell count.

**Map shape and biomes:** The planetoid **map shape is a sphere**; the **entire area** is **segmented into biomes** (desert, forest, marsh, canyon). Each biome has a harvest place, a couple of monster camps, one camp outside a dungeon, and a side quest giver. See [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md) and [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md).

**Homestead and glide:** The **homestead starts on a plateau at the top of a mountain**. The player can **glide down** from the plateau to the ground to explore the planetoid. This supports the MVP loop: complete day/night cycles while exploring the sphere, with a clear “home base” (plateau) and a fast way down (glide). Implementation: plateau as starting spawn/homestead location; glide ability (e.g. GAS or movement mode) to descend; return to plateau by travel/climb or fast travel as needed.

---

## 2. Astroneer: what they do (reference for scale and approach)

Research from Astroneer wikis, modding docs, and community:

### 2.1 Planet size and feel

- **No published dimensions in meters.** Planets are described as **Small**, **Medium**, or **Large** (e.g. Sylva = Medium; Desolo = moon/smaller). Community sites measure “walk around” or “sprint across” in **minutes** rather than meters.
- **Sylva (starting planet, “medium”):** Terran type; ~12 minute day/night cycle; “plains and forests,” “rocky mountains,” “long, deep ravines.” Fandom: “Much of the planet’s surface is covered by plains and forests … There are also rocky mountains with little vegetation. Long, deep ravines may also be found across the planet’s surface.”
- **Takeaway:** For “Astroneer-like size,” aim for a **medium** feel: traversable in a reasonable session, with distinct regions (valleys, mountains, ravines). Exact UE units or km² can be chosen later; start with a single Landscape or World Partition layout that feels “one medium planet” (order of magnitude: several minutes to cross on foot, not 100 km).

### 2.2 Tech (for reference only — we do not use voxels)

- **Voxel-based terrain:** Astroneer uses a voxel grid; terrain is deformable (dig/carve). HomeWorld uses **static or baked terrain** (Landscape, no runtime voxel deformation) per [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md).
- **Procedural placement:** Objects (resources, props) are placed via **Procedural Placement** + **Procedural Modifier**. Key params (from [Astroneer modding](https://astroneermodding.readthedocs.io/en/latest/guides/proceduralGeneration.html)):
  - **Radius:** e.g. 600 (spawn spacing / density).
  - **Max Projection Distance:** e.g. 1500 (max distance between placed objects).
  - **Orientation:** “Align to planet up” for spherical planets.
- **Biomes per planet:** Surface biomes are **named per planet type** (e.g. Valleys_Exotic, Mountains_Exotic, Hills_Exotic, Rolling_Exotic). So “valleys” and “mountains” are first-class biome names in Astroneer, which aligns with Pride’s focus (valleys, mountains, canyons, spires).
- **Layers:** Surface vs cave/crust layers; different placement rules per layer.

**Use for HomeWorld:** (1) **Scale** — target a “medium” planet feel (traversal time, density); (2) **Placement** — our PCG and scripts already use radius/density and per-biome logic; (3) **Biome names** — we can use Pride_Canyons, Pride_Valleys, Pride_Mountains, Pride_Spires as region or biome names.

### 2.3 Surface area (working assumption)

- No exact Astroneer radius/circumference in public docs. For implementation:
  - **Option A:** Start with a **single Landscape** of moderate size (e.g. 2 km × 2 km to 4 km × 4 km in UE; 4–16 km²). Test traversal and POI density; scale up with World Partition if needed.
  - **Option B:** Use **World Partition** from the start with a grid (e.g. 8×8 or 16×16 cells) and a total world size in the “medium” range (e.g. 4–16 km² total), then tune cell size and streaming.
- **Decision:** Defer exact dimensions; document “Pride surface area: Astroneer-like (medium); exact size TBD; see PLANETOID_PRIDE_MVP.md and STACK_PLAN for World Partition.”

---

## 3. Best approach: implementing canyons, valleys, mountains, spires (UE5)

### 3.1 Engine and tools (UE5)

- **Landscape:** UE’s **Landscape** is the primary terrain system. Non-voxel; heightmap-based; supports **Sculpt**, **Paint**, and **procedural tools**.
  - **Sculpt mode:** Raise/lower, smooth, flatten; brushes for hills, valleys, cliffs.
  - **Erosion tool:** Thermal erosion simulation; moves “soil” from high to low; good for **natural canyon/valley** shapes and weathered look. Use with **Noise** for variation.
  - **Noise tool:** Perlin (or similar) noise on heightmap; raise/lower; different scales for large vs small variation. Combines well with erosion for canyons and ridges.
  - **Landscape Splines / Blueprint Brushes:** For roads, rivers, or guided carving (e.g. spline-driven canyon paths).
- **World Partition:** For large worlds, **World Partition** streams cells by distance. Supports very large maps (docs and tutorials mention 100 km²+); HLOD and streaming distance are tunable. Pride can start as one Landscape or a WP grid; scale up when size is fixed.
- **Third-party / marketplace:** **Brushify** (Cliffs & Canyons), **TerraPrime** (PCG landscape, erosion, biomes) are cited for canyon/cliff and realistic terrain. Use for reference or assets if adopted; not required for first pass.

### 3.2 Terrain style (canyons, valleys, mountains, spires)

| Feature    | Approach |
|-----------|----------|
| **Canyons** | Heightmap: lower elevation along curves or splines; erosion tool to soften walls; noise for variation. Optionally **masked** material (rock on walls, floor material in bottom). PCG or manual meshes for cliff details. |
| **Valleys** | Lower areas between raised “mountain” masses; use heightmap sculpt + erosion so valleys read as corridors or basins. Valleys can be the “low” in a high-low noise pattern. |
| **Mountains** | Large-scale heightmap peaks and ridges; erosion on slopes; noise for ridges and secondary peaks. Multiple passes (broad raise, then erosion, then noise) often look better than one pass. |
| **Spires** | **Option A:** Heightmap “needles” (narrow, tall peaks) — possible but heightmap resolution may limit sharpness. **Option B:** **Static meshes** for spires (rock pillars) placed by PCG or hand; aligns with “large spires” as landmarks. **Option C:** Hybrid — broad peak in heightmap + mesh spire on top. |

### 3.3 Pipeline (recommended for Pride MVP)

1. **Define approximate size** — e.g. one Landscape 2–4 km a side, or World Partition grid with total area in that range; document in `planetoid_map_config.json` or a Pride-specific config.
2. **Blockout** — Sculpt large shapes: mountain masses, valley corridors, canyon cuts. Use erosion + noise to break up flatness and add realism.
3. **Spires** — Add as **static meshes** (or placeholders) in key locations; PCG or script for density; later replace with final art.
4. **Materials** — Paint or auto-material (height/slope based) so canyons and mountains read (e.g. rock on steep slopes, different material in valley floors).
5. **PCG** — Use existing **Planetoid_POI_PCG** and placement scripts; align with Pride biomes (Canyon-first; valleys/mountains/spires as regions or tags). Radius/density in line with Astroneer-style spacing (e.g. our existing `poi_points_per_squared_meter` and similar).
6. **Streaming** — If/when map grows, use World Partition; keep cell size and HLOD tuned for performance.

### 3.4 References (URLs)

- **UE Landscape:** [Landscape Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-overview) (5.0); [Landscape Outdoor Terrain](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-outdoor-terrain-in-unreal-engine) (5.7); [Landscape Sculpt Mode](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-sculpt-mode-in-unreal-engine) (5.7).
- **Erosion / noise:** UE docs reference **Landscape Erosion Tool** (thermal erosion) and **Landscape Noise Tool** (Perlin-style). Third-party guides (e.g. Toxigon) describe combining erosion + noise for realistic canyon/valley terrain.
- **World Partition / large worlds:** [Large worlds in UE5](https://www.unrealengine.com/en-US/blog/large-worlds-in-ue5-a-whole-new-open-world); community tutorials (e.g. 100 km² landscape, World Partition).
- **Astroneer:** [Procedural Generation (modding)](https://astroneermodding.readthedocs.io/en/latest/guides/proceduralGeneration.html); [Sylva (Fandom)](https://astroneer.fandom.com/wiki/Sylva); [Planets (Fandom)](https://astroneer.fandom.com/wiki/Planets). Voxel/planet tech: [round-planets (Voxel.Wiki)](https://voxel.wiki/wiki/round-planets).

---

## 4. Summary

| Item | Decision or reference |
|------|------------------------|
| **Pride** | First MVP planetoid; biome focus = **canyons, valleys, mountains, large spires**. |
| **Surface area** | Not fixed; start **Astroneer-like (medium)**; exact size TBD; consider 2–4 km a side or 4–16 km² total as a first implementation range. |
| **Astroneer** | Medium planet feel; procedural placement Radius/Max Projection; biomes like Valleys, Mountains; “long deep ravines,” “rocky mountains.” No voxels in HomeWorld. |
| **UE5 approach** | Landscape + Erosion + Noise for canyons/valleys/mountains; spires as meshes (or hybrid); World Partition when scaling up; PCG for POIs and density. |
| **Config** | Pride-specific map/terrain config can extend `planetoid_map_config.json` or add `pride_planetoid_config.json` when dimensions and regions are locked. |

---

## 5. Task linkage

- **Vision:** Pride = first MVP planetoid; canyons, valleys, mountains, large spires. Reflected in [workflow/VISION.md](workflow/VISION.md) and [PLANETOID_DESIGN.md](PLANETOID_DESIGN.md).
- **Biomes:** [PLANETOID_BIOMES.md](PLANETOID_BIOMES.md) Canyon biome and variants (rocks, crystals) fit Pride; add Pride-specific **region** or **terrain** names (Pride_Canyons, Pride_Valleys, Pride_Mountains, Pride_Spires) when implementing.
- **Implementation:** When building Pride’s level: use this doc for terrain pipeline and scale; update `planetoid_map_config.json` or add Pride config; ensure PCG and scripts respect Pride biome focus.
