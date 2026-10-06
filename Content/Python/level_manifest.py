# level_manifest.py
# CONTEXT_PACK_V1 bite 3: dump every actor in L_VS_MVP_Markers to
# Docs/level/L_VS_MVP_Markers_manifest.json.
#
# Why this exists: Docs/handoffs/CONTEXT_PACK_V1.md records that portal
# destinations turned out to be TargetPoints rather than portal components,
# which made a lookup come back empty. Reading class and label straight out of a
# committed file settles that kind of question without opening the Editor.
#
# Bounds only. No line traces: a trace answers a ray question, and an unattended
# trace returns nothing here, so the manifest records what is actually readable
# without a viewport. Containment is a point-in-box test against
# get_actor_bounds(False).
#
# Usage, in the Editor (Tools -> Execute Python Script):
#     exec(open(r"<repo>/Content/Python/level_manifest.py").read())
# Writes the manifest.
#
# Usage, headless:
#     UnrealEditor-Cmd.exe <uproject> -run=pythonscript \
#         -script=<repo>/Content/Python/level_manifest.py -unattended -nopause \
#         -nosplash -nullrhi -abslog=<abs log path>
# Same write, no window.
#
# Stale check (bite 3 "Done (Test)"): regenerate into memory and diff against the
# committed JSON. Any mismatch on label, class, location, or bounds fails. Run it
# with -check appended to the -run=pythonscript arguments:
#     UnrealEditor-Cmd.exe <uproject> -run=pythonscript \
#         -script=<...>/level_manifest.py -check -unattended ...
#
# Rerun after every level merge. The map is LFS-backed, so "stale" is a field
# mismatch and never a .umap mtime.
#
# Idempotent: rerunning on an unchanged level rewrites the same bytes. No
# volatile fields (no timestamp, no host, no map mtime) are emitted, so a diff
# of the committed file shows only real level changes.

import json
import os
import sys

try:
    import unreal
except ImportError:
    unreal = None

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))

LEVEL_NAME = "L_VS_MVP_Markers"
LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/" + LEVEL_NAME
MANIFEST_RELPATH = os.path.join("Docs", "level", LEVEL_NAME + "_manifest.json")
MANIFEST_ABSPATH = os.path.join(_REPO_ROOT, MANIFEST_RELPATH)
SCHEMA = "homeworld.level_manifest.v1"

# 1 cm resolution. Actor transforms and bounds are float32 in the map, so 0.1 cm
# is far finer than the map can change without the value visibly moving, and it
# keeps a regenerated dump byte-identical when nothing actually changed.
ROUND_DP = 1

# "What sits under it" is a ground-plane question, so a level-spanning container
# is one whose XY footprint already holds nearly every actor: the ground plate
# and the landscape do that, and listing them would repeat the same hundred
# entries in a hundred rows while saying nothing. Judged by XY coverage, not box
# volume — a 1200 m x 860 m plate only 40 cm thick is a fraction of a percent of
# the level union by volume yet spans the entire floor, so a volume rule misses
# exactly the actor it was written for. Excluded containers are named in the
# manifest so nothing is hidden.
SPANNING_COVERAGE = 0.8

# Actors that own no geometry report a zero extent. Recording them as real boxes
# would make "contains" true for every point that happens to coincide, so they are
# recorded with null bounds and excluded from containment.
_EPS = 0.5


def _log(msg):
    if unreal:
        unreal.log("level_manifest: " + str(msg))
    else:
        print("level_manifest: " + str(msg))


def _r(v):
    return round(float(v), ROUND_DP)


def _v3(v):
    return {"x": _r(v.x), "y": _r(v.y), "z": _r(v.z)}


def _min_c(o, e):
    return {"x": _r(o.x - abs(e.x)), "y": _r(o.y - abs(e.y)), "z": _r(o.z - abs(e.z))}


def _max_c(o, e):
    return {"x": _r(o.x + abs(e.x)), "y": _r(o.y + abs(e.y)), "z": _r(o.z + abs(e.z))}


def _has_bounds(b):
    if not b:
        return False
    e = b["extent"]
    return abs(e["x"]) > _EPS or abs(e["y"]) > _EPS or abs(e["z"]) > _EPS


def _contains(b, p):
    """True if world point p is inside axis-aligned box b. Bounds only, no trace."""
    lo = b["min"]
    hi = b["max"]
    return (lo["x"] - _EPS <= p["x"] <= hi["x"] + _EPS
            and lo["y"] - _EPS <= p["y"] <= hi["y"] + _EPS
            and lo["z"] - _EPS <= p["z"] <= hi["z"] + _EPS)


