# L_SizeTest placement

Master placement for the size-test map. Sizes stay in `Docs/art/SCALE.md`. `Content/Python/apply_size_test_metrics.py` reads the JSON block below and moves the actors. It does not invent a spot.

Units are meters. Unreal Z is up. The island actor is at z = 450. The walkable top is that same height: five downward traces agreed at 45,000 cm on 2026-10-11. The cone hangs below the pad and is not the floor. The placer snaps mesh bottoms onto the traced top, measures again, and does not save if any bottom is more than 2 cm off. Yaw 0 faces +X. Yaw 90 faces +Y, toward the cottage from the south. The size-test coat faces mesh −Y, so its mesh yaw offset is +90. The walk clip plays only while moving, on that same axis.

Setup practices for this map and the next one are in `Docs/context/SCENE_SETUP.md` and `Docs/level/L_SizeTest_CONTEXT.md`.

The homestead holds the cottage, rocks, trees, and flowerbeds. The bear and the guards are not on the island. Guards stay at the camp. Path stones, fence, moss, and the porch stump stay off this scene.

The cottage porch faces south. Two herb beds sit on that apron, long side parallel to the facade, with a path between them aimed at the door. Lupines stand in those beds. The player stands on that path, facing the door, 6 m inside the pad edge. Flowerbeds and lupines do not block the pawn. The cottage collision is the walls and a 1.4 m south door; the porch is open and the pad is the floor inside. The field mesh is scaled under the island as the plain.

```json
{
  "player": {"x": -8, "y": -9, "z": 451, "yaw": 90},
  "homestead": [
    {"label": "SM_Size_Island", "mesh": "SM_Size_Island", "x": 0, "y": 0, "z": 450, "yaw": 0},
    {"label": "SM_Size_Cottage", "mesh": "SM_Size_Cottage", "x": -8, "y": 0, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S", "mesh": "SM_Size_Pine_S", "x": -16, "y": 12, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_M", "mesh": "SM_Size_Pine_M", "x": -16, "y": 2, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_L", "mesh": "SM_Size_Pine_L", "x": 14, "y": 12, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S_B", "mesh": "SM_Size_Pine_S", "x": 14, "y": -6, "z": 453, "yaw": 0},
    {"label": "SM_Size_Rock", "mesh": "SM_Size_Rock", "x": 6, "y": -2, "z": 453, "yaw": 20},
    {"label": "SM_Size_Rock_B", "mesh": "SM_Size_Rock", "x": 10, "y": 6, "z": 453, "yaw": 140},
    {"label": "SM_Size_Rock_C", "mesh": "SM_Size_Rock", "x": -16, "y": 8, "z": 453, "yaw": 60},
    {"label": "SM_Size_HerbBed", "mesh": "SM_Size_HerbBed", "x": -9.6, "y": -7, "z": 453, "yaw": 0},
    {"label": "SM_Size_HerbBed_B", "mesh": "SM_Size_HerbBed", "x": -6.4, "y": -7, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine", "mesh": "SM_Size_Lupine", "x": -9.6, "y": -7, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine_B", "mesh": "SM_Size_Lupine", "x": -6.4, "y": -7, "z": 453, "yaw": 0}
  ],
  "plains": {"label": "SM_Size_Field", "mesh": "SM_Size_Field", "x": 0, "y": 0, "z": 0, "yaw": 0, "scale": 20},
  "removeLabels": [
    "SM_Size_Bear",
    "SK_Size_Bear",
    "SK_Size_Partner",
    "SK_Size_Child",
    "SM_Size_Kettle",
    "SM_Size_Bed",
    "SM_Size_Stump",
    "SM_Size_Shrine",
    "SM_Size_Perch",
    "SM_Size_Fence",
    "SM_Size_Moss",
    "SM_Size_Crystal",
    "SM_Size_Path",
    "SK_Size_Bull"
  ]
}
```
