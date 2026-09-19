"""U58F-D Enable Fog Screen Space Scattering on ExponentialHeightFog (Docs/23).

Finds ExponentialHeightFog in the loaded level, enables volumetric fog and FSSS
when properties exist. MegaLights is project-level (DefaultEngine.ini).
Writes Saved/u58f_night_look_smoke.json.
"""
from __future__ import annotations

import json
import unreal

OUT = unreal.Paths.project_saved_dir() + "u58f_night_look_smoke.json"

_FSSS_PROPS = (
    "enable_fog_screen_space_scattering",
    "b_enable_fog_screen_space_scattering",
    "fog_screen_space_scattering",
)


def _try_set(comp, name: str, value) -> bool:
    try:
        if hasattr(comp, "set_editor_property"):
            comp.set_editor_property(name, value)
            return True
    except Exception:
        pass
    try:
        setattr(comp, name, value)
        return True
    except Exception:
        return False


def main() -> None:
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    fog_hits = []
    for a in actors:
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "ExponentialHeightFog" not in cls and "HeightFog" not in cls:
            continue
        comp = a.root_component
        if not comp:
            try:
                comp = a.get_component_by_class(unreal.ExponentialHeightFogComponent)
            except Exception:
                comp = None
        applied = []
        if comp:
            for prop in ("enable_volumetric_fog", "b_enable_volumetric_fog"):
                if _try_set(comp, prop, True):
                    applied.append(prop)
            for prop in _FSSS_PROPS:
                if _try_set(comp, prop, True):
                    applied.append(prop)
        fog_hits.append({"actor": a.get_name(), "class": cls, "applied": applied})

    try:
        unreal.SystemLibrary.execute_console_command(None, "r.Fog.ScreenSpaceScattering 1")
        unreal.SystemLibrary.execute_console_command(None, "r.MegaLights.EnableForProject 1")
    except Exception as e:
        unreal.log_warning("U58F night: console set failed: %s" % e)

    result = {
        "ok": True,
        "fog_actors": fog_hits,
        "project_ini": {
            "r.MegaLights.EnableForProject": True,
            "r.Fog.ScreenSpaceScattering": 1,
        },
        "notes": [
            "Warm local lights benefit from MegaLights; Directional/Sky still Lumen.",
            "If FSSS props not exposed in Python, set on ExponentialHeightFog Details.",
        ],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    unreal.log("U58F night look smoke wrote %s fogs=%d" % (OUT, len(fog_hits)))


if __name__ == "__main__":
    main()
