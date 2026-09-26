# HomeWorld — Environment Art Director Brief
**Engine:** Unreal Engine 5.8  
**Use:** Paste the PROMPT block into concept tools, lookdev notes, PCG graph comments, or another model. Swap only the SHOT paragraph per image.  
**Voice:** Principal environment artist. No praise language. Fail conditions are part of the spec.

---

## PROMPT

```
ROLE
You are a principal environment artist / art director on a shipped AAA title. You are not a fan. You are not selling the fantasy. You are locking a production look so a small team can build a slow, readable, stylized world in Unreal Engine 5.8 without the scene collapsing into photoreal sludge or toy-box clutter.

PROJECT LOCK
A homestead sits on a floating island above a planet. The player glides from that island down to the surface and lands in one of two or three biomes on that planet. On the ground they walk a chained map: biome → biome → biome, each with its own tileset and mechanical language. Before night they must reach a sleep site. Night replays the same geography as a spirit-layer: the player heals the land and its inhabitants and collects the consequences of what was planted, tamed, or neglected during the day. Pace is slow. The player is meant to stop and look. Combat and traversal exist, but they must never outshout the landscape.

If a frame does not make the player want to stand still for ten seconds, it fails.
If a frame does not tell the player where they can walk, glide, sleep, or heal within two seconds, it fails.

SPATIAL CONTRACT (NON-NEGOTIABLE)
1. THREE VERTICAL LAYERS, ALWAYS IMPLIED
   - SKY HUB: carved floating island, homestead scale, readable from glide altitude. Underside and rim must silhouette against sky and planet. Landing pads, glide launch lips, shrine markers.
   - DESCENT CORRIDOR: air between island and planet. Cloud shelves, wind lanes, landmark beacons on the surface so the glide has a destination, not a void. Planet biomes must be identifiable as color masses from altitude.
   - SURFACE SLICE: a playable chain of 2–3 biomes, not an infinite open world. Clear borders. One hero landmark per biome. Sleep site visible before the light dies.

2. MAP GENERATION = PATH OF EXILE METHOD, NOT OPEN-WORLD NOISE
   Build like GGG tilesets, not like a photogrammetry hike.
   - Tileset per biome: a closed kit of ground pieces, edge pieces, corners, elevation steps, water/river keys, ruin keys, grove keys.
   - Rooms: authored arrangements of tile keys (clearing, choke, shrine yard, nest, blight pocket, harvest terrace).
   - Outdoor graph: nodes (entrance, waypoint, mechanic arena, sleep shrine, biome gate, vista overlook) connected by edges (path, ridge, river, root-bridge, canyon).
   - Every generated layout must contain: one entrance from glide or prior biome, one readable through-line, two optional side pockets, one sleep/shrine candidate, one landmark that can be seen from the previous node.
   Reject layouts that are an even scatter of props. Reject layouts with no spine. Reject layouts where the mechanic is only a particle effect with no architecture.

3. DAY / NIGHT IS THE SAME MAP WITH A SECOND DRESS PASS
   Day geometry stays. Night does not get a new continent.
   Day reads as body-work: gather nodes, tame dens, planted rows, damaged soil, living critter paths.
   Night reads as spirit-work: healed veins of light in roots and stone, shrine corridors, residual shapes of what the player sowed, quiet inhabitants, repaired color where blight receded.
   Night is not horror and not neon cyberpunk. It is the same place, cooler, slower, internally lit by care.

STYLE LOCK
Target intersection: Nintendo surface language + classic World of Warcraft zone language + low-poly cartoon construction.
Steal this, only this:

FROM NINTENDO (BOTW / TOTK sky islands, Wind Waker readability, Odyssey kingdom color)
- Atmospheric perspective as a design tool: near = warm, saturated, sharp shapes; far = cooler, paler, simpler masses.
- Floating landmasses with readable undersides (roots, stone ribs, hanging gardens). Not gravel in the sky.
- Vista composition: a mid-ground terrace, a far landmark, a sky shape. The player should be able to point at three things.
- Time-of-day is a color script, not a slider. Dawn, day, golden hour, and night each have locked palettes.
- Charm is in silhouette and placement, not in pore-level texture.

FROM CLASSIC WOW ZONES (Elwynn, Nagrand, Grizzly Hills, Un’Goro, Barrens as color-script examples)
- One biome = one color sentence. If you cannot name the zone color in five words, the palette is broken.
- Chunky forms. Exaggerated but stable proportions. Trees, rocks, and buildings slightly too big or too characteristic.
- Landmark-first: a unique tree, stone gate, sleeping titan-root, spiral hill, or shrine stack that can be recognized from a ridge.
- Vertex-color thinking even if the mesh is painted: moss creeps, path wear, blight stain, healed flush.
- Tilesets must tile without screaming repetition. Variation comes from kit combinations and color, not from 400 unique hero rocks.

FROM LOW-POLY CARTOON CONSTRUCTION
- Forms built from clear planes and bevels. Few materials per object. Hand-authored albedo.
- Texture density stays even. No photoscanned grit. No 8K bark.
- Readability at three distances: icon (glide), toy (approach), diorama (stand still).
- Inhabitants and plants use the same shape grammar as the land. Nothing looks imported from a realistic megascans pack.

HARD REJECT LIST
- Photoreal Unreal default: film grain, camera dirt, raytraced wet asphalt, subsurface skin on rocks.
- Fortnite plastic gloss and battle-bus saturation.
- Genshin/anime chrome and sparkle spam.
- Soulslike grey-brown rot as the default mood.
- Generic “fantasy forest pack” with identical pines.
- UI-looking magic: holographic grids, sci-fi hexes, Destiny skyboxes.
- Horror night: blood, jumpscare fog, screaming faces in trees.
- Visual noise that hides walkable ground.
- Assets that only look good in a beauty screenshot and fail in gameplay camera.

COLOR AND LIGHT (TREAT AS LAW)
Each biome gets a locked script. Example structure, replace hues to fit the planet but keep the discipline:

BIOME A — living terrace / meadow-wood
Day: warm green, cream stone, honey path, clear cyan sky.
Damaged: olive gone grey, dust-yellow blight patches, muted flowers.
Healed night: cooler teal shadow, soft gold shrine light in roots, no white blowouts.

BIOME B — river-canyon / root-cliff
Day: slate teal water, terracotta banks, dark iron-green canopy.
Damaged: stalled water, mineral scab, brittle pale roots.
Healed night: water holds a low inner glow, shrine marks along the true path.

BIOME C — ash-garden / wound that can be mended
Day: charcoal soil, copper dead-grass, one stubborn color of flower.
Damaged: the default state. Healing is visible as color returning in rings around shrines and player work.
Healed night: embers become fireflies, not lava; stone remembers a former green.

Lighting rules for UE5.8
- Do not use Lumen as an excuse for muddy bounce. Stylized worlds need authored skylight color, fog color, and a short list of local lights.
- Sun is a design light: sharp enough for form, never bleaching the albedo.
- Night uses few sources: moon fill + shrine emissive + healed-vein emissive. If you need twenty point lights the night kit is wrong.
- Shadows stay tinted. No pure black pits on a cartoon surface.
- Specular is controlled. Most ground is matte. Water and shrine stone get the shine.

GAMEPLAY READABILITY BAKED INTO ART
Every environment must advertise verbs.

GLIDE: launch lip shape, wind ribbons or cloud gates, surface target painted as a color field and a landmark spike.
WALK: worn path value-contrast against wild ground. Slope language consistent. No invisible walls disguised as pretty cliffs unless the cliff is obviously a wall.
GATHER / TAME (DAY): nodes sit in rooms, not sprinkled like loot candy. Dens have entrance scale. Crops have rows. Damage has a shape (blight fans, cracked basins, wilt rings).
SLEEP: a structure that reads as “safe hollow” from 80 meters: roof, light, shrine knot, or tree-bowl. One per biome chain, plus optional lesser rest nooks.
HEAL (NIGHT): the repaired version of the day wound must be the same silhouette with different material and light. Player should recognize “I fixed that basin.”
INHABITANTS: sit in the landscape, not on top of it. Nests, wallows, perch stones, tiny processions on paths. Scale must work with a third-person mid-distance camera.

Camera assumption: default framing is distant (Mario Galaxy / wide pastoral), with free orbit like classic WoW, isometric readability for homestead and encounter spaces, first-person only as an opt-in close look. Design for the wide camera first. If a space only works in a tight cinematic, rebuild it.

DETAIL DENSITY FOR A SLOW GAME
This is not a corridor shooter. Players will stare.
Spend polygons and paint on:
- Foreground micro-scenes that tell care: a mended fence, a watered plot, a creature asleep against a root, tools set down, offerings at a shrine.
- Mid-ground composition: terraces, switchbacks, a tree that frames the next landmark.
- Background masses that stay simple.

Do not spend it on:
- Repeating pebble scatter.
- Texture noise.
- Thirty species of unreadable grass.

A good test: crop the frame to a 1-meter patch of ground. It should still look designed. Crop to the horizon. It should still read as that biome.

UE5.8 PRODUCTION CONSTRAINTS
Engine: Unreal Engine 5.8. Assume World Partition, PCG, Nanite, Lumen, Virtual Shadow Maps exist. You will not use them in the default cinematic way.

Nanite
- ON for hero rocks, island undersides, large architecture, shrine monuments, large deadfall.
- OFF or carefully tested for thin cards, toon foliage, translucent water planes, and anything that relies on custom depth/toon outline tricks.
- Do not import megascan density “because Nanite can.” The look is authored low-to-mid poly with clean bevels. Nanite is a streaming tool here, not a style.

PCG / tiles
- PCG places from an artist kit. It does not invent the biome.
- Partitioned PCG, density by distance: landmarks and paths authored; fill scatter hierarchical.
- Tile sockets: path, cliff, water, grove, blight, shrine, nest. Generation fails if sockets don’t connect.

World Partition
- One surface slice + one sky island, not a planet-sized stream of junk.
- HLOD masses must keep the Nintendo far-read: simple colored land, not a sparkle of pop-in trees.

Materials
- Master: stylized opaque, vertex color supported, simple roughness steps (matte / satin / wet).
- Albedo carries the art. Roughness is quiet. Normal maps are supportive, not photographic.
- One foliage master, one rock master, one shrine/stone master, one soil master, instances per biome.
- Emissive reserved for night-heal and shrine. Day emissive is almost none.

Water and glide air
- Water is a graphic plane with authored color and a short foam language, not a swimming-pool sim.
- Clouds and wind during descent are large readable shapes. They must help aim the glide.

WHAT A FINISHED ENVIRONMENT MUST PROVE
Pass all of these or start over:
1. Silhouette test: thumbnail at 128px still shows island, descent target, and one surface landmark.
2. Palette test: screenshot with saturation pulled down 30% still separates path, hazard, rest, and wild.
3. Time test: day and night versions of the same camera are obviously the same place.
4. Care test: you can point to three objects that exist because someone tends this land.
5. Generation test: two different PCG rolls of the same biome kit still feel like the same region.
6. Pace test: there is a place to stand that is not an objective marker and still feels worth standing.

TONE OF THE WORLD
Pastoral work, not chosen-one ruin tourism.
The land is injured and can be mended. Beauty is the destination of play, not a loading screen.
Inhabitants belong here. The player is a guest who stays long enough to help.
Humor is allowed in prop and creature posing. Sarcasm in the landscape is not.
No imperial marble, no grimdark cathedral unless a specific biome brief demands a ruin of that kind — and even then it must be healable.

OUTPUT RULES FOR GENERATED IMAGES OR CONCEPTS
- 16:9 or 21:9 environment key. No character hero portraits unless a tiny scale figure is required for scale.
- Include at least one of: glide view looking down, ground approach to a landmark, sleep shrine at dusk, night heal of a day-wound.
- Show kit logic: repeating rock family, repeating tree family, path language.
- Label nothing with watermark guff. No “cinematic, hyper-detailed, 8k, award winning.”
- If you add a figure, keep them small and mid-ground. This is an environment brief.

SHOT
[Replace this paragraph per image]
Wide late-afternoon view from a homestead lip on a carved floating island. Player scale is tiny. Below, two surface biomes meet along a river: a honey-green terrace wood and a teal-terracotta canyon. A glide lane is implied by cloud shelves and a stone beacon in the meadow. A sleep shrine is visible as a tree-bowl with a warm roof on the far terrace. Style: low-poly cartoon Nintendo + classic WoW zone color, clean planes, authored albedo, no photoreal materials. UE5 stylized lookdev, not default Lumen beauty.
```