def _contains_xy(b, p):
    """True if p's ground position is inside b's footprint, ignoring Z."""
    lo = b["min"]
    hi = b["max"]
    return (lo["x"] - _EPS <= p["x"] <= hi["x"] + _EPS
            and lo["y"] - _EPS <= p["y"] <= hi["y"] + _EPS)


def _box_volume(b):
    d = b["max"]["x"] - b["min"]["x"]
    w = b["max"]["y"] - b["min"]["y"]
    h = b["max"]["z"] - b["min"]["z"]
    return max(0.0, d) * max(0.0, w) * max(0.0, h)


def _union_box(boxes):
    if not boxes:
        return None
    return {
        "min": {"x": min(b["min"]["x"] for b in boxes),
                "y": min(b["min"]["y"] for b in boxes),
                "z": min(b["min"]["z"] for b in boxes)},
        "max": {"x": max(b["max"]["x"] for b in boxes),
                "y": max(b["max"]["y"] for b in boxes),
                "z": max(b["max"]["z"] for b in boxes)},
    }


def _level_bounds(actors):
    """The level's overall box: the union of every actor box that has one.
    Used only as the denominator for the spanning-volume threshold, so the plain
    union is the honest measure rather than any single actor's box."""
    boxes = [a["bounds"] for a in actors if a["bounds"]]
    if not boxes:
        return None
    union = _union_box(boxes)
    return {"min": union["min"], "max": union["max"], "volume": _box_volume(union)}


def _subsystem(cls_name):
    """Return the named editor subsystem, or None. UE 5.8: the subsystems replace
    the deprecated EditorLevelLibrary helpers."""
    try:
        if not hasattr(unreal, "get_editor_subsystem"):
            return None
        cls = getattr(unreal, cls_name, None)
        if cls is None:
            return None
        return unreal.get_editor_subsystem(cls)
    except Exception:
        return None


def _load_level():
    """Load LEVEL_PATH. LevelEditorSubsystem first; EditorLevelLibrary as fallback
    so the script still runs if the subsystem is unavailable."""
    sub = _subsystem("LevelEditorSubsystem")
    if sub is not None and hasattr(sub, "load_level"):
        try:
            if sub.load_level(LEVEL_PATH):
                return True
        except Exception as e:
            _log_warning_note("LevelEditorSubsystem.load_level: " + str(e))
    try:
        if unreal.EditorLevelLibrary.load_level(LEVEL_PATH):
            return True
    except Exception as e:
        _log_warning_note("EditorLevelLibrary.load_level: " + str(e))
    return False


def _get_world():
    sub = _subsystem("UnrealEditorSubsystem")
    if sub is not None and hasattr(sub, "get_editor_world"):
        try:
            w = sub.get_editor_world()
            if w:
                return w
        except Exception:
            pass
    try:
        return unreal.EditorLevelLibrary.get_editor_world()
    except Exception:
        return None


def _all_level_actors():
    """Every actor in the level. EditorActorSubsystem first; EditorLevelLibrary as
    fallback. UNVERIFIED is reported rather than silently yielding an empty list,
    because an empty manifest reads exactly like a level that contains nothing."""
    sub = _subsystem("EditorActorSubsystem")
    if sub is not None and hasattr(sub, "get_all_level_actors"):
        try:
            actors = list(sub.get_all_level_actors())
            _log("actors via EditorActorSubsystem: " + str(len(actors)))
            return actors
        except Exception as e:
            _log_warning_note("EditorActorSubsystem.get_all_level_actors: " + str(e))
    actors = list(unreal.EditorLevelLibrary.get_all_level_actors())
    _log("actors via EditorLevelLibrary: " + str(len(actors)))
    return actors


def _box_is_empty(box):
    """True if a World Partition probe returned a box with no extent.

    The library returns a non-None but zero box for a level with no loaded WP data.
    Content/Python/level_loader.py:262 already treats zero extent as 'not available',
    and accepting a zero box as proof that World Partition is active would stamp a
    false 'yes' into the one file whose whole purpose is being trustworthy."""
    if box is None:
        return True
    lo = box["min"]
    hi = box["max"]
    return (abs(hi["x"] - lo["x"]) <= _EPS
            and abs(hi["y"] - lo["y"]) <= _EPS
            and abs(hi["z"] - lo["z"]) <= _EPS)


