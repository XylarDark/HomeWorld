"""Stand a TripoSR mesh on its feet and scale the height to 2 m.

TripoSR lays the body in the XY plane. The thin axis is depth. Of the other
two, the height axis is the one with a tight end (the head) and a wide end.
"""

import sys

import numpy as np
import trimesh

PLAYER_HEIGHT_M = 2


def height_axis(vertices: np.ndarray) -> tuple[int, float]:
    extents = vertices.max(axis=0) - vertices.min(axis=0)
    candidates = list(np.argsort(extents)[1:])
    best_axis = int(candidates[-1])
    best_gap = -1.0
    head_sign = 1.0
    for axis in candidates:
        others = [i for i in range(3) if i != axis]
        low = np.quantile(vertices[:, axis], 0.1)
        high = np.quantile(vertices[:, axis], 0.9)

        def spread(mask: np.ndarray) -> float:
            sample = vertices[mask][:, others]
            return float(np.linalg.norm(sample - sample.mean(axis=0), axis=1).mean())

        spread_low = spread(vertices[:, axis] <= low)
        spread_high = spread(vertices[:, axis] >= high)
        gap = abs(spread_low - spread_high)
        if gap > best_gap:
            best_gap = gap
            best_axis = int(axis)
            head_sign = 1.0 if spread_high < spread_low else -1.0
    return best_axis, head_sign


def stand(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    vertices = mesh.vertices.copy()
    axis, head_sign = height_axis(vertices)
    if head_sign < 0:
        vertices[:, axis] *= -1.0
    # Map the height axis onto Blender Z, and keep a right-handed frame.
    order = [i for i in range(3) if i != axis] + [axis]
    stood = vertices[:, order]
    stood[:, 2] -= stood[:, 2].min()
    height = float(stood[:, 2].max())
    if height <= 0:
        raise RuntimeError("Mesh has no height.")
    stood *= PLAYER_HEIGHT_M / height
    mesh.vertices = stood
    return mesh


def main() -> None:
    source = sys.argv[1]
    dest = sys.argv[2]
    mesh = trimesh.load(source, force="mesh")
    stand(mesh)
    mesh.export(dest)
    size = mesh.vertices.max(axis=0) - mesh.vertices.min(axis=0)
    print(f"wrote {dest} height {size[2]:.3f} m")


if __name__ == "__main__":
    main()
