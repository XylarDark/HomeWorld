# pcg_settings_introspect.py
# Run from Unreal Editor: Tools -> Execute Python Script (or via MCP execute_python_script).
#
# Introspects PCG node settings (Get Landscape Data, Surface Sampler, Static Mesh Spawner)
# and, if the project graph exists, settings from actual graph nodes. Use output to find
# property names for try_set_get_landscape_selector and mesh list automation (see docs/PCG_ELEGANT_SOLUTIONS.md).
# Does not create or save any assets.
# Output: Saved/pcg_settings_introspect_5.7.txt (or similar).
# See docs/PCG_VARIABLES_NO_ACCESS.md.

import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    sys.exit(1)


def _project_saved_dir():
    """Return project Saved directory path."""
    try:
        proj = unreal.Paths.project_dir()
        if proj:
            return os.path.normpath(os.path.join(proj, "Saved"))
    except Exception:
        pass
    try:
        proj = unreal.SystemLibrary.get_project_directory()
        if proj:
            return os.path.normpath(os.path.join(proj, "Saved"))
    except Exception:
        pass
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(script_dir))
    return os.path.join(root, "Saved")


def _introspect_settings(settings, label):
    """For a PCGSettings (or similar) object, try to list and read properties. Returns list of (name, type_str, readable, value_str)."""
    results = []
    if settings is None:
        return results
    # Try dir() and get_editor_property for each non-dunder attribute
    names = set()
    for name in dir(settings):
        if name.startswith("_"):
            continue
        names.add(name)
    # Also try common UE snake_case / C++ style names we care about
    for extra in ("actor_filter", "actor_selector", "component_selector", "component_filter",
                  "b_unbounded", "b_unbound", "unbounded", "sampling_properties", "tag", "selected_tags"):
        names.add(extra)
    for name in sorted(names):
        try:
            if hasattr(settings, "get_editor_property"):
                val = settings.get_editor_property(name)
            else:
                val = getattr(settings, name, None)
            if callable(val):
                continue
            type_str = type(val).__name__
            try:
                value_str = str(val)[:200]
            except Exception:
                value_str = "<cannot repr>"
            results.append((name, type_str, True, value_str))
        except Exception as e:
            results.append((name, "?", False, str(e)[:150]))
    return results


def _introspect_nested(settings, prefix="", depth=0, max_depth=2):
    """Recursively introspect nested structs (e.g. actor_selector) to find tag/selector props. Returns list of (path, type_str, readable, value_str)."""
    results = []
    if settings is None or depth > max_depth:
        return results
    names = set()
    for name in dir(settings):
        if name.startswith("_"):
            continue
        names.add(name)
    for extra in ("actor_selector", "actor_filter", "selector_settings", "tag", "selected_tag", "tag_name", "filter_tag", "landscape_tag", "mesh_selector_parameters", "mesh_entries"):
        names.add(extra)
    for name in sorted(names):
        path = "%s.%s" % (prefix, name) if prefix else name
        try:
            if hasattr(settings, "get_editor_property"):
                val = settings.get_editor_property(name)
            else:
                val = getattr(settings, name, None)
            if callable(val):
                continue
            type_str = type(val).__name__
            try:
                value_str = str(val)[:120]
            except Exception:
                value_str = "<cannot repr>"
            results.append((path, type_str, True, value_str))
            # Recurse into structs that might hold tag/selector/mesh (for Get Landscape Data and Spawner)
            if depth < max_depth and type_str not in ("str", "int", "float", "bool", "NoneType"):
                if any(x in name.lower() for x in ("tag", "selector", "filter", "mesh", "actor", "component", "entry", "parameter")):
                    try:
                        if val is not None and not isinstance(val, (str, int, float, bool)):
                            sub = _introspect_nested(val, path, depth + 1, max_depth)
                            results.extend(sub)
                    except Exception:
                        pass
        except Exception as e:
            results.append((path, "?", False, str(e)[:100]))
    return results


