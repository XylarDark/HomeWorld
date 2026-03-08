# place_resource_nodes.py
# Run from Unreal Editor with DemoMap open (Tools -> Execute Python Script or via MCP).
# Reads demo_map_config.json "resource_node_positions" and spawns BP_HarvestableTree at each position (cm).
# Uses resource_nodes_per_biome.json to decide which resource node types apply for the current biome
# (see docs/PLANETOID_BIOMES.md §1.1–§1.2). Placement uses the config for node type/variant selection.
# Idempotent: ensures Building folder exists (via ensure_week2_folders), then skips spawning if an actor
# of the same Blueprint class already exists within RADIUS_CM of that position.
# See docs/tasks/DAY7_RESOURCE_NODES.md.

import json
import os
import sys

try:
    import unreal
except ImportError:
    print("ERROR: Run this script inside Unreal Editor (Python Editor Script Plugin).")
    raise

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

DEMO_LEVEL_SUBPATH = "DemoMap"
BP_HARVESTABLE_TREE_PATH = "/Game/HomeWorld/Building/BP_HarvestableTree"
BP_HARVESTABLE_ORE_PATH = "/Game/HomeWorld/Building/BP_HarvestableOre"
BP_HARVESTABLE_FLOWER_PATH = "/Game/HomeWorld/Building/BP_HarvestableFlower"
RADIUS_CM = 150.0  # consider "already placed" if an instance exists within this distance


def _log(msg):
    unreal.log("Resource nodes: " + str(msg))


def _load_config():
    """Load Content/Python/demo_map_config.json."""
    defaults = {
        "demo_level_path": "/Game/HomeWorld/Maps/DemoMap",
        "resource_node_positions": [],
        "biome": "Forest",
        "alignment": "Neutral",
    }
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "demo_map_config.json")
        if not os.path.exists(config_path):
            return defaults
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        positions = data.get("resource_node_positions")
        if isinstance(positions, list):
            out = []
            for p in positions:
                if isinstance(p, dict) and "x" in p and "y" in p and "z" in p:
                    out.append({"x": float(p["x"]), "y": float(p["y"]), "z": float(p["z"])})
            defaults["resource_node_positions"] = out
        ore_positions = data.get("resource_node_ore_positions")
        if isinstance(ore_positions, list):
            ore_out = []
            for p in ore_positions:
                if isinstance(p, dict) and "x" in p and "y" in p and "z" in p:
                    ore_out.append({"x": float(p["x"]), "y": float(p["y"]), "z": float(p["z"])})
            defaults["resource_node_ore_positions"] = ore_out
        flower_positions = data.get("resource_node_flower_positions")
        if isinstance(flower_positions, list):
            flower_out = []
            for p in flower_positions:
                if isinstance(p, dict) and "x" in p and "y" in p and "z" in p:
                    flower_out.append({"x": float(p["x"]), "y": float(p["y"]), "z": float(p["z"])})
            defaults["resource_node_flower_positions"] = flower_out
        defaults["demo_level_path"] = data.get("demo_level_path", defaults["demo_level_path"])
        defaults["biome"] = data.get("biome", defaults["biome"])
        defaults["alignment"] = data.get("alignment", defaults["alignment"])
        return defaults
    except Exception as e:
        _log("Config load warning: " + str(e))
        return defaults


