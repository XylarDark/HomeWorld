# EXIT VISION_MARKET_TECH_V1

**Kind:** Design and studio lookup. Not a Conductor Research cycle. No `PROMPT_` pair. No Do bites. This file is not an implement order.

**Date:** 2026-10-22

**Ask:** Review HomeWorld as a game director and a principal engineer. Four parts: vision and market, developer prowess, tech health, and what is missing. End with a ranked top-5.

**Already covered:** Nothing. This file is the first entry for this body.

**Sources:** The repository files cited in the analysis below. No external page was retrieved.

**Reuse:** The sort into NOV20 and FUTURE, and the reopen conditions, live in `Docs/46_NOV20_UPGRADE_PLAN.md`. This file does not restate that sort.

**Amendment 2026-10-22.** UL2 3A and UL2 4A are Lead locks. A finished pad ladder spends 1 `ITEM_MOSS` from the kitchen chest, and that is what puts the guard to sleep. Stress stays at cap 100, +10 for a hit, and +5 for a bonk, and the MissedTend test stays on those numbers. Moss and stress stay on the November slice. Where the review below left them off that slice, the sentence is corrected. Approved tracks that the review wanted quarantined are question 7 in the plan, not a silent drop.

The analysis below is the 2026-10-22 review, with that amendment applied.

---

This is a read of the design canon and the C++ as they stand on 22 October 2026. The played game and the written game are not the same size.

## 1. Vision and market impact

HomeWorld is a third-person care adventure. You live with your family on a floating homestead. By day you gather and travel. Sleep at the bed turns you into a spirit. At night you cross back unseen, ease the camp guards until they sleep, and bring a loved one home. You do not kill. That paragraph is the product, in `Docs/VISION_BOARD.md` and the five gates in `Docs/canon/PILLARS.md`: love is the stakes, care replaces killing, one stroke you can fail, home stays safe, the place teaches itself.

