# Industry-standard approaches for MVP: game world, 2D→character, characters/monsters

**Purpose:** This document summarizes industry-standard approaches only as far as they inform **HomeWorld's Act 1 MVP**: one homestead corner, one playable loop (tutorial day/night), one moment (e.g. claim homestead), and good-looking marketing material. Each section ends with explicit **"For MVP we commit to…"** decisions tied to existing systems and docs.

**Audience:** Designers, level authors, and developers deciding how to scope world building, character generation (including 2D→3D), and the character/monster cast for the vertical slice.

**How to use:** Read the three pillars for context; when making scope or implementation decisions, use the **"For MVP we commit to:"** sections at the end of each pillar as the single reference for what we build now versus what we defer.

**Related docs:**

- **Vision and scope:** [VisionBoard/Core/VISION.md](../../VisionBoard/Core/VISION.md), [VisionBoard/MVP/MVP_TUTORIAL_PLAN.md](../../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md), [VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md)
- **Gap analysis:** [MVP_GAP_ANALYSIS_VISION.md](../MVP_GAP_ANALYSIS_VISION.md)

---

## 1. Purpose and scope

**Act 1 MVP** means: one playable loop (explore → fight → build; tutorial day/night), **one moment** (e.g. claiming the homestead after the first boss), and **one beautiful corner** (e.g. homestead compound) polished for screenshots and a short demo. **Assets and visuals are mandatory** so we can produce marketing material; the asset pipeline and a small, intentional cast of characters and monsters are required, not optional.

This doc does three things:

1. **Pillar 1 — Game world:** How studios typically build a vertical-slice world (blockout → art → polish; small open area vs. full open world; PCG to support a hero area). We map that to DemoMap, Homestead, and ForestIsland_PCG.
2. **Pillar 2 — Character generation from 2D image:** How 2D→3D and UGC/avatar pipelines work; where HomeWorld's Milady pipeline fits and what we defer for MVP.
3. **Pillar 3 — Characters and monsters:** How studios scope a tiny but shippable cast (player, family, enemies, boss) and minimal animation/VFX for a first slice.

Each pillar ends with **"For MVP we commit to:"** so the team has a single reference for what we are building now versus what we defer.

---

## 2. Pillar 1: Game world for MVP

### 2.1 Industry-standard summary

**Vertical-slice world pipeline:** Studios typically build one strong area for a vertical slice: **blockout → greybox → art pass → polish**. The goal is one framed "hero shot" and one clear gameplay path, not full world production. Modular kits (walls, props, foliage) speed iteration; level designers own layout and flow, art owns final look.

**Small open area vs. full open world:** For a first slice, many teams use a **single map** (World Partition or not) with a **clearly bounded play area** — e.g. one valley, one compound, one biome — rather than a full open world. Streaming and HLODs matter when the world grows; for MVP, one well-framed level or region is enough. The "beautiful corner" is chosen in advance and lit and dressed to read well in screenshots.

