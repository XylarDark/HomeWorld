# Opening tutorial interview

Open. One lock at a time. Scribe the pick here before the beat it blocks. Do not start the next round until this one has a pick or a skip.

The sequence is the Opening tutorial in [`Docs/VISION_BOARD.md`](../VISION_BOARD.md). This file does not copy it. The queue is [`OPENING_TUTORIAL_TASKS.md`](OPENING_TUTORIAL_TASKS.md).

## Already locked — do not ask

- The walk, stop, and hop on `L_SizeTest` pass the initial movement pass. 2026-10-17.
- A heart sits beside the prop and turns with the view. Its height starts at the player's head and rises so the shape never clips the prop or the floor, including as the shape scales. 2026-10-21.
- The shoulder wisp marks an object, and the opening interact reaches it, only when that object is within 280 cm and inside the passed aim box: half-extent 0.3, center 0.5 above the middle of the view. The development frame is off. 2026-10-21.
- That box stays the look point. The hard edge is gone. Within 280 cm and in front of the camera, the actor closest to that point takes the shoulder wisp. The perched actor keeps it until another is at most three quarters of that look distance. The wisp on the shoulder means there is no interact. The wisp perched beside the actor, with one world E, is the interact. No crosshair and no frame. Heart placement is unchanged. 2026-10-22.
- The fastest homestead walk already kept in play is 450 cm/s (`BodyWalkSpeed` in `Source/HomeWorld/HomeWorldTraversalComponent.h`).
- The approach hides the cottage with a copse of pines and large stones. Hills and valleys are later. [`Docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`](../handoffs/research/TERRAIN_HEIGHT_LATER.md).
- The walk stays 450 cm/s until a replay says that single speed is wrong.
- The played return stands. The partner walks inside and waits by the kettle. The child goes to their room. 2026-10-18.
- Sleep in the bed grants spirit form. Night does not. The bed returns you to the body. Dawn does not. The Night sentence is `hw.Playtest.FastForward sleep`, then E at the bed: into spirit or not, stayed on the island, and whether the sky stayed day. 2026-10-21.
- The day glide is a body glide toward camp smoke, with no pickup. The smoke is the existing day-descent sign. No smoke actor until the camp clearing is placed. 2026-10-21.
- The dawn mist is not an actor and not a new state. It stays a sky read for the later dress row. 2026-10-21.
- A dawn-glide stop, when added, stops before the launch at a marker spawned for that run only. It does not add a meadow. 2026-10-21.
- A bonk launches you back onto the island. It does not slow the step and does not dim the shoulder light. It does not wait on the mist.
- The bull stays the later field and cave tame.
- The armor gift is the backpack. The glider is crafted at the armory at dawn, and the descent waits on that craft. Speed and bonk tries stay. Round 6.
- The first glider spends wood, silk, and metal already in the armory chest at dawn. This night does not gather them. Later crafts spend what a wisp delivers from the warehouse. 2026-10-21.
- That spend is one wood, one silk, and one metal. Silk and metal stay out of the six-slot carry. An empty chest leaves the armory table's open reply. A press with that stock present crafts the glider, and the descent refuses until then. 2026-10-21.
- A healed wisp is set with E on a wood, herb, or stone node. The node fills to 10 and that pile is credited to the matching chest. The player does not carry it. A second fill is refused. The wisp returns to the legs. Silk, fiber, and metal nodes are refused. 2026-10-21.
- The dawn meadow's site is chosen at the desk on `L_SizeTest` after the Night pass. No coordinate is written. 2026-10-21.
- One guard's sightline is the existing spirit-lit box: 180 by 180 by 120 cm. A missing guard does not count as an avoid. 2026-10-21.
- Herb at the hot springs revives a damaged wisp so it follows at the legs and can take a task or a delivery route. The claimed companion stays on the shoulder. One revive spends one opening herb chunk. The click heart on that wisp, drawn when it is collected, sets the heal: 20 seconds when the heart is completed in 3 seconds or less, plus 10 seconds for each second over 3. A partial second counts, so 3.1 and 4.0 are both 30 seconds, and 4.1 is 40. The heart may run past 3 seconds. Lead confirmed this for the binary on 2026-10-21. The Night table stays empty until the bed press.
- This tutorial night finds damaged wisps only at the copse, the pond, and the hot springs. Wider sites stay later. 2026-10-21.
- E at the hot springs starts the heal from 600 cm. 2026-10-21.
- Healed wisps keep the built arc at the legs: the first two sit 34 cm to either side and 20 cm behind, the third sits 52 cm behind in the center, and a fourth reuses a slot. 2026-10-21.
- A finished pad ladder sleeps that guard. Wait calls the glide home and does not sleep the guard. A reach is spirit within 280 cm of a waking guard. One E on the shrine, after the three sleeps, frees a separate captive and walks the partner. Moss is not a new carry id. `hw.Playtest.FastForward shrine` runs the ladders and stops before that E. Round 17. 2026-10-21.
- The warehouse is not on the tutorial night. No warehouse building, and no new spoken line. The healed wisps at your legs are the hint. The planetoid teaches setting them on herbs, trees, and the other nodes. Spawned nodes have quality, and the player hunts the best. Quality increases time, durability before breaking, and lowers crafting time. Time means the crafted effect lasts longer. Durability is uses before it breaks. Crafting time is how long the station takes. Node modifiers are tagged mods. The wisp and the delivery route weight which mods can roll. Paradox corrupts. The rune stays visible. 2026-10-21. The tags are effect duration, durability, and crafting time. Other tags wait until you name one. Wrath / Grace is the first axis. Grace weights effect duration. Wrath weights durability. This axis does not weight crafting time. The second axis is Greed / Generosity. Generosity lowers crafting time. Greed snatches the craft when the stroke is late or wrong. This axis does not weight effect duration or durability. The other five axes wait until a new tag is named. 2026-10-21.

