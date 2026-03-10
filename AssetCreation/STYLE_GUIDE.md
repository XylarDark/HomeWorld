# HomeWorld — Art direction and style guide

**Target:** Clean cartoon, similar to Super Mario Galaxy but lower resolution; wholesome feel.

---

## 1. Style pillars

- **Super Mario Galaxy–like:** Low-poly, soft shapes, readable silhouettes, bright but not garish colors. Simple materials (minimal PBR roughness/metallic complexity). Charming and readable at distance.
- **Lower rez:** Low–mid poly counts for fast iteration and performance. See poly budgets below.
- **Wholesome:** Rounded forms, friendly proportions. Avoid sharp or dark. Palette and lighting should feel safe and inviting.

---

## 2. Poly budgets (guideline)

| Asset type | Triangle target | Notes |
|------------|-----------------|-------|
| **Key character** | 2K–15K | Default character; keep readable at mid distance. |
| **Props (harvestables, furniture)** | 500–3K | Trees, rocks, crates, chairs. |
| **Environment kit pieces** | 500–2K | Walls, pillars, doors for homestead/dungeon. |
| **Small pickups / foliage** | 200–1K | Flowers, herbs, small rocks. |

Use Blender’s Decimate modifier or manual retopology if AI-generated meshes are too heavy.

---

## 3. Do’s and don’ts

- **Do:** Soft edges, clear silhouettes, limited palette per biome/set. One material per mesh type for simplicity.
- **Don’t:** Overly realistic textures, heavy normal detail, or dark/gritty tones for MVP. Avoid non-manifold geometry and n-gons when possible.

---

## 4. Reference images

Store style references and concept art in **RefImages/** (e.g. Super Mario Galaxy screens, wholesome character/prop refs). Keep filenames descriptive so prompts and mood stay consistent.

---

## 5. Blender export preset (UE5)

Use this preset for every FBX/GLB export so the batch import script and UE behave consistently.

| Setting | Value |
|---------|--------|
| **Forward** | X |
| **Up** | Z |
| **Apply Scaling** | FBX Unit Scale |
| **Apply Modifiers** | On |
| **Smoothing** | Face (not Normals) |
| **Triangulate Faces** | Off (preserve custom normals if needed) |
| **FBX version** | 2020.2 |
| **Include** | Visible Objects (or Selected Objects if you prefer) |

**Before export:** In Blender, apply all transforms (`Ctrl+A` → All Transforms). Set object origin to center of mass; snap geometry to world origin for alignment.

**Export destination:** `AssetCreation/Exports/<Category>/` where `<Category>` is one of: Characters, Harvestables, Homestead, Dungeon, Biomes.

Reference: [Blender–UE5 workflow](https://srogers4.github.io/blender-ue5-workflow/blender/export_settings/).

---

## 6. Ability visuals (MVP)

Ability **gameplay** is in GAS (C++/Blueprint). **Art** for abilities (VFX, icons, animations) is a later pass. For MVP use placeholder cubes or simple Niagara/curves; document specific ability visuals when you add them.
