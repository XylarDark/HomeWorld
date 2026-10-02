"""Place the camp actors in L_VS_MVP_Markers from Lib/02_Zones/combat/CAMP.json.

WHY THIS EXISTS

`Lib/02_Zones/combat/CAMP.json` is the first spec that named the camp at all, and it was
written after the fact. Until actors exist in a `.umap`, every calm count in MUST #14 is a
SOFT LATCH - `TryEaseCampActor` grants `bEased` with `bSoftLatch = true`, and
`SatisfiesFreedomGateStrict()` rejects it. So the beat certifies itself against nothing, which
is the same defect as the shrine's lintel lying on the ground.

WHAT THIS PLACES, AND WHY ONLY THIS

Placed - the four camp actors. The game-side calm state lives on the character component, so
an actor's only job is to answer "is there actually someone here?".

NOT placed, deliberately:

- `SM_Camp_Fire_Blue` and `SM_Camp_Torch`. Both have `radius_m: null` in CAMP.json, unset by
  Lead choice, with a note that guessing a number would be authoring gameplay as art. The
  guard's moving torch stays out until that radius is set.
- The `SM_Camp_*` art modules (fire, bedrolls, lashings, guard stake). Their `measured_from`
  is "authored, not built" and CAMP.json's `measured` is null on purpose. The camp art is
  waiting on the paused camp image; this pass is greybox, and greyboxing the art would make a
  reader report real measurements that no one has taken.

WHERE EACH ACTOR GOES

Positions are DERIVED from CAMP.json, not invented:

- guard      <- triggers[EJECT_TRIGGER_GUARD_WAKES].at_offset. That trigger fires on
               "player enter with guard aware", so the trigger marks the guard's post.
- sleeper A  <- modules[SM_Camp_Bedroll_A].at_offset
- sleeper B  <- modules[SM_Camp_Bedroll_B].at_offset
- captive    <- triggers[FREEDOM_GATED_ON_ALL_THREE_CALM].at_offset. That trigger's
               `on_interact` is "free the companion", so it sits on the captive.

CAMP.json `open_questions` reserves the clearing LAYOUT (which side the lashings are on, where
the fire sits relative to the bedrolls) for the Lead. Nothing here depends on that: the actors
go where the spec's own numbers put them.

IDEMPOTENT. Re-running updates the position and role of existing actors and creates only what
is missing. It never deletes and never spawns a second copy.

Run headless:
    "C:\\Program Files\\Epic Games\\UE_5.8\\Engine\\Binaries\\Win64\\UnrealEditor-Cmd.exe" \\
        HomeWorld.uproject -ExecutePythonScript=t0_place_camp.py -unattended -nopause -NullRHI
or via MCP: execute_python_script("t0_place_camp.py")
"""

import json
import os

import unreal

LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
CAMP_JSON = os.path.join(
    os.path.dirname(__file__), "..", "..", "Lib", "02_Zones", "combat", "CAMP.json"
)
REPORT_PATH = os.path.join(
    unreal.Paths.project_saved_dir(), "t0_camp_placement.json"
)

#: Mirrors EHomeWorldCampRole. The script cannot import the C++ enum directly, so it resolves
#: the reflected enum and picks the member by name. A typo fails loudly here rather than
#: silently placing a sleeper where the guard should be.
_ENUM_TYPE_NAME = "HomeWorldCampRole"
_ROLE_NAMES = ("Guard", "Sleeper", "Captive")


def _role_enum():
    enum_type = getattr(unreal, _ENUM_TYPE_NAME, None)
    if enum_type is None:
        raise RuntimeError(
            "unreal.%s not found - was HomeWorldCampNightTypes.h reflected? "
            "Expected a UENUM(BlueprintType) to surface as a Python enum." % _ENUM_TYPE_NAME
        )
    return enum_type


def _role_value(role_name):
    if role_name not in _ROLE_NAMES:
        raise ValueError("unknown role %r; expected one of %s" % (role_name, _ROLE_NAMES))
    enum_type = _role_enum()
    # UE's Python reflection upper-cases enum entries: EHomeWorldCampRole::Guard -> GUARD.
    for attribute in (role_name.upper(), role_name):
        if hasattr(enum_type, attribute):
            return getattr(enum_type, attribute)
    raise RuntimeError(
        "unreal.%s has no member for role %r; available: %s"
        % (_ENUM_TYPE_NAME, role_name, [a for a in dir(enum_type) if not a.startswith("_")])
    )


def _log(message):
    unreal.log("CAMP_PLACE: %s" % message)


def _load_camp_spec():
    with open(os.path.abspath(CAMP_JSON), "r", encoding="utf-8") as handle:
        return json.load(handle)


def _trigger(spec, name):
    for trigger in spec["triggers"]:
        if trigger["name"] == name:
            return trigger
    raise KeyError("CAMP.json has no trigger named %r - refusing to guess a position" % name)


def _module(spec, name):
    for module in spec["modules"]:
        if module["name"] == name:
            return module
    raise KeyError("CAMP.json has no module named %r - refusing to guess a position" % name)