def _probe_world_partition(world):
    """Measure, do not assume. Returns (state, box, evidence).

    state is True (World Partition confirmed by a non-empty bounds box), False (a
    library answered with nothing), or "unknown" (no probe answered at all). Every
    raw result comes back as evidence, so a reader can see what was measured
    instead of taking this script's word for it.

    Bite 3's value is that a reader can trust this file, and a World Partition level
    that loaded only some cells would silently under-report.
    docs/KNOWN_ERRORS.md records exactly that failure: a headless commandlet
    reported 14 actors for a level with 1,270 external actor files behind it."""
    evidence = []
    if world is None:
        return "unknown", None, ["no editor world"]

    lib = getattr(unreal, "WorldPartitionBlueprintLibrary", None)
    if lib is not None:
        # The editor-world variant takes no arguments and uses the context world in
        # UE 5.8; the runtime variant takes one. Trying both signatures beats
        # assuming, and TypeError means the signature is wrong, not the world.
        attempts = []
        if hasattr(lib, "get_editor_world_bounds"):
            attempts.append(("get_editor_world_bounds(world)",
                             lambda: lib.get_editor_world_bounds(world)))
            attempts.append(("get_editor_world_bounds()",
                             lambda: lib.get_editor_world_bounds()))
        if hasattr(lib, "get_runtime_world_bounds"):
            attempts.append(("get_runtime_world_bounds(world)",
                             lambda: lib.get_runtime_world_bounds(world)))
        for name, attempt in attempts:
            try:
                box = attempt()
            except TypeError as e:
                evidence.append(name + ": signature mismatch (" + str(e) + ")")
                continue
            except Exception as e:
                evidence.append(name + ": raised " + str(e))
                continue
            parsed = _parse_box(box)
            if parsed is None:
                evidence.append(name + ": None")
            elif _box_is_empty(parsed):
                evidence.append(name + ": zero-extent box, no loaded WP data")
            else:
                evidence.append(name + ": non-empty box")
                return True, parsed, evidence

    try:
        if hasattr(world, "get_world_partition"):
            wp = world.get_world_partition()
            evidence.append("world.get_world_partition(): " + repr(wp))
            if wp is not None:
                return True, None, evidence
            return False, None, evidence
    except Exception as e:
        evidence.append("world.get_world_partition(): raised " + str(e))

    if any(e.endswith(": non-empty box") or e.endswith(": non-empty box")
           or "non-empty box" in e for e in evidence):
        return True, None, evidence
    if any(e.endswith(": None") for e in evidence):
        return False, None, evidence
    return "unknown", None, evidence


def _count_external_actor_files():
    """How many external actor files this level has on disk.

    This is the completeness evidence, and it is measured rather than assumed.
    World Partition stores a level's actors as per-cell files under
    Content/__ExternalActors__/<...>/<MapName>/ rather than inside the .umap. Zero
    files means every actor is inline in the map, so an inline enumeration cannot be
    short. A non-zero count next to a low actor total would mean cells never loaded
    and the manifest would be incomplete.

    Returns (count, directory, directory_exists)."""
    root = os.path.join(_REPO_ROOT, "Content", "__ExternalActors__",
                        "HomeWorld", "Maps", LEVEL_NAME)
    if not os.path.isdir(root):
        return 0, root, False
    total = 0
    for _dirpath, _dirnames, filenames in os.walk(root):
        total += sum(1 for f in filenames if f.endswith(".uasset"))
    return total, root, True


def _parse_box(box):
    """Convert a UE box to {min, max} in cm, or None if the shape is unfamiliar."""
    if box is None:
        return None
    if hasattr(box, "min") and hasattr(box, "max"):
        return {"min": _v3(box.min), "max": _v3(box.max)}
    if hasattr(box, "center") and hasattr(box, "extent"):
        c = box.center
        e = box.extent
        cx, cy, cz = _v3(c).values()
        ex, ey, ez = _v3(e).values()
        return {"min": {"x": cx - abs(ex), "y": cy - abs(ey), "z": cz - abs(ez)},
                "max": {"x": cx + abs(ex), "y": cy + abs(ey), "z": cz + abs(ez)}}
    return None


def _open_level():
    """Load LEVEL_PATH and wait for its actors to appear. Returns True if loaded."""
    _load_level()
    for _ in range(40):
        world = _get_world()
        if world is not None:
            path = ""
            try:
                path = world.get_path_name().split(".")[0]
            except Exception:
                path = ""
            if LEVEL_NAME in path:
                _log("level open: " + path)
                return world
        _sleep(0.25)
    raise RuntimeError("could not open " + LEVEL_PATH)


def _log_warning_note(msg):
    if unreal:
        unreal.log_warning("level_manifest: " + msg)
    else:
        print("level_manifest: WARNING " + msg)


def _sleep(sec):
    try:
        import time
        time.sleep(sec)
    except Exception:
        pass