The long horizon in `VisionBoard/Core/VISION.md` is a campaign across seven sin/virtue pairs. That file is theme. It does not set the prototype. The prototype that is actually in motion is one day on the homestead island, then a field, then one pine camp, then a shrine home. That cut is the critical path in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`, aimed at a 20 November deadline play. Cave, second forest, river, marsh, roost, bull, party outings, the home loop past the kettle, the six-resource carry, cloud-wisp fertilizer, and spirit sickness are shelved on that path.

**Who it is for.** People who want Spiritfarer’s “care is the verb” and Breath of the Wild’s “the land tells you what to do,” and who do not want a management sim or a combat loop. `Docs/canon/DESIGN_ETHOS.md` names those sources and is explicit about what to leave behind: no time loop, no ant-scale, no free flight, no kill. The player is 2 m tall and “not from this planet,” standing among 5 m animals and 5–9 m pines, with a giant saved for later (`Docs/art/SCALE.md`, `Docs/VISION_BOARD.md` Shape). That scale is the quiet fantasy. It is closer to a gentle colossus read than to a life sim.

**Where it sits.** The honest neighbors are Spiritfarer (bring them home, healing as the action), the BotW glide-as-a-fall, Journey’s one warm color in a cool world, and a drawing game like Ōkami or Chicory for the single stroke. Outer Wilds is a cousin for the camp and the close horizon, and the ethos correctly refuses the mystery clock. On a Steam cozy shelf it will be filed next to A Short Hike and the wholesome-adventure tag. It should not be filed next to Stardew or a survival crafter. The early GDD still describes that other game: six resources, a food-tame, a campfire-to-tent-to-cottage unlock (`Docs/01_GDD_MVP.md`, `Docs/30_DEMO_SPINE.md`). The vision board wins when they disagree, and they disagree.

**What is distinctive.**

- Family is in the first minute, then one of them is taken. The stakes are love, and the homestead stays warm afterward. That is a real hook. Most “cozy” games never take anyone.
- Night is a form you earn by sleeping, not a palette swap. Dawn does not end it. Overstaying is a body drag and, at five stacks, a live glide home (`Docs/VISION_BOARD.md` open-direction table). Death is a bonk that sends you home (`Docs/canon/DESIGN_ETHOS.md`).
- One drawable stroke, fail-able, shared by every axis. Grace finishes the ease, Wrath shoves, a paradox runs both and they interfere (`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`). Marks change the stroke. They do not add a second verb family.
- The 30-second steered fall through pass-through clouds, with no flight HUD and no energy meter (`Docs/01_GDD_MVP.md` §9, `Docs/43_CLOUDS_WISPS_DESIGN.md`).

**What is generic.** A six-slot gather inventory, craft stations, a threat-meter tame, hurt wisps you press E on, and a GAS health bar the design is not allowed to spend (`Docs/03_SYSTEMS_MVP.md`, `Source/HomeWorld/HomeWorldAttributeSet.h`). The seven deadly sins will read as a morality sim on a store page until one axis is visible in play. Doc 45 correctly parks six of the seven. The names are still the long-horizon pitch, and they are the part most likely to make the game sound like every other “virtue” RPG.

**Steam today.** A wishlist page cannot be cut from the current build. The walked world is the greybox measurement scene `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`. Midday on the island passed on 18 October. Bed-to-spirit, one wisp in the backpack, and a one-press heal at the hot springs have passed. The glider craft, the launch, the field, and the camp have not (`Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`, `docs/SESSION_NOW.md`). Polish gates G-ENV, G-ASSET, and G-FEEL are all red (`Docs/qa/POLISH_READINESS.md`). The queue says the repo has no sound files, and custom hero meshes are off the November path. `Docs/20_UASSET_AI_POLICY.md` already tracks Valve’s January 2026 AI disclosure rule, which matters the moment a generated still becomes a shipped mesh.

The capsule that would pull wishlists is already specified and not yet playable as a picture in motion: dusk homestead, warm windows, dark coat, small shoulder spirit, child arriving as you do (`Docs/00_SHOTLIST.md` Shot 1, `Docs/02_ART_BIBLE.md`, the stills named in the vision board). The eight-second trailer verb is the night fall through spirit-blue clouds, then one guard eased to sleep. Greybox footage of E-to-heal will not carry a page. The hook line that matches the canon is short enough to ship: by day you live with them; at night you become a spirit and bring one of them home, and you never kill.

## 2. What it demonstrates

**This would impress a studio.**

The product spine is unusually decided for a prototype. Pillars, a scale card, a shelved list with dates, and a rule that a feature failing two pillars waits. Most solo projects never get that far. The October design docs (`Docs/41` through `Docs/45`) are the same shape: a scope paragraph, numbered picks, and an explicit “this does not rewrite the other file.” Companion party is the best of them. One possessed pawn, partner and child as follow presence on day trips only, every test and every night stays solo, the save stores who is home rather than where they stand (`Docs/41_COMPANION_PARTY_DESIGN.md`). That is a designer refusing a second controller.

The stroke, the bonk-home, the bed-as-form, and the strict-versus-soft rescue gate are real design and engineering, not slogans. `HomeWorldCampNight` tests the three-calmed gate. `SatisfiesFreedomGateStrict` is what a played rescue is supposed to use, because the loose gate can pass with no camp actors (`Docs/CANON_MAP.md` §4). Spirit stealth is a closed, stamped system with lit volumes and an alert, in `Source/HomeWorld/HomeWorldSpiritStealthComponent.h`, not a missing feature. The seeded field generator in `Source/HomeWorld/HomeWorldZoneGenerator.h` states its stream order as a determinism contract and does not pretend to spawn actors. `HomeWorldZoneGeneratorTests.cpp` holds 12 tests on that contract.

The host suite is large for this stage: on the order of 140 automation tests across the `*Tests.cpp` files, including 25 home-loop tests, 10 camp-night tests, and stroke tests split between rules and the pawn. The interact table in `Source/HomeWorld/HomeWorldInteractResolver.h` is the right idea: one press, rows in priority order, a new prop is a row.

**This would not impress a player yet, and a principal would circle it.**

`AHomeWorldCharacter` is about 7,500 lines of `.cpp` and about 1,000 lines of header, with dozens of `Try*` methods covering tame, heal, nurture, craft, minigames, boss seals, kettle, dog, fish, bed, glider, shrine, fertilizer, bull, barn, ease, and captive. The resolver says a new prop is a row. The pawn still is the row. That is the tactical-tornado pattern the project’s own complexity note describes in `docs/architecture/design-complexity-brief.md`.

A lot of “closed” phase-board work is a log and a placeholder. `swarm/PHASE_BOARD.md` stamps P0–P7, Reap & Sow, Demo Spine, and Night Feel closed, and still says no T0 beat has a tracked prove. The live proof is the playtest queue, which has passed a greybox midday and three night beats. `AHomeWorldNightEncounterPlaceholder`, `HomeWorldMinigameStubMarker`, and `UHomeWorldGameplayAbility` (activate, commit, end) are scaffolds. Health and stamina exist on `UHomeWorldAttributeSet` while `Docs/42_HOME_LOOP_DESIGN.md` records that traversal does not spend stamina and the GDD forbids a flight meter. `UHomeWorldStressComponent` implements the UL2 4A numbers, cap 100, +10 for a hit, and +5 for a bonk, plus the moss meal and the Grace-to-Wrath swap. That component stays. Doc 45 stage 0 is the older line that left this off the queue.

The art bible and the scale card still disagree in public. `Docs/art/SCALE.md` locks the cottage at 26 m by 23 m and says the 9 by 11 m card is the earlier art lock. `Docs/02_ART_BIBLE.md` still states 9 m by 11 m. `Docs/00_CANON.md` still says an adult is 1.8 m and the island is 18–24 m. Scale is the fantasy. Three documents naming three homes is how a dressed mesh comes back the wrong size.

## 3. Tech health

**Architecture.** One game module, `Source/HomeWorld/HomeWorld.Build.cs`, depending on Enhanced Input, GAS, Gameplay Tags, Smart Objects, UMG, and AI. That dependency list is reasonable. The split the module does not have is inside the pawn. World subsystems exist and are the right seams: time of day, inventory, family, save, craft, home loop, spirit roster, spirit assignment, session. Opening lookup has its own registry (`HomeWorldOpeningRegistry.h`) so finds do not walk the world every time. Components exist for stealth, stroke, stress, nurture, beast tame, shrine, traversal. The pawn still reaches through all of them. New work lands as another `Try*` on the character because that is where the last beat landed.

**Tests.** They are real and they encode locks: form gates, day gates, camp night, strokes, party flags, home-loop bites, cloud descent, zone seeds. They largely run in a test world that will spawn a missing marker rather than load `L_SizeTest` (`HomeWorldFirstLoopTests.cpp` spawns a `GlideStart` tag if none exists). That is the right kind of test for a rule, and the wrong kind of test for “the beat is in the game.” The canon map already separates “logic done” from “level unbuilt” for kettle, day camp, planetside boot, and the camp rescue. The playtest queue is the level proof, and it is ahead of the code proof only on the island night. Field and camp are not on the map. `docs/SESSION_NOW.md` says the meadow, the nodes, and the clearing are not saved.

**Coupling and risk.**

- `HomeWorldCharacter.cpp` is the merge hazard. The session note already says another agent owns source and the placers.
- Soft success. A missing camp actor can still satisfy the loose freedom gate and log `SOFT_LATCH_ONLY` (`Docs/CANON_MAP.md` §4). Useful so a reviewer is not hard-blocked. Poisonous as a definition of done.
- Two worlds. Polish readiness measures `L_VS_MVP_Markers`. The walk measures `L_SizeTest`. Island measurement inside Unreal is still missing, and the polish note records the last time that gap hid a 19 m island under a 180 m spec.
- Scope leak. The campfire-to-cottage reveal, the minigame stub, and the boss seal are compiled beside the rescue. Whether they leave the November path is question 7 in `Docs/46_NOV20_UPGRADE_PLAN.md`, because each has an approve. Stress is not in that leak.
- Doc mass. The canon map’s header is a warning: hundreds of markdown files, and a closed system was once reported missing because nothing pointed at it. The map and the playtest queue are the cure. The phase board is not. It is a September stamp log sitting on top of an October prototype.

**Debt that will slow the next feature.** Every new opening beat currently needs a character method, a resolver row, a tag, a host test, a queue row, and often a placer. The row and the tag are the cheap part. The method on the god pawn is the slow part. A second slowdown is false completeness: agents and reviews treat a CLOSED track or a passing host test as a scene. The scene rule in `Docs/context/SCENE_SETUP.md` already says a scene is not done until its verify script logs a pass in the open editor. The prototype does not yet live by that sentence.

**Top 5 fixes by payoff**

1. **Move verb bodies off the pawn, along the rows that already exist in `HomeWorldInteractResolver.h`.** Opening, camp night, homestead stations, and traversal each own their `Try*`. The character resolves and moves. Payoff is every beat after the glider. Cost is a focused split, not a rewrite. Risk is a long file that is already under another owner, so it wants a single editor and a green host run.
2. **Make the played map the only success for a beat.** Host tests keep the rules. A beat the queue calls open cannot go green without the actor on `L_SizeTest`. Retire the loose freedom gate from any path a playtest or a quest sweep can treat as the rescue. Payoff is an end to “logic done, level unbuilt” as a surprise.
3. **Do not extend the scaffolds that are not a November row.** Health as a combat attribute, the minigame stub, the boss-seal stub, and the campfire-to-tent-to-cottage reveal stay compiled until question 7 in `Docs/46_NOV20_UPGRADE_PLAN.md` is picked. `UHomeWorldStressComponent` is not on that shelf. UL2 4A keeps it, and UL2 3A keeps the moss spend on the pad.
4. **One scale source.** `Docs/art/SCALE.md` already names the walked plan. Point the art bible and `Docs/00_CANON.md` at it and delete the leftover meters from those files’ active sections. Payoff is the first dressed cottage and the first pine coming back at the size the fantasy needs.
5. **One island measurement in the editor, then stop proving the other map.** `env.ue_island_measured` is missing, and the polish note says why that specific check exists. After it is recorded, `L_SizeTest` is the world the gates mean. `L_VS_MVP_Markers` stays history.

## 4. What is missing, and what is worth exploring

The game is missing a place a stranger can stand in and understand in thirty seconds. The rules are ahead of the ground. These are the moves that change that, with a rough cost and the risk that matters.

| Move | Why it helps | Cost | Risk |
|---|---|---|---|
| Hold the November path as the whole product through the deadline play. Field shell, three nodes, day eject, night glide, three guards, one ease, shrine home. | It is the only sequence that contains the hook: family, fall, ease, return. `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md` already shelved the rest. Shipping that list is the vertical slice. | S as discipline. The code for several shelved systems is already written, so the cost is refusing to extend them. | The slice can feel small if the stroke is a timing bar with no read. That is a feel risk, and it is the one this cut is for. |
| One dressed trailer beat on masters already in the project: dusk claim at the cottage, then one night ease. One licensed homestead loop, moved ahead of the 16 November audio row. | Wishlists convert on a picture and a verb. Shot 1 and the player stills are the picture. The ease is the verb. Greybox E-presses are neither. | M. Materials exist (`Docs/qa/POLISH_READINESS.md` lists the eleven masters). Sound and a readable stroke effect do not. | AI-assisted meshes hit the disclosure rule in `Docs/20_UASSET_AI_POLICY.md`. A beautiful still that is illegal to ship as a mesh is a false win. |
| Put the stroke in a stranger’s hands before any new system. The dog is already the sin/virtue sample in the opening (`Docs/VISION_BOARD.md` tutorial). | “One stroke you can fail” is the pillar that makes this not a walking sim and not a crafter. If a new player cannot fail it on purpose, the camp rescue has no game inside it. | S to M, depending on how much of the wind-up is already in `HomeWorldStrokeReportComponent`. | This is taste. A clean log will not tell you if the shove-home feels fair. A person who has not read the bible has to miss it once. |
| Leave the home loop past the kettle, party outings, fertilizer, and the six-slot carry on their owner locks. The queue gives them no extra day. Moss and stress stay: UL2 3A spends 1 `ITEM_MOSS` from the kitchen chest when a pad ladder finishes, and UL2 4A keeps cap 100, +10 for a hit, and +5 for a bonk. | The owner files stay the locks. Detaching moss or stress would break the ease and the MissedTend test. | S to stop extending the systems that have no November day. | A craft-unlock quarantine would hide an approved track. That choice is question 7 in `Docs/46_NOV20_UPGRADE_PLAN.md`. |
| Lead the store fantasy with scale, in one still: 2 m coat, 5 m bear, warm cottage, cool valley. | It is the thing no neighbor on the cozy shelf has, and `Docs/art/SCALE.md` already locked it. The capsule does not need the sin table. | S once a blockout walk exists. The size-test tasks in `Docs/art/SIZE_TEST_TASKS.md` are this still. | If the bear is a cube, the still advertises a prototype. Wait until the shoulder height reads. |
| Treat the bonk-home as a shareable clip only after the glide home is visible. | “You do not die; the island pulls you back” is a one-sentence differentiator next to the no-kill pitch. | S if `HomeWorldBonkArc` is already the motion. | Shown too early it looks like a fail state. Shown after the cottage is warm, it looks like the world refusing to lose you. |
| Keep Doc 44 on paper. | The three-player visit, raid, and half-share collection is a coherent later game (`Docs/44_MULTIPLAYER_FUTURE_DESIGN.md`). It is also how this slice dies. | S to keep refusing it. L if anyone “prepares” netcode. | The readiness section will tempt a replication pass. The file says the slice stays one client. Believe the file. |
| A five-person blind play of the island day, then one guard, with no doc in the room. | The place-teaches-itself pillar has never been measured. Host tests cannot measure it. The same on-screen fail twice is already the playtest rule. | S. | You may learn the kettle, the bed, and the heart icon are doing the teaching that the land was supposed to do. That is the useful result. |

I would not add a grappling hook, pair toys, lair coils, a flight meter, or a seventh resource. The principle lock and the do-not list already parked them, and they blur the novel line: family, one stroke, home above a living world.

## Ranked moves

1. **Finish the November rescue slice and touch nothing else.** It is the only build that contains the fantasy a Steam page can say in one sentence.
2. **Get the stroke fail-able in a stranger’s hands on the dog, then on one guard.** That is the game inside the slice. Without it the page is a walking tour.
3. **Cut one trailer from that slice:** dusk claim, cloud fall, one ease, shrine home, one music loop, masters only. That is the wishlist object.
4. **Take the verb bodies off `AHomeWorldCharacter` and make `L_SizeTest` the only map that can pass a beat.** That is the engineering move that keeps the next year from calcifying in one file and in empty-world tests.
5. **Point every scale sentence at `Docs/art/SCALE.md`, and leave health, the minigame stubs, and the campfire-to-cottage reveal for question 7.** Moss and stress stay on the slice under UL2. The November path does not grow a second game beside the one the pillars named.
