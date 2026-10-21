# Game tool catalog

Read this before a new editor tool, Python placer, or import script.

- **Use:** extend the tool named here. Do not add a second copy.
- **Candidate:** stop for the interview. Scribe the pick in the file that already owns that beat, then change this row to Use and name the script. Do not open a second research body.
- **Hold:** do not build it.

A Candidate sets feel. This file does not approve one.

## Use

Tools already in the project.

| Tool | Job |
|---|---|
| `Tools/Safe-Build.ps1` | The only compile. |
| `Tools/RunTests.ps1` | Automation tests. `-Quest` runs the in-editor opening sweep (`quest_test_runner.py` + manifest); results `Saved/quest_tests.json`. `-QuestCheck` is the host-only quest preflight (`quest_preflight.py`: manifest vs C++ beats/stop words, no Editor). `-QuestCoverage` is the host-only quest coverage matrix (`quest_coverage.py`): declared coverage per beat, no Editor. |
| `Tools/Package-AfterClose.ps1` | Package after the editor is closed. |
| `Content/Python/start_editor.py` | Open the editor and wait for UnrealMCP. |
| UnrealMCP, port 55557 | Editor calls. Epic `ModelContextProtocol` stays off. |
| `Content/Python/reimport_size_test.py` | Size-test mesh reimport. One row per mesh. |
| `Content/Python/reimport_size_bull.py`, `reimport_size_bear.py` | Shared import, then load `L_SizeTest` and replace that actor. |
| `place_size_test.py`, `apply_homestead_scene.py`, `verify_homestead_scene.py`, `apply_size_test_metrics.py`, `measure_size_bounds.py` | Opening island placement, metrics, and the pass log. |
| `cabin_shell.py`, `armory_shell.py`, `wisp_place.py` | Cottage shell, armory shell, wisp place. |
| `place_ease_pad.py`, `verify_ease_pad.py` | Ease pad. |
| `place_field_greybox.py`, `verify_field_greybox.py` | Field greybox. |
| ComfyUI, `Tools/Invoke-TripoSR.ps1`, `Tools/Start-MixarMcp.ps1` | Front still, rigid mesh, clean and export. Door: `Docs/context/ART_ASSET_DOOR.md`. |
| `Content/Python/capture_shotlist_mrq.py` | Hero stills through Movie Render Queue. |
| `Content/Python/homeworld_material_graph.py` | Ten master materials. Sheet: `Docs/02_MATERIAL_SHEET.md`. |
| Day Sequence, Gameplay Ability System, Enhanced Input, PCG, Procedural Vegetation Editor, MegaLights, fog screen-space scattering, Lumen Lite | Enabled. Records: `docs/UE/UE58_TECH.md`, `Docs/23_UE58_FEATURE_ADOPTION.md`. |
| A probe | `start_editor.py`, an `hw.*` cheat, or `verify_homestead_scene.py`. Not a new `tmp_*.py`. |
| `hw.Playtest.FastForward` | The situation tool. Runs the earlier opening beats for real, then places the pawn and logs `playtest_ff: ready for <name>`. No argument stops at night. `hw.Night.Wisp` with numbers is a seed hook, not the arrival. |

A new situation is a beat word, a skip, a place to stand, and one sentence in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. It is not a new `hw.*` command, a save file, or a `tmp_*.py`. The command row is `Docs/COMMANDS_AND_LOG_TAGS.md`.

## Candidate

Each row waits for one interview. The question is the whole round.