def _actor_class_name(actor):
    try:
        return str(actor.get_class().get_name())
    except Exception:
        return "?"


def _actor_tags(actor):
    try:
        return sorted(str(t) for t in actor.tags)
    except Exception:
        return []


def _actor_label(actor):
    for attr in ("get_actor_label", "get_name"):
        try:
            value = getattr(actor, attr)()
            if value:
                return str(value)
        except Exception:
            continue
    return str(actor)


def _blueprint_path(actor):
    """The /Game path of the Blueprint this instance came from, when it has one.
    Content-level provenance: 'is this a BP_WoodPile or a bare C++ actor' is the
    question the manifest is read to answer, and the class name alone does not
    answer it."""
    try:
        cls = actor.get_class()
        outer = cls.get_outer()
        while outer is not None:
            name = str(outer.get_name())
            if name.startswith("/Game/") or name.startswith("/Script/"):
                return name
            outer = outer.get_outer()
    except Exception:
        pass
    return None


def collect():
    """Load the level and return the manifest as a plain dict."""
    world = _open_level()
    wp_state, wp_box, wp_evidence = _probe_world_partition(world)
    ext_count, ext_dir, ext_exists = _count_external_actor_files()
    if wp_state is True:
        _log_warning_note(
            "this level uses World Partition, so the actor list may be short of the full "
            "level. Check external_actor_files and counts below before trusting it.")
    _log("world_partition=" + repr(wp_state) + " external_actor_files=" + str(ext_count))

    raw = []
    for actor in _all_level_actors():
        if not actor:
            continue
        try:
            loc = _v3(actor.get_actor_location())
            origin, extent = actor.get_actor_bounds(False)
            bounds = {
                "origin": _v3(origin),
                "extent": _v3(extent),
                "min": _min_c(origin, extent),
                "max": _max_c(origin, extent),
            }
            bounds["volume"] = _box_volume(bounds)
        except Exception as e:
            _log_warning_note("bounds failed for " + _actor_label(actor) + ": " + str(e))
            loc = None
            bounds = None
        if not _has_bounds(bounds):
            bounds = None
        raw.append({
            "label": _actor_label(actor),
            "name": _actor_name(actor),
            "class": _actor_class_name(actor),
            "blueprint": _blueprint_path(actor),
            "path": _asset_path(actor),
            "tags": _actor_tags(actor),
            "location": loc,
            "bounds": bounds,
        })

    # Level-spanning containers: those whose XY footprint already holds nearly every
    # positioned actor. Judged on the floor, because that is the axis "sits under"
    # resolves on, and a thin wide plate spans it while looking tiny by volume.
    placed = [a for a in raw if a["location"]]
    spanning = set()
    for a in raw:
        b = a["bounds"]
        if b and placed:
            hits = sum(1 for p in placed if _contains_xy(b, p["location"]))
            coverage = hits / float(len(placed))
        else:
            coverage = 0.0
        a["container_coverage"] = round(coverage, 4)
        if coverage >= SPANNING_COVERAGE:
            spanning.add(a["label"])

    # Containment: actor B sits under actor A when B's box contains A's location.
    # Point-in-box on the recorded bounds. No trace, no collision query.
    for a in raw:
        under = []
        if a["location"]:
            for b in raw:
                if b is a or not b["bounds"]:
                    continue
                if b["label"] in spanning:
                    continue
                if _contains(b["bounds"], a["location"]):
                    under.append(b["label"])
        a["under"] = sorted(under)

    raw.sort(key=lambda a: (a["class"], a["label"]))

    class_counts = {}
    for a in raw:
        class_counts[a["class"]] = class_counts.get(a["class"], 0) + 1

    level_box = _level_bounds(raw)
    return {
        "schema": SCHEMA,
        "generator": "Content/Python/level_manifest.py",
        "level": {
            "name": LEVEL_NAME,
            "path": LEVEL_PATH,
            "units": "centimetres",
            "rounding_decimals": ROUND_DP,
            "world_partition": wp_state,
            "world_partition_bounds": wp_box,
            "world_partition_probe": wp_evidence,
            "external_actor_files": ext_count,
            "external_actor_dir_exists": ext_exists,
        },
        "completeness": {
            "actors_enumerated": len(raw),
            "external_actor_files": ext_count,
            "verdict": (
                "complete: the level has no external actor files, so every actor is inline "
                "in the .umap and an inline enumeration cannot have missed a cell"
                if ext_count == 0 else
                "INCOMPLETE: " + str(ext_count) + " external actor file(s) exist under " + ext_dir
                + ". World Partition stores actors there, not in the .umap, so " + str(ext_count)
                + " files against " + str(len(raw)) + " enumerated actors means cells were "
                  "never loaded and this list is short"),
        },
        "rules": {
            "bounds_source": "Actor.get_actor_bounds(False) - actor bounds, not traces",
            "under": "labels whose bounds box contains this actor's location point on all three axes",
            "spanning_containers_excluded": (
                "a container whose XY footprint holds " + str(int(SPANNING_COVERAGE * 100))
                + "% or more of the positioned actors is level-spanning (ground plate, "
                + "landscape) rather than 'under it'; every such label is named in "
                + "spanning_containers_excluded so nothing is hidden"),
            "zero_extent_actors": "recorded with null bounds and excluded from containment",
            "container_coverage": "fraction of positioned actors whose XY position falls inside this actor's footprint",
        },
        "level_bounds": {
            "min": level_box["min"],
            "max": level_box["max"],
        } if level_box else None,
        "counts": {
            "actors": len(raw),
            "actors_with_bounds": sum(1 for a in raw if a["bounds"]),
            "actors_without_bounds": sum(1 for a in raw if not a["bounds"]),
            "classes": len(class_counts),
            "positioned": len(placed),
        },
        "spanning_containers_excluded": sorted(spanning),
        "class_counts": [{"class": k, "count": v} for k, v in sorted(class_counts.items())],
        "actors": raw,
    }


