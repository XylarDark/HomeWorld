# External AI agents and Editor automation

This doc describes how **external AI** (LLMs) can automate UE5 Editor building and level work in HomeWorld. "External AI" here means an LLM (in Cursor or a separate service) that **generates Python** which then runs in the Editor — not in-game Mass agents (those are in [FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md) and [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md)).

---

## What is "external AI" in this context?

- An LLM (Cursor’s model, Grok, Claude, GPT, or a script-generation service) produces **Python code** that uses the Unreal Engine Python API (`unreal` module).
- That code runs in the Editor via:
  - **MCP:** Cursor calls `execute_python_script` and the script runs inside the Editor, or
  - **Manual:** Tools → Execute Python Script (or Editor Python Console).
- Use case: "Generate a PCG home blueprint" or "Spawn 10 modular walls in a circle" → agent produces a script → you run it in the Editor.

---

## Primary path: Cursor + UnrealMCP

No extra server is required:

1. **Cursor** (with built-in AI) uses **UnrealMCP** tools to talk to the running Editor ([MCP_SETUP.md](MCP_SETUP.md)).
2. The AI writes or edits Python in `Content/Python/` and runs it via MCP `execute_python_script`, or uses MCP tools directly (spawn actor, set property, etc.).
3. Reusable workflows are saved as scripts in `Content/Python/` so they can be re-run without MCP.

See [.cursor/rules/09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc) for MCP-first priorities.

---

## Optional path: External script generator

You can use an **external** service that takes a natural-language prompt and returns Python:

1. Send a prompt (e.g. "Build whimsical forest home with 8 walls and a PCG farm") to the service.
2. Receive generated Python code.
3. **Review the code** (see Security below).
4. Save it to `Content/Python/` or run it via MCP `execute_python_script` or Tools → Execute Python Script.

Optional tools (not part of this repo; use at your own risk):

- **UE5-MCP** (e.g. VedantRGosavi/UE5-MCP): HTTP server that returns Python from a prompt; you run the script in the Editor yourself.
- **CrewAI** or similar: Multi-agent workflows that can output Python for UE.
- **Custom HTTP endpoint:** Any service that returns Python given a prompt.

We do not embed or endorse a specific third-party repo; integrate and review any generated code before execution.

---

## HomeWorld conventions

All generated or example scripts must follow project rules:

- **Paths:** Use `/Game/HomeWorld/` only. See [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md):
  - Maps: `/Game/HomeWorld/Maps/`
  - PCG: `/Game/HomeWorld/PCG/`
  - Building: `/Game/HomeWorld/Building/`
  - Mass: `/Game/HomeWorld/Mass/`
  - AI: `/Game/HomeWorld/AI/`
  - SmartObjects: `/Game/HomeWorld/SmartObjects/`
- **Idempotency:** Scripts must be safe to run multiple times. Check for existing assets/actors before creating; do not blindly delete-and-recreate. See [.cursor/rules/00-core-principles.mdc](../.cursor/rules/00-core-principles.mdc) (Idempotency Protocol).
- **Naming:** HomeWorld only; no RealmBond or other project names in paths or comments.

---

## Example prompt and script

**Prompt (copy-paste for an LLM):**

"Using the UE5 Python API, write a script that: (1) ensures the directory /Game/HomeWorld/Building/ exists; (2) spawns 10 static mesh actors in a circle (radius 300, Z=0) — use a placeholder mesh path if the project has one, otherwise spawn Actor at locations and log; (3) ensures a PCG volume exists at origin or logs that PCG setup is manual. Use only /Game/HomeWorld/ paths. Script must be idempotent: check before creating. Run inside Unreal Editor (import unreal)."

**Example output script (style only; asset paths depend on your content):**

```python
# Example: LLM-generated "build home" style script. Idempotent; HomeWorld paths only.
# Run from Editor: Tools -> Execute Python Script, or via MCP execute_python_script.
import unreal

def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    building_path = "/Game/HomeWorld/Building"
    if not editor_asset_lib.does_directory_exist(building_path):
        editor_asset_lib.make_directory(building_path)
        unreal.log("External AI: Created " + building_path)

    # Spawn actors in a circle (idempotent: check existing or use tag)
    editor_level = unreal.EditorLevelLibrary.get_editor_world()
    if not editor_level:
        unreal.log("External AI: No editor world")
        return
    import math
    radius = 300.0
    count = 10
    for i in range(count):
        angle = 2 * math.pi * i / count
        loc = unreal.Vector(radius * math.cos(angle), radius * math.sin(angle), 0.0)
        # Use a valid asset path from your project, e.g. /Game/HomeWorld/Building/SM_Wall
        # If no mesh: spawn Actor and log
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, loc)
        if actor:
            actor.set_actor_label("BuildCircle_%d" % i)
    unreal.log("External AI: Placed %d actors in circle" % count)
    unreal.EditorLevelLibrary.save_current_level()

if __name__ == "__main__":
    main()
```

Actual asset paths (e.g. static mesh for walls) must match your [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md); the above uses `unreal.Actor` as a safe fallback if no mesh path exists. A full idempotent reference script is in [Content/Python/llm_build_home_example.py](../Content/Python/llm_build_home_example.py).

---

## Security

- **Always review generated code before running.** Do not execute untrusted script in the Editor.
- Generated Python runs with full Editor and project access (assets, level, file system via `unreal` and standard Python). Validate paths and logic before execution.
- Prefer saving generated scripts to `Content/Python/` and running them explicitly (MCP or Tools → Execute Python Script) rather than blind `exec()` of network response.

---

## References

- [MCP_SETUP.md](MCP_SETUP.md) — Cursor–Editor bridge (UnrealMCP)
- [.cursor/rules/09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc) — MCP-first workflow
- [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) — HomeWorld content paths
- [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md) — In-game agent building (Mass + Smart Objects)
- Epic: [Python scripting in Unreal Engine](https://docs.unrealengine.com/5.7/en-US/python-scripting-in-unreal-engine/)