| Tool | Beat | Read first | Question |
|---|---|---|---|
| PCG fill on the flat pad | The filled ground around the hand-placed copse. Hills stay later. | [PCG overview](https://dev.epicgames.com/documentation/unreal-engine/procedural-content-generation-overview). Pick goes in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md`. | Which meshes are allowed in the first graph, and which actors stay hand-placed? |
| Procedural Vegetation pine | The 5 m, 7 m, and 9 m pines. | [Procedural Vegetation Editor](https://dev.epicgames.com/documentation/unreal-engine/procedural-vegetation-editor-in-unreal-engine). Gate: `Docs/handoffs/U58F_C_PVE_PINE.md`. | Does the art director accept one stylized pine master before any graph work? |
| State Tree for one guard | Ease until that guard sleeps. | [Artificial Intelligence](https://dev.epicgames.com/documentation/unreal-engine/artificial-intelligence-in-unreal-engine), [5.8 release notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes). | What are the states a player can see, and which existing ease function is the leaf? |
| Smart Object on one station | Bed, kettle, or ease pad. | [Smart Objects](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine). | Which one station is first, and what does a failed reservation look like? |
| AI Perception on the camp guard | The sightline reads from outside. No HUD marker. | [AI Perception](https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-in-unreal-engine), [EQS overview](https://dev.epicgames.com/documentation/unreal-engine/environment-query-system-overview-in-unreal-engine). | What in the level shows the cone, and which cheat logs that the guard saw the spirit? |
| Niagara shoulder light | Five steps of light. No bar. | [Niagara](https://dev.epicgames.com/documentation/unreal-engine/creating-visual-effects-in-niagara-for-unreal-engine). Pick goes in `Docs/context/OPENING_TUTORIAL_INTERVIEW.md`. | Which step is the first sprite, and which night cheat shows it? |
| Day Sequence homestead versus camp | Warm home, cool camp. The bed still grants the form. | [Day Sequence](https://dev.epicgames.com/documentation/unreal-engine/day-sequence-time-of-day-plugin-for-unreal-engine). The 5.8 page marks it Experimental. | Which two times are the first pair, midday and the opening night? |
| Sequencer for the child's one line | The bed-and-dawn line, once. | Movie Render Queue is already Use. [Movie Render Pipeline](https://dev.epicgames.com/documentation/unreal-engine/movie-render-pipeline-in-unreal-engine). | Is the line a world actor or a sequence, and what makes it play only once? |
| Nav mesh for the child run | The child meets the spirit as the player arrives. | [Navigation Mesh settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/navigation-mesh-settings-in-the-unreal-engine-project-settings). Body: `Docs/handoffs/research/UE_PATHING.md`. | Which note in that file already covers the doorway? |
| Stroke draw | Grace on the dog, later the roost. | Body: `Docs/handoffs/research/RUNE_DRAW.md`. | Read that file before a new draw tool. |

The world teaches the approach. Outside notes for that rule, not a new tool: [Inside — Teaching through Level Design](https://www.gamedeveloper.com/design/inside-teaching-through-level-design), [What Happened Here? Environmental Storytelling](https://www.gdcvault.com/play/1012647/what-happened-here-environmental).

## Hold

| Tool | Why it stays unbuilt |
|---|---|
| Landscape on the opening island | Hills and valleys are later. `Docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`. Engine doc: [Landscape](https://dev.epicgames.com/documentation/unreal-engine/landscape-outdoor-terrain-in-unreal-engine). |
| Mesh Terrain in place of Landscape | Sandbox only until `APPROVE U58F-G`. `docs/UE/UE58_TECH.md`. |
| Movie Render Graph | Deferred. `Docs/23_UE58_FEATURE_ADOPTION.md`. Queue stays `capture_shotlist_mrq.py`. |
| MetaHuman, crowds, mobile, Mover | Rejected or deferred in the same adoption doc. |
| A dialogue tree | Guidance is a short contextual hint. |
| A HUD marker for the guard | The camp approach is readable from outside. |
| A second probe library | Probes use the three doors in the Use table. |
| A quest list as the teacher | Body: `Docs/handoffs/research/QUEST_TRACKER.md`. The world stays the teacher. |
| Modeling Mode as a hero mesh | Beta blockout only. [Modeling Mode](https://dev.epicgames.com/documentation/unreal-engine/getting-started-with-modeling-mode). Hero meshes stay on the stills path. |

`VisionBoard/Core/VISION.md` adds no tool. The seven virtue pairs stay in the virtue bible and the Gameplay Ability System.
