# Asset workflow, image-to-3D research, and MVP deliverable (marketing-ready)

**Purpose:** Define a good workflow and tools for asset generation; research **image-to-3D** (e.g. scan a Milady image → 3D copy) with a deferred pass if not realistic short-term; and align next work with the **MVP deliverable**: **marketing-ready** slice with **assets and visuals mandatory** for good-looking marketing material. **Launching on Steam is not required for MVP** — Steam store and packaged build for distribution are post-MVP when we choose to ship.

**Assets and visuals are mandatory for MVP** so we can produce screenshots, capsule art, and trailer material. Current focus: preparing assets and visual quality — **Act 2 prep is not in scope** (see [VisionBoard/NEXT_30_DAY_WINDOW.md](../VisionBoard/NEXT_30_DAY_WINDOW.md)).

**Phased execution:** For a step-by-step plan, see **[VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](../VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md)** (Phase 1: workflow, Phase 2: image-to-3D deferred; Phase 3–4 packaged build/store draft are optional for MVP).

**See also:** [TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) (full Milady pipeline), [workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md) (for when we launch on Steam — not required for MVP).

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

### Asset creation directory and batch import

**Source assets** live in **`AssetCreation/`** at project root. That directory holds Blender/AI source work and a single export location so automation always knows where to look.

