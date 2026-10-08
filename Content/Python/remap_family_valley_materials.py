"""Rename the two out-of-canon blend materials onto cited master instances.

Run with Blender, from the repo root:

    blender --background blender/floating_island_homestead_LIB.blend --python Content/Python/remap_family_valley_materials.py

M_FamilySilhouette -> M_BeastStylized_Family (cites M_BeastStylized).
M_ValleyNight -> M_StylizedGrass_ValleyNight (cites M_StylizedGrass).
"""

import bpy

RENAMES = {
    "M_FamilySilhouette": "M_BeastStylized_Family",
    "M_ValleyNight": "M_StylizedGrass_ValleyNight",
}


def main():
    changed = []
    for old, new in RENAMES.items():
        material = bpy.data.materials.get(old)
        if material is None:
            if bpy.data.materials.get(new) is not None:
                print("REMAP: %s already %s" % (old, new))
                continue
            print("REMAP: %s not in this blend" % old)
            continue
        material.name = new
        changed.append("%s -> %s" % (old, new))
    if changed:
        bpy.ops.wm.save_mainfile()
        print("REMAP: saved " + ", ".join(changed))
    else:
        print("REMAP: nothing to save")


if __name__ == "__main__":
    main()