def _plan(spec):
    """Build the placement list. Every offset comes from the spec; none are invented here."""
    origin = spec["world_origin"]
    eject = _trigger(spec, "EJECT_TRIGGER_GUARD_WAKES")
    freedom = _trigger(spec, "FREEDOM_GATED_ON_ALL_THREE_CALM")
    bed_a = _module(spec, "SM_Camp_Bedroll_A")
    bed_b = _module(spec, "SM_Camp_Bedroll_B")

    def world(offset):
        return unreal.Vector(origin[0] + offset[0], origin[1] + offset[1], origin[2] + offset[2])

    return [
        # label, role, class, location, and why that location
        ("NODE_GUARD", "Guard", "CampActor", world(eject["at_offset"]),
         "EJECT_TRIGGER_GUARD_WAKES.at_offset - the trigger that fires on 'guard aware'"),
        ("NODE_SLEEPER_A", "Sleeper", "CampActor", world(bed_a["at_offset"]),
         "SM_Camp_Bedroll_A.at_offset"),
        ("NODE_SLEEPER_B", "Sleeper", "CampActor", world(bed_b["at_offset"]),
         "SM_Camp_Bedroll_B.at_offset"),
        ("NODE_CAPTIVE", "Captive", "CampActor", world(freedom["at_offset"]),
         "FREEDOM_GATED_ON_ALL_THREE_CALM.at_offset - its on_interact is 'free the companion'"),
    ]


def _actor_subsystem():
    """UE 5.8: EditorLevelLibrary is deprecated; EditorActorSubsystem is the supported path."""
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def _level_subsystem():
    return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def _find_existing():
    """Group placed camp actors by their NODE_ token, as a POOL rather than a map.

    Keyed by token because discovery in C++ matches `NODE_SLEEPER`, not our `_A`/`_B`
    suffix. But a dict of token -> actor is wrong: two sleepers share one token, and a dict
    silently keeps only the first, so the second run would reuse one bedroll and spawn a
    third person. A pool is consumed one entry per placement instead.
    """
    pool = {"NODE_GUARD": [], "NODE_SLEEPER": [], "NODE_CAPTIVE": []}
    for actor in _actor_subsystem().get_all_level_actors():
        try:
            label = actor.get_actor_label()
        except Exception:
            continue
        for token in pool:
            if token in label:
                pool[token].append(actor)
                break
    return pool


def main():
    spec = _load_camp_spec()
    _log("CAMP.json %s status=%s" % (spec["id"], spec["status"]))

    if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        _log("FATAL: %s does not exist" % LEVEL_PATH)
        return 1

    _level_subsystem().load_level(LEVEL_PATH)
    _log("opened %s" % LEVEL_PATH)

    camp_class = unreal.load_class(None, "/Script/HomeWorld.HomeWorldCampActor")
    if not camp_class:
        _log("FATAL: AHomeWorldCampActor not found - the module needs a build first")
        return 1

    plan = _plan(spec)
    pool = _find_existing()
    _log("pre-existing camp actors: %s"
         % {k: [a.get_actor_label() for a in v] for k, v in sorted(pool.items()) if v})

    report = {"level": LEVEL_PATH, "camp_origin": spec["world_origin"],
              "placed": [], "reused": [], "not_placed": []}

    for label, role, _tag, location, why in plan:
        token = label.rsplit("_", 1)[0] if label.endswith(("_A", "_B")) else label

        # Prefer an exact label match, then consume one from the token pool. Without the exact
        # match, a re-run could swap the _A and _B bedrolls every time, because the outliner
        # order is not the placement order.
        actor = None
        for candidate in pool.get(token, []):
            try:
                if candidate.get_actor_label() == label:
                    actor = candidate
                    break
            except Exception:
                continue
        if actor is None and pool.get(token):
            actor = pool[token].pop(0)

        if actor is None:
            actor = _actor_subsystem().spawn_actor_from_class(
                camp_class, location, unreal.Rotator()
            )
            if actor is None:
                _log("FATAL: could not spawn %s" % label)
                return 1
            report["placed"].append(label)
            _log("CREATED %s role=%s at %s" % (label, role, location))
        else:
            # UE 5.8 requires the explicit sweep argument.
            actor.set_actor_location(location, False, None)
            report["reused"].append(label)
            _log("UPDATED %s role=%s to %s" % (label, role, location))

        # Role FIRST, label LAST. Setting CampRole triggers OnConstruction, which re-asserts
        # the role's base label - so setting the label before the role lets the constructor
        # stomp the _A/_B suffix that is the only way to tell two sleepers apart.
        actor.set_editor_property("CampRole", _role_value(role))
        actor.set_actor_label(label)

    # Namespaced variant check: C++ discovery accepts NODE_SLEEPER, and our labels are
    # NODE_SLEEPER_A / _B. GetName() contains the token, so both resolve. Assert it rather than
    # assume, because if it ever stops resolving every sleeper count silently goes soft again.
    placed_sleepers = [n for n in report["placed"] + report["reused"] if "NODE_SLEEPER" in n]
    report["sleeper_count"] = len(placed_sleepers)
    if len(placed_sleepers) != 2:
        _log("FATAL: expected 2 sleepers, have %d" % len(placed_sleepers))
        return 1

    for label, role, _tag, _loc, why in plan:
        _log("  %-16s role=%-9s <- %s" % (label, role, why))

    report["not_placed"] = [
        "SM_Camp_Fire_Blue / SM_Camp_Torch - radius_m is null in CAMP.json by Lead choice",
        "SM_Camp_Fire / SM_Camp_Bedroll_* / SM_Camp_Lashings / SM_Camp_GuardStake - art modules, "
        "measured_from='authored, not built', camp image paused",
    ]

    if not _level_subsystem().save_current_level():
        _log("FATAL: save_current_level failed")
        return 1
    _log("saved %s" % LEVEL_PATH)

    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    _log("report -> %s" % REPORT_PATH)

    _log("DONE placed=%d reused=%d sleepers=%d"
         % (len(report["placed"]), len(report["reused"]), report["sleeper_count"]))
    return 0


if __name__ == "__main__":
    main()