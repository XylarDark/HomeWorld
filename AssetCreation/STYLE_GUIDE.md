# HomeWorld — export preset

**Look law lives in one place:** [Docs/02_ART_BIBLE.md](../Docs/02_ART_BIBLE.md) (updated 2026-09-30).

Do not restate style here. The old “Super Mario Galaxy rounded / no sharp forms” pillar is retired. Current law is semi-polygon facets with detail on top, Zelda/Pixar face, one living eye per important object.

This file only keeps the Blender → UE export preset.

---

## Poly budgets (guideline)

| Asset type | Triangle target | Notes |
|---|---|---|
| Player body | 800–2,500 | Face may go higher. Coat stays cheap. |
| Enemy / beast body | 8k–25k faceted | Eyes and brows are the hero. |
| Cabin / shrine structure | 2k–8k | Detail kit is separate. |
| Kit piece (fence, stone, sprig) | 40–300 | Instance. One hero stalk per bed. |
| Bug / moth | 80–200 | Cull at distance. |

---

## Blender export preset (UE5)

| Setting | Value |
|---|---|
| Forward | X |
| Up | Z |
| Apply Scaling | FBX Unit Scale |
| Apply Modifiers | On |
| Smoothing | Face, custom normals preserved |
| Triangulate Faces | Off |
| FBX version | 2020.2 |

Before export: apply transforms. Origin at ground contact. Mark sharp facet edges and freeze custom normals so UE import does not rebuild them.

Import in UE with normals and tangents. Do not let the engine soften facets.

Export destination: `AssetCreation/Exports/<Category>/` — Characters, Harvestables, Homestead, Dungeon, Biomes.

Scripted export: [Blender/export_to_asset_creation.py](Blender/export_to_asset_creation.py).
