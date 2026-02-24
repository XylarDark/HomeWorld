# llm_build_home_example.py
# Reference script for external-AI-generated "build home" style automation.
# Use as a style and path reference for LLM prompts; actual assets must match
# docs/CONTENT_LAYOUT.md. Scripts must remain idempotent (check-before-create).
# Run from Editor: Tools -> Execute Python Script, or via MCP execute_python_script.

"""
Example: build-home style automation using only HomeWorld paths.
- Ensures /Game/HomeWorld/Building/ exists.
- Spawns a small number of placeholder actors in a circle (idempotent by label).
- Does not require existing meshes; uses Actor if no static mesh path is valid.
See docs/EXTERNAL_AI_AUTOMATION.md and docs/CONTENT_LAYOUT.md.
"""

import math
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor.")
    sys.exit(0)


def _log(msg):
    unreal.log("LLM Build Home Example: " + str(msg))
    print("LLM Build Home Example: " + str(msg))


def main():
    editor_asset_lib = unreal.EditorAssetLibrary()
    building_path = "/Game/HomeWorld/Building"
    if not editor_asset_lib.does_directory_exist(building_path):
        editor_asset_lib.make_directory(building_path)
        _log("Created " + building_path)
    else:
        _log("Exists " + building_path)

    world = unreal.EditorLevelLibrary.get_editor_world()
    if not world:
        _log("No editor world; skip spawn.")
        return

    # Idempotent: only spawn if we don't already have our tagged actors
    existing = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)
    label_prefix = "LLMBuildCircle_"
    count_existing = sum(1 for a in existing if a.get_actor_label().startswith(label_prefix))
    circle_count = 10
    if count_existing >= circle_count:
        _log("Already placed %d circle actors; skip spawn (idempotent)." % count_existing)
        return

    radius = 300.0
    for i in range(circle_count):
        angle = 2 * math.pi * i / circle_count
        loc = unreal.Vector(radius * math.cos(angle), radius * math.sin(angle), 0.0)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, loc)
        if actor:
            actor.set_actor_label("%s%d" % (label_prefix, i))
    _log("Placed %d actors in circle (radius %.0f)." % (circle_count, radius))
    unreal.EditorLevelLibrary.save_current_level()


if __name__ == "__main__":
    main()
