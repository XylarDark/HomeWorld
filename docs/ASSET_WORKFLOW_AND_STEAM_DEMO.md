# Asset workflow, image-to-3D research, and Steam Demo prep

**Purpose:** Define a good workflow and tools for asset generation; research **image-to-3D** (e.g. scan a Milady image → 3D copy) with a deferred pass if not realistic short-term; and align next work with **Steam Demo** prep. Current focus: preparing assets and Steam Demo — **Act 2 prep is not in scope** (see [workflow/NEXT_30_DAY_WINDOW.md](workflow/NEXT_30_DAY_WINDOW.md)).

**Phased execution:** For a step-by-step plan to accomplish this work, see **[workflow/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](workflow/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md)** (Phase 1: workflow, Phase 2: image-to-3D deferred, Phase 3: packaged build + smoke test, Phase 4: store draft, Phase 5: consolidation).

**See also:** [tasks/MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md) (full Milady pipeline), [workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md) (Steam Demo checklist).

---

## 1. Asset generation workflow (overview)

**Content paths:** Full list of project paths and script index: [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md).

### Goals

- **Workflow:** Understand a good pipeline for adding and iterating on assets (characters, props, environments) without blocking gameplay work.
- **Automation:** Identify what we can automate (scripts, batch import, MCP/Python) vs what stays manual (one-time setup, DCC exports).

### Tools and automation we can use

| Area | Tools / approach | Automation notes |
|------|------------------|------------------|
| **Import into UE** | Datasmith, FBX/GLB import, VRM4U (characters) | Python: `EditorAssetLibrary`, import tasks; MCP for Editor state. Batch import scripts in `Content/Python/`. |
| **DCC pipelines** | Blender, Maya, 3ds Max → FBX/GLB | Export from DCC; scripted re-import in UE. Document export presets (scale, LODs) in CONTENT_LAYOUT or CONVENTIONS. |
| **Procedural / PCG** | UE PCG, Houdini (if used) | Already in use (ForestIsland_PCG). Config-driven; see [PCG_SETUP.md](PCG_SETUP.md), [PCG_BEST_PRACTICES.md](PCG_BEST_PRACTICES.md). |
| **AI / image-to-3D** | Meshy, Tripo, Luma, TripoSR (see §2) | API or plugin integration; manual upload as fallback. Deferred pass if full pipeline not realistic. |
| **Version control** | Git LFS (.uasset, .umap) | No automation change; ensure new assets go under correct paths per [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md). |
| **Placement in level** | Python `EditorLevelLibrary`, MCP spawn | Scripts like `place_*` for consistent placement; idempotent, create-if-missing. |

### Recommended workflow (high level)

1. **Source assets** — Create or obtain art (DCC, marketplace, or image-to-3D when ready).
2. **Import** — Use UE import (FBX/GLB/VRM) or Python batch import where repeatable.
3. **Content paths** — Use paths under `/Game/HomeWorld/` and the documented subfolders. **Single source of truth for all project content paths:** [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) (Maps, Characters, GameMode, PCG, Mass, AI, ZoneGraph, SmartObjects, Building, Milady, Homestead, UI, etc.). Do not create ad-hoc top-level folders without updating CONTENT_LAYOUT.
4. **Level placement** — Prefer Python/MCP for repeatable placement; manual for one-off or designer-authored layout.
5. **Document manual steps** — Any step automation cannot do (e.g. VRM4U import options, Meshy API key) goes in MILADY_IMPORT_SETUP, MILADY_VARIABLES_NO_ACCESS, or [KNOWN_ERRORS.md](KNOWN_ERRORS.md) per [automation-standards](.cursor/rules/automation-standards.mdc).

**Entry point for "how we add assets":** Follow §1 (this section); use [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) for path choices and [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) script index for existing automation (ensure_* folders, place_*, etc.).

### Repeatable asset step (ensure_* pattern)

The **repeatable-asset-step pattern** is: idempotent scripts that create content folders or key assets if missing (create-if-missing; safe to re-run). The reference scripts are the **ensure_*** scripts in `Content/Python/`:

