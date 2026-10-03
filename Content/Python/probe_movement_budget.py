# probe_movement_budget.py
# Runs INSIDE Unreal Editor as a Python script. Reads the movement numbers that
# Docs/canon/FEEL.md's traversal windows are denominated in, and writes them out.
#
# Run headless:
#   UnrealEditor-Cmd.exe HomeWorld.uproject -run=pythonscript \
#     -script=Content/Python/probe_movement_budget.py -unattended -nullrhi
#
# Writes: Saved/movement_probe.json
# Consumed by: Content/Python/traversal_budget.py
#
# ---------------------------------------------------------------------------
# WHY THIS EXISTS
# ---------------------------------------------------------------------------
#
# Docs/canon/FEEL.md has declared traversal windows - cabin->lookout 15-25 s, island
# circuit 45-90 s - since the GDD. Those windows are seconds. To ask whether they
# are physically achievable on the island that was actually built, you need the
# other half of the division: how fast does the character walk, in cm/s, and is
# that a number anyone has written down?
#
# It is not written down anywhere. It is a C++ default on ACharacter sitting in a
# Blueprint CDO. So the windows are, at present, unfalsifiable: they cannot be
# checked against the world because the quantity they are denominated in has never
# been extracted from it.
#
# This script extracts it. It is small on purpose. It reads numbers and writes
# them. It does not traverse anything, and it does not claim to - see the sibling
# note in traversal_budget.py about why measuring the walk itself needs the
# desktop.
#
# FAILURE IS LOUD. A probe that cannot read the walk speed writes
# `walk_speed_cm_s: null` plus an `errors` list, and traversal_budget.py treats a
# null walk speed as MISSING rather than falling back to a guess. A plausible
# default substituted here would produce a confident feasibility verdict built on
# a number nobody measured, which is the exact shape of failure this project has
# been spending a session removing.
# ---------------------------------------------------------------------------

import json
import os

import unreal

OUT_NAME = "movement_probe.json"


def _proj_dir() -> str:
    return unreal.Paths.project_dir()


def _out_path() -> str:
    return os.path.join(_proj_dir(), "Saved", OUT_NAME)


def _char_cdo():
    """The playable character as a class default object.

    BP_HomeWorldCharacter is the Blueprint the game mode spawns. Reading the CDO
    gives the authored values rather than whatever a placed instance happens to
    carry, which is the number FEEL.md's windows should be denominated in.
    """
    bp = unreal.load_object(
        None,
        "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
        ".BP_HomeWorldCharacter_C",
    )
    if not bp:
        return None
    return unreal.get_default_object(bp)


def _read(obj, prop: str, result: dict, required: bool = False):
    """Read one editor property, recording a failure instead of raising.

    A UE property that does not exist raises a generic Exception naming the
    property, which is the diagnostic we want - but only if it does not take the
    surrounding reads down with it.
    """
    try:
        return obj.get_editor_property(prop)
    except Exception as exc:  # noqa: BLE001
        result["errors"].append(f"{prop}: {type(exc).__name__}: {exc}")
        if required:
            return None
        return None


def main() -> None:
    result = {
        "engine": unreal.SystemLibrary.get_engine_version(),
        "is_editor": unreal.is_editor(),
        "errors": [],
    }

    # --- walk speed ---------------------------------------------------------
    # Each property is read independently. This is not defensive style, it is a
    # correction: the first version of this probe read them in one try block, a
    # single mis-named property raised, the except branch nulled out
    # `walk_speed_cm_s`, and the probe wrote a report claiming the walk speed was
    # unreadable while four good values sat in the same dict above it. One
    # unknown property name must never be able to discard a measurement that was
    # already taken.
    cdo = None
    cm = None
    try:
        cdo = _char_cdo()
        if cdo is None:
            result["errors"].append("BP_HomeWorldCharacter CDO not found")
        else:
            result["character_class"] = cdo.get_name()
            comps = cdo.get_components_by_class(unreal.CharacterMovementComponent)
            if not comps:
                result["errors"].append(
                    "no CharacterMovementComponent on the character CDO")
            else:
                cm = comps[0]
    except Exception as exc:  # noqa: BLE001 - a probe must not die silently
        result["errors"].append(f"character CDO read failed: {type(exc).__name__}: {exc}")

    if cm is not None:
        # walk_speed first: it is the load-bearing value. `optional` properties
        # are recorded but never allowed to gate the primary read.
        result["walk_speed_cm_s"] = _read(cm, "max_walk_speed", result, required=True)
        result["max_acceleration"] = _read(cm, "max_acceleration", result)
        result["braking_deceleration"] = _read(
            cm, "braking_deceleration_walking", result)
        result["ground_friction"] = _read(cm, "ground_friction", result)
        result["max_step_height_cm"] = _read(cm, "max_step_height", result)
        # 5.8 spells the walkable slope `walkable_floor_angle`, not `max_walk_slope`.
        # The latter raises on get_editor_property and does not appear in dir(cm)
        # at all - verified against BP_HomeWorldCharacter's CDO on 2026-10-03.
        # Recorded in docs/KNOWN_ERRORS.md.
        result["walkable_floor_angle_deg"] = _read(
            cm, "walkable_floor_angle", result)
        result["max_walk_speed_crouched"] = _read(
            cm, "max_walk_speed_crouched", result)
        result["properties_read_ok"] = result["walk_speed_cm_s"] is not None

    if result.get("walk_speed_cm_s") is None:
        # Do NOT invent a default. traversal_budget.py reports MISSING on a null
        # walk speed, which is correct: without it the windows cannot be checked.
        result["walk_speed_cm_s"] = None
        result["errors"].append(
            "walk speed was not read; traversal windows cannot be denominated")

    path = _out_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    unreal.log(
        f"MOVEMENT_PROBE walk_speed_cm_s={result.get('walk_speed_cm_s')} "
        f"errors={len(result['errors'])} -> {path}"
    )


if __name__ == "__main__":
    main()