# place_vs_mvp_pa_d.py
# PA-D: Idempotent Homestead kit dress (cliffs, garden, path) + refresh core DRESS_* anchors.
# Run in Unreal Editor or via MCP execute_python_script("place_vs_mvp_pa_d.py").
# Prerequisites: batch_import_asset_creation.py, place_vs_mvp_markers.py on Windows host.

from __future__ import annotations

import importlib
import json
import os
import re
import sys

try:
    import unreal
except ImportError:
    print("place_vs_mvp_pa_d: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "place_vs_mvp_pa_d:"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
PA_D_FOLDER = "VS_MVP/PA_D"
PA_D_LABEL_PREFIX = "PA_D_"

# Spec sources. These are READ, not restated.
#
# The cliff faces and the garden zone volume both live in Lib/01_Homestead, and
# this script used to hardcode copies of them directly under comments citing those
# files. The copies could drift from the spec with nothing to notice, and a comment
# citing a file is a claim about that file rather than a link to it -- so a spec
# edit would silently not apply here. An earlier note in this repo claimed the
# cliff positions were absent from SM_Cliff.json; they are not, they sit under
# modules[].origin. Both sources are parsed now, and a source that fails to parse
# raises rather than falling back to a literal, because a fallback is how the two
# copies started drifting in the first place.
LIB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "Lib", "01_Homestead")
CLIFF_SPEC_PATH = os.path.join(LIB_DIR, "SM_Cliff.json")
GARDEN_SPEC_PATH = os.path.join(LIB_DIR, "GARDEN_BLOCKING.md")


def _read_cliff_specs(path):
    """Graybox cliff face placements, in Blender metres, from SM_Cliff.json.

    Returns (specs, names_without_origin). A module listed in graybox_map but
    carrying no origin is returned in the second list so the caller can fail
    loudly -- guessing a position for it would be inventing geometry placement.
    """
    with open(path, "r", encoding="utf-8-sig") as handle:
        spec = json.load(handle)
    wanted = list(spec.get("graybox_map") or [])
    by_name = {m.get("name"): m for m in (spec.get("modules") or [])}
    specs, missing = [], []
    for name in wanted:
        origin = (by_name.get(name) or {}).get("origin")
        if origin is None:
            missing.append(name)
            continue
        specs.append((name, tuple(float(v) for v in origin)))
    if not wanted:
        raise ValueError(f"{path} declares no graybox_map")
    return tuple(specs), missing


def _read_garden_envelope(path):
    """The garden zone volume, from the Envelope table in GARDEN_BLOCKING.md.

    That table's volume row reads:

        | Zone volume (graybox) | **4.0 × 2.5 × 0.6 m** at (−3.5, 0.5, 0.0) |

    Returns ((cx, cy, cz), (sx, sy, sz)). Both halves are read from that one row
    because the placements below are derived from both: the planters from the
    centre, the fence from the centre and the half-extents. Reading the centre
    alone would have left the fence behind whenever the spec's envelope moved --
    the two used to agree only because they were both typed out by hand.

    The minus sign is U+2212 MINUS SIGN, not U+002D HYPHEN-MINUS, and the size
    separator is U+00D7. A regex written for plain ASCII finds nothing in that
    row. It was written that way first, and the loud failure is the only reason
    that was caught rather than papered over with a fallback to the literal this
    function replaced.
    """
    with open(path, "r", encoding="utf-8-sig") as handle:
        text = handle.read()
    for line in text.splitlines():
        if "Zone volume" not in line:
            continue
        centre = _XYZ_RE.search(line)
        size = _SIZE_RE.search(line)
        if centre and size:
            return (tuple(_to_float(v) for v in centre.groups()),
                    tuple(_to_float(v) for v in size.groups()))
        raise ValueError(
            f"{path} has a 'Zone volume' row that is missing "
            + ("the (x, y, z) centre" if not centre else "the N x N x N m size")
            + f": {line.strip()!r}")
    raise ValueError(f"{path} has no 'Zone volume' row")


