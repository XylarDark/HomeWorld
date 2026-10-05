# Asset creation — source assets and exports

All source asset work for HomeWorld lives here. Exports (FBX/GLB) go into `Exports/` by category; a batch import script in the project imports them into Unreal Content.

**Full workflow:** [docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md](../docs/Assets/ASSET_WORKFLOW_AND_STEAM_DEMO.md) (asset workflow, automation, batch import).

**External sources / licenses:** [docs/Assets/EXTERNAL_ASSET_MANIFEST.md](../docs/Assets/EXTERNAL_ASSET_MANIFEST.md) (free-tier ladder, bundle inventory). **Attribution for files in `Exports/`:** [Exports/ATTRIBUTION.md](Exports/ATTRIBUTION.md).

**Style:** [STYLE_GUIDE.md](STYLE_GUIDE.md) — clean cartoon, Super Mario Galaxy–like, lower rez, wholesome.

**MCP:** Official Blender Lab MCP served by **Mixar** + Unreal (unrealMCP) — see [docs/Setup/MCP_SETUP.md](../docs/Setup/MCP_SETUP.md) (Mixar MCP section). Do not use PyPI `uvx blender-mcp` with the Lab addon.

---

## Cursor → Mixar MCP → export → UE

1. **Mixar running** as the MCP server: `.\Tools\Start-MixarMcp.ps1` (headless, blocks until `localhost:9876` is reachable).
2. **Cursor** has `mixar` + `unrealMCP` in `.cursor/mcp.json` (copy from `.cursor/mcp.json.example`).
3. **Create / clean** the mesh in Mixar (via MCP or UI). Apply transforms.
4. **Export** with the STYLE_GUIDE preset to `Exports/<Category>/`:
   - Helper: [Blender/export_to_asset_creation.py](Blender/export_to_asset_creation.py) (`export_fbx(category=..., filename=...)`).
   - Categories: Characters, Harvestables, Homestead, Dungeon, Biomes.
5. **Import into UE** via MCP: `execute_python_script("batch_import_asset_creation.py")` (or Tools → Execute Python Script).
6. **Assign / place** meshes on Blueprints / config-driven place scripts as usual.

Only one blender-mcp client at a time (Cursor or Claude Desktop, not both).

---

## How to add a new asset

1. **Create or generate** — Use AI (Meshy/Tripo/Mixar) or model in Mixar. Save sources in `AI_Sources/` or `Blender/` as needed.
2. **Clean up in Mixar** — Apply transforms, optional decimate for lower rez, simple UVs. Export with the **Mixar export preset** (see STYLE_GUIDE) to `Exports/<Category>/` (e.g. `Exports/Harvestables/tree_01.fbx`). Prefer `Blender/export_to_asset_creation.py` so settings stay consistent — it is a plain `bpy` script and works in Mixar unchanged.
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

## Mixar export preset (summary)

- **Forward:** X | **Up:** Z  
- **Apply Scaling:** FBX Unit Scale  
- **Apply Modifiers:** on  
- **Smoothing:** Face (not Normals)  
- **FBX version:** 2020.2  

Export destination: `AssetCreation/Exports/<Category>/`. See [STYLE_GUIDE.md](STYLE_GUIDE.md) for full preset and poly budgets.