def main():
    lines = []
    lines.append("PCG settings introspection (Python)")
    lines.append("Run from Unreal Editor. No assets created or saved.")
    lines.append("")

    # Get Landscape Data — full dump for actor selector / tag (no-API automation)
    try:
        cls = getattr(unreal, "PCGGetLandscapeSettings", None)
        if cls is not None:
            try:
                settings = cls()
            except Exception:
                settings = None
            if settings is not None:
                lines.append("=== PCGGetLandscapeSettings (all properties) ===")
                for name, type_str, readable, value_str in _introspect_settings(settings, "GetLandscape"):
                    lines.append("  %s: type=%s readable=%s value=%s" % (name, type_str, readable, value_str))
                lines.append("  --- nested (actor/selector/tag) ---")
                for path, type_str, readable, value_str in _introspect_nested(settings, "GetLandscape", 0, max_depth=3):
                    lines.append("  %s: type=%s readable=%s value=%s" % (path, type_str, readable, value_str))
                lines.append("")
            else:
                lines.append("=== PCGGetLandscapeSettings: could not instantiate ===")
                lines.append("")
        else:
            lines.append("=== PCGGetLandscapeSettings: class not found in unreal ===")
            lines.append("")
    except Exception as e:
        lines.append("=== PCGGetLandscapeSettings error: %s ===" % e)
        lines.append("")

    # Surface Sampler
    try:
        cls = getattr(unreal, "PCGSurfaceSamplerSettings", None)
        if cls is not None:
            try:
                settings = cls()
            except Exception:
                settings = None
            if settings is not None:
                lines.append("=== PCGSurfaceSamplerSettings ===")
                for name, type_str, readable, value_str in _introspect_settings(settings, "SurfaceSampler"):
                    lines.append("  %s: type=%s readable=%s value=%s" % (name, type_str, readable, value_str))
                lines.append("")
            else:
                lines.append("=== PCGSurfaceSamplerSettings: could not instantiate ===")
                lines.append("")
        else:
            lines.append("=== PCGSurfaceSamplerSettings: class not found in unreal ===")
            lines.append("")
    except Exception as e:
        lines.append("=== PCGSurfaceSamplerSettings error: %s ===" % e)
        lines.append("")

    # PCGComponent (graph property)
    try:
        cls = getattr(unreal, "PCGComponent", None)
        if cls is not None:
            try:
                comp = cls()
            except Exception:
                comp = None
            if comp is not None:
                lines.append("=== PCGComponent (sample) ===")
                for name, type_str, readable, value_str in _introspect_settings(comp, "PCGComponent"):
                    if "graph" in name.lower():
                        lines.append("  %s: type=%s readable=%s value=%s" % (name, type_str, readable, value_str))
                lines.append("")
            else:
                lines.append("=== PCGComponent: could not instantiate ===")
                lines.append("")
        else:
            lines.append("=== PCGComponent: class not found ===")
            lines.append("")
    except Exception as e:
        lines.append("=== PCGComponent error: %s ===" % e)
        lines.append("")

    # PCGStaticMeshSpawnerSettings and PCGStaticMeshSpawnerEntry (for mesh list automation) — full dump
    try:
        spawner_cls = getattr(unreal, "PCGStaticMeshSpawnerSettings", None)
        entry_cls = getattr(unreal, "PCGStaticMeshSpawnerEntry", None)
        lines.append("=== PCGStaticMeshSpawner (all properties for mesh list) ===")
        lines.append("  PCGStaticMeshSpawnerSettings: %s" % ("found" if spawner_cls else "NOT in unreal"))
        lines.append("  PCGStaticMeshSpawnerEntry: %s" % ("found" if entry_cls else "NOT in unreal"))
        if spawner_cls is not None:
            try:
                settings = spawner_cls()
            except Exception:
                settings = None
            if settings is not None:
                for name, type_str, readable, value_str in _introspect_settings(settings, "Spawner"):
                    lines.append("  %s: type=%s readable=%s value=%s" % (name, type_str, readable, value_str))
                lines.append("  --- nested (mesh/selector/entries) ---")
                for path, type_str, readable, value_str in _introspect_nested(settings, "Spawner", 0, max_depth=3):
                    lines.append("  %s: type=%s readable=%s value=%s" % (path, type_str, readable, value_str))
        lines.append("")
    except Exception as e:
        lines.append("=== PCGStaticMeshSpawner error: %s ===" % e)
        lines.append("")

    # Load ForestIsland_PCG and introspect actual node settings (real property names)
    graph_path = "/Game/HomeWorld/PCG/ForestIsland_PCG"
    try:
        if unreal.EditorAssetLibrary.does_asset_exist(graph_path):
            graph_asset = unreal.load_asset(graph_path)
            if graph_asset is not None:
                lines.append("=== Graph nodes from %s ===" % graph_path)
                nodes = getattr(graph_asset, "nodes", None) or []
                get_landscape_cls = getattr(unreal, "PCGGetLandscapeSettings", None)
                spawner_cls = getattr(unreal, "PCGStaticMeshSpawnerSettings", None)
                for node in nodes:
                    try:
                        settings = node.get_settings() if hasattr(node, "get_settings") else None
                        if settings is None:
                            continue
                        cls_name = type(settings).__name__
                        lines.append("  --- Node settings: %s ---" % cls_name)
                        for path, type_str, readable, value_str in _introspect_nested(settings, cls_name):
                            lines.append("    %s: type=%s readable=%s value=%s" % (path, type_str, readable, value_str))
                        if get_landscape_cls and isinstance(settings, get_landscape_cls):
                            lines.append("  (Use above to add tag/selector props to try_set_get_landscape_selector)")
                        if spawner_cls and isinstance(settings, spawner_cls):
                            lines.append("  (Use above for mesh_entries / mesh_selector_parameters)")
                    except Exception as e:
                        lines.append("  Node error: %s" % (str(e)[:100]))
                lines.append("")
        else:
            lines.append("=== Graph %s not found (run create_demo_from_scratch once to create it) ===" % graph_path)
            lines.append("")
    except Exception as e:
        lines.append("=== Graph introspection error: %s ===" % e)
        lines.append("")

    out_dir = _project_saved_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "pcg_settings_introspect_5.7.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    unreal.log("PCG introspect: wrote %s" % out_path)
    print("PCG introspect: wrote %s" % out_path)


if __name__ == "__main__":
    main()
