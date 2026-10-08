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
| Who teaches the dawn rule? | The child, in one line, before the first night out. The bed and the dawn. Then the rule is live. 2026-10-08. |
| Does a late wake change the homestead? | No. The place stays warm. The slow is the body alone. 2026-10-08. |

## Reading boundary

This board states current product direction. Implementation progress, test
results, and task ordering belong in their active records, not here. When the
Lead changes direction, replace the affected current statement here.