# Sign class covers U+002D HYPHEN-MINUS and U+2212 MINUS SIGN. Both appear in
# Lib/01_Homestead: the JSON specs are ASCII, the Markdown specs are typographic.
# Escapes are spelled out rather than pasted literally, so the character class is
# unambiguous to read and to edit. _to_float normalises before float() sees it.
_MINUSES = "-\u2212"
_TIMES = "x\u00d7X"
_NUM = r"[%s]?\d+(?:\.\d+)?" % re.escape(_MINUSES)
_XYZ_RE = re.compile(r"\(\s*(%s)\s*,\s*(%s)\s*,\s*(%s)\s*\)" % (_NUM, _NUM, _NUM))
_SIZE_RE = re.compile(
    r"(%s)\s*[%s]\s*(%s)\s*[%s]\s*(%s)\s*m"
    % (_NUM, re.escape(_TIMES), _NUM, re.escape(_TIMES), _NUM))


def _to_float(text):
    """float() on a number written with a typographic minus."""
    return float(str(text).strip().replace("\u2212", "-"))

CLIFF_SPECS, _CLIFF_MISSING_ORIGIN = _read_cliff_specs(CLIFF_SPEC_PATH)
if _CLIFF_MISSING_ORIGIN:
    raise ValueError(
        "SM_Cliff.json lists these in graybox_map but gives them no origin: "
        + ", ".join(_CLIFF_MISSING_ORIGIN)
        + ". Add the origin or drop the name; do not let this script invent one.")

GARDEN_CENTER_BL, GARDEN_SIZE_BL = _read_garden_envelope(GARDEN_SPEC_PATH)
_HALF = tuple(s / 2.0 for s in GARDEN_SIZE_BL)

# Planters straddle the garden centre, so moving the centre in GARDEN_BLOCKING.md
# moves them. The 0.6 m spacing is kit-local and not spec'd.
PLANTER_SPECS = tuple(
    ("SM_Planter_" + suffix,
     (GARDEN_CENTER_BL[0] + dx, GARDEN_CENTER_BL[1] + dy, GARDEN_CENTER_BL[2]))
    for suffix, dx, dy in (("A", -0.6, 0.0), ("B", 0.0, 0.0), ("C", 0.6, 0.0))
)

# Low rail segments. The first four are the midpoints of the four envelope edges,
# derived so they follow the spec's centre and size; the fifth is a corner fillet
# whose offset is a visual choice and is the one number here that GARDEN_BLOCKING.md
# does not determine. These were five hand-typed coordinates that happened to match
# the envelope exactly. Deriving four of them removes a silent-drift risk; the
# fillet keeps its literal and says so.
FENCE_SEGMENTS_BL = (
    (GARDEN_CENTER_BL[0] - _HALF[0], GARDEN_CENTER_BL[1], GARDEN_CENTER_BL[2]),
    (GARDEN_CENTER_BL[0], GARDEN_CENTER_BL[1] + _HALF[1], GARDEN_CENTER_BL[2]),
    (GARDEN_CENTER_BL[0] + _HALF[0], GARDEN_CENTER_BL[1], GARDEN_CENTER_BL[2]),
    (GARDEN_CENTER_BL[0], GARDEN_CENTER_BL[1] - _HALF[1], GARDEN_CENTER_BL[2]),
    (GARDEN_CENTER_BL[0] - 1.0, GARDEN_CENTER_BL[1] + 0.75, GARDEN_CENTER_BL[2]),
)

# CRUMB path ends. NOT SPEC'D: no file in Lib/01_Homestead declares these two
# points, and this comment previously sat directly above them implying otherwise.
# They are kit-local until someone gives them a spec to live in.
PATH_START_BL = (-6.0, 1.0, 0.0)
PATH_END_BL = (7.0, -3.5, 0.0)
PATH_STONE_NAMES = ("SM_PathStone_A", "SM_PathStone_B", "SM_PathStone_C")


def _log(msg, data=None):
    line = PREFIX + " " + str(msg)
    if data is not None:
        line += " " + str(data)
    unreal.log(line)
    print(line)


def blender_to_ue_cm(loc):
    x, y, z = float(loc[0]), float(loc[1]), float(loc[2])
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def destroy_existing_pa_d():
    to_destroy = []
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            label = ""
        folder = ""
        try:
            folder = str(actor.get_folder_path())
        except Exception:
            pass
        if label.startswith(PA_D_LABEL_PREFIX) or folder.replace("\\", "/") == PA_D_FOLDER:
            to_destroy.append(actor)
    for actor in to_destroy:
        unreal.EditorLevelLibrary.destroy_actor(actor)
    if to_destroy:
        _log("Removed existing PA-D actors", {"count": len(to_destroy)})
    return len(to_destroy)


