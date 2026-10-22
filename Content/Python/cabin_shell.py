"""Greybox log-cabin, centimeters, origin on the cottage actor.

Local +X is east and +Y is north. The shell is 26 m by 23 m, from
(-800, -800) to (1800, 1500). The porch lip is y = -800. Walls are 30 cm.
The first floor is 5 m to the upper floor. The upstairs walls are another
5 m, and the roof sits on that plate. The stair is the west side of the
great room. There is no door leaf.

The back door is x 290..530 so the dog lane at world x = -3.9 still passes.
See Docs/level/L_SizeTest_ROOM_PLAN.md.
"""

import os

# Outer shell, centimeters, local to the cottage actor. Wall boxes are centered
# on these lines, so the outside face is half a wall further out.
SHELL_MIN_X = -800.0
SHELL_MAX_X = 1800.0
SHELL_MIN_Y = -800.0
SHELL_MAX_Y = 1500.0
WALL = 30.0

# Full sizes: center x, y, z and full x, y, z.
BOXES = [
    # South wall, y = -300. Entry x -290..-10. Window x 500..700.
    (-545.0, -300.0, 250.0, 510.0, 30.0, 500.0),
    (245.0, -300.0, 250.0, 510.0, 30.0, 500.0),
    (600.0, -300.0, 50.0, 200.0, 30.0, 100.0),
    (600.0, -300.0, 375.0, 200.0, 30.0, 250.0),
    (1250.0, -300.0, 250.0, 1100.0, 30.0, 500.0),
    (-150.0, -300.0, 410.0, 280.0, 30.0, 180.0),
    # North wall, y = 1500. Back door x 290..530 (2.4 m), on the dog's line.
    (-255.0, 1500.0, 250.0, 1090.0, 30.0, 500.0),
    (1165.0, 1500.0, 250.0, 1270.0, 30.0, 500.0),
    (410.0, 1500.0, 410.0, 240.0, 30.0, 180.0),
    # West wall. Window y -220..-60, south of the stair.
    (-800.0, -260.0, 250.0, 30.0, 80.0, 500.0),
    (-800.0, -140.0, 50.0, 30.0, 160.0, 100.0),
    (-800.0, -140.0, 375.0, 30.0, 160.0, 250.0),
    (-800.0, 720.0, 250.0, 30.0, 1560.0, 500.0),
    # East wall. Windows y -80..80 and y 920..1080.
    (1800.0, -190.0, 250.0, 30.0, 220.0, 500.0),
    (1800.0, 0.0, 50.0, 30.0, 160.0, 100.0),
    (1800.0, 0.0, 375.0, 30.0, 160.0, 250.0),
    (1800.0, 500.0, 250.0, 30.0, 840.0, 500.0),
    (1800.0, 1000.0, 50.0, 30.0, 160.0, 100.0),
    (1800.0, 1000.0, 375.0, 30.0, 160.0, 250.0),
    (1800.0, 1290.0, 250.0, 30.0, 420.0, 500.0),
    # Upstairs walls, 5 m, on the same lines. The north wall is solid.
    # The south opening is the way onto the upper porch.
    (-545.0, -300.0, 750.0, 510.0, 30.0, 500.0),
    (245.0, -300.0, 750.0, 510.0, 30.0, 500.0),
    (600.0, -300.0, 550.0, 200.0, 30.0, 100.0),
    (600.0, -300.0, 875.0, 200.0, 30.0, 250.0),
    (1250.0, -300.0, 750.0, 1100.0, 30.0, 500.0),
    (-150.0, -300.0, 910.0, 280.0, 30.0, 180.0),
    (500.0, 1500.0, 750.0, 2600.0, 30.0, 500.0),
    (-800.0, -260.0, 750.0, 30.0, 80.0, 500.0),
    (-800.0, -140.0, 550.0, 30.0, 160.0, 100.0),
    (-800.0, -140.0, 875.0, 30.0, 160.0, 250.0),
    (-800.0, 720.0, 750.0, 30.0, 1560.0, 500.0),
    (1800.0, -190.0, 750.0, 30.0, 220.0, 500.0),
    (1800.0, 0.0, 550.0, 30.0, 160.0, 100.0),
    (1800.0, 0.0, 875.0, 30.0, 160.0, 250.0),
    (1800.0, 500.0, 750.0, 30.0, 840.0, 500.0),
    (1800.0, 1000.0, 550.0, 30.0, 160.0, 100.0),
    (1800.0, 1000.0, 875.0, 30.0, 160.0, 250.0),
    (1800.0, 1290.0, 750.0, 30.0, 420.0, 500.0),
    # Kitchen pier. The opening west of it is about 5 m.
    (600.0, 350.0, 250.0, 30.0, 300.0, 500.0),
    # Pantry. Door faces south, 1.8 m, x 1510..1690.
    (1455.0, 500.0, 250.0, 110.0, 30.0, 500.0),
    (1745.0, 500.0, 250.0, 110.0, 30.0, 500.0),
    (1600.0, 500.0, 410.0, 180.0, 30.0, 180.0),
    (1400.0, 650.0, 250.0, 30.0, 300.0, 500.0),
    (1600.0, 800.0, 250.0, 400.0, 30.0, 500.0),
    # Upper floor. A hole over the stair, x -800..-620, y 40..800.
    (500.0, -380.0, 480.0, 2600.0, 840.0, 40.0),
    (590.0, 420.0, 480.0, 2420.0, 760.0, 40.0),
    (500.0, 1150.0, 480.0, 2600.0, 700.0, 40.0),
    # Ground porch rail, gap at the entry. Upper porch rail on the floor above.
    (-575.0, -780.0, 45.0, 450.0, 20.0, 90.0),
    (925.0, -780.0, 45.0, 1750.0, 20.0, 90.0),
    (500.0, -800.0, 550.0, 2600.0, 20.0, 100.0),
    # Upstairs room walls, 5 m, from the upper floor to the roof plate.
    (-540.0, 800.0, 750.0, 80.0, 30.0, 500.0),
    (45.0, 800.0, 750.0, 610.0, 30.0, 500.0),
    (745.0, 800.0, 750.0, 310.0, 30.0, 500.0),
    (1470.0, 800.0, 750.0, 660.0, 30.0, 500.0),
    (200.0, 1000.0, 750.0, 30.0, 400.0, 500.0),
    (200.0, 1370.0, 750.0, 30.0, 260.0, 500.0),
    (800.0, 1150.0, 750.0, 30.0, 700.0, 500.0),
    (500.0, 1200.0, 750.0, 600.0, 30.0, 500.0),
    (1300.0, 900.0, 750.0, 30.0, 200.0, 500.0),
    (1300.0, 1370.0, 750.0, 30.0, 260.0, 500.0),
    # Hearth, two couches facing it, kitchen counter run.
    (-480.0, 280.0, 80.0, 180.0, 220.0, 160.0),
    (-240.0, 160.0, 35.0, 90.0, 180.0, 70.0),
    (-240.0, 400.0, 35.0, 90.0, 180.0, 70.0),
    (1710.0, 80.0, 50.0, 70.0, 520.0, 100.0),
    (1670.0, -120.0, 94.0, 40.0, 50.0, 8.0),
    (1685.0, 160.0, 70.0, 70.0, 70.0, 140.0),
    (1710.0, 380.0, 30.0, 40.0, 40.0, 60.0),
    (-480.0, 40.0, 25.0, 160.0, 80.0, 50.0),
    (-200.0, 40.0, 25.0, 160.0, 80.0, 50.0),
    (-500.0, -550.0, 25.0, 180.0, 60.0, 50.0),
    (400.0, -550.0, 25.0, 180.0, 60.0, 50.0),
    (1500.0, -550.0, 40.0, 40.0, 200.0, 80.0),
    (800.0, 200.0, 45.0, 220.0, 140.0, 90.0),
    (200.0, 200.0, 525.0, 160.0, 80.0, 50.0),
    # Porch posts, up to the 5 m wall plate. The entry path is x = -150.
    (-800.0, -800.0, 250.0, 40.0, 40.0, 500.0),
    (-450.0, -800.0, 250.0, 40.0, 40.0, 500.0),
    (200.0, -800.0, 250.0, 40.0, 40.0, 500.0),
    (900.0, -800.0, 250.0, 40.0, 40.0, 500.0),
    (1500.0, -800.0, 250.0, 40.0, 40.0, 500.0),
]

