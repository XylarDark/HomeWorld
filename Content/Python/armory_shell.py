"""Greybox armory, centimeters, origin on the armory pad.

Local +X is east and +Y is north. The door faces the cottage yard on the
west. The shell is 7 m by 6 m outside, walls 30 cm thick and 4 m high; the
room is 6.4 m by 5.4 m. A 42 cm body needs the opening below: the door is
2.4 m wide and 3 m tall, with the lintel above.

The armor table stands against the inside of the east wall, from the
metrics sheet. See Docs/level/L_SizeTest_ROOM_PLAN.md.
"""

# Full sizes: center x, y, z and full x, y, z.
BOXES = [
    # West wall, door y -120..120 (2.4 m), lintel above 3 m.
    (-335.0, -210.0, 200.0, 30.0, 180.0, 400.0),
    (-335.0, 210.0, 200.0, 30.0, 180.0, 400.0),
    (-335.0, 0.0, 350.0, 30.0, 240.0, 100.0),
    # East, south, north. Footprint x -350..350, y -300..300.
    (335.0, 0.0, 200.0, 30.0, 600.0, 400.0),
    (0.0, -285.0, 200.0, 700.0, 30.0, 400.0),
    (0.0, 285.0, 200.0, 700.0, 30.0, 400.0),
]

# Capsule center, local cm. In through the yard door, past the table, back out.
WALK = [
    (-550.0, 0.0),
    (150.0, 0.0),
    (-550.0, 0.0),
]