## Rounds

### Round 1 — Approach

Picked 2026-10-17. The cottage is hidden by a copse of pines and large stones. The pad grows so the start sits beyond that copse. The ground stays flat. Hills and valleys wait in [`Docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`](../handoffs/research/TERRAIN_HEIGHT_LATER.md). The walk stays 450 cm/s until Luke replays the approach and says that speed is wrong.

### Round 2 — The exit

Picked 2026-10-18. The tutorial is one day on the island, starting at midday with the played opening. Evening and night stay on the island. The player wakes at dawn, still on the island. The mist clears at that dawn. The bonk does not wait on the mist. The last mechanic is the day glide down to the field. The field is the first wild place. It is not the tutorial.

### Round 3 — The dog

Picked 2026-10-18. One tame fight with a dog, on the island, is the first tame and the sin/virtue sample. They are the same lesson. The bull is unchanged.

### Round 4 — How the dog fight is passed

Picked 2026-10-18. The dog is injured and afflicted by Wrath. This beat is after crafting. Getting too close knocks you away. Approaching at anything faster than the slowest opening-wheel step also knocks you away. That step is 150 cm/s. At that step you draw a Grace symbol, and it eases the Wrath. Then you use an herb that has been mixed with a spirit. That mix is the crafted consumable. The dog is tamed. No camp combat. The bull is unchanged.

### Round 5 — What the island still introduces

Picked 2026-10-18.

- The armory lesson is the partner's gift. Round 6 names the piece and the exit craft. Speed and bonk tries stay.
- The observatory has no quest. Research has no quest. Curiosity and attention to subtle clues are what lead you there.
- Cooking is the kettle brew. No second recipe on the island.
- Fishing is after the dog. Stand at the pond and press E. One fish. No minigame.

### Round 6 — The backpack and the glider

Picked 2026-10-18.

- The partner's gift is the backpack. It is the first armor. It holds special items you find, for upgrades around the homestead, and only a limited number. That number is not named. It is not the material inventory. Materials stay in the station chests. The armory table opens. The kept walk stays 450 cm/s. Bonk tries stay.
- The glider is crafted at that table at dawn. It is the last new piece before leaving the island. The day glide does not start until that craft is done. The glide stays a body glide toward camp smoke, with no pickup. The mist still clears at that dawn.
- The glider's recipe is wood, silk, and metal. Round 8.
- Later armor is the encounter set in [`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`](../VIRTUE_ATTRIBUTE_BIBLE.md). This round does not build the mark bench.

