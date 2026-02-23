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

After this, follow [WEEK1_TASKS.md](WEEK1_TASKS.md) in the Editor.

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

`scripts/SetEnv-BundledDotNet.bat` is used by the two solution-related batch files; edit its UE path if the engine is installed elsewhere.

If you add or remove C++ files, regenerate project files so the solution stays in sync.

**Visual Studio Installer:** The project’s `.vsconfig` requests **.NET 8.0 Runtime (LTS)** and **.NET SDK**, not .NET 6.0. If the Installer prompts for “.NET 6.0 Runtime (Out of support)”, cancel and ensure **.NET 8.0 Runtime** and **.NET SDK** are installed instead (Individual components in the Installer). The C# parts of the solution target .NET 8.0.

**Rebuild All in Visual Studio:** The **VisualStudioTools** plugin is disabled in `.uproject` so that “Rebuild All” works without build-order issues (UBT would otherwise require UE5Rules to be built before the game when that plugin is enabled). To use the plugin: enable it in **Edit > Plugins**, then when building the full solution build **UE5Rules** first, then **HomeWorld**. For game-only builds, use **`Build-HomeWorld.bat`**.
