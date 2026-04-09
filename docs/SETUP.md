# HomeWorld – Developer Setup Guide

This guide walks you through setting up the project so you can open the Editor, run scripts, and play in-editor. Do each step once; later sections cover validation, building, and troubleshooting.

---

## What you need before starting

- **Windows** (project is developed on Windows).
- **Unreal Engine 5.7** (or 5.4+; 5.7 recommended). Install from Epic Games Launcher.
- **HomeWorld repo** cloned locally (e.g. `git clone` and open the folder).

For a **pinned toolchain matrix** (Visual Studio workloads, Git LFS, Python, `UE_EDITOR`, C++ IntelliSense options, and Cursor plugin decisions), see [Setup/DEV_ENV_MATRIX.md](Setup/DEV_ENV_MATRIX.md).

---

## Setup steps (do in order)

### Step 1: Install the engine and open the project

1. Install **Unreal Engine 5.7** from the Epic Games Launcher. The project targets UE 5.7 and is compatible with 5.7.x (including 5.7.3). The project is developed code-first; see [CONVENTIONS.md](CONVENTIONS.md) for conventions.
2. Open **`HomeWorld.uproject`** (double-click or from the Launcher). Allow first-time load and compile.

### Step 2: Confirm plugins are enabled

In the Editor, go to **Edit → Plugins** and confirm these are enabled (they are listed in the .uproject):
   - **PCG**, **Gameplay Abilities**, **Enhanced Input**, **Day Night Sequencer**, **Steam Sockets** (replaces SteamCore for co-op).
   **Restart the Editor** after enabling any new plugins.  
   For **Week 2 family agents**, also enable the UE 5.7 Mass + State Tree stack (see [Week 2 plugins](#week-2-plugins-mass--state-trees) below).

### Step 3: (Optional) Add free assets

- **FAB:** Survival character (or equivalent).
- **Quixel:** Biomes/vegetation for forest.  
  The team will add specific asset names/links here when chosen.

### Step 4: Confirm World Partition on your main level

Primary levels **must** use World Partition. Open **Main** (`/Game/HomeWorld/Maps/Main`) in the Editor → **World Settings** → enable **World Partition** if not already. If Main was created without it, use **World Partition → Convert Level** once. Content paths: [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md).

### Step 5: Set up the MCP bridge (Cursor ↔ Editor)

Run **`Setup-MCP.bat`** from the project root. This installs the tools that let Cursor’s AI agent control the Unreal Editor (spawn actors, create Blueprints, set properties). See [Setup/MCP_SETUP.md](Setup/MCP_SETUP.md) for details and troubleshooting.

### Step 6: (Optional) Cursor Agent CLI and automation

To run the 30-day automation loop without starting each session manually: install the [Cursor Agent CLI](https://cursor.com/docs/cli/overview), run `agent login` (or set `CURSOR_API_KEY`), then run `.\Tools\RunAutomationLoop.ps1` from the project root. See [Automation/AUTOMATION_LOOP_UNTIL_DONE.md](Automation/AUTOMATION_LOOP_UNTIL_DONE.md). For a short “is everything ready?” checklist, see [Automation/AUTOMATION_READINESS.md](Automation/AUTOMATION_READINESS.md).

### Step 7: (Optional) Cursor rules and plugins

The repo ships a `.cursor/rules/` directory; open the project in Cursor and the rules load automatically. Key rules: `unreal-cpp.mdc`, `unreal-project.mdc`, `09-mcp-workflow.mdc`, `07-ai-agent-behavior.mdc`, `08-project-context.mdc`. Optional: run `/parallel-setup` once for the Parallel plugin; run `/setup` in Cursor once for Compound Engineering review agents (see `.cursor/rules/10-compound-engineering.mdc`).

---

## What to do next

After setup, follow [workflow/README.md](workflow/README.md) and [workflow/30_DAY_SCHEDULE.md](workflow/30_DAY_SCHEDULE.md) for current tasks.

**CI (optional):** For full build and automation tests in GitHub Actions, use a self-hosted Windows runner with UE 5.7. See [Setup/CI_SETUP.md](Setup/CI_SETUP.md). The [validate.yml](../.github/workflows/validate.yml) workflow runs on every push (lint, docs, C++ pairing) without needing the Editor.

---

## Plugins (reference)

All required plugins are enabled in `HomeWorld.uproject`. No Marketplace install is needed for co-op: **Steam Sockets** (in .uproject) replaces SteamCore/Steam Sessions.

| Plugin | .uproject name | Purpose |
|--------|----------------|---------|
| PCG (Procedural Content Generation) | `PCG` | Worlds/biomes |
| Gameplay Ability System (GAS) | `GameplayAbilities` | PoE-style combat |
| Steam Sockets | `SteamSockets` | Co-op (replaces SteamCore) |
| Enhanced Input | `EnhancedInput` | Better controls |
| Day Night Sequencer (UE5.5+) | `DaySequence` | Day/night cycles |

**Week 2 plugins (Mass + State Trees):** For autonomous family agents (Week 2+), enable UE 5.7 recommended: **MassEntity**, **MassGameplay**, **MassAI**, **MassNavigation**, **MassRepresentation**, **StateTree**, **ZoneGraph**, **SmartObjects**. Restart the Editor after enabling. Validation: Plugins tab shows Mass / StateTree / ZoneGraph / SmartObjects enabled. See [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md).

**Python/PCG scripts:** For the demo map and PCG forest scripts, **PythonScriptPlugin** and **PCGPythonInterop** must also be enabled. Restart the Editor after first enable.

**Milady Character Import pipeline (optional):** For the Milady chibi protagonist pipeline, install **VRM4U**, **Meshy-for-Unreal**, and a Web3/Wallet plugin; add them to `HomeWorld.uproject`. One-time setup is in [Assets/MILADY_IMPORT_SETUP.md](Assets/MILADY_IMPORT_SETUP.md). Content paths: [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md).

---

## Git and LFS

Use this checklist to confirm Git and GitHub setup.

- [ ] **Repo exists:** HomeWorld repo is created and accessible. **.gitignore:** Repo root `.gitignore` contains standard UE5 entries (Binaries/, Intermediate/, Saved/, DerivedDataCache/, IDE/OS entries).
- [ ] **Git LFS:** In terminal, `git lfs version` returns a version. Repo root `.gitattributes` exists and contains LFS rules for `*.uasset` and `*.umap`.
- [ ] **Terminal (project root):** `git init` done; `git lfs track ".uasset" ".umap"` run; `.gitattributes` has the LFS lines; `git remote -v` shows `origin`; branch is `main` (or `master`); pushed to remote.
- [ ] **Team:** Each member can clone, then right-click **HomeWorld.uproject** → **Generate Visual Studio project files** (or run Engine Build.bat with -projectfiles), then open the .uproject or solution.

**Troubleshooting:** If `git push -u origin main` fails with `src refspec main does not match any`, rename the branch: `git branch -M main` then `git push -u origin main`.

---

## How to confirm setup is complete

Use this checklist to confirm first-phase setup before starting tasks. Work through each section in order.

**In-repo (no Editor):**

- [ ] **Plugins:** In `HomeWorld.uproject`, the `Plugins` array includes `PCG`, `GameplayAbilities`, `EnhancedInput`, `SteamSockets`, and `DaySequence` (or `TimeOfDay`), each with `"Enabled":true`.
- [ ] **Default map:** In `Config/DefaultEngine.ini`, under `[/Script/EngineSettings.GameMapsSettings]`, `GameDefaultMap` and `EditorStartupMap` are set. **First launch:** Editor opens on DemoMap. **After first load:** init_unreal creates MainMenu (if missing) and sets EditorStartupMap to MainMenu so the next launch opens on the main menu. See [Default map and Editor startup map](#default-map-and-editor-startup-map-list-55) below.
- [ ] **Docs:** `docs/workflow/README.md`, `docs/workflow/30_DAY_SCHEDULE.md`, `docs/SETUP.md`, `docs/SESSION_LOG.md`, `docs/CONTENT_LAYOUT.md` exist.
- [ ] **Main map:** World Partition is enabled (open Main → World Settings → Enable World Partition). See [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md).

**C++ and default pawn:**

- [ ] **C++ builds:** After generating Visual Studio project files, **HomeWorld** and **HomeWorldEditor** targets build (see [Building (C++)](#building-c)).
- [ ] **Default game mode:** **Project Settings → Maps & Modes** → Default GameMode is **HomeWorldGameMode**; Default Pawn Class is **HomeWorldCharacter** (or a Blueprint child). See [CONVENTIONS.md](CONVENTIONS.md#input-setup-enhanced-input).
- [ ] **PIE:** Character moves with WASD, camera follows mouse (third-person). Enhanced Input assets are created automatically when the Editor loads (`Content/Python/init_unreal.py`). If movement still fails, run `setup_enhanced_input.py` once or assign **IA_Move**, **IA_Look**, **IMC_Default** on the pawn per [CONVENTIONS.md](CONVENTIONS.md).

**Developer (Editor):**

- [ ] UE 5.4+ (or 5.7) installed; project opens without plugin errors. **Edit > Plugins** shows PCG, Gameplay Abilities, Enhanced Input, Steam Sockets, Day Night Sequencer enabled.
- [ ] FAB/Quixel assets (or equivalents) acquired if needed.
- [ ] Team has run through the [workflow Pre–Day 1 checklist](workflow/README.md) if applicable.

When all above are checked, proceed to [workflow/30_DAY_SCHEDULE.md](workflow/30_DAY_SCHEDULE.md) and the task specs in [TaskLists/TaskSpecs/](TaskLists/TaskSpecs/).

**Testing:** The `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (`test_*.py`) appear in **Tools → Test Automation**. You can also run the PIE test runner: `Content/Python/pie_test_runner.py`. Level tests use the latent level loader; see [Testing/LEVEL_TESTING_PLAN.md](Testing/LEVEL_TESTING_PLAN.md). For a full PIE flow (~30–60 s), run `test_level_pie_flow.py` from Test Automation. For manual checks, run through this checklist and play-test.

**Recording errors:** When you fix a build, lint, or runtime error, add it to [KNOWN_ERRORS.md](KNOWN_ERRORS.md) so the team doesn’t repeat it.

### Default map and Editor startup map (List 55)

**Config file:** `Config/DefaultEngine.ini`, section `[/Script/EngineSettings.GameMapsSettings]`.

| Key | Effect | Current default |
|-----|--------|-----------------|
| **GameDefaultMap** | Map used when the game starts (packaged exe or PIE). | `/Game/HomeWorld/Maps/MainMenu.MainMenu` — game starts on main menu; **Play** loads DemoMap via Game Instance. MainMenu is created automatically on first Editor load (init_unreal + ensure_main_menu_map). |
| **EditorStartupMap** | Level the Editor opens when you launch the project. | First launch: **DemoMap** (so Editor always opens). After first load, init_unreal sets this to **MainMenu** so the next launch opens on the main menu. |

**How to change:**

- **Editor always opens on DemoMap:** Set `EditorStartupMap=/Game/HomeWorld/Maps/DemoMap.DemoMap` in DefaultEngine.ini and leave it; init_unreal will not overwrite it if it is already set to MainMenu (it only switches DemoMap → MainMenu when MainMenu exists).
- **Packaged game skips main menu (start in DemoMap):** Set `GameDefaultMap=/Game/HomeWorld/Maps/DemoMap.DemoMap`. Use this for testing or a kiosk-style launch.

---

## PIE: Character not visible / can't move

If when you press Play the character doesn't appear and you can't move:

1. **PlayerStart in the level** — The pawn spawns at a PlayerStart. If there is none, it may spawn at (0,0,0) and fall or be in the void. With the **Main** level open, run **Tools → Execute Python Script** → `Content/Python/setup_level.py` to add a PlayerStart (above landscape or at 0,0,300). Or place one manually: **Place Actors → Basic → Player Start** and put it on the ground.
2. **Input assets on the character** — Movement and camera need **IA_Move**, **IA_Look**, and **IMC_Default** assigned on the default pawn. The Editor runs Enhanced Input setup on load (`Content/Python/init_unreal.py`). Run **Tools → Execute Python Script** → `Content/Python/setup_character_blueprint.py` to assign those assets to the character Blueprint. Or in **Content → HomeWorld → Characters**, open **BP_HomeWorldCharacter**, select **Class Defaults**, and set **Move Action** = IA_Move, **Look Action** = IA_Look, **Default Mapping Context** = IMC_Default. Save.
3. **GameMode default pawn** — **Project Settings → Maps & Modes** (or open **BP_GameMode**): set **Default Pawn Class** to **BP_HomeWorldCharacter**. If it's None or another class, the correct character won't spawn.
4. **Full bootstrap** — If you're unsure what's missing, with **Main** open run **Tools → Execute Python Script** → `Content/Python/bootstrap_project.py`. It creates input assets, character Blueprint, project settings, and a PlayerStart, then save the level and try PIE again.

---

## Building (C++)

The project has a C++ game module (`Source/HomeWorld/`). To build from an IDE or command line:

1. **Generate project files:** Right-click `HomeWorld.uproject` in Explorer and choose **Generate Visual Studio project files**, or run the Engine’s `Build.bat` with `-projectfiles -project="path/to/HomeWorld.uproject" -game -rocket -progress` (path to `HomeWorld.uproject` in the project root). This produces the `.sln` and project files next to the `.uproject`.
2. **Build:**
   - **Game only (simplest):** Run **`Build-HomeWorld.bat`** from the project root. Uses the Engine’s Build.bat and bundled .NET; no SDK install needed. The batch file uses a hardcoded UE path (e.g. `C:\Program Files\Epic Games\UE_5.7\...`); edit it if your engine is installed elsewhere.
   - **Full solution from command line:** Run **`Build-Solution-WithBundledDotNet.bat`** to build the whole solution (C++ + C#) using the Engine’s bundled .NET 8 SDK—no system .NET install required.
   - **Full solution in Visual Studio:** Run **`Open-HomeWorld-In-VS.bat`** to open the solution with `DOTNET_ROOT` set to the Engine’s bundled .NET 8 SDK; then build in VS as usual (no system .NET install needed). Optional: to open the .sln without the launcher, install the [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) and add it to PATH so the solution builds cleanly.
3. **Run:** Launch the editor via the `.uproject` (double-click or from IDE). PIE (Play In Editor) uses the built game module.

**Batch files (project root):**

| When you want to… | Use this |
|-------------------|----------|
| Build the game only | **Build-HomeWorld.bat** |
| Open the solution in Visual Studio (with bundled .NET) | **Open-HomeWorld-In-VS.bat** |
| Build the full solution from command line | **Build-Solution-WithBundledDotNet.bat** |
| Run the PCG forest script (Editor opens and runs script) | **Run-PCGForestScript.bat** (set `UE_EDITOR` in the file first) |
| Run the demo map script (village + PCG forest) | **Run-DemoMapScript.bat** (set `UE_EDITOR` in the file first) |
| Set up MCP (Cursor-to-Editor bridge) | **Setup-MCP.bat** (one-time; installs uv, clones unreal-mcp, copies plugin) |
| Package for Windows (Shipping) | **Package-HomeWorld.bat** (RunUAT BuildCookRun; close Editor first) |

`SetEnv-BundledDotNet.bat` (project root) is used by the two solution-related batch files; edit its UE path if the engine is installed elsewhere.

If you add or remove C++ files, regenerate project files so the solution stays in sync.

**Visual Studio Installer:** The project’s `.vsconfig` requests **.NET 8.0 Runtime (LTS)** and **.NET SDK**, not .NET 6.0. If the Installer prompts for “.NET 6.0 Runtime (Out of support)”, cancel and ensure **.NET 8.0 Runtime** and **.NET SDK** are installed instead (Individual components in the Installer). The C# parts of the solution target .NET 8.0.

**Rebuild All in Visual Studio:** The **VisualStudioTools** plugin is disabled in `.uproject` so that “Rebuild All” works without build-order issues (UBT would otherwise require UE5Rules to be built before the game when that plugin is enabled). To use the plugin: enable it in **Edit > Plugins**, then when building the full solution build **UE5Rules** first, then **HomeWorld**. For game-only builds, use **`Build-HomeWorld.bat`**.

---

## Packaging (shipping build)

For Steam Early Access or distribution you need a **packaged** (cooked + staged) build. Use either the Editor or command line. **Source:** [Sharing and Releasing Projects (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/sharing-and-releasing-projects-for-unreal-engine); [Packaging Projects for Windows](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-unreal-engine-projects-for-windows) (verify menu paths in Epic 5.7 docs if your Editor differs).

**Prerequisites:** Close the Editor before command-line packaging. Ensure the project builds (run **`Build-HomeWorld.bat`** or **`.\Tools\Safe-Build.ps1`**).

### From the Editor

1. Open the project in Unreal Editor (UE 5.7).
2. **File → Package Project → Windows (64-bit)** (or the target platform).
3. Choose an output directory (e.g. `Saved/StagedBuilds` or a custom path). Packaging will cook content and produce an executable and content in that folder.
4. Run the packaged executable from the chosen output to verify.

### From the command line (RunUAT)

Use the Engine's **RunUAT** (Unreal Automation Tool) to cook and package without the Editor:

- **RunUAT location:** `C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\RunUAT.bat` (adjust if UE 5.7 is installed elsewhere).
- **Example (Windows 64-bit Shipping):** From project root, run **`Package-HomeWorld.bat`** (see project root), or invoke RunUAT manually with BuildCookRun; output under `Saved\StagedBuilds`.

**Validation:** After packaging, launch the game from the staged directory and confirm: level loads, character moves, no missing content. For a Steam store checklist, see [workflow/STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md).
