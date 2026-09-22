# vs_mvp_ds_visual_helpers.py — DS-A shared visuals (engine primitives, KEEP-LOCAL level markers).
# Used by place_vs_mvp_gc_craft.py and place_vs_mvp_gc_placeholders.py.

from __future__ import annotations

try:
    import unreal
except ImportError:
    unreal = None  # type: ignore

PREFIX = "DS-Visual:"
COTTAGE_LABEL = "GP_Demo_Cottage"
COTTAGE_TAG = "DS_Demo_Cottage"
CUBE = "/Engine/BasicShapes/Cube.Cube"


def log(msg: str) -> None:
    if unreal:
        unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def load_mesh(path: str):
    if not unreal:
        return None
    try:
        return unreal.load_asset(path)
    except Exception:
        return None


def find_actor_by_label(label: str):
    if not unreal:
        return None
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def _ensure_tag(actor, tag_name: str) -> None:
    if not actor:
        return
    try:
        tags = list(actor.get_editor_property("tags") or [])
        name = unreal.Name(tag_name)
        if name not in tags:
            tags.append(name)
            actor.set_editor_property("tags", tags)
    except Exception as exc:
        log("tag warn " + tag_name + ": " + str(exc))


def _set_hidden_in_game(actor, hidden: bool) -> None:
    if not actor:
        return
    for fn_name in ("set_actor_hidden_in_game", "set_is_hidden_ed", "set_hidden"):
        fn = getattr(actor, fn_name, None)
        if not fn:
            continue
        try:
            fn(hidden)
            log(("hide " if hidden else "show ") + "via " + fn_name)
            return
        except Exception:
            continue
    try:
        actor.set_editor_property("hidden", hidden)
    except Exception as exc:
        log("hidden warn: " + str(exc))


def ensure_cottage_blockout(base: unreal.Vector, offset: unreal.Vector) -> bool:
    """Idempotent GP_Demo_Cottage shell — hidden until PROGRESS:COTTAGE_UNLOCK reveals it."""
    if not unreal:
        return False
    loc = base + offset
    existing = find_actor_by_label(COTTAGE_LABEL)
    if existing:
        existing.set_actor_location(loc, False, True)
        _ensure_tag(existing, COTTAGE_TAG)
        _ensure_tag(existing, COTTAGE_LABEL)
        _set_hidden_in_game(existing, True)
        log("reuse " + COTTAGE_LABEL + " (hidden until unlock)")
        return True

    mesh = load_mesh(CUBE)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc, unreal.Rotator(0, 0, 0))
    if not actor:
        log("FAIL spawn " + COTTAGE_LABEL)
        return False
    try:
        actor.set_actor_label(COTTAGE_LABEL)
    except Exception:
        pass
    _ensure_tag(actor, COTTAGE_TAG)
    _ensure_tag(actor, COTTAGE_LABEL)
    smc = actor.get_component_by_class(unreal.StaticMeshComponent)
    if smc and mesh:
        if hasattr(smc, "set_static_mesh"):
            smc.set_static_mesh(mesh)
        else:
            smc.set_editor_property("static_mesh", mesh)
        try:
            actor.set_actor_scale3d(unreal.Vector(3.5, 2.8, 2.2))
        except Exception:
            smc.set_world_scale3d(unreal.Vector(3.5, 2.8, 2.2))
    _set_hidden_in_game(actor, True)
    try:
        actor.set_folder_path("VS_MVP/Markers/DS_DemoSpine")
    except Exception:
        pass
    log("spawn " + COTTAGE_LABEL + " blockout (hidden until unlock)")
    return True


def refresh_craft_station_visual(actor) -> None:
    """Editor hint: craft stations get runtime DS-A meshes from C++ BeginPlay."""
    if not actor:
        return
    try:
        actor.set_editor_property("station_kind", actor.get_editor_property("station_kind"))
    except Exception:
        pass
    log("craft station " + str(actor.get_actor_label()) + " — PIE applies DS-A mesh/label")
