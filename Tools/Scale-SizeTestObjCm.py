"""Write size-test OBJ files in centimeters.

TripoSR stands these meshes in meters. Unreal reads an OBJ unit as one
centimeter, so a meter file lands a hundred times too small.
"""

import os

import numpy as np
import trimesh

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "AssetCreation", "SizeTest"))
NAMES = (
    "SM_Size_Bear",
    "SM_Size_Pine_S",
    "SM_Size_Pine_M",
    "SM_Size_Pine_L",
    "SM_Size_Kettle",
)


def main():
    for name in NAMES:
        path = os.path.join(ROOT, name + ".obj")
        mesh = trimesh.load(path, force="mesh")
        height = float(mesh.vertices[:, 2].max() - mesh.vertices[:, 2].min())
        if height > 20.0:
            print(f"{name} already centimeters, height {height:.1f}")
            continue
        mesh.vertices = np.asarray(mesh.vertices) * 100.0
        mesh.export(path)
        height = float(mesh.vertices[:, 2].max() - mesh.vertices[:, 2].min())
        print(f"{name} centimeters, height {height:.1f}")


if __name__ == "__main__":
    main()