- **Folders:** `ensure_milady_folders.py`, `ensure_ui_folders.py`, `ensure_week2_folders.py`, `ensure_homestead_folders.py` — create `/Game/HomeWorld/` subfolders (Milady, UI, Mass/AI/ZoneGraph/SmartObjects/Building, Homestead).
- **Maps / levels:** `ensure_demo_map.py`, `ensure_homestead_map.py`, `ensure_main_menu_map.py`, `ensure_planetoid_level.py` — ensure level assets exist (or log manual steps).
- **Placeholders / Blueprints:** `ensure_portal_blueprint.py`, `ensure_demo_portal.py`, `ensure_dungeon_entrance_blueprint.py`, `ensure_wbp_main_menu.py` — create-if-missing for portal, dungeon entrance, main menu widget.

For the full list and per-script purpose, see [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) § Script index. No new script is required for Phase 1; use these as the reference when adding repeatable asset steps.

### Automation vs manual (Phase 1 reference)

Per [automation-standards](.cursor/rules/automation-standards.mdc): steps we cannot set from MCP, Python, or GUI automation are listed as "no access" with a manual step; new items are logged in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md). This table is the single reference for "what we can automate" vs "what needs one-time or manual" in the asset workflow.

| Area | Automatable | Manual / one-time | Where documented |
|------|-------------|-------------------|------------------|
| **Content folders** | Python: `ensure_milady_folders.py`, `ensure_ui_folders.py`, `ensure_week2_folders.py`; idempotent create-if-missing | — | [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) script index |
| **Batch import** | Python: `EditorAssetLibrary`, import tasks; MCP for Editor state; batch scripts in `Content/Python/` | — | §1 Tools table |
| **Level placement** | Python `EditorLevelLibrary`, MCP spawn; scripts like `place_*`, `place_portal_placeholder.py`, `place_resource_nodes.py` | — | §1 Recommended workflow |
| **PCG** | Volume placement, bounds, Surface Sampler params, graph assignment (`set_graph`) where exposed | Get Landscape Data **By Tag** + tag name; Static Mesh Spawner mesh list; Actor Spawner template/class in graph Details | [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) |
| **VRM4U import** | Re-import via Editor or script once path is set | Import options (e.g. scale, LOD, rig) in Import dialog; one-time per asset type | [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md); document options in MILADY_VARIABLES_NO_ACCESS or [KNOWN_ERRORS.md](KNOWN_ERRORS.md) if automation cannot set them |
| **Meshy / image-to-3D** | API or plugin when integrated | Meshy API key (project/plugin settings); one-time. Manual upload → download GLB → VRM4U import if pipeline deferred | [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md) § API keys; [ASSET_WORKFLOW_AND_STEAM_DEMO.md](ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 |
| **DCC export** | Scripted re-import in UE once file exists | Export presets (scale, LODs) in Blender/Maya/3ds Max; document in CONTENT_LAYOUT or CONVENTIONS | §1 Tools table |
| **State Tree** | Create empty asset via script | Graph editing (Selector, branches, conditions, tasks, blackboard); no Python/MCP API | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) § Gap 2; [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md) |
| **Portal / Level Streaming** | Place actor, tag; Blueprint default LevelToOpen via `ensure_portal_blueprint.py` | Set LevelToOpen on spawned actor in Details if Python cannot set C++ UPROPERTY | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) § Gap 1 |
| **Widget Blueprint (e.g. WBP_MainMenu)** | Create-if-missing script (`ensure_wbp_main_menu.py`) when Editor exposes factory | Buttons and bindings in Editor after create; MCP create_umg_widget_blueprint/add_button may fail | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Research log; CHARACTER_GENERATION_AND_CUSTOMIZATION §2 |

**No-access docs:** For each "no access" item above, the linked doc gives the **manual step** (what to do in Editor or one-time). New gaps are logged to [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) with date, feature, what is needed, why automation didn't cover it, and suggested approach. Milady-specific import options that automation cannot set: document in `docs/MILADY_VARIABLES_NO_ACCESS.md` (create when needed) or [KNOWN_ERRORS.md](KNOWN_ERRORS.md); cross-reference from §1 and [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md).

---

## 2. Image-to-3D (Milady): vision and research

### Vision