def _load_resource_nodes_per_biome():
    """Load Content/Python/resource_nodes_per_biome.json for per-biome node types/variants (PLANETOID_BIOMES §1.1–§1.2)."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "resource_nodes_per_biome.json")
        if not os.path.exists(config_path):
            return {}
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        _log("resource_nodes_per_biome load warning: " + str(e))
        return {}


def _load_planetoid_alignments():
    """Load Content/Python/planetoid_alignments.json for alignment-based branching (PLANETOID_BIOMES §3, §3.1)."""
    try:
        proj_dir = unreal.SystemLibrary.get_project_directory()
        config_path = os.path.join(proj_dir, "Content", "Python", "planetoid_alignments.json")
        if not os.path.exists(config_path):
            return {}
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        _log("planetoid_alignments load warning: " + str(e))
        return {}


def _get_editor_world():
    """Editor world; prefer UnrealEditorSubsystem, fallback EditorLevelLibrary."""
    try:
        import level_loader
        return level_loader.get_editor_world()
    except Exception:
        return unreal.EditorLevelLibrary.get_editor_world() if hasattr(unreal, "EditorLevelLibrary") else None


def _save_current_level():
    """Save current level; prefer LevelEditorSubsystem, fallback EditorLevelLibrary."""
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem) if hasattr(unreal, "get_editor_subsystem") else None
        if subsys and hasattr(subsys, "save_current_level"):
            return subsys.save_current_level()
    except Exception:
        pass
    if hasattr(unreal, "EditorLevelLibrary") and hasattr(unreal.EditorLevelLibrary, "save_current_level"):
        unreal.EditorLevelLibrary.save_current_level()
        return True
    return False


def _get_current_level_path():
    """Return the asset path of the current editor level, or None."""
    try:
        world = _get_editor_world()
        if not world:
            return None
        path = world.get_path_name() if hasattr(world, "get_path_name") else ""
        if not path or "." not in path:
            return None
        path = path.split(".")[0]
        if ":" in path:
            path = path.split(":")[0]
        return path if path.startswith("/") else None
    except Exception:
        return None


def _actor_location_cm(actor):
    """Return (x, y, z) in cm or None."""
    try:
        loc = actor.get_actor_location()
        if loc is not None:
            return (loc.x, loc.y, loc.z)
    except Exception:
        pass
    return None


def _distance_cm(a, b):
    """Euclidean distance between (x,y,z) tuples in cm."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def main():
    _log("Starting resource node placement...")
    # Ensure /Game/HomeWorld/Building/ exists so BP_HarvestableTree can be created there
    try:
        import ensure_week2_folders
        ensure_week2_folders.main()
    except Exception as e:
        _log("Could not ensure Building folder: " + str(e))
    config = _load_config()
    demo_path = config.get("demo_level_path", "/Game/HomeWorld/Maps/DemoMap")
    positions = config.get("resource_node_positions", [])
    biome = config.get("biome", "Forest")
    alignment = config.get("alignment", "Neutral")

    # Branch on alignment using planetoid_alignments.json (PLANETOID_BIOMES §3, §3.1)
    alignments_cfg = _load_planetoid_alignments()
    align_entry = alignments_cfg.get(alignment) if isinstance(alignments_cfg, dict) else None
    harvest_rule = align_entry.get("harvest_rule", "full") if isinstance(align_entry, dict) else "full"
    if alignment == "Corrupted" and harvest_rule in ("disabled_or_minimal", "disabled", "minimal"):
        _log("Alignment is Corrupted with harvest_rule=%s; skipping resource node placement (fight zone)." % harvest_rule)
        return
    if align_entry:
        _log("Using planetoid_alignments for alignment: %s (activity_focus=%s, harvest_rule=%s)" % (
            alignment,
            align_entry.get("activity_focus", "—"),
            harvest_rule,
        ))

    # Load per-biome node types so placement uses config (PLANETOID_BIOMES §1.1–§1.2)
    nodes_per_biome = _load_resource_nodes_per_biome()
    biome_entries = nodes_per_biome.get(biome, []) if isinstance(nodes_per_biome, dict) else []
    if biome_entries:
        _log("Using resource_nodes_per_biome for biome: %s (%d node types)" % (biome, len(biome_entries)))
    else:
        _log("No resource_nodes_per_biome entry for biome '%s'; placing with default type." % biome)

    current = _get_current_level_path()
    if not current or DEMO_LEVEL_SUBPATH not in (current or ""):
        _log("Current level is not DemoMap. Open DemoMap and run this script again.")
        return

    if not positions:
        _log("No resource_node_positions in config; add positions to demo_map_config.json.")
        return

    bp_asset = unreal.load_asset(BP_HARVESTABLE_TREE_PATH) if unreal.EditorAssetLibrary.does_asset_exist(BP_HARVESTABLE_TREE_PATH) else None
    if not bp_asset:
        _log("Blueprint not found at " + BP_HARVESTABLE_TREE_PATH + ". Create BP_HarvestableTree per docs/tasks/DAY7_RESOURCE_NODES.md.")
        return

    try:
        actor_class = bp_asset.generated_class() if callable(getattr(bp_asset, "generated_class", None)) else getattr(bp_asset, "generated_class", None)
        if not actor_class:
            actor_class = bp_asset.get_editor_property("generated_class")
    except Exception as e:
        _log("Could not get generated_class from Blueprint: %s. Create BP_HarvestableTree per docs/tasks/DAY7_RESOURCE_NODES.md." % e)
        return
    if not actor_class:
        _log("Could not get generated_class from Blueprint; try spawning manually.")
        return

    world = _get_editor_world()
    if not world:
        _log("No editor world.")
        return

    # Existing actors of this class (for idempotency)
    existing = unreal.GameplayStatics.get_all_actors_of_class(world, actor_class) or []
    existing_locs = []
    for a in existing:
        loc = _actor_location_cm(a)
        if loc:
            existing_locs.append(loc)

    spawned = 0
    for i, pos in enumerate(positions):
        target = (pos["x"], pos["y"], pos["z"])
        if any(_distance_cm(target, ex) <= RADIUS_CM for ex in existing_locs):
            continue
        # Use config to pick logical node type/variant for this position (when we have multiple BPs we can spawn by type)
        node_type_name = "Trees"
        variant_id = None
        if biome_entries:
            entry = biome_entries[i % len(biome_entries)]
            if isinstance(entry, dict):
                node_type_name = entry.get("node_type", node_type_name)
                variants = entry.get("variants", [])
                variant_id = variants[0] if variants else None
        location = unreal.Vector(target[0], target[1], target[2])
        rotation = unreal.Rotator(0, 0, 0)
        try:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
            if actor:
                existing_locs.append(target)
                spawned += 1
                _log("Spawned at (%.0f, %.0f, %.0f) type=%s variant=%s" % (target[0], target[1], target[2], node_type_name, variant_id or "—"))
        except Exception as e:
            _log("Failed to spawn at (%.0f, %.0f, %.0f): %s" % (target[0], target[1], target[2], e))

    _log("Done. Spawned %d new resource node(s); %d position(s) already had an instance." % (spawned, len(positions) - spawned))

    # Ore nodes (MVP tutorial List 6: mine some ore)
    ore_positions = config.get("resource_node_ore_positions", [])
    ore_spawned = 0
    if ore_positions and unreal.EditorAssetLibrary.does_asset_exist(BP_HARVESTABLE_ORE_PATH):
        ore_bp = unreal.load_asset(BP_HARVESTABLE_ORE_PATH)
        if ore_bp:
            try:
                ore_class = ore_bp.generated_class() if callable(getattr(ore_bp, "generated_class", None)) else getattr(ore_bp, "generated_class", None) or ore_bp.get_editor_property("generated_class")
            except Exception:
                ore_class = None
            if ore_class:
                ore_existing = unreal.GameplayStatics.get_all_actors_of_class(world, ore_class) or []
                ore_locs = [_actor_location_cm(a) for a in ore_existing]
                ore_locs = [loc for loc in ore_locs if loc]
                for pos in ore_positions:
                    target = (pos["x"], pos["y"], pos["z"])
                    if any(_distance_cm(target, ex) <= RADIUS_CM for ex in ore_locs):
                        continue
                    loc = unreal.Vector(target[0], target[1], target[2])
                    try:
                        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(ore_class, loc, unreal.Rotator(0, 0, 0))
                        if actor:
                            ore_locs.append(target)
                            ore_spawned += 1
                            _log("Spawned ore at (%.0f, %.0f, %.0f)" % target)
                    except Exception as e:
                        _log("Failed to spawn ore at (%.0f, %.0f, %.0f): %s" % (target[0], target[1], target[2], e))
        else:
            _log("Ore positions configured but BP_HarvestableOre not loaded. Run create_bp_harvestable_ore.py first.")
    elif ore_positions:
        _log("resource_node_ore_positions set but BP_HarvestableOre missing. Run create_bp_harvestable_ore.py first.")

    # Flower nodes (MVP tutorial List 6: pick some flowers)
    flower_positions = config.get("resource_node_flower_positions", [])
    flower_spawned = 0
    if flower_positions and unreal.EditorAssetLibrary.does_asset_exist(BP_HARVESTABLE_FLOWER_PATH):
        flower_bp = unreal.load_asset(BP_HARVESTABLE_FLOWER_PATH)
        if flower_bp:
            try:
                flower_class = flower_bp.generated_class() if callable(getattr(flower_bp, "generated_class", None)) else getattr(flower_bp, "generated_class", None) or flower_bp.get_editor_property("generated_class")
            except Exception:
                flower_class = None
            if flower_class:
                flower_existing = unreal.GameplayStatics.get_all_actors_of_class(world, flower_class) or []
                flower_locs = [_actor_location_cm(a) for a in flower_existing]
                flower_locs = [loc for loc in flower_locs if loc]
                for pos in flower_positions:
                    target = (pos["x"], pos["y"], pos["z"])
                    if any(_distance_cm(target, ex) <= RADIUS_CM for ex in flower_locs):
                        continue
                    loc = unreal.Vector(target[0], target[1], target[2])
                    try:
                        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(flower_class, loc, unreal.Rotator(0, 0, 0))
                        if actor:
                            flower_locs.append(target)
                            flower_spawned += 1
                            _log("Spawned flower at (%.0f, %.0f, %.0f)" % target)
                    except Exception as e:
                        _log("Failed to spawn flower at (%.0f, %.0f, %.0f): %s" % (target[0], target[1], target[2], e))
        else:
            _log("Flower positions configured but BP_HarvestableFlower not loaded. Run create_bp_harvestable_flower.py first.")
    elif flower_positions:
        _log("resource_node_flower_positions set but BP_HarvestableFlower missing. Run create_bp_harvestable_flower.py first.")

    if spawned > 0 or ore_spawned > 0 or flower_spawned > 0:
        _save_current_level()
        _log("Level saved.")


if __name__ == "__main__":
    main()
