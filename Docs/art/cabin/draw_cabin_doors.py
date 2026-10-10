"""One-off plan of the cabin door swings. Leafs park inside their rooms."""
from PIL import Image, ImageDraw, ImageFont
import math

S = 22
OX, OY = 90, 70
# feet: x east from interior west wall, y north from interior south wall
# porch occupies y -8..0

def pt(x, y):
    return (OX + x * S, OY + (35 - y) * S)

def arc_points(hinge, radius, a0, a1, n=24):
    hx, hy = hinge
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append(pt(hx + radius * math.cos(a), hy + radius * math.sin(a)))
    return pts

img = Image.new("RGB", (29 * S + 180, 43 * S + 160), "white")
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 18)
    small = ImageFont.truetype("arial.ttf", 14)
    title = ImageFont.truetype("arial.ttf", 22)
except OSError:
    font = small = title = ImageFont.load_default()

fills = {
    "porch": (236, 230, 220),
    "living": (248, 244, 236),
    "kitchen": (244, 236, 224),
    "hall": (232, 232, 232),
    "child": (236, 242, 236),
    "bath": (230, 238, 242),
    "closet": (226, 226, 226),
    "couple": (242, 236, 236),
}

rooms = [
    ("porch", -0.01, -8, 29, 0),
    ("living", 0, 0, 17, 14),
    ("kitchen", 17, 0, 29, 14),
    ("hall", 0, 14, 29, 22),
    ("child", 0, 22, 10, 35),
    ("bath", 10, 22, 18, 31),
    ("closet", 10, 31, 18, 35),
    ("couple", 18, 22, 29, 35),
]
for name, x0, y0, x1, y1 in rooms:
    d.polygon([pt(x0, y0), pt(x1, y0), pt(x1, y1), pt(x0, y1)], fill=fills[name])

def wall(x0, y0, x1, y1):
    d.line([pt(x0, y0), pt(x1, y1)], fill="black", width=4)

# outer shell, interior 29 by 35, porch to y=-8
wall(0, -8, 29, -8)
wall(0, -8, 0, 35)
wall(29, -8, 29, 35)
wall(0, 35, 29, 35)
# south wall of house with front-door gap x 13-17
wall(0, 0, 13, 0)
wall(17, 0, 29, 0)
# living / kitchen, gap y 1-6
wall(17, 0, 17, 1)
wall(17, 6, 17, 14)
# living / hall, gap x 6-11
wall(0, 14, 6, 14)
wall(11, 14, 29, 14)
# hall / back rooms
wall(0, 22, 6, 22)       # child door gap x 6-10
wall(10, 22, 10, 22)     # corner
wall(14, 22, 18, 22)     # bath door gap x 10-14, couple door starts at 18
wall(22, 22, 29, 22)     # couple door gap x 18-22
# vertical splits
wall(10, 22, 10, 35)
wall(18, 22, 18, 35)
# closet line, gap x 15.5-18
wall(10, 31, 15.5, 31)

def swing(hinge, radius, a0, a1):
    pts = arc_points(hinge, radius, a0, a1)
    d.line(pts, fill=(160, 40, 40), width=2)
    d.line([pt(*hinge), pts[0]], fill=(160, 40, 40), width=2)
    d.line([pt(*hinge), pts[-1]], fill=(160, 40, 40), width=2)
    d.ellipse([pt(hinge[0] - 0.15, hinge[1] + 0.15), pt(hinge[0] + 0.15, hinge[1] - 0.15)], fill=(160, 40, 40))

# Front door, hinge SE corner (17, 0), closed west, open north along kitchen wall
swing((17, 0), 4, math.pi, math.pi / 2)
# Child, hinge SE (10, 22), closed west, open north along east wall
swing((10, 22), 4, math.pi, math.pi / 2)
# Bath, hinge SW (10, 22), closed east, open north along west wall
swing((10, 22), 4, 0, math.pi / 2)
# Couple, hinge SW (18, 22), closed east, open north along west wall
swing((18, 22), 4, 0, math.pi / 2)
# Closet door, hinge NE of bath (18, 31), swings north into closet
swing((18, 31), 2.5, math.pi, math.pi / 2)

def box(x0, y0, x1, y1, fill):
    d.polygon([pt(x0, y0), pt(x1, y0), pt(x1, y1), pt(x0, y1)], outline="black", fill=fill)

box(0.4, 4, 2.4, 8, (140, 140, 140))          # chimney
box(6, 6, 9.5, 8.5, (190, 160, 120))          # table
box(4.2, 7.2, 5.6, 9.2, (170, 140, 100))      # seat
box(0.5, 27, 3.7, 33.3, (210, 200, 180))      # twin
box(11.2, 28.4, 16.2, 30.8, (200, 210, 220))  # tub
box(16.4, 26.5, 17.7, 28.2, (210, 210, 210))  # toilet
box(16.4, 24.2, 17.7, 25.6, (180, 200, 210))  # basin
box(23, 28.3, 28, 35, (220, 210, 200))        # queen
box(27, 7.5, 29, 10.5, (60, 60, 60))          # stove
box(27, 3.5, 29, 5.5, (180, 190, 200))        # sink

def label(text, x, y, f=font):
    d.text(pt(x, y), text, fill="black", font=f, anchor="mm")

label("PORCH", 14.5, -4)
label("LIVING", 8, 8)
label("KITCHEN", 23, 8)
label("HALL  8 FT", 14.5, 18)
label("CHILD", 5, 30)
label("BATH", 14, 27)
label("CLOSET", 14, 33)
label("COUPLE", 23.5, 26)
d.text((OX, 18), "30 FT by 36 FT exterior", fill="black", font=title)
d.text((OX, img.height - 48), "Red arcs swing into the room and park on the side wall. The hall has no leaf.", fill=(120, 30, 30), font=small)

img.save(r"c:\dev\HomeWorld\Docs\art\cabin\SM_Home_Cabin_doors.png")
print("wrote", img.size)