### Round 7 — Night spirit piles

Picked 2026-10-18. The resource at each place is not named.

- You are spirit because you slept in the bed. Night does not grant the form.
- Wisps appear at the copse, the pond, and the hot springs.
- You set a spirit on a harvestable. It sits there and fills that node's pile to 10. Round 8 says the player does not carry that pile.
- The wider set of copse nodes stays later. This night is the first lesson.

### Round 8 — Wisps bring the materials home

Picked 2026-10-18.

- The player finds wisps and sets them. The player does not collect the materials.
- A tree gives wood. A tree with a silkworm infestation gives silk instead. A grass tuft gives fiber. A rock gives stone or metal. The wisp can gather either from rocks.
- At 10, the wisp flies back to the homestead and drops the pile in the chest beside the station that spends that material.
- Those chests are the crafting inventory. One sits beside each station that takes materials. They show what the wisps have brought.
- The hot springs show wisps and have no harvest pile yet.
- Fishing stays a game the player plays. It is not a wisp pile. The pond's yield is otherwise unnamed.
- The glider craft spends wood, silk, and metal from the armory chest.

#### 2026-10-19 — the wisp loop, restated

Luke restated the wisp loop on 2026-10-19. These lines supersede round 8 where they differ.

- You find a damaged wisp in the wild. It goes into the backpack as a special item; it does not follow you yet.
- Take it to the hot springs, deposit it there, and give it herb. Over time it heals and revives.
- A healed wisp follows you near your legs, not at your shoulder.
- Any wisp you carry can be assigned to tasks or delivery routes.
- Collection goes to a central warehouse. From there a wisp takes resources to the chests the player chooses. A delivery route is set with click start and click end.
- The armory-wood test was named and scratched.
- Closed 2026-10-21. The other five axes wait until a new tag is named.

#### 2026-10-21 — what the heal is for

Picked 2026-10-21. Herb at the hot springs revives a damaged wisp. It then follows at the legs and can be assigned to a task or a delivery route. The companion already claimed stays on the shoulder. One revive spends one opening herb chunk.

#### 2026-10-21 — heal time

Picked 2026-10-21. The click heart on a damaged wisp, drawn when that wisp is collected, sets that wisp's heal. Completing the heart in 3 seconds or less sets 20 seconds. Each second over 3 seconds adds 10 seconds. A partial second counts: 3.1 and 4.0 are both one second over, so the heal is 30 seconds, and 4.1 is 40. The heart may run past 3 seconds. One opening herb chunk is still spent when the heal starts at the hot springs. Lead confirmed this for the binary on 2026-10-21. The Night table stays empty until the bed press.

#### 2026-10-21 — hot-spring range

Picked 2026-10-21. E at the hot springs starts the heal from 600 cm. That is the distance to the spring, not the heal time and not the follower distance.

#### 2026-10-21 — leg followers

Picked 2026-10-21. Healed wisps keep the built arc at the legs. The first two sit 34 cm to either side and 20 cm behind. The third sits 52 cm behind in the center. A fourth reuses a slot. They stay off the shoulder.

#### 2026-10-21 — where the night wisps stand

Picked 2026-10-21. This tutorial night finds damaged wisps only at the copse, the pond, and the hot springs. Wider sites stay later.

#### 2026-10-21 — warehouse and node quality

Picked 2026-10-21. The warehouse is not on the tutorial night. The night hints that, on the planetoid, wisps can be set on herbs, trees, and the other nodes. Spawned nodes have quality. The player hunts the best quality. Quality increases time, durability before breaking, and lowers crafting time. Time means the crafted effect lasts longer. Durability is uses before it breaks. Crafting time is how long the station takes. Other related stat buffs are not named. On 2026-10-21 Luke set aside the virtue bible's "no hidden stat line" for node modifiers. The picked shape is tagged mods on the node. The wisp you set, and the delivery route, weight which mods can roll. Paradox corrupts: both poles, stronger, and they interfere. The rune stays the thing you see. The tags are effect duration, durability, and crafting time. Other tags wait until you name one. The map starts now, one pole at a time. The first axis is Wrath / Grace. Grace weights effect duration. Wrath weights durability. This axis does not weight crafting time. The second axis is Greed / Generosity. Generosity lowers crafting time. Greed snatches the craft when the stroke is late or wrong. This axis does not weight effect duration or durability. The other five axes wait until a new tag is named. The night, the dog, and the zone order stay.

