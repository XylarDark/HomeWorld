"""Greybox log-cabin, centimeters, origin on the cottage actor.

Local +X is east and +Y is north. The shell is 26 m by 23 m, from
(-800, -800) to (1800, 1500). The porch lip is y = -800. Walls are 30 cm.
The first floor is 5 m to the upper floor. That floor covers the whole
cottage, porch included, and the upstairs ceiling is 8.2 m. The stair
is the west side of the great room. There is no door leaf.

The back door is x 290..530 so the dog lane at world x = -3.9 still passes.
See Docs/level/L_SizeTest_ROOM_PLAN.md.
"""

import os

# Full sizes: center x, y, z and full x, y, z.
BOXES = [
    # South wall, y = -300. Entry x -290..-10 (2.8 m).
    (-545.0, -300.0, 250.0, 510.0, 30.0, 500.0),
    (895.0, -300.0, 250.0, 1810.0, 30.0, 500.0),
    (-150.0, -300.0, 410.0, 280.0, 30.0, 180.0),
    # North wall, y = 1500. Back door x 290..530 (2.4 m), on the dog's line.
    (-255.0, 1500.0, 250.0, 1090.0, 30.0, 500.0),
    (1165.0, 1500.0, 250.0, 1270.0, 30.0, 500.0),
    (410.0, 1500.0, 410.0, 240.0, 30.0, 180.0),
    # West and east, first floor.
    (-800.0, 600.0, 250.0, 30.0, 1800.0, 500.0),
    (1800.0, 600.0, 250.0, 30.0, 1800.0, 500.0),
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
    # Upper shell, 5 m to 8.2 m.
    (-800.0, 350.0, 660.0, 30.0, 2300.0, 320.0),
    (1800.0, 350.0, 660.0, 30.0, 2300.0, 320.0),
    (500.0, 1500.0, 660.0, 2600.0, 30.0, 320.0),
    (500.0, -800.0, 550.0, 2600.0, 20.0, 100.0),
    # Upper porch opens into the living room. Jambs at y = -300, gap x -200..800.
    (-500.0, -300.0, 660.0, 600.0, 30.0, 320.0),
    (1300.0, -300.0, 660.0, 1000.0, 30.0, 320.0),
    # Bedrooms off the living room. Wall y = 800. Doors x -500..-260 and 1100..1340.
    (-650.0, 800.0, 660.0, 300.0, 30.0, 320.0),
    (420.0, 800.0, 660.0, 1360.0, 30.0, 320.0),
    (1570.0, 800.0, 660.0, 460.0, 30.0, 320.0),
    # Couple bedroom east wall, bath between, child bedroom to the east.
    (200.0, 1150.0, 660.0, 30.0, 700.0, 320.0),
    (800.0, 1150.0, 660.0, 30.0, 700.0, 320.0),
    (500.0, 1200.0, 660.0, 600.0, 30.0, 320.0),
    # Markers beside the walk.
    (-480.0, 280.0, 80.0, 180.0, 220.0, 160.0),
    (-480.0, 40.0, 25.0, 160.0, 80.0, 50.0),
    (-200.0, 40.0, 25.0, 160.0, 80.0, 50.0),
    (-500.0, -550.0, 25.0, 180.0, 60.0, 50.0),
    (400.0, -550.0, 25.0, 180.0, 60.0, 50.0),
    (1500.0, -550.0, 40.0, 40.0, 200.0, 80.0),
    (1200.0, 280.0, 45.0, 220.0, 140.0, 90.0),
    (200.0, 200.0, 525.0, 160.0, 80.0, 50.0),
    # Porch posts. The entry path is x = -150.
    (-800.0, -800.0, 160.0, 40.0, 40.0, 320.0),
    (-450.0, -800.0, 160.0, 40.0, 40.0, 320.0),
    (200.0, -800.0, 160.0, 40.0, 40.0, 320.0),
    (900.0, -800.0, 160.0, 40.0, 40.0, 320.0),
    (1500.0, -800.0, 160.0, 40.0, 40.0, 320.0),
]

# Ten steps, 50 cm rise, 76 cm run, up to the upper floor.
for _step in range(10):
    _top = 50.0 * (_step + 1)
    BOXES.append((-710.0, 78.0 + _step * 76.0, _top * 0.5, 180.0, 76.0, _top))

# Porch crawl, off the entry. Clear width 130 cm.
CRAWL_WALLS = [
    (1335.0, -550.0, 160.0, 30.0, 200.0, 320.0),
    (1495.0, -550.0, 160.0, 30.0, 200.0, 320.0),
]
FILLER = (1415.0, -550.0, 160.0, 120.0, 200.0, 320.0)

# Capsule center, local cm. Enter, cross the kitchen and pantry, out the
# north door, and leave. The stair is west of this path.
WALK = [
    (-150.0, -1100.0),
    (-150.0, -500.0),
    (-150.0, -100.0),
    (1000.0, -100.0),
    (1600.0, 100.0),
    (1600.0, 650.0),
    (1600.0, 100.0),
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