- **Purpose:** One place for all asset-creation work: `.blend`/AI outputs, **Exports/** (FBX/GLB ready for import), AI_Sources, RefImages. The **batch import script** reads `AssetCreation/Exports/` and imports into `/Game/HomeWorld/...` by category.
- **Export preset (Blender):** Forward **X**, Up **Z**; Apply Scaling **FBX Unit Scale**; Apply Modifiers; Smoothing **Face**; FBX 2020.2. Export to `AssetCreation/Exports/<Category>/` (Characters, Harvestables, Homestead, Dungeon, Biomes). Full preset and style notes: [AssetCreation/STYLE_GUIDE.md](../AssetCreation/STYLE_GUIDE.md).
- **Batch import script:** `Content/Python/batch_import_asset_creation.py`. Scans `AssetCreation/Exports/` subfolders, maps each to `/Game/HomeWorld/<Category>/`, and runs `AssetImportTask` for every FBX/GLB. Idempotent (replace existing). Run from Editor: **Tools → Execute Python Script**, or via MCP: `execute_python_script("batch_import_asset_creation.py")`.
- **Style and art direction:** Clean cartoon, SMG-like, lower rez, wholesome; poly budgets and do's/don'ts: [AssetCreation/STYLE_GUIDE.md](../AssetCreation/STYLE_GUIDE.md). Short "how to add a new asset" steps: [AssetCreation/README.md](../AssetCreation/README.md).

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

**Phased context:** This section aligns with **Phase 2** of [VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](../VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) (image-to-3D deferred pass). **Phase 2 gate — List 72:** Met: image-to-3D deferred; resume path documented.

**Cross-links:** Full Milady pipeline and Phase 4 (2D PNG → 3D): [TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) Phase 4.

### Vision

**Scan an image of a Milady and produce a 3D copy** — e.g. single 2D art or photo → 3D model suitable for in-game use (chibi, rigged or static).

### Current project state

- **[MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md)** Phase 4: **Meshy** is the intended path (PNG → Meshy image-to-3D → GLB/VRM → VRM4U import). Phase 4.2 is “Call Meshy image-to-3D from UE” (high effort, 1+ day).
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

**Decision (Phase 2 / List 72):** Image-to-3D (Milady) — feasible via Meshy or Tripo; **full pipeline deferred** to post–Steam Demo (or next asset sprint). Manual path: PNG → Meshy/Tripo → GLB → VRM4U import.

If we **defer** full “scan Milady image → 3D in-game” this cycle:

1. **Document** in this file and in [MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md): “Image-to-3D (Milady) — feasible via Meshy or Tripo; deferred to post–Steam Demo (or next asset sprint).”
2. **Short-term option:** Manual path: export one Milady PNG → upload to Meshy (or Tripo) → download GLB → import in UE with VRM4U; use as placeholder or reference. No automation required for demo.
3. **When resuming:** See [When resuming the image-to-3D pipeline](#when-resuming-the-image-to-3d-pipeline-phase-2-step-23) below.

### When resuming the image-to-3D pipeline (Phase 2 step 2.3)

**Purpose:** Clear steps for a future session (or next asset sprint) to implement the full "scan Milady image → 3D in-game" pipeline. Phase 2 gate 2.3 — resume path documented.

**What to implement:**

- **Option A — Meshy from UE:** Follow [MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) Phase 4: 4.1 (API key and plugin config), 4.2 (Call Meshy image-to-3D from UE — upload PNG, poll/callback, download GLB/VRM), 4.3 (save output to project path). Wire `UHomeWorldMiladyImportSubsystem` (or equivalent) so that after PNG is fetched, the Meshy plugin is invoked; on completion, save to e.g. `Content/HomeWorld/Milady/Generated/<tokenId>.glb` and trigger VRM4U import.
- **Option B — Tripo / TripoSR path:** Add Tripo or TripoSR integration (plugins exist for Unreal/Blender/ComfyUI): same flow — pass PNG → request 3D → poll or callback → download GLB → VRM4U import. Document chosen plugin and any API keys in [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md).

**Where to document "variables with no access":**

- **Create when needed:** `docs/MILADY_VARIABLES_NO_ACCESS.md` — list any Meshy/Tripo/VRM4U options (e.g. import scale, LOD, retargeter settings) that MCP, Python, or GUI automation cannot set; include manual step and suggested future approach per [automation-standards](.cursor/rules/automation-standards.mdc).
- **Alternatively or in addition:** [MILADY_IMPORT_SETUP.md](MILADY_IMPORT_SETUP.md) (Known issues and plugin order) or [KNOWN_ERRORS.md](KNOWN_ERRORS.md) for one-off or engine-specific items.
- **New gaps:** Log to [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) with date, feature, what is needed, why automation didn't cover it, and suggested approach.

**References:** [VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](../VisionBoard/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 2 step 2.3; [MILADY_IMPORT_ROADMAP.md](../TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md) Phase 4.

### Phase 2 step 2.2 — optional manual run (List 72)

**Outcome:** Manual run skipped; tools not required for autonomous session. If Meshy/Tripo and VRM4U are available, the manual path (one Milady PNG → Meshy or Tripo → download GLB → import in UE with VRM4U) can be run once; note outcome (success, quality, blockers) in SESSION_LOG or a short subsection here.

---

## 3. Packaged build and Steam (optional for MVP)

**Goal:** When we choose to ship or distribute, prepare packaged build (runs, smoke test) and store checklist. **Not required for MVP deliverable** — MVP = marketing-ready (assets + visuals); Steam launch is post-MVP.

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

When generating the next 10-task list, **MVP priority = assets and visuals** (marketing-ready). Packaged build and Steam store tasks are optional for MVP; add them when we are preparing to ship. See [VisionBoard/NEXT_30_DAY_WINDOW.md](../VisionBoard/NEXT_30_DAY_WINDOW.md).

---

## 4. Summary

| Focus | Action |
|-------|--------|
| **Asset workflow** | Use §1 as reference; automate import/placement where possible; document manual steps per automation-standards. |
| **Image-to-3D (Milady)** | Feasible (Meshy, Tripo/TripoSR). Implement when ready; if deferred, use manual upload → GLB → VRM4U for placeholder and document deferred decision here and in MILADY_IMPORT_ROADMAP. |
| **Assets and visuals (mandatory for MVP)** | Quality assets and visual polish for marketing material (screenshots, capsule, trailer). Asset workflow §1 is the entry point. |
| **Packaged build / Steam** | Optional for MVP. When we ship: follow [workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md); packaged build + smoke test + store draft. |
| **Act 2 prep** | Not in current scope; deferred until after assets and MVP deliverable. |