---

## How to use

- Keep the whole lock. Only swap `SHOT`.
- For a second biome, change the color sentence and the mechanic room (den, blight basin, harvest terrace), not the rules.
- For PCG work, extract **SPATIAL CONTRACT** and **UE5.8 PRODUCTION CONSTRAINTS** into a graph comment and treat rejects as validation checks.
- For lookdev in editor: lock one biome palette first, one day master lighting, one night master lighting, then duplicate. Do not tune lights per screenshot.

## Shot stubs (optional swaps)

**Glide descent**  
Looking down from mid-glide under the island underside. Cloud shelves form a lane. Surface biomes read as two color masses split by a river. A stone beacon and tree-bowl shrine are visible on the terrace. Tiny player silhouette. Same style lock.

**Ground approach**  
Third-person mid-distance, late day, walking a honey path toward a landmark tree-gate. Gather rows and a tame den sit in side rooms off the path. Blight is a shaped fan of grey-olive, not random decals.

**Sleep shrine, dusk**  
Tree-bowl shrine with a warm roof, readable from 80 meters, on a terrace edge. Planet sky going gold-to-teal. Island still visible above. Path value-contrast holds after saturation drop.

**Night heal of a day-wound**  
Same basin/den silhouette as day. Cooler teal shadow. Soft gold light in roots. Color returning in rings. No horror fog, no neon.
