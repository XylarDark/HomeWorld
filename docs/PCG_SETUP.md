# PCG Setup — HomeWorld (UE 5.7)

Single reference for procedural trees/rocks on the landscape: what the script does, what you must do in the Editor, and where to look for help.

---

## Prerequisites

- Level open (e.g. **Main**) with a **Landscape** in it.
- **Landscape** → Details → **Component Subsection** = **1x1** (required for PCG in UE 5.x).
- The Landscape must be findable by **Get Landscape Data** via the tag **`PCG_Landscape`** (the script can add this tag).

---

## What the script does

The script (**create_demo_map.py**, or **setup_level.py** with `run_pcg=True`) **only**:

1. **Tags the Landscape** with **`PCG_Landscape`** if missing (`ensure_landscape_has_pcg_tag()`).
2. **Creates and sizes one PCG Volume** to the landscape bounds (or config), labeled **PCG_Forest** in the Outliner.
3. Saves the level.

The script **does not**:

- Create or modify the PCG graph.
- Set **Get Landscape Data** (Actor By Tag, tag name, Component By Class).
- Assign the graph to the PCG Volume.
- Run Generate.

So **running the script alone never produces trees or rocks**. You must create (or reuse) the graph, set Get Landscape Data, assign the graph to the volume, and click Generate.

---

## Steps only you do (in the Editor)

1. **Create a PCG Graph** (or copy one from a reference project — see References below).
2. In the graph, add **Get Landscape Data** and set it in **Details**:
   - **Actor** → **By Tag**, tag **`PCG_Landscape`**.
   - **Component** → **By Class** → **Landscape Component** (if available).
3. Wire the graph: **Get Landscape Data** → **Surface Sampler** (Surface); **Input** → **Surface Sampler** (Bounding Shape); **Surface Sampler** → **Static Mesh Spawner** → **Output**.
4. **Assign the graph** to the **PCG Volume** (Outliner → select PCG_Forest → Details → **Graph** → your graph).
5. Click **Generate**.

If the script already placed the volume, you only need to create/configure the graph, assign it to that volume, and Generate.

---

## Detailed manual steps (from scratch)

If you prefer to build the graph from zero in the Editor, see **[docs/tasks/PCG_MANUAL_SETUP.md](tasks/PCG_MANUAL_SETUP.md)** for step-by-step (tag Landscape, create graph, add Get Landscape Data / Surface Sampler / Static Mesh Spawner, set By Tag + `PCG_Landscape`, add PCG Volume, assign graph, Generate).

---

## References

- **Required settings automation cannot set:** See [docs/PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md) for a list of variables/settings that are necessary but not (reliably) settable from Python/MCP.
- **[freetimecoder/unreal-pcg-examples](https://github.com/freetimecoder/unreal-pcg-examples)** — Full project with PCG graphs and maps; works in UE 5.7. Open a level with a PCG Volume + graph, hit Generate, then inspect the graph (Get Landscape Data settings, node order).
- **[PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5](https://github.com/PacktPublishing/Procedural-Content-Generation-with-Unreal-Engine-5)** — Book repo, UE 5.4+; **Chapter_2** is “Craft your first lush, procedurally generated forest.” Open the Chapter_2 project in 5.7 and mirror its graph layout and Details settings in HomeWorld.
- **Epic docs:** [PCG Framework Node Reference (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine), [Get Landscape Data (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PCG/UPCGGetLandscapeSettings). In 5.4+, landscape is provided only via **Get Landscape Data**; the graph Input provides bounds.

---

## If nothing generates

1. **Landscape:** Component Subsection = **1x1**; actor has tag **`PCG_Landscape`**.
2. **Get Landscape Data:** Details → Actor **By Tag**, tag **`PCG_Landscape`**; Component **By Class** → **Landscape Component** if needed.
3. **Wiring:** Get Landscape Data **Out** → Surface Sampler **Surface** only; Input → Surface Sampler **Bounding Shape**; Surface Sampler → spawner → Output.
4. **Output Log:** Search for `PCG` or `No surfaces found`; fix 1–2 if the Surface Sampler reports no surface.

See **docs/KNOWN_ERRORS.md** entries for *PCG Generate does nothing* and *PCG Surface Sampler: No surfaces found*.
