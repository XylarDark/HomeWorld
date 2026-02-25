# pcg_settings_introspect.py
# Run from Unreal Editor: Tools -> Execute Python Script (or via MCP execute_python_script).
#
# Introspects PCG node settings (Get Landscape Data, Surface Sampler) to see which
# properties Python can read/write. Does not create or save any assets.
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


def main():
    lines = []
    lines.append("PCG settings introspection (Python)")
    lines.append("Run from Unreal Editor. No assets created or saved.")
    lines.append("")

    # Get Landscape Data
    try:
        cls = getattr(unreal, "PCGGetLandscapeSettings", None)
        if cls is not None:
            try:
                settings = cls()
            except Exception:
                settings = None
            if settings is not None:
                lines.append("=== PCGGetLandscapeSettings ===")
                for name, type_str, readable, value_str in _introspect_settings(settings, "GetLandscape"):
                    lines.append("  %s: type=%s readable=%s value=%s" % (name, type_str, readable, value_str))
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

    out_dir = _project_saved_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "pcg_settings_introspect_5.7.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    unreal.log("PCG introspect: wrote %s" % out_path)
    print("PCG introspect: wrote %s" % out_path)


if __name__ == "__main__":
    main()
