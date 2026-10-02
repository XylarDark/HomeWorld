# Grok Imagine prompts — environment maps and asset sheets

**Purpose:** turn Imagine's output into *measurement*, so an agent can place geometry from a
picture instead of guessing. Two artefacts per zone:

| Artefact | Answers | Consumed by |
|---|---|---|
| **The grid map** | where things are, how far apart | the placer — becomes world coordinates |
| **The asset sheet** | what each object looks like | the modeller — becomes geometry + master material |

⚠️ **The honest limit, stated first.** Image models are *bad at numbers*. A diffusion model
cannot count metres and will produce confident, plausible, wrong dimensions. So the grid map
must be built on a **visible ruler** and read as *proportions to be measured by a human or an
agent with a scale bar*, not as authoritative coordinates. Anything else and you get
confident garbage — the same failure as an inverted sign on a headline number.

**Therefore every prompt below does three things:** puts a literal ruler on the canvas,
demands a countable grid, and asks for a **legend keyed to named objects**. If the model
ignores the ruler, the output is still useful as composition reference and **must not be used
for distances**. Check it before trusting it.

---

# PART 1 — THE GRID MAP

## 1A. The homestead — top-down measured grid

```
A precise top-down architectural site plan of a small floating island homestead,
viewed from directly above, orthographic, no perspective, no tilt.

CRITICAL - include a literal measuring apparatus:
- Draw a clear 1-metre grid over the entire image as thin cyan lines.
- Place a horizontal scale bar in the bottom-left corner labelled exactly
  "0    1    2    3    4    5    6    7    8    9    10 METRES"
- Mark the island's longest axis with a dimension line labelled in metres.
- Every object must have a leader line to a small label box giving its name
  AND its approximate size in metres, e.g. "SM_Cabin 5.5 x 4.5 x 5.5 m".

The island is roughly 21 m across one way and 14 m the other. The plateau is
irregular - layered torn earth at the rim, NOT a circle and NOT a clean disc.

Place these objects at these positions, all in metres from the island centre
(0,0) with +Y toward the back:

  SM_Cabin              5.5 x 4.5 x 5.5 m    at (-6.0, +1.0)   gabled log cabin, stone chimney
  SM_Garden_Beds        4.0 x 2.5 x 0.6 m    at (-3.5, +0.5)   three raised planters in a row
  SM_Lookout_Pad        3.0 x 2.5 x 0.2 m    at (+7.0, -3.5)   flat stone pad at the cliff edge
  SM_Glider_Perch       2.0 x 1.5 x 0.5 m    at (+7.5, -4.5)   small perch beside the pad
  SM_Shrine_Homestead   1.5 x 1.5 x 2.0 m    at (-2.0, +3.5)   four posts and a lintel, see-through
  SM_Pine_A             2.0 x 2.0 x 9.0 m    at (-8.0, -2.0)   tall pine
  SM_Pine_B             2.0 x 2.0 x 8.0 m    at (+3.0, +3.0)   tall pine
  SM_Pine_C             2.0 x 2.0 x 10.0 m   at (+5.5, +1.5)   tall pine
  SM_Path_Homestead     10.0 x 1.2 m strip   from (0,0) to the lookout, passing the garden

A stone path must visibly connect the cabin, past the garden, to the lookout pad.
A cliff mass runs along the far rim with three torn faces. Drop shadows straight
down, no sun angle, so the plan reads flat and measurable.

Style: clean technical line drawing, white background, black outlines, one accent
colour per object family. This is a working drawing, not an illustration.
```

**Then measure it back.** Put the saved image in the Blender scene at true scale, add a
`SM_ScaleRef_Adult` (0.6 × 0.4 × 1.8 m) beside one object, and measure whether the drawn
proportions match the spec. If they do not, the spec wins and the image is composition only.

---

## 1B. The planet — two zones, top-down

Zone 1 is the **open field**; Zone 2 is the **pine forest with the camp**. Draw them as
**two separate plans**, because they have different mechanic language and a different
boundary between them.

