# pcg_generate_nothing_diagnostic.py
# Diagnostic for "Generate produces nothing". Run from Editor (Tools -> Execute Python Script or MCP).
# Checks: graph on volume, landscape tag, landscape/proxy components (WP), volume bounds, mesh assets.
# When root has 0 components and proxies have components, calls ensure_landscape_has_pcg_tag() to tag all loaded proxies.
# After running, click Generate; check Output Log for LogPCG and "No surfaces found" if still failing.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run inside Unreal Editor.")
    exit(1)


def _find_pcg_volume(world):
    try:
        volumes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.PCGVolume)
        for vol in (volumes or []):
            try:
                tags = getattr(vol, "tags", [])
                if not hasattr(tags, "__iter__"):
                    tags = vol.get_editor_property("tags") if hasattr(vol, "get_editor_property") else []
                tag_strs = [str(t) for t in tags] if tags else []
                if "PCG_Exclusion" not in tag_strs:
                    return vol
            except Exception:
                return vol
    except Exception:
        pass
    return None


def main():
    world = unreal.EditorLevelLibrary.get_editor_world() if hasattr(unreal, "EditorLevelLibrary") else None
    if not world:
        unreal.log("PCG diagnostic: No editor world.")
        return

    # C: Graph assigned to volume?
    volume = _find_pcg_volume(world)
    graph_assigned = None
    graph_path = ""
    if volume:
        comp = volume.get_component_by_class(unreal.PCGComponent) if hasattr(volume, "get_component_by_class") else None
        if comp:
            g = None
            for prop in ("generation_graph", "graph", "generated_graph"):
                try:
                    if hasattr(comp, "get_editor_property"):
                        g = comp.get_editor_property(prop)
                    else:
                        g = getattr(comp, prop, None)
                    if g is not None and str(g) != "None":
                        break
                except Exception:
                    continue
            graph_assigned = g is not None and str(g) != "None"
            graph_path = (g.get_path_name() if g and hasattr(g, "get_path_name") else str(g))[:120]
        else:
            graph_path = "no PCGComponent"
    else:
        graph_path = "no volume"

    # D: Landscape tag and component count (0 = WP cells not loaded, or components on proxies only)
    landscapes = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Landscape) if world else []
    land = landscapes[0] if landscapes else None
    has_tag = False
    comp_count = 0
    proxy_count = 0
    proxy_component_total = 0
    if land:
        try:
            tags = getattr(land, "tags", []) or (land.get_editor_property("tags") if hasattr(land, "get_editor_property") else [])
            tag_strs = [str(t) for t in tags] if tags else []
            has_tag = "PCG_Landscape" in tag_strs
        except Exception:
            pass
        try:
            comp_class = getattr(unreal, "LandscapeComponent", None)
            if comp_class and hasattr(land, "get_components_by_class"):
                comp_count = len(land.get_components_by_class(comp_class))
        except Exception:
            pass
    # H6: In WP, components may be on LandscapeStreamingProxy only; Get Landscape Data may not see them
    try:
        proxy_class = getattr(unreal, "LandscapeStreamingProxy", None)
        if proxy_class and world:
            proxies = unreal.GameplayStatics.get_all_actors_of_class(world, proxy_class)
            proxy_count = len(proxies) if proxies else 0
            comp_class = getattr(unreal, "LandscapeComponent", None)
            if comp_class and proxies:
                for px in proxies[:20]:
                    if hasattr(px, "get_components_by_class"):
                        proxy_component_total += len(px.get_components_by_class(comp_class))
    except Exception:
        pass

    # B: Do mesh assets exist?
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "pcg_forest_config.json")
    mesh_paths = []
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        mesh_paths = list(cfg.get("static_mesh_spawner_meshes") or [])[:4]
    except Exception:
        pass
    registry = unreal.AssetRegistryHelpers.get_asset_registry() if hasattr(unreal, "AssetRegistryHelpers") else None
    existing = 0
    if registry and mesh_paths:
        for path in mesh_paths:
            try:
                obj = registry.get_asset_by_object_path(path)
                if obj and obj.is_valid():
                    existing += 1
            except Exception:
                pass

    if comp_count == 0 and proxy_component_total > 0:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            import create_pcg_forest
            import importlib
            importlib.reload(create_pcg_forest)
            create_pcg_forest.ensure_landscape_has_pcg_tag()
            unreal.log("PCG diagnostic: applied WP fix (tag all loaded LandscapeStreamingProxy(s) with PCG_Landscape). Click Generate on PCG_Forest.")
        except Exception as e:
            unreal.log("PCG diagnostic: could not apply WP tag fix: %s" % e)

    msg = "PCG diagnostic: graph_assigned=%s, landscape_tag=%s, landscape_components=%d, meshes_in_registry=%d/%d." % (graph_assigned, has_tag, comp_count, existing, len(mesh_paths))
    if comp_count == 0 and proxy_component_total > 0:
        msg += " Applied WP fix: tagged all loaded LandscapeStreamingProxy(s) with PCG_Landscape. Click Generate."
    elif comp_count == 0:
        msg += " landscape_components=0: load the World Partition region, then run this diagnostic again to apply proxy tag fix, then click Generate."
    else:
        msg += " Click Generate then check Output Log for LogPCG and 'No surfaces found'."
    unreal.log(msg)


if __name__ == "__main__":
    main()