**Procedural placement:** PCG (Unreal's PCG, Houdini, or similar) is used to **support** the hero area: forests, rocks, foliage, resource pockets. Density, radius, and surface alignment (e.g. "align to landscape normal") are tuned so the result looks intentional. The hero area itself (homestead compound, key path) is usually **hand-placed**; PCG fills the surrounding context. Per-level or per-biome graphs keep identity clear (e.g. one graph per planetoid in Astroneer-style designs).

**One identity per level:** Treat the slice as **one identity** — one biome feel, one palette, one prop set — so the slice reads as a single place. Expanding to multiple biomes or planetoids comes after the first slice ships.

### 2.2 HomeWorld alignment

- **Primary world:** [DemoMap](/Game/HomeWorld/Maps/DemoMap) and Homestead are the main playable spaces. DemoMap is the primary demo/playable map for MVP.
- **PCG:** [ForestIsland_PCG](../../Content/HomeWorld/PCG/ForestIsland_PCG.uasset) and scripts (`create_demo_from_scratch.py`, `create_pcg_forest.py`) set up volume, graph, and surface sampling. Mesh list and Get Landscape Data (e.g. by tag) often require one-time manual setup; see [PCG/PCG_SETUP.md](../PCG/PCG_SETUP.md), [PCG/PCG_BEST_PRACTICES.md](../PCG/PCG_BEST_PRACTICES.md), [PCG/PCG_VARIABLES_NO_ACCESS.md](../PCG/PCG_VARIABLES_NO_ACCESS.md).
- **Planetoid design:** [VisionBoard/Planetoid/PLANETOID_DESIGN.md](../../VisionBoard/Planetoid/PLANETOID_DESIGN.md) and [PLANETOID_BIOMES.md](../../VisionBoard/Planetoid/PLANETOID_BIOMES.md) define the 7 sin-themed levels and four biomes (desert, forest, marsh, canyon). For MVP we scope to **one primary world** (DemoMap/Homestead); the first Pride planetoid slice is optional and can follow later.

### 2.3 For MVP we commit to

- **One framed homestead compound** as the "beautiful corner" — placed buildings (or placeholders), resource nodes, and PCG so one shot is screenshot-ready (lighting, no holes, no floating meshes). Default corner per [VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md) §2: Homestead compound.
- **A PCG forest ring / surroundings** that feel deliberate (trees, rocks, harvestables) via ForestIsland_PCG and locked mesh list/landscape tag; hand-polish the compound itself.
- **Optional:** One small Pride planetoid slice later (portal from DemoMap → Pride with one biome/POI). Act 1 MVP does **not** depend on it; we can ship the slice on DemoMap/Homestead only.

---

## 3. Pillar 2: Character generation from 2D image (Milady)

### 3.1 Industry-standard summary

**Image-to-3D tools:** Pipelines like **Meshy**, **Tripo**, **TripoSR**, **Luma** take a single 2D image (or multi-view) and produce a 3D model (GLB, VRM, FBX). Quality and speed vary; typical use is **manual upload → download GLB → import in-engine** for prototype, and **API + plugin** for automated UGC/avatar flows. Single-image input is common; multi-view improves fidelity when available.

**Import and rigging in UE:** GLB/VRM are imported via plugins (e.g. **VRM4U**); auto-rig and retargeting map the result to the project skeleton (Mannequin or custom). Scale and LOD (e.g. chibi 0.1x) are set at import or in a post step. One target skeleton keeps animation and gameplay logic simple.

**UGC / avatar pipelines:** Games that allow "player-supplied" or custom characters usually: (1) validate format and poly count, (2) run content moderation, (3) map to one or few skeletons for animation, (4) separate **editor-time** (curation, import) from **runtime** (load, display). Full automation (wallet → verify → fetch art → convert → spawn) is a larger integration; many teams ship a **manual prototype path** first (upload image → external tool → download → import) and automate later.

**NFT/collectible-to-game:** Wallet connect → verify ownership → resolve metadata (e.g. tokenURI) → fetch image (e.g. from IPFS) → pass to image-to-3D → import. This is the path described in HomeWorld's Milady roadmap; industry practice is to defer full automation until the rest of the slice is stable and to use a manual or semi-manual path for the first demo.

### 3.2 HomeWorld alignment

- **Milady pipeline:** [docs/TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) — wallet connect, NFT verification, fetch PNG from IPFS, Meshy (or Tripo) image-to-3D, VRM4U import, retargeting, chibi scale.
- **Asset workflow and image-to-3D:** [Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md](../Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 — tools (Meshy, Tripo, Luma), deferred full pipeline, manual path (PNG → Meshy/Tripo → GLB → VRM4U), and "when resuming" steps.
- **Content paths:** `/Game/HomeWorld/Milady/` for imported meshes, materials, animations, Blueprints; [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md). Batch import and ensure scripts: `ensure_milady_folders.py`, `batch_import_asset_creation.py`.

### 3.3 For MVP we commit to

- **Static stylized characters only** for MVP — player, partner, child, and NPCs use project content that fits [AssetCreation/STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md) (clean cartoon, SMG-like, poly budgets). No dependency on Milady auto-import for the slice to ship.
- **Milady auto-import (wallet → NFT → image→3D) is post-MVP.** When we resume, follow [MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) and [ASSET_WORKFLOW_AND_STEAM_DEMO.md](ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 "When resuming the image-to-3D pipeline."
- **Optional:** One **manual** Milady prototype (export PNG → upload to Meshy/Tripo → download GLB → VRM4U import) is allowed if it does not block core MVP work; use as reference or placeholder only.

---

## 4. Pillar 3: Characters and monsters for MVP

### 4.1 Industry-standard summary

**Character/creature pipeline:** Standard pipeline is **concept → sculpt (e.g. ZBrush) → retopo → UV → rig (full or semi-auto) → animate → LOD**. For a vertical slice, studios ship a **small cast** with clear silhouettes and a **minimal but focused animation set**: idle, walk/run, attack, hit-react, death (or equivalent, e.g. "convert"). Poly budgets and LOD counts are set per platform; stylized games use lower counts and simpler materials.

**Stylized MVP constraints:** Low–mid poly (e.g. key character 2K–15K triangles, props 500–3K) and one material per mesh type keep iteration fast and performance predictable. Readability at mid distance and a consistent art direction (e.g. Super Mario Galaxy–like, wholesome) matter more than realistic detail.

**Enemy design for a first slice:** Teams typically ship **one or two enemy archetypes** (e.g. melee, ranged) and **one boss** that anchor the core loop (e.g. "scout → fight → claim home"). Behavior is simple (behavior trees, State Tree, or scripted sequences); the goal is clear feedback (attack, hit, defeat/convert) and one memorable boss moment. Placeholder art is acceptable if the read is clear.

**NPC pipeline:** Partner and child reuse the same character pipeline (same or shared skeleton, different meshes/materials). Variation is achieved via mesh swaps and materials rather than bespoke systems. In-world triggers (e.g. meal triggers, love task, game with child) are placed and tagged so the tutorial loop can be completed.

**Integration with combat/abilities:** Character and enemy meshes plug into the ability system (e.g. GAS): ability montages, VFX hooks, and death/convert moments are driven by the same skeleton or retargeted animations. One skeleton (or few) plus retargeting keeps the scope manageable.

### 4.2 HomeWorld alignment

- **Style and poly budgets:** [AssetCreation/STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md) — key character 2K–15K, props 500–3K, environment kit 500–2K, small pickups/foliage 200–1K; clean cartoon, wholesome.
- **Character and abilities:** `BP_HomeWorldCharacter`, GAS abilities (PrimaryAttack, Dodge, Interact, Place, etc.), family/NPCs, night encounter and boss stubs. Conversion (strip sin → loved) and HUD (Converted count) are in place; see [VISION.md](../../VisionBoard/Core/VISION.md) and [MVP_GAP_ANALYSIS_VISION.md](../MVP_GAP_ANALYSIS_VISION.md).
- **Tutorial loop:** [MVP_TUTORIAL_PLAN.md](../../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md) — 13-step loop (wake → meals → love task → game with child → gather → bed → spectral → combat → boss → wake to family taken). Partner and child must exist in level with correct tags; in-world triggers for meals, love task, game with child (e.g. BP_MealTrigger_*, interact with Partner/Child).

### 4.3 For MVP we commit to

- **Playable cast:**  
  - **1 player character** matching STYLE_GUIDE (readable silhouette, movement and abilities working).  
  - **1 partner + 1 child** with clear read (silhouettes, tags) for love task and game-with-child beats; placed in DemoMap (or tutorial level) with in-world triggers.
- **Monsters:**  
  - **1–2 basic enemies** that support scout/combat beats (melee or simple AI).  
  - **1 boss** that anchors "claim homestead" and/or night climax; placeholder art OK if readable.
- **Animation / VFX minimum:**  
  - For each combatant: **idle**, **walk/run**, **attack**, **hit-react**, **death/convert**.  
  - Simple VFX/audio hooks for attack and conversion so the moment reads clearly.  
  - Existing GAS and conversion HUD (Converted count, etc.) stay; add or tune only what is needed for the slice.

---

## 5. References and citations

- **Epic / Unreal:** UE 5.7 documentation (World Partition, PCG, Animation Rigging, retargeting). Prefer official Epic docs and project docs ([PCG/PCG_SETUP.md](../PCG/PCG_SETUP.md), [PCG/PCG_BEST_PRACTICES.md](../PCG/PCG_BEST_PRACTICES.md), [UE/UE57_TECH.md](../UE/UE57_TECH.md)).
- **Project docs:** [VISION.md](../../VisionBoard/Core/VISION.md), [MVP_TUTORIAL_PLAN.md](../../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md), [VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md), [MVP/MVP_GAP_ANALYSIS_VISION.md](../MVP/MVP_GAP_ANALYSIS_VISION.md), [PLANETOID_DESIGN.md](../../VisionBoard/Planetoid/PLANETOID_DESIGN.md), [MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md), [Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md](../Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md), [STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md).
- **External research:** When industry-standard research is added from Parallel or other sources, add a short "Parallel research (user-provided)" or citation note here with date and topic.

**Maintenance:** This doc is a snapshot. When the engine version, tools, or MVP scope change, refresh the relevant pillar and note the date at the top of the updated section.