#### 2026-10-21 — mod tags

Picked 2026-10-21. The tags are effect duration, durability, and crafting time. Other tags wait until you name one. Pole weighting starts now, one pole at a time. The first axis is Wrath / Grace. Grace weights effect duration. Wrath weights durability. This axis does not weight crafting time. The second axis is Greed / Generosity. Generosity lowers crafting time. Greed snatches the craft when the stroke is late or wrong. This axis does not weight effect duration or durability. The other five axes wait until a new tag is named.

#### 2026-10-21 — the glider's materials

Picked 2026-10-21. The first glider spends wood, silk, and metal already in the armory chest at dawn. This night does not gather them. Later crafts spend what a wisp delivers from the warehouse.

#### 2026-10-21 — the warehouse hint

Picked 2026-10-21. No warehouse building on the tutorial night, and no new spoken line. The healed wisps at your legs are the hint. The planetoid teaches setting a wisp on a herb, a tree, or another node.

### Round 9 — Where the dawn meadow sits

Picked 2026-10-21. The site waits until the Night pass releases `L_SizeTest`. No landmark and no coordinate is named. Nothing is placed for it on that map.

### Round 10 — How far a guard can see

Picked 2026-10-21. One guard's sightline is the existing spirit-lit box: 180 by 180 by 120 cm. A missing guard does not count as an avoid. Nothing is placed for it while the Night pass owns `L_SizeTest`.

### Round 11 — The dawn mist

Picked 2026-10-21. No mist actor and no new state. The line stays a sky read for the later dress row.

### Round 12 — Camp smoke

Picked 2026-10-21. The day glide keeps the existing smoke sign. No smoke actor until the camp clearing is placed.

### Round 13 — The dawn-glide stop

Picked 2026-10-21. The stop is before the launch, at a marker spawned for that run only. No meadow is added.

### Round 14 — The Night sentence

Picked 2026-10-21. `hw.Playtest.FastForward sleep`, then E at the bed. The sentence says whether that press granted spirit, whether the player stayed on the island, and whether the sky stayed day. The table stays empty until that play.

### Round 15 — The heal in the binary

Picked 2026-10-21. The binary uses the heal lock: 20 seconds at 3 seconds or under, plus 10 seconds per second over. A partial second counts. The heart may run past 3 seconds.

### Round 16 — The meadow site

Picked 2026-10-21. The site is chosen at the desk on `L_SizeTest` after the Night pass. No coordinate is written.

### Round 17 — The shrine unlocks

Picked 2026-10-21. 1A, then 2A 3A 4A 5A 6A 7A. The moss addition was not taken: a new carry id conflicts with the six-slot set, so the sleep spends nothing.

- A matched commit that finishes that guard's pad calls `TryEaseCampActor` for that guard. Wait does not. A wrong step does not.
- Wait calls the same glide home a late paradox already calls. It does not mark the guard asleep.
- A reach is spirit form, within 280 cm of that `NODE_GUARD`, while that guard is still awake. The 180 by 180 by 120 cm light box stays the sightline.
- Three pads, one on each guard. Finishing that pad's ladder is the one sleep.
- One E on the shrine, after the three sleeps, calls the free and then `CompleteShrineReturn`. A missing guard still refuses the free.
- The captive is a separate `NODE_CAPTIVE` actor. Freeing it uses the ready-to-return flag. The kettle partner is not moved.
- `hw.Playtest.FastForward shrine` runs the three ladders, spawns the captive and a shrine for that run, and stops before the E. Nothing is saved into `L_SizeTest`.
