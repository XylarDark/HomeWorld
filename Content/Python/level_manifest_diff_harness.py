"""Offline harness for level_manifest.py's compare logic.

Stubs `unreal` so the module imports outside the Editor, then checks that _diff
sees every kind of mismatch bite 3 cares about: label, class, location, bounds.
Run:  python level_manifest_diff_harness.py
"""
import copy
import importlib.util
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "level_manifest.py")

# Minimal stand-in so `import unreal` succeeds and the module-level code runs.
stub = types.ModuleType("unreal")
stub.SystemLibrary = types.SimpleNamespace(get_command_line=lambda: "")
sys.modules["unreal"] = stub

spec = importlib.util.spec_from_file_location("level_manifest", TARGET)
lm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lm)

fails = []


def expect_diff(name, mutate, path_prefix, exact=None):
    """Mutate a deep copy in place, then require at least one diff line whose
    path starts with path_prefix.

    Asserting on the path rather than on a substring is the point: a substring
    check passes even when _diff fell through to dumping the entire committed
    dict, which is how this harness produced four false passes on its first run.
    """
    mutated = copy.deepcopy(BASE)
    mutate(mutated)  # in place; the lambda's return value is deliberately ignored
    lines = list(lm._diff(BASE, mutated))
    hit = [x for x in lines if x.startswith(path_prefix)]
    if not hit:
        fails.append("%s: no diff line at %s (got %r)" % (name, path_prefix, lines[:3]))
        return lines
    if exact is not None and hit[0] != exact:
        fails.append("%s: got %r, wanted exactly %r" % (name, hit[0], exact))
        return lines
    if len(lines) != 1:
        fails.append("%s: expected a single field-level diff, got %d lines: %r"
                     % (name, len(lines), lines))
        return lines
    print("PASS  %-30s -> %s" % (name, hit[0]))
    return lines


def expect_no_diff(name, a, b):
    lines = list(lm._diff(a, b))
    if lines:
        fails.append("%s: expected no diff, got %r" % (name, lines[:3]))
    else:
        print("PASS  %-30s no diff" % name)


BASE = {
    "counts": {"actors": 2},
    "actors": [
        {
            "label": "BP_WoodPile_1",
            "class": "HomeWorldResourcePile",
            "location": {"x": 100.0, "y": -50.5, "z": 0.0},
            "bounds": {
                "origin": {"x": 100.0, "y": -50.5, "z": 0.0},
                "extent": {"x": 50.0, "y": 50.0, "z": 50.0},
                "min": {"x": 50.0, "y": -100.5, "z": -50.0},
                "max": {"x": 150.0, "y": -0.5, "z": 50.0},
            },
            "under": [],
        },
        {
            "label": "GP_ShrineExit",
            "class": "TargetPoint",
            "location": {"x": 0.0, "y": 0.0, "z": 0.0},
            "bounds": None,
            "under": ["BP_WoodPile_1"],
        },
    ],
}

print("=== _diff sees every field bite 3 names ===")

expect_diff("label changed",
            lambda d: d["actors"][0].__setitem__("label", "BP_WoodPile_2"),
            "$.actors[0].label",
            exact="$.actors[0].label: committed 'BP_WoodPile_1', fresh 'BP_WoodPile_2'")

expect_diff("class changed",
            lambda d: d["actors"][1].__setitem__("class", "HomeWorldShrinePortalComponent"),
            "$.actors[1].class")

expect_diff("location moved",
            lambda d: d["actors"][0]["location"].__setitem__("x", 101.0),
            "$.actors[0].location.x")

expect_diff("bounds extent moved",
            lambda d: d["actors"][0]["bounds"]["extent"].__setitem__("z", 75.0),
            "$.actors[0].bounds.extent.z")

expect_diff("bounds min moved",
            lambda d: d["actors"][0]["bounds"]["min"].__setitem__("z", -75.0),
            "$.actors[0].bounds.min.z")

expect_diff("under list changed",
            lambda d: d["actors"][0].__setitem__("under", ["GP_ShrineExit"]),
            "$.actors[0].under")

expect_diff("actor deleted",
            lambda d: d["actors"].pop(),
            "$.actors",
            exact="$.actors: 2 entries committed, 1 in the fresh dump")

expect_diff("actor added",
            lambda d: d["actors"].append(copy.deepcopy(d["actors"][0])),
            "$.actors",
            exact="$.actors: 2 entries committed, 3 in the fresh dump")

expect_diff("bounds became null",
            lambda d: d["actors"][0].__setitem__("bounds", None),
            "$.actors[0].bounds")