**Scan an image of a Milady and produce a 3D copy** — e.g. single 2D art or photo → 3D model suitable for in-game use (chibi, rigged or static).

### Current project state

- **[MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md)** Phase 4: **Meshy** is the intended path (PNG → Meshy image-to-3D → GLB/VRM → VRM4U import). Phase 4.2 is “Call Meshy image-to-3D from UE” (high effort, 1+ day).
- **Meshy-for-Unreal** plugin (if installed) and Meshy API key are one-time setup; see [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md).

### Research: image-to-3D tools (single image → 3D)

| Tool | Summary | UE / pipeline fit |
|------|---------|-------------------|
| **Meshy** | Image → 3D in minutes; .fbx, .obj, .glb, .usdz, etc. Good detail and texture. | Already in roadmap; Meshy-for-Unreal plugin; API for automation. |
| **Tripo3D / TripoSR** | Image-to-3D; TripoSR is open-source (Stability AI + Tripo), single image, fast, MIT. Tripo has Unreal/Blender/ComfyUI plugins. | Strong candidate; plugins could integrate into pipeline. |
| **Luma** | Broader creative AI (text, image, video, audio); 3D via ecosystem. | Less direct “image → 3D” focus; evaluate if needed. |
| **Others** | Rodin, Kaedim, etc. | Evaluate for quality, format (GLB/FBX), and UE compatibility. |

**Conclusion:** Image-to-3D from a single Milady image **is realistic** with existing services (Meshy, Tripo/TripoSR). The main cost is **pipeline integration** (API keys, plugin setup, async job handling, VRM4U import, scaling/rigging).

### Deferred pass (if not doing full pipeline now)

If we **defer** full “scan Milady image → 3D in-game” this cycle:

1. **Document** in this file and in [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md): “Image-to-3D (Milady) — feasible via Meshy or Tripo; deferred to post–Steam Demo (or next asset sprint).”
2. **Short-term option:** Manual path: export one Milady PNG → upload to Meshy (or Tripo) → download GLB → import in UE with VRM4U; use as placeholder or reference. No automation required for demo.
3. **When resuming:** Implement or extend Phase 4 (Meshy from UE) or add Tripo/TripoSR path; document in MILADY_IMPORT_SETUP and MILADY_VARIABLES_NO_ACCESS any options automation cannot set.

---

## 3. Steam Demo prep (priority)

**Goal:** Prepare for a **Steam Demo** — packaged build runs, smoke test passes, store checklist in progress.

### Entry point

- **[workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md)** — single checklist for:
  - Packaged build (run `Package-HomeWorld.bat` or `.\Tools\Package-AfterClose.ps1` after closing Editor)
  - Smoke test (run exe from `Saved\StagedBuilds\...\HomeWorld.exe`)
  - Store page content (draft title, description, capsule, screenshots)
  - Steamworks/depots when applicable

### Immediate actions

1. **Packaged build** — Close Editor; run `.\Tools\Package-AfterClose.ps1` (or build Shipping then `Package-HomeWorld.bat`). See checklist § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](KNOWN_ERRORS.md) if Stage fails.
2. **Smoke test** — Launch the packaged exe; confirm level loads, character moves, no critical errors.
3. **Store draft** — Use checklist § Store page content to draft copy and plan screenshots/capsule.

### Task list linkage

When generating the next 10-task list, **Steam Demo prep** tasks can include: run packaged build, run smoke test, update STEAM_EA_STORE_CHECKLIST status, add store draft items. See [workflow/NEXT_30_DAY_WINDOW.md](workflow/NEXT_30_DAY_WINDOW.md) (Steam Demo prep phase).

---

## 4. Summary

| Focus | Action |
|-------|--------|
| **Asset workflow** | Use §1 as reference; automate import/placement where possible; document manual steps per automation-standards. |
| **Image-to-3D (Milady)** | Feasible (Meshy, Tripo/TripoSR). Implement when ready; if deferred, use manual upload → GLB → VRM4U for placeholder and document deferred decision here and in MILADY_IMPORT_ROADMAP. |
| **Steam Demo prep** | Follow [workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md); get packaged build + smoke test + store draft in progress. |
| **Act 2 prep** | Not in current scope; deferred until after assets and Steam Demo. |
