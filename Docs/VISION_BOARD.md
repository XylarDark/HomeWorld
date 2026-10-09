# HomeWorld — prototype vision

| Field | Current direction |
|---|---|
| **Status** | Product canon, updated 2026-10-08 |
| **Theme and long-horizon campaign** | [`VisionBoard/Core/VISION.md`](../VisionBoard/Core/VISION.md) |
| **Gameplay slice** | [`Docs/01_GDD_MVP.md`](01_GDD_MVP.md) |

---

## The game in one paragraph

You begin at home with your loved ones. By day, you gather and explore the living
world. When you find the camp, your loved one is taken and you are sent home. At
night, sleep at the bed lets you become spirit. You travel back unseen, ease
the guards' suffering until they sleep, free your loved one, and bring them
home. You tend what depends on you. You do not kill: spirit encounters heal and
convert. The world teaches through its shape, materials, and light.

## Current product principles

| Principle | Direction |
|---|---|
| **Love is the stakes** | Family is present from the start. A loved one is taken at the camp, and the prototype includes the rescue and return home. |
| **Day and night have different work** | By day, gather and explore. By night, become spirit and tend: ease suffering, help things rest, and nurture the home. |
| **Night is a form** | The player becomes spirit by sleeping at the bed. Night does not automatically grant the form. |
| **Care replaces killing** | Combat does not kill. Spirit encounters heal, calm, or convert their targets according to the encounter. |
| **The world communicates** | Terrain, material, silhouette, and light teach a place's purpose before UI. UI may name an action after the player acts. |
| **Guidance stays in the world** | Family guides are present from the start. Guidance is a short contextual hint, not a dialogue tree. |

## Prototype journey

1. Wake at an intact, welcoming homestead with family present.
2. Gather and prepare during the day. Sleep at the bed is the form change.
3. Freely steer the glider through the cloud descent from the homestead to the open field, then gather there.
4. Discover the camp during the day. The loved one is taken and the player is sent home.
5. At night, become spirit, use spirit-stealth to reach the guards, ease their suffering until they sleep, and free the loved one.
6. Return home with the loved one. Continue the day-gather/night-tend loop.
7. When that loop is complete, the same cliff glide can enter the cave mouth. An Atlas sleeper is bound there by a snake. The shape is `Docs/context/BOSS_LAIR_LOCK.md`.

The homestead, open field, and pine-forest camp form the prototype's three
places. The glide connects them; it is traversal, not a separate mechanic
family. Current route geometry and unresolved route values live in
[`Docs/context/HOMEWORLD_ROUTE.md`](context/HOMEWORLD_ROUTE.md).

## Feel and presentation

The homestead reads as safe, warm, handmade, and hopeful above a living world.
The game is cartoon fantasy, not cutesy-infantile or high fantasy, and never
photoreal, grimdark, or science fiction. A place announces its purpose through
its form and environment. The camp must
make the guard's sightline legible from outside so the player can understand
the approach without a HUD marker.

## Open direction questions

The Round 7 questions are answered. Do not ask them again.

