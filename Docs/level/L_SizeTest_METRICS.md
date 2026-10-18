# L_SizeTest placement

Master placement for the size-test map. The room layout is `Docs/level/L_SizeTest_ROOM_PLAN.md`. Floor and play facts are `Docs/level/L_SizeTest_CONTEXT.md`. Sizes for later art stay in `Docs/art/SCALE.md`. `Content/Python/scene_placement.py` reads the JSON block below and moves the actors. It does not invent a spot.

Units are meters. Unreal Z is up. Yaw 0 faces +X. Yaw 90 faces +Y. Setup practices are in `Docs/context/SCENE_SETUP.md`.

The homestead list is the cottage, the trees and rocks between the south start and the door, herb beds, lupines, the partner at the south door, and the child beside them. The bed row is not the sleep bed. The walk pad is an engine cube with the cube material the cottage walls use. Hills are not on this pad.

```json
{
  "player": {"x": -6, "y": -58, "z": 451, "yaw": 90},
  "pad": {"x": 70, "y": 140, "z": 1},
  "homestead": [
    {"label": "SM_Size_Island", "mesh": "SM_Size_Island", "x": 0, "y": 0, "z": 450, "yaw": 0},
    {"label": "SM_Size_Cottage", "mesh": "SM_Size_Cottage", "x": -8, "y": 0, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S", "mesh": "SM_Size_Pine_S", "x": -6.4, "y": -46, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_M", "mesh": "SM_Size_Pine_M", "x": -16, "y": -44, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_L", "mesh": "SM_Size_Pine_L", "x": 4, "y": -44, "z": 453, "yaw": 0},
    {"label": "SM_Size_Pine_S_B", "mesh": "SM_Size_Pine_S", "x": 14, "y": -50, "z": 453, "yaw": 0},
    {"label": "SM_Size_Rock", "mesh": "SM_Size_Rock", "x": -12, "y": -48, "z": 453, "yaw": 20},
    {"label": "SM_Size_Rock_B", "mesh": "SM_Size_Rock", "x": 2, "y": -50, "z": 453, "yaw": 140},
    {"label": "SM_Size_Rock_C", "mesh": "SM_Size_Rock", "x": -4, "y": -40, "z": 453, "yaw": 60},
    {"label": "SM_Size_HerbBed", "mesh": "SM_Size_HerbBed", "x": -12.2, "y": -8.3, "z": 453, "yaw": 0},
    {"label": "SM_Size_HerbBed_B", "mesh": "SM_Size_HerbBed", "x": -6.8, "y": -8.3, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine", "mesh": "SM_Size_Lupine", "x": -12.2, "y": -8.3, "z": 453, "yaw": 0},
    {"label": "SM_Size_Lupine_B", "mesh": "SM_Size_Lupine", "x": -6.8, "y": -8.3, "z": 453, "yaw": 0},
    {"label": "SM_Size_Kettle", "mesh": "SM_Size_Kettle", "x": 1.8, "y": 0.0, "z": 453, "yaw": 180},
    {"label": "SM_Size_Bed", "mesh": "SM_Size_Bed", "x": -9.5, "y": 9.0, "z": 453, "yaw": 0},
    {"label": "SK_Size_Partner", "mesh": "SK_Player_Female", "x": -9.5, "y": -8.2, "z": 453, "yaw": 0},
    {"label": "SK_Size_Child", "mesh": "SK_Player_Female", "x": -8.0, "y": -8.6, "z": 453, "yaw": 270, "scale": 0.6}
  ],
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