# One ramp in the stair opening. Local cm: bottom and top of the walking surface.
RAMP = ((-695.0, 40.0, 0.0), (-695.0, 800.0, 500.0), 150.0)

# The kitchen counter run is the consumable station. Half the 200 cm played body.
COUNTER_BOX_INDEX = 63

# Gable on the upstairs wall plate (z = 1000). Ridge runs east-west at y = 600.
# Eaves overhang the south and north walls by about 60 cm.
ROOF_WIDTH = 2680.0
ROOF = (
    ("CabinRoof_South", (500.0, -360.0, 958.0), (500.0, 600.0, 1630.0)),
    ("CabinRoof_North", (500.0, 1560.0, 958.0), (500.0, 600.0, 1630.0)),
)

# Porch crawl, off the entry. Clear width 130 cm.
CRAWL_WALLS = [
    (1335.0, -550.0, 160.0, 30.0, 200.0, 320.0),
    (1495.0, -550.0, 160.0, 30.0, 200.0, 320.0),
]
FILLER = (1415.0, -550.0, 160.0, 120.0, 200.0, 320.0)

# Local cm. Warm point lights under each floor's ceiling.
LIGHTS = [
    (-200.0, 200.0, 320.0),
    (1100.0, 0.0, 320.0),
    (200.0, 100.0, 900.0),
    (-300.0, 1100.0, 900.0),
    (500.0, 1000.0, 900.0),
    (1050.0, 1100.0, 900.0),
    (1550.0, 1100.0, 900.0),
]

# Capsule center, local cm. Enter, cross the kitchen and pantry, out the
# north door, and leave. The stair is west of this path.
WALK = [
    (-150.0, -1100.0),
    (-150.0, -500.0),
    (-150.0, -100.0),
    (1000.0, -100.0),
    (1200.0, -100.0),
    (1200.0, 400.0),
    (1600.0, 400.0),
    (1600.0, 650.0),
    (1600.0, 400.0),
    (1200.0, 400.0),
    (1200.0, -100.0),
    (1000.0, -100.0),
    (410.0, -100.0),
    (410.0, 1650.0),
    (410.0, -100.0),
    (-150.0, -100.0),
    (-150.0, -500.0),
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
