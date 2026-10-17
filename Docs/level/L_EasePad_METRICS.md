# L_EasePad placement

One flat floor, one player start, and one ease pad. Units are meters. `Content/Python/place_ease_pad.py` reads the JSON block and does not invent a spot.

The floor is 20 m across so the 300 cm weak-hit step stays on it. The pad sits on the floor. Its focus is 3 m ahead of the pad, on the actor. Camp actors, the cottage, and stroke actors are not in this list.

```json
{
  "player": {
    "x": 0,
    "y": -2,
    "z": 1.1,
    "yaw": 0
  },
  "floor": {
    "label": "SM_EasePad_Floor",
    "x": 0,
    "y": 0,
    "z": -0.5,
    "sx": 20,
    "sy": 20,
    "sz": 1
  },
  "pad": {
    "label": "EasePad",
    "x": 0,
    "y": 0,
    "z": 0
  }
}
```