def spawn_pa_d_actor(mesh_name, static_mesh, location_blender):
    loc = blender_to_ue_cm(location_blender)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        _log("Spawn failed", {"mesh": mesh_name})
        return None
    sm_comp = actor.get_component_by_class(unreal.StaticMeshComponent)
    if sm_comp and static_mesh:
        sm_comp.set_static_mesh(static_mesh)
    actor.set_actor_label(PA_D_LABEL_PREFIX + mesh_name)
    actor.set_folder_path(PA_D_FOLDER)
    return actor


def _lerp_bl(a, b, t):
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
    )


def sample_path_points(count=5):
    count = max(2, int(count))
    points = []
    for i in range(count):
        t = i / float(count - 1)
        points.append(_lerp_bl(PATH_START_BL, PATH_END_BL, t))
    return points


def place_exact_mesh(mesh_index, mesh_name, location_blender, counts, optional=False):
    entry = mesh_index.get(mesh_name)
    if not entry:
        if optional:
            _log("Optional mesh missing (skip)", {"mesh": mesh_name})
        else:
            _log("Mesh missing", {"mesh": mesh_name})
        return 0
    _path, mesh = entry
    if spawn_pa_d_actor(mesh_name, mesh, location_blender):
        counts["spawned"] = counts.get("spawned", 0) + 1
        if mesh_name.startswith("SM_Cliff"):
            counts["cliffs"] = counts.get("cliffs", 0) + 1
        elif mesh_name.startswith("SM_Planter"):
            counts["planters"] = counts.get("planters", 0) + 1
        elif mesh_name.startswith("SM_Garden_Fence"):
            counts["fence"] = counts.get("fence", 0) + 1
        elif mesh_name.startswith("SM_PathStone"):
            counts["path_stones"] = counts.get("path_stones", 0) + 1
        return 1
    return 0


def ensure_level():
    import place_vs_mvp_markers

    importlib.reload(place_vs_mvp_markers)
    place_vs_mvp_markers.create_or_load_level()
    return True


def run_dress_refresh():
    import place_vs_mvp_dress as dress

    importlib.reload(dress)
    _log("Refreshing DRESS_* kit via place_vs_mvp_dress")
    dress.main()


def main():
    _log("Start PA-D Homestead place")
    ensure_level()
    removed = destroy_existing_pa_d()

    import place_vs_mvp_dress as dress

    importlib.reload(dress)
    mesh_index = dress.build_mesh_index()
    counts = {"removed_pa_d": removed, "spawned": 0, "cliffs": 0, "planters": 0, "fence": 0, "path_stones": 0}

    for mesh_name, loc in CLIFF_SPECS:
        place_exact_mesh(mesh_index, mesh_name, loc, counts, optional=False)

    for mesh_name, loc in PLANTER_SPECS:
        place_exact_mesh(mesh_index, mesh_name, loc, counts, optional=True)

    fence_mesh = "SM_Garden_Fence_Seg"
    if mesh_index.get(fence_mesh):
        for idx, loc in enumerate(FENCE_SEGMENTS_BL):
            label = fence_mesh if idx == 0 else fence_mesh + "_" + str(idx + 1)
            entry = mesh_index.get(fence_mesh)
            if entry and spawn_pa_d_actor(label, entry[1], loc):
                counts["spawned"] = counts.get("spawned", 0) + 1
                counts["fence"] = counts.get("fence", 0) + 1
    else:
        _log("Optional mesh missing (skip)", {"mesh": fence_mesh})

    path_points = sample_path_points(5)
    for i, loc in enumerate(path_points):
        stone_name = PATH_STONE_NAMES[i % len(PATH_STONE_NAMES)]
        place_exact_mesh(mesh_index, stone_name, loc, counts, optional=True)

    # place_vs_mvp_dress.main() -> create_or_load_level() -> load_level reloads from disk
    # and drops actors that were spawned but not saved yet.
    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved after PA-D spawn (before dress reload)", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("Save after PA-D spawn warning", {"error": str(exc)})

    run_dress_refresh()

    try:
        unreal.EditorLevelLibrary.save_current_level()
        _log("Saved current level", {"path": LEVEL_PATH})
    except Exception as exc:
        _log("Save level warning", {"error": str(exc)})

    _log("Done", counts)
    return 0


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)
