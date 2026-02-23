# HomeWorld – Developer Setup Checklist

Do these steps once. Everything else for first-phase setup is already in the repo.

1. **Engine:** Install Unreal Engine 5.7 (recommended); 5.4+ may work. The project targets UE 5.7 and is compatible with 5.7.x (including 5.7.3). Project is developed code-first; see [CONVENTIONS.md](CONVENTIONS.md).
2. **Project:** Open `HomeWorld.uproject`; allow first-time load/compile.
3. **Plugins:** In Editor, **Edit > Plugins** – confirm these are enabled (all are in .uproject):
   - **PCG**, **Gameplay Abilities**, **Enhanced Input**, **Day Night Sequencer**, **Steam Sockets** (replaces SteamCore for co-op).
   **Restart UE5 after enabling any new plugins.**  
   Note: **Mass Entity** is deprecated (5.5+) and has been removed from this project. When you add swarms (e.g. Weeks 3–4), enable whatever Mass-related plugin Epic documents as the replacement.
4. **Free assets:**
   - **FAB:** Survival character (or equivalent).
   - **Quixel:** Biomes/vegetation for forest.
   - The team will add specific asset names/links here when chosen.
5. **World:** Confirm the project uses Open World / World Partition (already set in `Config/DefaultEngine.ini`).
6. **Roles (optional):** Note Designer / Artist / Programmer / Tester and who leads Week 1.

7. **MCP (Cursor-to-Editor bridge):** Run **`Setup-MCP.bat`** from the project root. This installs the tools that let Cursor's AI agent control the Unreal Editor directly (spawn actors, create Blueprints, set properties). See [MCP_SETUP.md](MCP_SETUP.md) for details and troubleshooting.
8. **Cursor rules:** The repo ships a full `.cursor/rules/` directory that guides Cursor's AI agent. Open the project in Cursor and the rules are picked up automatically — no extra setup. Skim `.cursor/rules/` for an overview; key rules:
   - `unreal-cpp.mdc` — C++ conventions and UE 5.7 API pitfalls.
   - `unreal-project.mdc` — project layout, plugins, default pawn.
   - `09-mcp-workflow.mdc` — MCP-first workflow priorities.
   - `05-error-handling.mdc` — error recording policy (`docs/KNOWN_ERRORS.md`).
   - `08-project-context.mdc` — HomeWorld-specific context and conventions.

After this, follow [TASKLIST.md](TASKLIST.md) for current tasks.

---

## Plugins

All required plugins are enabled in `HomeWorld.uproject`. No Marketplace install is needed for co-op: **Steam Sockets** (in .uproject) replaces SteamCore/Steam Sessions.

| Plugin | .uproject name | Purpose |
|--------|----------------|---------|
| PCG (Procedural Content Generation) | `PCG` | Worlds/biomes |
| Gameplay Ability System (GAS) | `GameplayAbilities` | PoE-style combat |
| Steam Sockets | `SteamSockets` | Co-op (replaces SteamCore) |
| Enhanced Input | `EnhancedInput` | Better controls |
| Day Night Sequencer (UE5.5+) | `DaySequence` | Day/night cycles |

**Swarms (future):** Mass Entity is deprecated in UE 5.5+ and has been removed from this project. When implementing night swarms, enable and use whatever Mass-related plugin Epic documents as the replacement.

**Python/PCG scripts:** For the demo map and PCG forest scripts, **PythonScriptPlugin** and **PCGPythonInterop** must also be enabled. Restart the Editor after first enable.

---

## Git and LFS

Use this checklist to confirm Git and GitHub setup.

- [ ] **Repo exists:** HomeWorld repo is created and accessible. **.gitignore:** Repo root `.gitignore` contains standard UE5 entries (Binaries/, Intermediate/, Saved/, DerivedDataCache/, IDE/OS entries).
- [ ] **Git LFS:** In terminal, `git lfs version` returns a version. Repo root `.gitattributes` exists and contains LFS rules for `*.uasset` and `*.umap`.
- [ ] **Terminal (project root):** `git init` done; `git lfs track ".uasset" ".umap"` run; `.gitattributes` has the LFS lines; `git remote -v` shows `origin`; branch is `main` (or `master`); pushed to remote.
- [ ] **Team:** Each member can clone, then right-click **HomeWorld.uproject** → **Generate Visual Studio project files** (or run Engine Build.bat with -projectfiles), then open the .uproject or solution.

