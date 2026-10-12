"""Greybox log-cabin, centimeters, origin on the cottage actor.

Local +X is east and +Y is north. The porch lip is y = -680. There is no
door leaf. Wall thickness is 30 cm. A 42 cm body needs the openings below;
a real 91 cm door is the width of this body.

The plan is the open log-home pattern (great room, kitchen in that volume,
covered porch, private suite off the back), grown so a 2 m body has the
spare a person has in those rooms. See Docs/level/L_SizeTest_ROOM_PLAN.md.
"""

import os

# Full sizes: center x, y, z and full x, y, z.
BOXES = [
    # South wall. Entry x -290..-10 (2.8 m), lintel above 3.2 m.
    (-470.0, -280.0, 250.0, 360.0, 30.0, 500.0),
    (545.0, -280.0, 250.0, 1110.0, 30.0, 500.0),
    (-150.0, -280.0, 410.0, 280.0, 30.0, 180.0),
    # North, west, east. Footprint x -650..1100, house y -280..1020.
    (225.0, 1020.0, 250.0, 1750.0, 30.0, 500.0),
    (-650.0, 370.0, 250.0, 30.0, 1300.0, 500.0),
    (1100.0, 370.0, 250.0, 30.0, 1300.0, 500.0),
    # Kitchen corner pier. The opening west of it is 4.4 m, into the great room.
    (350.0, 240.0, 250.0, 30.0, 160.0, 500.0),
    # Pantry on the north-east of the kitchen. Door faces south.
    (850.0, 340.0, 250.0, 60.0, 30.0, 500.0),
    (1080.0, 340.0, 250.0, 40.0, 30.0, 500.0),
    (820.0, 450.0, 250.0, 30.0, 220.0, 500.0),
    # Private wall. Couple door x -280..-40. Child door x 300..580.
    (-465.0, 560.0, 250.0, 370.0, 30.0, 500.0),
    (130.0, 560.0, 250.0, 340.0, 30.0, 500.0),
    (840.0, 560.0, 250.0, 520.0, 30.0, 500.0),
    # Couple bath, west of the bedroom. Door y 640..860.
    (-370.0, 600.0, 250.0, 30.0, 80.0, 500.0),
    (-370.0, 940.0, 250.0, 30.0, 160.0, 500.0),
    # Closet north of that bath. Door x -600..-420.
    (-625.0, 860.0, 250.0, 50.0, 30.0, 500.0),
    (-395.0, 860.0, 250.0, 50.0, 30.0, 500.0),
    # Couple bedroom / child room.
    (80.0, 790.0, 250.0, 30.0, 460.0, 500.0),
    # Child bath. Door y 640..860.
    (740.0, 600.0, 250.0, 30.0, 80.0, 500.0),
    (740.0, 940.0, 250.0, 30.0, 160.0, 500.0),
    # Hearth on the west wall of the great room.
    (-540.0, 80.0, 250.0, 160.0, 180.0, 500.0),
    # Porch posts along the lip. The entry path is x = -150.
    (-650.0, -680.0, 250.0, 40.0, 40.0, 500.0),
    (-450.0, -680.0, 250.0, 40.0, 40.0, 500.0),
    (280.0, -680.0, 250.0, 40.0, 40.0, 500.0),
    (720.0, -680.0, 250.0, 40.0, 40.0, 500.0),
    (1100.0, -680.0, 250.0, 40.0, 40.0, 500.0),
]

# Porch crawl. Clear width 130 cm, so an 84 cm body fits and a 160 cm body does not.
CRAWL_WALLS = [
    (430.0, -500.0, 250.0, 30.0, 200.0, 500.0),
    (590.0, -500.0, 250.0, 30.0, 200.0, 500.0),
]
FILLER = (510.0, -500.0, 250.0, 120.0, 200.0, 500.0)

# Capsule center, local cm. Enter the great room, cross into the kitchen,
# the couple suite, and the child room, then leave.
WALK = [
    (-150.0, -1100.0),
    (-150.0, -480.0),
    (-150.0, -110.0),
    (600.0, -110.0),
    (-150.0, -110.0),
    (-150.0, 390.0),
    (-150.0, 740.0),
    (-500.0, 740.0),
    (-500.0, 940.0),
    (-500.0, 740.0),
    (-150.0, 740.0),
    (-150.0, 390.0),
    (420.0, 390.0),
    (420.0, 740.0),
    (900.0, 740.0),
    (420.0, 740.0),
    (420.0, 390.0),
    (-150.0, 390.0),
    (-150.0, -110.0),
    (-150.0, -480.0),
    (-150.0, -1100.0),
]


def write_obj(path):
    verts = []
    faces = []

    def add_box(cx, cy, cz, sx, sy, sz):
        hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
        x0, x1 = cx - hx, cx + hx
        y0, y1 = cy - hy, cy + hy
        z0, z1 = cz - hz, cz + hz
        base = len(verts)
        verts.extend(
            [
                (x0, y0, z0),
                (x1, y0, z0),
                (x1, y1, z0),
                (x0, y1, z0),
                (x0, y0, z1),
                (x1, y0, z1),
                (x1, y1, z1),
                (x0, y1, z1),
            ]
        )
        for quad in (
            (0, 1, 2, 3),
            (4, 7, 6, 5),
            (0, 4, 5, 1),
            (3, 2, 6, 7),
            (0, 3, 7, 4),
            (1, 5, 6, 2),
        ):
            faces.append(tuple(base + i + 1 for i in quad))

    for box in BOXES:
        add_box(*box)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Greybox cabin walls, centimeters, Z up. No door leaf.\n")
        for x, y, z in verts:
            handle.write("v %.3f %.3f %.3f\n" % (x, y, z))
        for a, b, c, d in faces:
            handle.write("f %d %d %d %d\n" % (a, b, c, d))
    return path