| Question | Answer |
|---|---|
| Where does the spirit wound sit? | On the homestead. Seen by day, healed at night. |
| Does the plant slot read as heal or as garden? | Garden. |
| Which family owns the rune's visual read? | The rune is removed. |
| Which document fixes the island top? | The art bible owns the look. The route owns the meters. |
| Family silhouette and night valley materials | Remap both onto the ten masters. 2026-10-08. |
| Camp clearing size | The interview lock. |
| Shrine height and silhouette | Twice player height. A standing stone. |
| What grants the spirit form? | The bed alone. Sleep is the form change. No rune, no second gate. Night does not grant it. 2026-10-08. |
| What ends the spirit form? | The bed, or max spirit-sickness. Dawn does not end it. Still out at dawn: stay spirit, gain a stack, move slower. Five stacks, ten seconds apart. The window is tuned so three-quarters of the furthest reach can still make the bed. Distance is not a wall. Only the fifth stack flies you to the bed and into the body. 2026-10-08. |
| What clears spirit sickness? | Touching the bed. Stacks go to zero even if you do not sleep. Only a late wake carries the slow: if you had stacks, waking applies 15 percent for at most one minute. A clean night has none. 2026-10-08. |
| How do stacks read? | The body tells them. A drag on the step, a colder scarf, a hitch in the glide. No number, no bar. 2026-10-08. |
| What does the fifth-stack boot feel like? | A live glide home. You stay on the body. You land at the bed, then you are body. No cut. 2026-10-08. |
| Who teaches the dawn rule? | The child, once, in one line, before the first night out. The bed and the dawn. Then the body is the reminder. 2026-10-08. |
| Does a late wake change the homestead? | No. The place stays warm. The slow is the body alone. 2026-10-08. |
| What does the one-minute slow touch? | Movement only. Walk and glide are 15 percent slower. Gather, ease, and the bed stay full speed. 2026-10-08. |
| How hard is the drag while stacks are up? | The same 15 percent. One stack or five, it does not add. Movement only. 2026-10-08. |
| How does the scarf read the stacks? | Five steps colder, one per stack. The slow stays a flat 15 percent. You can count without a number. 2026-10-08. |
| Can the fifth stack interrupt? | Yes. It starts the glide at once, even mid-ease. The beat stays. You return and finish. The interrupt costs time, not progress. 2026-10-08. |
| When does the cave fog lift? | The next dawn after the rescue. The loved one is home. Late or clean, it does not matter. 2026-10-08. |
| Who shows the fog has lifted? | The child. They are playing near the edge, and if you leave, they find you. The fog is not a secret. 2026-10-08. |
| When can you enter the cave? | The same dawn the fog lifts. The child shows you. You can glide in that morning. 2026-10-08. |
| What does the cave ask first? | A look, then the coil. A worn track runs from the shrine at the first coil to the loose scale. No one speaks. The shrine brings the field bull through, after you have ridden it once. Before that, the track is there and the shrine is dark. No second bull. The mouth is glider or spirit only, the first time. After the first coil, that shrine is your return. The coil is gated by the bull. The bull works at night, and you need not be spirit. 2026-10-08. |
| Where does the cave shrine pair? | The homestead standing stone. Sleep is still the form change. The stone is travel. After the first coil, it works day and night, either form. 2026-10-08. |
| Where is the bull when you leave? | It follows you home through the stone. It waits in a small barn by the cabin. The barn is there from the first wake, empty, one warm eye, hay. It reads as waiting. Faceted, the bull fits. Not a second house. 2026-10-08. |
| Does the second coil need a new door? | No. Same bull, same shrine. The worn track continues to the second scale. 2026-10-08. |
| How does the second coil go? | On foot, then the bull. You walk the track, tickle the low scale, the snake shifts, then the bull hits it. The bull does not tickle. 2026-10-08. |
| Must both day coils be done before the night? | Yes. First and second by day. One dawn can do both. The night opens that same dusk. No skipping. 2026-10-08. |
| Is the night order fixed? | Only the ask is last. Heals, guards, the third coil, and the eye can be any order. All of them must be done before the ask. An early ask: it stirs, then sleeps. No punish, no hint. The unfinished beat is visible. 2026-10-08. |
| What form after the rise? | Still spirit, on the shoulder. The zoom happens and you can move. It is not a lock. The card reads HomeWorld, holds one breath, about six seconds, and fades on its own. The homestead stone is there the whole time. You land at home, still spirit. You can wander. The bed ends it when you choose. Dawn still stacks if you leave again. 2026-10-08. |
| Is the family awake when you land? | No. It is still night. They are asleep. No greeting until you sleep and wake. 2026-10-08. |
| What is the morning after the rise? | A still morning. The family is up, quiet. No line. You can leave when you want. The cave mouth is just there. 2026-10-08. |
| Is the giant still risen the next day? | Yes, and quiet. It is seated. The cave reads as a room. The snake is in the pool. You can walk to it. No second ask. 2026-10-08. |
| What if the tickle misses? | The snake shifts the scale away. A full breath, about six seconds, and it settles. A tickle during the shift does nothing. No stun. The bull stun is only for a missed ram. 2026-10-08. |

## Reading boundary

This board states current product direction. Implementation progress, test
results, and task ordering belong in their active records, not here. When the
Lead changes direction, replace the affected current statement here.
