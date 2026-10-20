# L_SizeTest placement

Master placement for the size-test map. The room layout is `Docs/level/L_SizeTest_ROOM_PLAN.md`. Floor and play facts are `Docs/level/L_SizeTest_CONTEXT.md`. Sizes for later art stay in `Docs/art/SCALE.md`. `Content/Python/scene_placement.py` reads the JSON block below and moves the actors. It does not invent a spot.

Units are meters. Unreal Z is up. Yaw 0 faces +X. Yaw 90 faces +Y. Setup practices are in `Docs/context/SCENE_SETUP.md`.

The homestead list is the cottage, the trees and rocks between the south start and the door, herb beds, lupines, the partner at the south door, the child beside them, and the armor table. The bed row is not the sleep bed. The walk pad is an engine cube with the cube material the cottage walls use. The armor table is an engine cube too; the kitchen counter is the consumable station and it grows at play with the kettle on top. The armory block is the second building, in front of the cottage's east wing across the courtyard, its door on the west wall facing the courtyard; `Content/Python/armory_shell.py` grows its walls from that origin and the placer checks its door, walls, floor, and a 42 cm walk. The opening dog stands on the east lawn; the placer gives it a clear nine-metre approach lane and 2.8 m of clearance from every solid. The walk stays on the flat pad. Water sheets, the farm plot, and the hill steps sit off that walk. Their centers and sizes are the `water`, `steps`, and `samples` lists. The `graph` block names those places and does not add a coordinate or a height. The top hill step is listed and not spawned until a glide has happened.

