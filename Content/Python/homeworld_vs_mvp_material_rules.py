# homeworld_vs_mvp_material_rules.py
# Pure-Python mesh basename -> Docs/02 master mapping for VS_MVP DRESS_* actors.
# Used by assign_vs_mvp_materials.py; unit-tested without Unreal Editor.

from __future__ import annotations

from homeworld_master_material_defs import MASTER_NAMES

DRESS_LABEL_PREFIX = "DRESS_"
DRESS_FOLDER = "VS_MVP/Dress"

MASTERS_DIR = "/Game/HomeWorld/Materials/Masters"
INSTANCES_DIR = "/Game/HomeWorld/Materials/Instances"
MPC_PATH = "/Game/HomeWorld/Materials/MPC_HomeWorld_Time"
MPC_SCALAR_NAME = "NightMix"

# Ordered rules: first match wins (most specific patterns first).
# Each entry: (predicate(mesh_basename) -> bool, master_name)
_MESH_RULES: tuple[tuple, ...] = (
    # Spirit layer accents (shrine glow, wounds, night layer)
    (
        lambda n: any(k in n for k in ("Glow", "Spirit", "Wound")),
        "M_SpiritUnlit",
    ),
    (lambda n: n.startswith("SM_Beast"), "M_BeastStylized"),
    # Stored / world resource proxies (Docs/02 cite matrix)
    (lambda n: "RES_STONE" in n, "M_CliffRock"),
    (lambda n: "RES_WOOD" in n or "RES_FUEL" in n, "M_WoodWild"),
    (lambda n: "RES_SEED" in n or "RES_CROP" in n, "M_Nurtured"),
    (lambda n: "RES_" in n, "M_GatherHerb"),
    # Foliage cards before generic pine trunk
    (
        lambda n: any(k in n for k in ("Foliage", "Needle", "Canopy", "Card", "_Leaves")),
        "M_FoliageCard",
    ),
    (lambda n: "Pine" in n, "M_WoodWild"),
    (
        lambda n: n.startswith("SM_Cliff")
        or n.startswith("SM_Islet")
        or "ValleyLip" in n
        or "Chunk_Torn" in n,
        "M_CliffRock",
    ),
    (
        lambda n: n in ("SM_IslandTop", "SM_Planet_GroundPlate")
        or any(k in n for k in ("Grass", "Soil", "GardenBed")),
        "M_StylizedGrass",
    ),
    (
        lambda n: "PathStone" in n
        or "Path_Planet" in n
        or "LandingCircle" in n
        or n == "SM_Lookout_Pad",
        "M_PathStone",
    ),
    (
        lambda n: any(
            k in n
            for k in ("Gather", "Herb", "Berry", "Bush", "Fern", "Vine", "Flax", "Planter")
        ),
        "M_GatherHerb",
    ),
    (
        lambda n: n.startswith("SM_Cabin")
        or n == "SM_Glider_Perch"
        or "Roof_Hamlet" in n
        or "Perch" in n,
        "M_WoodCabin",
    ),
    (lambda n: "Shrine" in n, "M_WoodCabin"),
    (lambda n: any(k in n for k in ("Nurture", "Crop")), "M_Nurtured"),
)


def mesh_basename_from_actor_label(label: str) -> str | None:
    """Return StaticMesh asset basename from a DRESS_* actor label."""
    if not label or not label.startswith(DRESS_LABEL_PREFIX):
        return None
    return label[len(DRESS_LABEL_PREFIX) :]


def resolve_master_for_mesh(mesh_name: str) -> str | None:
    """Map mesh basename to one of the ten Docs/02 masters."""
    if not mesh_name or mesh_name.startswith("UCX_") or mesh_name.startswith("M_"):
        return None
    for predicate, master in _MESH_RULES:
        if predicate(mesh_name):
            if master in MASTER_NAMES:
                return master
    return None


def material_asset_candidates(master_name: str) -> tuple[str, ...]:
    """Prefer MI under Instances; fall back to master material."""
    if master_name not in MASTER_NAMES:
        return ()
    short = master_name[2:]  # M_StylizedGrass -> StylizedGrass
    return (
        f"{INSTANCES_DIR}/MI_{short}",
        f"{INSTANCES_DIR}/{master_name}_Inst",
        f"{MASTERS_DIR}/{master_name}",
    )