```
Two separate top-down measured site plans side by side, both orthographic from
directly above, no perspective. Same measuring apparatus on BOTH: a 1-metre cyan
grid across each, a labelled 0-10 m scale bar bottom-left of each, and leader
lines to label boxes giving every object's name and size in metres.

--- ZONE 1: THE OPEN FIELD ---
Open, low, long sightlines, sparse. Roughly 60 x 40 m of walkable ground.

  SM_LandingCircle     8.0 x 8.0 m        at (0, -70)     clearing with a ring of stones
  SM_Gather_Bushes     ~1 m tall each     4 of them      at (5, -88), spread over 3 m
  SM_Path_Planet_SegA  1.4 m wide x 18 m  from (2, -82)
  SM_Path_Planet_SegB  1.4 m wide x 22 m  from (8, -100)
  SM_Path_Planet_SegC  1.4 m wide x 20 m  from (4, -118)
  SM_RES nodes         ~0.5 m each        scattered along the path - herbs, seeds, wood, stone, fibre
  SM_Shrine_Return     1.5 x 1.5 x 2.0 m  at (6, -75)     four posts, a lintel, see-through gap
  SM_SpiritWound_01    1.1 x 1.1 x 2.4 m  at (-4, -115)   STANDING broken marker, one post shorter
  SM_Roof_Hamlet_01    3.8 x 3.2 m        at (-12, -90)    distant roofline
  SM_Roof_Hamlet_02    3.3 x 2.7 m        at (-8, -105)
  SM_Roof_Hamlet_03    ~3 m               at (-14, -112)

This zone must read as GATHER: open, low, spreading, nothing tall in the middle
except the two standing spirit markers. Trees only at the far edges.

--- ZONE 2: THE PINE FOREST WITH THE CAMP ---
Dense pines, close walls, low visibility - a marked contrast to Zone 1. The camp
sits in a clearing. The forest closes as a TREELINE boundary: pines thicken into
an unbroken wall, and beyond the wall the ground simply continues out of view.

  THE CAMP - mark the firing line and the sleeper positions explicitly:

  NODE_GUARD           1.0 m wide figure at (12, -90), FACING SOUTH-WEST toward
                       the approach. Draw its line of sight as a dashed red wedge
                       roughly 25 degrees wide, extending about 12 m. Label it
                       "LINE OF SIGHT - player must avoid this".
  NODE_SLEEPER_1       reclining figure at (10.5, -88.5) - inside the guard's arc
  NODE_SLEEPER_2       reclining figure at (13.5, -88.5) - inside the guard's arc
  CAMP_FIRE            1.2 m across at (12, -89) - the one warm light in the zone
  SM_Path_Approach     the player's walking line in from the treeline, passing
                       OUTSIDE the dashed arc, reaching the camp

  Draw the camp clearing as roughly 20 m across, ringed by pines so the player
  cannot simply walk around the encounter - the approach is a corridor.
  Label the treeline "TERRAIN CONTINUES - not a wall".

Style: technical line drawing, white background. Zone 1 in cool open tones,
Zone 2 in dense dark green, to make the difference between mechanic languages
obvious at a glance.
```

---

# PART 2 — THE ASSET SHEETS

**One isolated image per object.** These become the modeller's reference, so background and
lighting must be flat and the object must be unambiguous.

```
A single [OBJECT] on a plain flat mid-grey background, centred, filling about
70% of the frame, lit by even soft light from the front with no harsh shadows,
no cast shadow on the ground, no props, no scenery, no other objects.

Rendered as a clean faceted low-poly game asset: flat shaded, hard edges,
visible planar facets, no smooth subdivision, no texture, no decal, no text
label, no watermark. Cartoon and handmade in feel - warm, readable, simple -
not photoreal, not gritty, not sci-fi, not neon.

[PASTE THE MEASURED SIZE AND ANY SHAPE NOTE HERE]
```

### Angles — how many, and why

**Three per object: front elevation, 3/4 view, and top-down.** That is the minimum that lets
an agent rebuild a volume without guessing.

| Angle | Why it is needed | What it fixes |
|---|---|---|
| **Front elevation** | height and width are read directly off a flat silhouette | "is it tall or is it wide" — the exact number the collision check uses |
| **3/4 view** | shows depth, which a front elevation completely hides | depth is the dimension most often wrong, because a flat image invites a flat model |
| **Top-down** | plan footprint and whether the object occludes what is behind it | whether two objects 1.5 m apart actually overlap at the player's eye height |

**Why not more:** a fourth angle adds detail without adding *dimension*. Profile (side) and
3/4-rear are cheap to derive from front + top + 3/4, and asking for them mostly produces
images that drift stylistically from the first three — which is worse than one clean set,
because the model then has to reconcile them.

**Why not fewer:** front + top only is the classic mistake — you get a correct width and height
and a completely invented depth. One view is worse still: an agent cannot tell a 1 × 1 × 3
post from a 1 × 3 × 1 shelf.

**The two exceptions, where one more view earns its place:**

- **The camp** (guard, both sleepers, fire) — add a **player's-eye view from the approach**,
  at 1.7 m height. It is the only view that tests the thing that matters: whether the player
  can see what they are supposed to react to, and whether the guard's arc reads before they
  are inside it.
