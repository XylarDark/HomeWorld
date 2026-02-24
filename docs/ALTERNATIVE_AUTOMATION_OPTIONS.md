# Alternative automation options (no MCP / no Python)

This doc describes ways to automate Unreal Editor work for HomeWorld **without** using MCP or Python. MCP and Python remain the primary automation path (see [MCP_SETUP.md](MCP_SETUP.md), [EXTERNAL_AI_AUTOMATION.md](EXTERNAL_AI_AUTOMATION.md)); this doc is for teams that want additional or non-Python options.

---

## 1. Blueprint Editor Utility Widget + startup

**What it is:** Editor Utility Widgets are Blueprint-based UI/scripts that run in the Editor. You can register a Blueprint class as a **startup object** so it runs every time the project opens.

**What it can automate:**

- **Create Asset** (via Editor Scripting Utilities → Asset Tools → Create Asset) when a **UFactory** exists for the asset type (e.g. State Tree, some data assets).
- Spawn actors in the level, set properties, save packages.
- Open custom panels or run one-off setup.

**Limitations:**

- Requires the **Editor Scripting Utilities** plugin (Edit → Plugins).
- You can only create assets for which a factory is exposed and which works with the Create Asset node. Building **graph-based** content (State Tree logic, AnimGraph, EQS) node-by-node is not exposed in Blueprint.
- Startup Blueprints run once at open; for batch runs you trigger the Widget manually or via Remote Control.

**References:** [Scripting and Automating the Editor](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-and-automating-the-unreal-editor), [Running Blueprints at Editor Startup](https://dev.epicgames.com/documentation/en-us/unreal-engine/running-blueprints-at-unreal-editor-startup).

---

## 2. C++ Editor module + IAssetTools + UFactory

**What it is:** An Editor-only C++ module (or code in an existing module under `#if WITH_EDITOR`) that uses **IAssetTools::CreateAsset()** with a **UFactory** to create assets, and plugin APIs (e.g. **UMassEntityConfigAsset::AddTrait()**) to fill them.

**What it can automate:**

- **Mass Entity Config:** Create a **UMassEntityConfigAsset** and add traits (MassAgent, MassMovement, MassRepresentationPoint, MassStateTree, etc.) and set the State Tree reference. Full automation is viable; HomeWorld provides a commandlet for this (see below).
- **State Tree:** Create an **empty** State Tree asset via the State Tree plugin’s factory; filling states/transitions requires the State Tree module APIs (no high-level “build from data” API documented).
- **Smart Object:** Create a **USmartObjectDefinition** if the plugin provides a factory; filling slots/events is plugin-specific.

**Limitations:**

- Requires C++ and an Editor module (or Editor-only code). State Tree and Smart Object “fill” APIs are not fully documented for programmatic authoring.
- EQS and AnimGraph have no documented programmatic creation; they remain Editor-only.

**References:** [IAssetTools](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Developer/AssetTools/IAssetTools), [UMassEntityConfigAsset](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/MassSpawner/UMassEntityConfigAsset), [Create Asset](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/EditorScripting/AssetTools/CreateAsset).

---

## 3. Remote Control (HTTP)

**What it is:** The **Remote Control** (Beta) feature runs an HTTP server inside the Editor. External clients can call Blueprint/C++ functions and read/write properties via REST.

**What it can automate:**

- Trigger any Blueprint or C++ function exposed to Remote Control (e.g. an Editor Utility Widget that creates assets or runs setup).
- Read/write object properties, search assets, batch operations.

**Limitations:**

- Beta feature; enable in Project Settings. Server runs in the Editor (not headless).
- Automation is only as strong as what you expose (e.g. a Blueprint that creates MEC); Remote Control does not add new “create State Tree graph” APIs by itself.

**References:** [Remote Control for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-for-unreal-engine), [Remote Control Quick Start](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-quick-start-for-unreal-engine).

---

## 4. Commandlets

**What it is:** Command-line applets run with the engine:  
`UE4Editor.exe YourGame.uproject YourModule.YourCommandlet [parm=value]...`

**What it can automate:**

- Batch creation of assets when a **UFactory** works in a commandlet context (no level, no UI). For example, the **CreateMEC** commandlet (HomeWorldEditor module) creates or updates a Mass Entity Config asset.
- Cooking, packaging, tests, asset processing.

**Limitations:**

- Commandlets run in a “raw” environment (no level loaded). Some factories or plugins may assume an open level or Editor UI. Mass Entity Config creation works; graph-heavy assets (State Tree, EQS, AnimGraph) are not documented for headless creation.

**References:** [UCommandlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UCommandlet), [Unreal Automation Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-automation-tool-for-unreal-engine).

---

## Per-asset summary

| Asset / system           | Blueprint + startup | C++ Editor / commandlet | Remote Control | Commandlet |
|--------------------------|---------------------|--------------------------|----------------|------------|
| **Mass Entity Config**  | Possible if exposed | **Yes** (CreateMEC commandlet) | Trigger C++/BP | **Yes** (CreateMEC) |
| **State Tree**          | Empty if factory    | Empty asset; fill not documented | Trigger only  | Empty if factory works |
| **Smart Object**        | Empty if factory    | Empty/partial if factory + API | Trigger only  | Unclear   |
| **EQS**                 | No                  | No                       | No             | No        |
| **AnimGraph**           | No                  | No                       | No             | No        |

---

## HomeWorld implementation: CreateMEC commandlet

HomeWorld provides a **commandlet** that creates or updates the **MEC_FamilyGatherer** Mass Entity Config asset so you can generate it without using the Editor UI or Python.

**Build:** Compile the project with the Unreal Editor **closed** (or Live Coding disabled), e.g. `Build-HomeWorld.bat`, so that the HomeWorldEditor module and commandlet are built.

**How to run (Editor must not be running):**

```bat
"C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe" "C:\dev\HomeWorld\HomeWorld.uproject" -run=HomeWorldEditor.CreateMEC
```

Or from the project root, using the engine’s RunUAT or the engine executable with `-run=HomeWorldEditor.CreateMEC`. The commandlet creates `/Game/HomeWorld/Mass/MEC_FamilyGatherer` (or the path you pass) and adds the standard traits; you still need to assign the State Tree asset and mesh in the Editor or by extending the commandlet.

**When to use:** Batch or CI workflows that need a valid MEC asset without opening the Editor; or to reset/regenerate the config to a known state.

---

## Future work

- **State Tree:** Explore State Tree module APIs to add states/transitions from data (e.g. from JSON or config). Currently only empty asset creation is documented.
- **Smart Object:** If the Smart Objects plugin exposes a factory and definition API, add a commandlet or Editor Utility to create definitions from data.
- **Remote Control:** If the team adopts Remote Control, expose a “Create MEC” or “Run week2 setup” endpoint that calls the commandlet or an Editor Utility.

---

## References

- [Scripting and Automating the Unreal Editor](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-and-automating-the-unreal-editor)
- [Scripting the Editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) (primary automation; this doc is for alternatives)
- [MCP_SETUP.md](MCP_SETUP.md), [EXTERNAL_AI_AUTOMATION.md](EXTERNAL_AI_AUTOMATION.md) (HomeWorld MCP and external AI)