**Troubleshooting:** If `git push -u origin main` fails with `src refspec main does not match any`, rename the branch: `git branch -M main` then `git push -u origin main`.

---

## Validation

Use this to confirm first-phase setup is complete before starting tasks.

**In-repo (no Editor):**

- [ ] **Plugins:** In `HomeWorld.uproject`, the `Plugins` array includes `PCG`, `GameplayAbilities`, `EnhancedInput`, `SteamSockets`, and `DaySequence` (or `TimeOfDay`), each with `"Enabled":true`.
- [ ] **Default map:** In `Config/DefaultEngine.ini`, under `[/Script/EngineSettings.GameMapsSettings]`, `GameDefaultMap` is set (e.g. `/Game/HomeWorld/Maps/Main.Main`).
- [ ] **Docs:** `docs/PROTOTYPE_VISION.md`, `docs/SETUP.md`, `docs/TEAM_APPROVAL_CHECKLIST.md`, `docs/TASKLIST.md`, `ROADMAP.md` exist.

**C++ and default pawn:**

- [ ] **C++ builds:** After generating Visual Studio project files, **HomeWorld** and **HomeWorldEditor** targets build (see [Building (C++)](#building-c)).
- [ ] **Default game mode:** **Project Settings → Maps & Modes** → Default GameMode is **HomeWorldGameMode**; Default Pawn Class is **HomeWorldCharacter** (or a Blueprint child). See [CONVENTIONS.md](CONVENTIONS.md#input-setup-enhanced-input).
- [ ] **PIE:** Character moves with WASD, camera follows mouse (third-person). If not, create and assign **IA_Move**, **IA_Look**, **IMC_Default** per [CONVENTIONS.md](CONVENTIONS.md).

**Developer (Editor):**

- [ ] UE 5.4+ (or 5.7) installed; project opens without plugin errors. **Edit > Plugins** shows PCG, Gameplay Abilities, Enhanced Input, Steam Sockets, Day Night Sequencer enabled.
- [ ] FAB/Quixel assets (or equivalents) acquired if needed.
- [ ] Team has run through [TEAM_APPROVAL_CHECKLIST.md](TEAM_APPROVAL_CHECKLIST.md) if applicable.

When all above are checked, proceed to [TASKLIST.md](TASKLIST.md) and the task docs in `docs/tasks/`.

**Testing and validation:** There is no automated test suite yet. Validation is done via the checklist above (plugins, default map, C++ build, default pawn, PIE) and manual play in the Editor. When making changes, run through the relevant checklist items and play-test where applicable. Automated tests may be added later; the docs will be updated when they are.

**Debug logs:** Agent/debug logs are written to `Saved/Logs/debug-cb22d5.log` (gitignored).

When you fix a build, lint, or runtime error, record it in [KNOWN_ERRORS.md](KNOWN_ERRORS.md) so we don't repeat it.

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

`scripts/SetEnv-BundledDotNet.bat` is used by the two solution-related batch files; edit its UE path if the engine is installed elsewhere.

If you add or remove C++ files, regenerate project files so the solution stays in sync.

**Visual Studio Installer:** The project’s `.vsconfig` requests **.NET 8.0 Runtime (LTS)** and **.NET SDK**, not .NET 6.0. If the Installer prompts for “.NET 6.0 Runtime (Out of support)”, cancel and ensure **.NET 8.0 Runtime** and **.NET SDK** are installed instead (Individual components in the Installer). The C# parts of the solution target .NET 8.0.

**Rebuild All in Visual Studio:** The **VisualStudioTools** plugin is disabled in `.uproject` so that “Rebuild All” works without build-order issues (UBT would otherwise require UE5Rules to be built before the game when that plugin is enabled). To use the plugin: enable it in **Edit > Plugins**, then when building the full solution build **UE5Rules** first, then **HomeWorld**. For game-only builds, use **`Build-HomeWorld.bat`**.
