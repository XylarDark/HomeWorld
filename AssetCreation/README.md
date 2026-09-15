# Asset creation — source assets and exports

All source asset work for HomeWorld lives here. Exports (FBX/GLB) go into `Exports/` by category; a batch import script in the project imports them into Unreal Content.

**Full workflow:** [docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md](../docs/Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md) (asset workflow, automation, batch import).

**External sources / licenses:** [docs/Assets/EXTERNAL_ASSET_MANIFEST.md](../docs/Assets/EXTERNAL_ASSET_MANIFEST.md) (free-tier ladder, bundle inventory). **Attribution for files in `Exports/`:** [Exports/ATTRIBUTION.md](Exports/ATTRIBUTION.md).

**Style:** [STYLE_GUIDE.md](STYLE_GUIDE.md) — clean cartoon, Super Mario Galaxy–like, lower rez, wholesome.

**MCP:** Official Blender Lab MCP (Blender 5.1+) + Unreal (unrealMCP) — see [docs/Setup/MCP_SETUP.md](../docs/Setup/MCP_SETUP.md) (Blender MCP section). Do not use PyPI `uvx blender-mcp` with the Lab addon.

---

## Cursor → Blender MCP → export → UE

1. **Blender running** with BlenderMCP addon → N-panel **Start MCP Server** (`localhost:9876`).
2. **Cursor** has `blender` + `unrealMCP` in `.cursor/mcp.json` (copy from `.cursor/mcp.json.example`).
3. **Create / clean** the mesh in Blender (via MCP or UI). Apply transforms.
4. **Export** with the STYLE_GUIDE preset to `Exports/<Category>/`:
   - Helper: [Blender/export_to_asset_creation.py](Blender/export_to_asset_creation.py) (`export_fbx(category=..., filename=...)`).
   - Categories: Characters, Harvestables, Homestead, Dungeon, Biomes.
5. **Import into UE** via MCP: `execute_python_script("batch_import_asset_creation.py")` (or Tools → Execute Python Script).
6. **Assign / place** meshes on Blueprints / config-driven place scripts as usual.

Only one blender-mcp client at a time (Cursor or Claude Desktop, not both).

---

## How to add a new asset

1. **Create or generate** — Use AI (Meshy/Tripo/StableGen) or model in Blender. Save sources in `AI_Sources/` or `Blender/` as needed.
2. **Clean up in Blender** — Apply transforms, optional decimate for lower rez, simple UVs. Export with the **Blender export preset** (see STYLE_GUIDE) to `Exports/<Category>/` (e.g. `Exports/Harvestables/tree_01.fbx`). Prefer `Blender/export_to_asset_creation.py` so settings stay consistent.
3. **Batch import into UE** — In Unreal Editor, run: `Tools → Execute Python Script` → `batch_import_asset_creation.py` (or run via MCP `execute_python_script("batch_import_asset_creation.py")`). The script reads `Exports/` and imports into `/Game/HomeWorld/...` by category.
4. **Assign and place** — In Editor, assign the new mesh to the right Blueprint (e.g. BP_HarvestableTree, BP_BuildOrder_Wall). Placement is config-driven via existing `place_*` scripts.

---

## Directory layout

| Path | Purpose |
|------|---------|
| `Exports/` | FBX/GLB ready for import. Subfolders: Characters, Harvestables, Homestead, Dungeon, Biomes. Batch import script reads from here. |
| `AI_Sources/` | Downloaded Meshy/Tripo outputs, or reference images used for AI (characters/, props/). |
| `RefImages/` | Style references, concept art (e.g. Super Mario Galaxy, wholesome look). |
| `Blender/` | Optional `.blend` files + [export_to_asset_creation.py](Blender/export_to_asset_creation.py). |

---

## Blender export preset (summary)

- **Forward:** X | **Up:** Z  
- **Apply Scaling:** FBX Unit Scale  
- **Apply Modifiers:** on  
- **Smoothing:** Face (not Normals)  
- **FBX version:** 2020.2  

Export destination: `AssetCreation/Exports/<Category>/`. See [STYLE_GUIDE.md](STYLE_GUIDE.md) for full preset and poly budgets.