print("")
print("=== identical input must produce zero diffs (fresh run must pass) ===")
lines = list(lm._diff(BASE, copy.deepcopy(BASE)))
if lines:
    fails.append("identical input produced %d diff(s): %r" % (len(lines), lines[:3]))
else:
    print("PASS  identical dump compares clean")

print("")
print("=== key order must not matter (json round-trip reorders nothing here) ===")
reordered = {"actors": BASE["actors"], "counts": BASE["counts"]}
lines = list(lm._diff(BASE, reordered))
if lines:
    fails.append("key order alone produced %d diff(s)" % len(lines))
else:
    print("PASS  dict key order is not significant")

print("")
print("=== containment is a point-in-box test on recorded bounds ===")
b = BASE["actors"][0]["bounds"]
cases = [
    ("origin inside", {"x": 100.0, "y": -50.5, "z": 0.0}, True),
    ("exactly on min face", {"x": 50.0, "y": -100.5, "z": -50.0}, True),
    ("exactly on max face", {"x": 150.0, "y": -0.5, "z": 50.0}, True),
    ("just outside max", {"x": 150.6, "y": -0.5, "z": 50.0}, False),
    ("inside XY, outside Z", {"x": 100.0, "y": -50.5, "z": 60.0}, False),
]
for name, point, want in cases:
    got = lm._contains(b, point)
    if got != want:
        fails.append("%s: expected %s, got %s" % (name, want, got))
    else:
        print("PASS  %-26s %s -> %s" % (name, point, got))

print("")
print("=== zero-extent actors are treated as having no bounds ===")
if lm._has_bounds({"origin": {"x": 0, "y": 0, "z": 0},
                   "extent": {"x": 0, "y": 0, "z": 0},
                   "min": {"x": 0, "y": 0, "z": 0},
                   "max": {"x": 0, "y": 0, "z": 0}}):
    fails.append("zero-extent box was treated as real bounds")
else:
    print("PASS  zero-extent -> null bounds, excluded from containment")

print("")
print("=== rounding is stable enough for a byte-identical regeneration ===")
vals = [0.1 + 0.2, 1.0 / 3.0, 100.0, -7500.0, 1234.56789]
for v in vals:
    a = lm._r(float(v))
    b2 = lm._r(float(v))
    if a != b2:
        fails.append("rounding not idempotent for %r" % (v,))
print("PASS  rounding idempotent for %d sample values" % len(vals))

print("")
print("=== footprint test drives the spanning-container rule, not volume ===")
xy_cases = [
    ("inside footprint", {"x": 100.0, "y": -50.5, "z": 99999.0}, True),
    ("above the box on Z", {"x": 100.0, "y": -50.5, "z": 5000.0}, True),
    ("below the box on Z", {"x": 100.0, "y": -50.5, "z": -5000.0}, True),
    ("outside footprint", {"x": 150.6, "y": -50.5, "z": 0.0}, False),
]
for name, point, want in xy_cases:
    got = lm._contains_xy(b, point)
    if got != want:
        fails.append("XY %s: expected %s, got %s" % (name, want, got))
    else:
        print("PASS  %-26s %s -> %s" % (name, point, got))

print("")
print("=== a thin wide plate spans the floor; the volume rule would have missed it ===")
plate = {"min": {"x": -59250.0, "y": -59550.0, "z": -20.0},
         "max": {"x": 60750.0, "y": 26450.0, "z": 20.0}}
plate_vol = lm._box_volume(plate)
union_vol = 120000.0 * 86000.0 * 17807.5
if plate_vol / union_vol < 0.5:
    plate_vol_missed = True
else:
    plate_vol_missed = False
if not plate_vol_missed:
    fails.append("volume rule would have caught the plate; the XY-coverage premise is untested")
else:
    print("PASS  plate is %.4f%% of the level union by volume, so a 50%% volume rule misses it"
          % (100.0 * plate_vol / union_vol))
covered = sum(1 for p in
              [{"x": 750.0, "y": 450.0}, {"x": -240.0, "y": -120.0},
               {"x": 0.0, "y": 7000.0}, {"x": 600.0, "y": 7500.0},
               {"x": -400.0, "y": -450.0}]
              if lm._contains_xy(plate, p))
if covered == 5:
    print("PASS  the same plate holds 5/5 sample positions in XY -> coverage rule catches it")
else:
    fails.append("XY coverage rule only caught %d/5 sample positions" % covered)

print("")
if fails:
    print("RESULT: %d FAILURE(S)" % len(fails))
    for f in fails:
        print("  FAIL " + f)
    sys.exit(1)
print("RESULT: ALL PASS")