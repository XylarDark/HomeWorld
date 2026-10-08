# First loop — what the agent can implement now

Written 2026-10-07. The design lock is the source. This file is the work queue for that lock.

Read, in this order, and do not restate their numbers here:

- `Docs/context/T0_INTERVIEW_LOCK.md`
- `Docs/context/T0_SHAPE_PLAN.md`
- `Docs/context/HOMEWORLD_ROUTE.md` (Recorded). A later recorded line wins.

`Docs/TaskLists/T0_EXECUTION_PHASES.md` and `Docs/TaskLists/T0_EXECUTION_QUEUE.md` are the pre-lock record. They still treat the rune as the way into spirit and the shrine as the way out to camp. Do not implement from them.

One item at a time. C++ for the verb. An automation test that fails if the verb is removed. Then stop. Level placement, meshes, and a desktop playtest are not items on this list.

## Already in code

Leave these alone. They already match the lock.

| Beat | Where | What is true |
|---|---|---|
| Tea gates the day sprint | `TryBrewNodeKettleTea` | Day body, spends one `RES_HERB`, faster movement until the day phase ends. Duration stays the existing stand-in. |
| Glide steer | `StartCloudDescent` / glide movement | One descent, unrestricted steering. Day and night share it. |
| Bull tame and ride | beast encounter | Field bull. Threat, herb approach, turn rate falls as speed rises. |
| Camp refusal of a kill | freedom gate | A killed or converted guard does not open the gate. |

## Implement

| # | Change | Done when |
|---|---|---|
| 1 | Sleep at `NODE_BED` is the form change. `CanEnterSpiritForm` grants spirit from the bed at night with the rune latch still locked. Remove the rune check from the bed path. **Done 2026-10-07.** | `HomeWorld.T0.M11.BedAtNightGrantsSpiritWithRuneLocked` and `HomeWorld.T0.M11.DayBedStaysBody` passed. |
| 2 | Morning garden is a pick. `NODE_GARDEN` day-body interact adds one `RES_HERB`. It does not spend a herb and it does not read as heal. Tea stays the existing brew. **Done 2026-10-07.** | `HomeWorld.T0.FL2.GardenPickThenTea` passed. |
| 3 | Day glide is a glide. `CollectCloudWisp` refuses while the phase is day. Clouds do not offer a day pickup. The day sign is camp smoke as a heading, with nothing to collect. **Done 2026-10-07.** | `HomeWorld.Transit.CloudDescent.UnrestrictedSteeringAndWispCarry` passed. |
| 4 | Night glide uses that same descent and collects cloud wisps. Cap carried wisps at two per night. **Done 2026-10-07.** | `HomeWorld.T0.FL4.NightGlideCarriesTwoWisps` passed. |
| 5 | `NODE_WOUND` is visible by day and healed at night by giving one carried night wisp. That spend is one of the two. Healed wound wisps follow the player. **Done 2026-10-07.** | `HomeWorld.T0.FL5.WoundTakesOneNightWisp` passed. |
| 6 | Homestead mix: one dung plus the other night wisp makes one fertilizer. Stop there. **Done 2026-10-07.** | `HomeWorld.T0.FL6.FertilizerMix` passed. |
| 7 | `NODE_SHRINE` returns home. It does not set a camp destination. The way out is the glide. Day body may return any time after leaving. At night only spirit form may return. A ridden bull returns with the player, then both are in the walk-to-barn state. The partner uses that same return, then is in the walk state. **Done 2026-10-07.** | `HomeWorld.T0.FL7.ShrineReturnsHome` passed. |
| 8 | Camp has three guards. Ease each until asleep. The freedom gate opens when all three are asleep. **Done 2026-10-07.** | `HomeWorld.T0.M16.FreedomGate` passed: two guards refuse, three open, a kill refuses. |
| 9 | Wake places the partner by the bed and the child in the garden. After the partner is taken, the child waits by the bed. After the tea gate, one family hint toward the edge fires once. **Done 2026-10-07.** | `HomeWorld.T0.FL9.FamilyPlacesAndHint` passed. |

Items 1–6 and 8–9 are C++ plus automation tests. Item 7 is the same, on the existing shrine component. None of them place actors in `L_VS_MVP_Markers`.

## After this list

Items 1–9 are done. The next queue is `Docs/TaskLists/T0_NEXT_QUEUE.md`.

## Parked

These are real, and they are not items here.

- Fertilizer after the mix. Answered 2026-10-08: the player spreads it on the night flight. The work is in `Docs/TaskLists/T0_NEXT_QUEUE.md`.
- The words of the family hint, past the lock’s “one hint toward the edge.”
- Meshes, materials, shrine silhouette, and promoting art into `Content/`.
- Desktop Wake prove. Luke plays that.
- Re-deriving `Docs/WORLD_METRICS.md` onto the scale pass. The route file owns the meters until that pass exists.
