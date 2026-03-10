# Asset creation — source assets and exports

All source asset work for HomeWorld lives here. Exports (FBX/GLB) go into `Exports/` by category; a batch import script in the project imports them into Unreal Content.

**Full workflow:** [docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md](../docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md) (asset workflow, automation, batch import).

**Style:** [STYLE_GUIDE.md](STYLE_GUIDE.md) — clean cartoon, Super Mario Galaxy–like, lower rez, wholesome.

---

## How to add a new asset

1. **Create or generate** — Use AI (Meshy/Tripo/StableGen) or model in Blender. Save sources in `AI_Sources/` or `Blender/` as needed.
2. **Clean up in Blender** — Apply transforms, optional decimate for lower rez, simple UVs. Export with the **Blender export preset** (see STYLE_GUIDE) to `Exports/<Category>/` (e.g. `Exports/Harvestables/tree_01.fbx`).
3. **Batch import into UE** — In Unreal Editor, run: `Tools → Execute Python Script` → `batch_import_asset_creation.py` (or run via MCP `execute_python_script("batch_import_asset_creation.py")`). The script reads `Exports/` and imports into `/Game/HomeWorld/...` by category.
4. **Assign and place** — In Editor, assign the new mesh to the right Blueprint (e.g. BP_HarvestableTree, BP_BuildOrder_Wall). Placement is config-driven via existing `place_*` scripts.

---

## Directory layout

| Path | Purpose |
|------|---------|
| `Exports/` | FBX/GLB ready for import. Subfolders: Characters, Harvestables, Homestead, Dungeon, Biomes. Batch import script reads from here. |
| `AI_Sources/` | Downloaded Meshy/Tripo outputs, or reference images used for AI (characters/, props/). |
| `RefImages/` | Style references, concept art (e.g. Super Mario Galaxy, wholesome look). |
| `Blender/` | Optional: .blend project files (can be gitignored if large). |

---

## Blender export preset (summary)

- **Forward:** X | **Up:** Z  
- **Apply Scaling:** FBX Unit Scale  
- **Apply Modifiers:** on  
- **Smoothing:** Face (not Normals)  
- **FBX version:** 2020.2  

Export destination: `AssetCreation/Exports/<Category>/`. See [STYLE_GUIDE.md](STYLE_GUIDE.md) for full preset and poly budgets.
