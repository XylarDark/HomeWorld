# External asset manifest (MVP and test environment)

**When to use this:** Whenever you add meshes, textures, or animations from the web (Megascans, Kenney, Mixamo, OpenGameArt, etc.). Append a row to the **Bundle inventory** table and keep `AssetCreation/Exports/ATTRIBUTION.md` updated for anything that requires attribution (for example CC-BY).

**Related:** [ASSET_WORKFLOW_AND_STEAM_DEMO.md](ASSET_WORKFLOW_AND_STEAM_DEMO.md), [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md), [AssetCreation/README.md](../../AssetCreation/README.md), [AssetCreation/STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md).

---

## Two tracks (same `/Game/HomeWorld/` layout)

| Track | Goal | What “good” means |
|--------|------|-------------------|
| **Automation / CI** | PIE checks, agents, regression (`pie_test_runner.py`, level scripts) | Deterministic levels, stable asset paths, predictable static mesh counts where tested; small payloads; avoid flaky World Partition unload during tests. |
| **MVP / marketing** | DemoMap homestead + PCG ring, tutorial loop, screenshots | [STYLE_GUIDE.md](../../AssetCreation/STYLE_GUIDE.md) budgets, one visual identity per level, hero framing per [VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md](../../VisionBoard/MVP/VERTICAL_SLICE_CHECKLIST.md). |

Both tracks use the same content roots in [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md). Test track may use primitive Engine shapes or tiny probe meshes; MVP track swaps in stylized or Megascans content without changing the wiring model (`pcg_forest_config.json`, `demo_map_config.json`, Blueprint defaults).

---

## Free-tier ladder (common internet sources)

Use this order when you want **no paid packs** first. Always record each bundle in the inventory table.

| Tier | Source | Typical use | Integration |
|------|--------|---------------|---------------|
| 1 | **Quixel Megascans** (Fab / Bridge, Epic account) | Ground, rocks, foliage, hero surfaces | Native UE import; PCG mesh lists can point at Megascans paths under Content. |
| 2 | **Kenney** and other **CC0** kits ([kenney.nl](https://kenney.nl/)) | Props, kits, UI | FBX/GLB → `AssetCreation/Exports/<Category>/` → `batch_import_asset_creation.py` → `/Game/HomeWorld/<Category>/`. |
| 3 | **Mixamo** (Adobe account) | Humanoid idle/walk/attack for dev | FBX → retarget to project skeleton; see Mixamo terms (not CC0). |
| 4 | **ambientCG** and similar **CC0** texture sites | Materials, ground | Import textures; build materials in UE. |
| 5 | **OpenGameArt**, **Poly Pizza**, **Sketchfab** (per-upload license) | Fills and experiments | Prefer CC0 or CC-BY; avoid GPL unless you comply; log license per upload. |

---

## Bundle inventory

Add one row per **download / pack / integration** (not per every `.uasset`).

| source_name | source_url | license | import_date | ue_path_pattern | used_by | track |
|-------------|------------|---------|-------------|------------------|---------|--------|
| Stylized Provencal (trees/rocks) | Project pack under `/Game/StylizedProvencal/` | Verify FAB / publisher EULA in your Epic account | (project baseline) | `/Game/StylizedProvencal/Meshes/*` | `pcg_forest_config.json` → ForestIsland_PCG spawners | MVP |
| Khronos glTF Box (sample) | https://github.com/KhronosGroup/glTF-Sample-Models/tree/main/2.0/Box | CC-BY 4.0 (Cesium donation); see ATTRIBUTION.md | 2026-05-13 | `/Game/HomeWorld/*/khronos_*` after batch import | Pipeline probe; optional PCG/BP test mesh | Automation |
| Quixel Megascans | https://www.fab.com/ or Quixel Bridge | Epic / Quixel terms (Unreal use) | (when imported) | e.g. `/Game/Megascans/...` | PCG / materials when team adds paths | MVP |
| Kenney CC0 packs | https://kenney.nl/assets | CC0 | (when added) | `/Game/HomeWorld/*` via Exports | Props / harvestables when art swaps in | MVP / Automation |

---

## Scripts and configs (quick reference)

| Step | Script or asset |
|------|-----------------|
| Batch import from disk | `Content/Python/batch_import_asset_creation.py` (Editor or MCP `execute_python_script`) |
| PCG mesh lists | `Content/Python/pcg_forest_config.json` → must match **ForestIsland_PCG** Static Mesh Spawner lists (see [PCG/PCG_SETUP.md](../PCG/PCG_SETUP.md)) |
| Demo layout / tutorial actors | `Content/Python/demo_map_config.json` → `place_partner.py`, `place_child.py`, `place_resource_nodes.py`, etc. |
| Player mesh + AnimBP | `Content/Python/character_blueprint_config.json` → `setup_character_blueprint.py` |

---

## Cast minimum (MVP tutorial)

| Role | Implementation in repo | Art expectation |
|--------|-------------------------|-----------------|
| Player | `BP_HomeWorldCharacter` + `character_blueprint_config.json` (`/Game/Man/...`) | One readable stylized or pack mesh; STYLE_GUIDE budgets. |
| Partner | `BP_Partner_Placeholder` + tag `Partner`; `place_partner.py` | Cube or simple mesh until final art; interact (E) for love task. |
| Child | `BP_Child_Placeholder` + tag `Child`; `place_child.py` | Same as partner for “game with child.” |
| Enemies / boss | C++/night encounter stubs; placeholder meshes acceptable | 1–2 enemy types + 1 boss per industry MVP doc when gameplay hooks land. |

See [VisionBoard/MVP/MVP_TUTORIAL_PLAN.md](../../VisionBoard/MVP/MVP_TUTORIAL_PLAN.md) and [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) for PIE verification commands.