def _actor_name(actor):
    try:
        return str(actor.get_name())
    except Exception:
        return ""


def _asset_path(actor):
    try:
        p = str(actor.get_path_name())
        return p.split(".")[0] + ("." + p.split(".")[1] if p.count(".") > 1 else "")
    except Exception:
        return None


# ---------------------------------------------------------------- comparison

def _diff(expected, actual, path="$"):
    """Yield 'path: expected <x>, found <y>' for every leaf that differs.
    List order is significant; dict key order is not."""
    if isinstance(expected, dict) and isinstance(actual, dict):
        for k in sorted(set(expected) | set(actual)):
            if k not in expected:
                yield "%s.%s: absent from the committed file, found %r" % (path, k, actual[k])
            elif k not in actual:
                yield "%s.%s: %r in the committed file, absent from the fresh dump" % (path, k, expected[k])
            else:
                for line in _diff(expected[k], actual[k], "%s.%s" % (path, k)):
                    yield line
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            yield "%s: %d entries committed, %d in the fresh dump" % (path, len(expected), len(actual))
        for i in range(min(len(expected), len(actual))):
            for line in _diff(expected[i], actual[i], "%s[%d]" % (path, i)):
                yield line
        return
    elif expected != actual:
        yield "%s: committed %r, fresh %r" % (path, expected, actual)


def check(fresh):
    """Compare a fresh dump against the committed manifest. Returns (ok, lines)."""
    if not os.path.isfile(MANIFEST_ABSPATH):
        return False, ["manifest missing at " + MANIFEST_RELPATH]
    with open(MANIFEST_ABSPATH, "r", encoding="utf-8") as f:
        committed = json.load(f)
    lines = list(_diff(committed, fresh))
    return (len(lines) == 0), lines


def write(manifest):
    directory = os.path.dirname(MANIFEST_ABSPATH)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    text = json.dumps(manifest, indent=2, sort_keys=False) + "\n"
    with open(MANIFEST_ABSPATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    counts = manifest["counts"]
    _log("wrote " + MANIFEST_RELPATH + " ({} actors, {} classes, {} positioned)".format(
        counts["actors"], counts["classes"], counts["positioned"]))
    return MANIFEST_ABSPATH


def _check_requested():
    for arg in sys.argv[1:]:
        if arg == "-check" or arg == "--check":
            return True
    try:
        line = unreal.SystemLibrary.get_command_line()
    except Exception:
        return False
    return bool(line) and ("-check" in line or "--check" in line)


def main():
    if not unreal:
        _log("unreal module unavailable. Run inside the Editor or via -run=pythonscript.")
        return 2
    try:
        manifest = collect()
    except Exception as e:
        _log_warning_note("collect failed: " + str(e))
        return 3
    if _check_requested():
        ok, lines = check(manifest)
        if ok:
            _log("CHECK PASS " + MANIFEST_RELPATH + " matches the loaded level")
            return 0
        _log_warning_note("CHECK FAIL " + MANIFEST_RELPATH + " is stale: "
                          + str(len(lines)) + " mismatch(es)")
        for line in lines[:80]:
            _log_warning_note("  " + line)
        if len(lines) > 80:
            _log_warning_note("  ... and " + str(len(lines) - 80) + " more")
        return 1
    write(manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())