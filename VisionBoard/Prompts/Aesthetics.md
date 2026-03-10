# Aesthetics — Vision Board

Use this when generating concept art, style references, or prompts for a clean cartoon, wholesome look. Source: [AssetCreation/STYLE_GUIDE.md](../AssetCreation/STYLE_GUIDE.md), [Core/VISION.md](../Core/VISION.md), project art direction.

---

## Style pillars

- **Super Mario Galaxy–like:** Low-poly, soft shapes, readable silhouettes, bright but not garish colors. Simple materials (minimal PBR roughness/metallic complexity). Charming and readable at distance.
- **Lower rez:** Low–mid poly counts for fast iteration and performance. See poly budgets below.
- **Wholesome:** Rounded forms, friendly proportions. Avoid sharp or dark. Palette and lighting should feel safe and inviting.

---

## Poly budgets (guideline)

| Asset type | Triangle target | Notes |
|------------|-----------------|-------|
| **Key character** | 2K–15K | Default character; keep readable at mid distance. |
| **Props (harvestables, furniture)** | 500–3K | Trees, rocks, crates, chairs. |
| **Environment kit pieces** | 500–2K | Walls, pillars, doors for homestead/dungeon. |
| **Small pickups / foliage** | 200–1K | Flowers, herbs, small rocks. |

---

## Do's and don'ts

- **Do:** Soft edges, clear silhouettes, limited palette per biome/set. One material per mesh type for simplicity.
- **Don't:** Overly realistic textures, heavy normal detail, or dark/gritty tones for MVP. Avoid non-manifold geometry and n-gons when possible.

---

## Reference images

Store style references and concept art in **AssetCreation/RefImages/** (e.g. Super Mario Galaxy screens, wholesome character/prop refs). Keep filenames descriptive so prompts and mood stay consistent.

---

## Theme alignment

- **"Love as Epic Quest"** — Dopamine from intense combat + Oxytocin from nurturing bonds. Visual tone should support both: exciting but not grim; nurturing and safe.
- **Roles:** Casual (healer/home) and hardcore (protector). Art should read clearly for both: home/family spaces feel cozy; combat/spirit spaces feel dynamic but not hostile.

---

## Ability visuals (MVP)

Ability **gameplay** is in GAS (C++/Blueprint). **Art** for abilities (VFX, icons, animations) is a later pass. For MVP use placeholder cubes or simple Niagara/curves; document specific ability visuals when you add them.