```json
{
  "player": {"x": -6, "y": -58, "z": 451, "yaw": 90},
  "pad": {"x": 100, "y": 140, "z": 1},
  "armory": {"x": -0.5, "y": -13, "yaw": 0},
  "dog": {"x": -3.9, "y": 20, "yaw": 270},
  "homestead": [
    {"label": "SM_Size_Island", "mesh": "SM_Size_Island", "x": 0, "y": 0, "z": 450, "yaw": 0},
    {"label": "SM_Size_Cottage", "mesh": "SM_Size_Cottage", "x": -8, "y": 0, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S", "mesh": "SM_Size_Pine_S", "x": -7.2, "y": -46, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_M", "mesh": "SM_Size_Pine_M", "x": -18, "y": -40, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_M_B", "mesh": "SM_Size_Pine_M", "x": -16, "y": -56, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_L", "mesh": "SM_Size_Pine_L", "x": 8, "y": -46, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S_B", "mesh": "SM_Size_Pine_S", "x": 20, "y": -40, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S_C", "mesh": "SM_Size_Pine_S", "x": 16, "y": -54, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_L_B", "mesh": "SM_Size_Pine_L", "x": 42, "y": 28, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_M_C", "mesh": "SM_Size_Pine_M", "x": 46, "y": 32, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S_D", "mesh": "SM_Size_Pine_S", "x": 44, "y": 24, "z": 453, "yaw": 0},
    {"label": "SM_Size_Rock", "mesh": "SM_Size_Rock", "x": -12, "y": -36, "z": 453, "yaw": 20},
    {"label": "SM_Size_Rock_B", "mesh": "SM_Size_Rock", "x": 6, "y": -56, "z": 453, "yaw": 140},
    {"label": "SM_Size_Rock_C", "mesh": "SM_Size_Rock", "x": -24, "y": -48, "z": 453, "yaw": 60},
    {"label": "SM_Size_Rock_D", "mesh": "SM_Size_Rock", "x": 14, "y": -34, "z": 453, "yaw": 30},
    {"label": "SM_Size_Rock_E", "mesh": "SM_Size_Rock", "x": -22, "y": -32, "z": 453, "yaw": 80},
    {"label": "SM_Size_HerbBed", "mesh": "SM_Size_HerbBed", "x": -12.2, "y": -9.2, "z": 453, "yaw": 0},
    {"label": "SM_Size_HerbBed_B", "mesh": "SM_Size_HerbBed", "x": -6.8, "y": -9.2, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine", "mesh": "SM_Size_Lupine", "x": -12.2, "y": -9.2, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine_B", "mesh": "SM_Size_Lupine", "x": -6.8, "y": -9.2, "z": 453, "yaw": 0},
    {"label": "SM_Size_Kettle", "mesh": "SM_Size_Kettle", "x": 1.8, "y": 0.0, "z": 453, "yaw": 180},
    {"label": "SM_Size_Bed", "mesh": "SM_Size_Bed", "x": -9.5, "y": 9.0, "z": 453, "yaw": 0},
    {"label": "SM_Size_ArmorTable", "mesh": "Cube", "x": 2.25, "y": -13, "z": 453, "yaw": 0, "size": [0.9, 1.4, 0.9]},
    {"label": "SK_Size_Partner", "mesh": "SK_Player_Female", "x": -9.5, "y": -10.5, "z": 453, "yaw": 0},
    {"label": "SK_Size_Child", "mesh": "SK_Player_Female", "x": -8.0, "y": -11, "z": 453, "yaw": 270, "scale": 0.6}
  ],
  "water": [
    {"label": "Water_Spring", "x": 28, "y": 22, "size": [4, 3, 0.4], "bottom": 2.2},
    {"label": "Water_HotSpring", "x": 20, "y": 22, "size": [8, 6, 0.3]},
    {"label": "Water_Backyard", "x": 4, "y": 26, "size": [32, 3, 0.15]},
    {"label": "Water_FarNorth", "x": -29, "y": 26, "size": [34, 3, 0.15]},
    {"label": "Water_WestDrop", "x": -46, "y": 14, "size": [3, 24, 0.15]},
    {"label": "Water_Pond", "x": -46, "y": 2, "size": [8, 12, 0.15]}
  ],
  "steps": [
    {"label": "Hill_Step1", "x": 28, "y": 22, "size": [10, 8, 3], "bottom": 0},
    {"label": "Hill_Step2", "x": 32, "y": 24, "size": [8, 6, 3], "bottom": 3},
    {"label": "Hill_Step3", "x": 35, "y": 26, "size": [6, 4, 3], "bottom": 6, "gated": "glide"}
  ],
  "samples": [
    {"label": "Path_A", "x": 12, "y": 10, "size": [3, 3, 0.3], "collision": "block", "tag": "ObservatoryPath"},
    {"label": "Path_B", "x": 18, "y": 14, "size": [3, 3, 0.3], "collision": "block", "tag": "ObservatoryPath"},
    {"label": "Path_C", "x": 24, "y": 17, "size": [3, 3, 0.3], "collision": "block", "tag": "ObservatoryPath"},
    {"label": "Observatory", "x": 32, "y": 24, "size": [3, 3, 2.5], "bottom": 6, "collision": "block", "tag": "Observatory"},
    {"label": "DogHouse", "x": -1.6, "y": 22.2, "size": [1.8, 1.4, 1.3], "collision": "none", "tag": "DogHouse"},
    {"label": "FarmPlot", "x": 22, "y": -30, "size": [20, 16, 0.08], "collision": "none"},
    {"label": "FarmGate", "x": 12, "y": -30, "size": [1.2, 2.4, 2], "collision": "block", "tag": "FarmGate"},
    {"label": "CaveNotch", "x": 32, "y": 29, "size": [4, 3, 3], "collision": "overlap", "tag": "CaveNotch"}
  ],
  "graph": {
    "nodes": [
      {"id": "peak", "kind": "peak", "label": "Observatory"},
      {"id": "spring", "kind": "spring", "label": "Water_Spring"},
      {"id": "hot_spring", "kind": "hot_spring", "label": "Water_HotSpring"},
      {"id": "pond", "kind": "pond", "label": "Water_Pond"},
      {"id": "path_a", "kind": "path_sample", "label": "Path_A"},
      {"id": "path_b", "kind": "path_sample", "label": "Path_B"},
      {"id": "path_c", "kind": "path_sample", "label": "Path_C"}
    ],
    "edges": [
      {"id": "ridge", "labels": ["Hill_Step1", "Hill_Step2", "Hill_Step3"]},
      {"id": "river", "labels": ["Water_Spring", "Water_HotSpring", "Water_Backyard", "Water_FarNorth", "Water_WestDrop", "Water_Pond"]},
      {"id": "walk", "flat": true, "labels": ["Path_A", "Path_B", "Path_C"]}
    ]
  },
  "plains": {"label": "SM_Size_Field", "mesh": "SM_Size_Field", "x": 0, "y": 0, "z": 0, "yaw": 0, "scale": 20},
  "removeLabels": [
    "SM_Size_Bear",
    "SK_Size_Bear",
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
