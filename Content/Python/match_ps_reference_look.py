# match_ps_reference_look.py
# Idempotent: put the readable light rig on L_VS_MVP_Markers, then aim the
# seven PS capture cameras at the kit the reference plates show.
# Run via MCP execute_python_script("match_ps_reference_look.py").

from __future__ import annotations

import json
import os

import unreal

import pa_e_shotlist_common as common
import vnp_night_tune_and_evidence as night


def _log(msg: str, data=None) -> None:
    line = "PS Reference: " + msg
    if data is not None:
        line += " " + json.dumps(data, default=str)
    unreal.log(line)
    print(line)


def _actors():
    return [a for a in unreal.EditorLevelLibrary.get_all_level_actors() if a]


def _label(actor) -> str:
    return common.actor_label(actor)


def _by_prefix(prefix: str):
    return [a for a in _actors() if _label(a).startswith(prefix)]


def _centroid(actors) -> unreal.Vector | None:
    if not actors:
        return None
    acc = unreal.Vector(0, 0, 0)
    n = 0
    for actor in actors:
        try:
            origin, _extent = actor.get_actor_bounds(False)
        except Exception:
            continue
        acc.x += origin.x
        acc.y += origin.y
        acc.z += origin.z
        n += 1
    if n == 0:
        return None
    return unreal.Vector(acc.x / n, acc.y / n, acc.z / n)


def _aim(label: str, loc: unreal.Vector, target: unreal.Vector) -> bool:
    actor = None
    for candidate in _actors():
        if _label(candidate) == label:
            actor = candidate
            break
    if actor is None:
        _log("camera missing", {"label": label})
        return False
    actor.set_actor_location(loc, False, False)
    try:
        rot = unreal.MathLibrary.find_look_at_rotation(loc, target)
    except Exception:
        rot = unreal.Rotator(pitch=-20.0, yaw=0.0, roll=0.0)
    actor.set_actor_rotation(rot, False)
    _log("aimed", {"label": label, "loc": [loc.x, loc.y, loc.z]})
    return True


def _boost_key_light() -> None:
    """Basic readable key. The preset moon at 3.5 leaves the kit black in editor stills."""
    for actor in _actors():
        label = _label(actor)
        cls = actor.get_class().get_name() if actor.get_class() else ""
        if label == night.TMP_MOON_LABEL or ("DirectionalLight" in cls and "moon" in label.lower()):
            applied = night._configure_directional_moon(actor, intensity=15.0)
            _log("key light", {"label": label, "applied": applied})
        if label == night.TMP_SKY_LABEL or "SkyLight" in cls:
            applied = night._configure_skylight(actor, intensity=3.0, recapture=True)
            _log("skylight", {"label": label, "applied": applied})
    for cmd in (
        "r.DefaultFeature.AutoExposure.Bias 1",
        "r.DefaultFeature.AutoExposure.MinBrightness 0.1",
        "r.DefaultFeature.AutoExposure.MaxBrightness 4",
        "viewmode lit",
    ):
        try:
            unreal.SystemLibrary.execute_console_command(None, cmd)
        except Exception:
            pass


def _shrine_glow(shrine) -> None:
    if shrine is None:
        return
    origin, _extent = shrine.get_actor_bounds(False)
    loc = unreal.Vector(origin.x, origin.y, origin.z + 80.0)
    existing = None
    for actor in _actors():
        if _label(actor) == "lit_shrine_blue":
            existing = actor
            break
    if existing is None:
        existing = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight, loc)
        if existing:
            existing.set_actor_label("lit_shrine_blue")
    if existing is None:
        return
    existing.set_actor_location(loc, False, False)
    comp = existing.get_editor_property("light_component") if hasattr(existing, "light_component") else existing.root_component
    if comp:
        night._try_set(comp, "intensity", 4000.0)
        night._try_set(comp, "light_color", unreal.LinearColor(0.35, 0.65, 1.0, 1.0))
        night._try_set(comp, "attenuation_radius", 600.0)
    _log("shrine glow", {"loc": [loc.x, loc.y, loc.z]})


def main() -> None:
    common.ensure_markers_editor_world("PS Reference")
    dress = _by_prefix(common.DRESS_LABEL_PREFIX)
    pa_d = _by_prefix("PA_D_")
    cabin = next((a for a in dress if "Cabin" in _label(a) and "Pine" not in _label(a)), None)
    island = next((a for a in dress if "IslandTop" in _label(a)), None)
    # Cliff meshes pull a combined centroid far underground. Aim from the cabin.
    center = _centroid([a for a in (cabin, island) if a]) or unreal.Vector(-600.0, -100.0, 150.0)
    if center.z < -200.0:
        center = unreal.Vector(center.x, center.y, 150.0)
    seeded = night.reseed_pa_e_tmp_night_fixtures([center.x, center.y, center.z])
    _boost_key_light()

    planters = [a for a in pa_d if "Planter" in _label(a)]
    stones = [a for a in pa_d if "PathStone" in _label(a)]
    shrine = next((a for a in _actors() if "Shrine" in _label(a)), None)
    cliff = next((a for a in pa_d if "Cliff" in _label(a)), None)
    _shrine_glow(shrine)

    garden = _centroid(planters) or center
    path = _centroid(stones) or center
    cabin_pt = _centroid([cabin]) if cabin else center
    shrine_pt = _centroid([shrine]) if shrine else center
    cliff_pt = _centroid([cliff]) if cliff else center

    aimed = {
        "PS_N_HighIso": _aim(
            "PS_N_HighIso",
            unreal.Vector(center.x, center.y - 2200.0, center.z + 1800.0),
            center,
        ),
        "PS_E_HighIso": _aim(
            "PS_E_HighIso",
            unreal.Vector(center.x + 2200.0, center.y, center.z + 1800.0),
            center,
        ),
        "PS_Cliff_Underside": _aim(
            "PS_Cliff_Underside",
            unreal.Vector(cliff_pt.x - 400.0, cliff_pt.y, cliff_pt.z - 200.0),
            unreal.Vector(cliff_pt.x, cliff_pt.y, cliff_pt.z + 100.0),
        ),
        "PS_Path_Corridor": _aim(
            "PS_Path_Corridor",
            unreal.Vector(path.x - 350.0, path.y, path.z + 140.0),
            unreal.Vector(path.x + 200.0, path.y, path.z + 40.0),
        ),
        "PS_Garden_Close": _aim(
            "PS_Garden_Close",
            unreal.Vector(garden.x - 280.0, garden.y - 220.0, garden.z + 160.0),
            unreal.Vector(garden.x, garden.y, garden.z + 40.0),
        ),
        "CAM_Hero": _aim(
            "CAM_Hero",
            unreal.Vector(center.x + 1400.0, center.y + 200.0, center.z + 280.0),
            cabin_pt,
        ),
        "CAM_CabinClose": _aim(
            "CAM_CabinClose",
            unreal.Vector(cabin_pt.x + 420.0, cabin_pt.y - 80.0, cabin_pt.z + 160.0),
            unreal.Vector(cabin_pt.x, cabin_pt.y, cabin_pt.z + 120.0),
        ),
    }
    stack = night.verify_homestead_night_lighting_stack(_actors())
    _log(
        "match pass",
        {
            "seeded": seeded.get("reason") or seeded.get("skipped"),
            "stack_ok": stack.get("stack_ok"),
            "aimed": aimed,
            "planters": len(planters),
            "path_stones": len(stones),
        },
    )


if __name__ == "__main__":
    main()
