# Task: Apply PCG forest to the map

**Goal:** Procedural forest around the village.

**Status:** Verified — 1161 static mesh actors in PIE. Landscape-sized volume, village exclusion zones.

**Latest:** PIE re-run with Editor open — 1161 PCG actors confirmed.

---

## Optional: In-depth verification

1. **Open Main:** Content → HomeWorld → Maps → Main.
2. **Viewport:** Use the 3D view to confirm trees (or proxy meshes) cover the intended landscape area and the village/clearing is relatively clear.
3. **Re-run if needed:** With Editor open, run `execute_python_script("create_demo_map.py")` via MCP, or **Tools → Execute Python Script** → `Content/Python/create_demo_map.py`. This uses [demo_map_config.json](../../Content/Python/demo_map_config.json) and [pcg_forest_config.json](../../Content/Python/pcg_forest_config.json).

---

## Config

- **Demo map:** `Content/Python/demo_map_config.json` (level path, volume center/extent, exclusion zones).
- **PCG forest:** `Content/Python/pcg_forest_config.json` (graph path, density, mesh references).