- **The spirit wound and the shrines** — add a **low-angle view from 20 m**, because the
  locked rule is that these must be identifiable **by shape at 20 m**. A 3/4 close-up will
  make anything look like a shrine. Only a 20 m view tests the actual requirement.

### The full asset list

Eleven objects, three angles each, 33 images — plus the two extra views above, so 35.

| # | Object | Size (m) | Family | Note for the prompt |
|---|---|---|---|---|
| 1 | `SM_Cabin` | 5.5 × 4.5 × 5.5 | build_place | rustic log cabin, gabled, stone chimney, porch with two posts and a rail |
| 2 | `SM_GardenBed` | 1.8 × 1.0 × 0.5 | build_place | raised wooden planter, empty soil, three of a kind |
| 3 | `SM_Kettle` | 0.5 × 0.5 × 0.7 | build_place | squat stone kettle with a wooden handle, on a low stone base |
| 4 | `SM_Pine` | 2.0 × 2.0 × 9.0 | spine | stylized conical pine, layered flat foliage cards, one trunk |
| 5 | `SM_Lookout_Pad` | 3.0 × 2.5 × 0.2 | spine | flat stone pad, deliberately dull, at a cliff edge |
| 6 | `SM_Shrine` | 1.5 × 1.5 × 2.0 | spirit | four posts, a lintel, an open gap you can see through, small cyan glow inside |
| 7 | `SM_SpiritWound` | 1.1 × 1.1 × 2.4 | spirit | broken standing stone, **right post shorter, lintel broken**, glow in the gap. Damaged, not built |
| 8 | `SM_Rune` | 1.6 × 0.4 × 0.9 | stealth | low broken horizontal stone, wider than tall, no glow |
| 9 | `SM_PlantSlot_Sprout` | 0.5 × 0.5 × 0.68 | heal | single narrow upright plant, soft, on a small soil pad |
| 10 | `NODE_GUARD` | ~1.8 m tall | combat | faceted stone-and-leather brute, standing, **facing south-west** |
| 11 | `NODE_SLEEPER` ×2 | reclining | combat | the same brute design asleep, must be readable as the same creature |

---

# PART 3 — VERIFICATION, and the order to do this in

## Measure before you build

1. **Drop the grid map into Blender at true scale.** Add a 1.8 m adult reference box.
2. **Compare three things** against the spec: the cabin's footprint, the shrine's gap, the
   distance from cabin to lookout (spec: ~15 m, a ~10 s walk at 1.4 m/s).
3. **If the ruler is missing or the proportions are off, the image is composition reference
   only.** Use it for shapes and layout ideas, never for coordinates. The spec is the
   source of truth — that is the whole point of DEC-0019 and of the gap that started this.
4. **Record what you measured in the spec JSON**, not in a comment. The original defect was a
   spec cited in a comment while the numbers lived in a script.

## Do assets before the camp; do the camp last

The camp is the one object set that changes the answer to a question rather than filling a
gap. The other ten are known shapes with known sizes. Author the ten, place them, verify the
report — then author the camp with the firing line you drew, and check the line of sight in
game, not in the picture.

## The order, cheapest first

| Step | Work | Why first |
|---|---|---|
| 1 | Homestead grid map (1A) | fixes positions for 5 objects at once |
| 2 | Assets 1–5, 8, 9 (three angles each) | no open questions, ten beats' worth of props |
| 3 | Zone 1 grid map (1B) | gather zone, and it is the one you will walk through most |
| 4 | Assets 6, 7 (+ the 20 m view) | spirit family, one silhouette to teach |
| 5 | **Camp** — grid, then 3 angles, then the player's-eye view | the climax; needs the firing line |
| 6 | Measure everything back into the specs | closes the loop that started this |

---

## What this cannot do

- **It cannot give authoritative dimensions.** Diffusion models do not count. The ruler is a
  request, not a guarantee, and a missing ruler means the numbers are decoration.
- **It cannot resolve the island-top fork.** `SM_IslandTop.json` says 21 × 14 × 0.5 crust,
  `GRAYBOX_LAYOUT.md` says 21 × 14 × **4.0**, the blend is 19.3 × 10.7 × 0.45. Three
  answers, none matching, and no image picks between them — that is a decision, not a
  measurement.
- **It cannot justify `M_FamilySilhouette` or `M_ValleyNight`.** They are in the blend and
  not among the ten masters. An image of a valley at night does not make it canon.
- **It will not make `heal`, `stealth` and `combat` into sections.** They are in the prototype
  with one volume each. A fuller reading is a bigger job that no T0 beat currently names.
