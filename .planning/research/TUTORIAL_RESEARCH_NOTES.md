# Tutorial research notes (R-01 to R-05)

**Date:** 2026-10-17.  
**Status:** Phase 0 notes. Not canon. Not a decision.  
**Method:** The Parallel search account returned “insufficient credit,” so these notes use web results retrieved the same day. A claim below is tied to a page that was actually returned. OoT Kokiri Forest, A Link Between Worlds, Stardew Valley’s first day, and a primary Dark Souls onboarding study were not in those results. They are not filled in from memory.

The opening this applies to is the sequence already in `Docs/VISION_BOARD.md`. These notes do not change it.

---

## R-01 — How Zelda teaches

Breath of the Wild’s Great Plateau is a miniature of the real game: free movement inside a bounded area, a few shrines, a tower, and the same pace as the rest of the game. Players often say it has no tutorial because the lesson is the place ([Black Box, 2017](https://noplatform.wordpress.com/2017/06/30/zelda-breath-of-the-wild-is-a-case-study-in-game-tutorials/)). Wikipedia describes the same area as exploration-first, with most of the Old Man’s lines skippable, and the paraglider as the thing that ends the lesson ([Great Plateau](https://en.wikipedia.org/wiki/Great_Plateau)).

The four Plateau shrines each demand one Sheikah Slate rune, then give the hearts back. The tools do not grow. The puzzles do ([Breath of the Wild's Montessori Method](https://www.gamedeveloper.com/design/breath-of-the-wild-s-montessori-method)).

An organic-tutorial writeup names the order that makes that work: show the new action in the open with nothing hurting you, repeat it with one extra constraint, then test it where failure costs something ([Examining Organic Tutorials](https://www.gamedeveloper.com/design/examining-organic-tutorials)).

Tears of the Kingdom’s Great Sky Island uses the same four-shrine shape for Ultrahand, Fuse, Ascend, and Recall. The shrines teach the action, then the island asks you to use it ([Nintendo Life](https://www.nintendolife.com/guides/zelda-tears-of-the-kingdom-great-sky-island-walkthrough-shrines-closed-door-quest-abilities)). Players also describe a ring: the long way is the full lesson, and the cold way lets a returning player skip it if they already know peppers and a pot ([r/tearsofthekingdom](https://www.reddit.com/r/tearsofthekingdom/comments/13ggxhh/the_level_design_of_the_great_sky_island_is/)). A critic’s complaint is the other side of that ring: the path is more forced than the Plateau, and Ultrahand and Fuse stay unclear after their shrines ([Escapist](https://www.escapistmagazine.com/zelda-tears-of-the-kingdom-great-sky-island-tutorial-obtuse-overwhelming-great-plateau/)).

Leaving the Plateau before the paraglider is a kill: a killbox, then a warp back ([GameFAQs](https://gamefaqs.gamespot.com/wii-u/632936-the-legend-of-zelda-breath-of-the-wild/answers/459287-can-you-get-off-the-great-plateau-without-the-paraglider)). That is “not yet,” and it is fatal for a moment. It is not a wound you carry.

Mark Brown’s tutorial talk, as transcribed from the video page, says a complex game should split the lesson across play, put hands on the system, and show instead of typing. He quotes Into the Breach’s Justin Ma: a line like “damages a tile and pushes adjacent tiles” loses to a short animation of the push ([Game Maker's Toolkit](https://www.youtube.com/watch?v=-GV814cWiAw)).

### Techniques worth keeping in view

1. Bound the first place. Freedom inside the bound is the lesson. The bound is not a menu.
2. One tool, then a new situation for that same tool. Do not add a second verb to make the puzzle harder.
3. Safe, then one constraint, then a cost.
4. Show the change. Name it after, in few words, or not at all.
5. A returning player needs a shorter path that still works if they already know the rule.
6. End the bound by granting the way out (the paraglider), not by a text recap.
7. A forced ring with four new powers at once is the version players call a tutorial. The Plateau’s complaint is smaller because the powers stay in one toolbox.

---

## R-02 — Depth without a hostile first hour

Path of Exile 2’s own director, Jonathan Rogers, told Eurogamer the sequel “should certainly be a lot easier to get into” without giving up later depth, that equipping abilities is streamlined, and that the opening is built so you meet the lesson no matter which way you walk first. Early tests failed when drop luck or a bad skill pick made the start feel empty ([Eurogamer](https://www.eurogamer.net/a-date-with-path-of-exile-2-a-new-class-smoother-onboarding-and-the-reason-why-this-had-to-be-a-sequel)).

In an MMORPG.com interview he says they cut incidental complexity, made skill gems easier, and added video because “no amount of texts” shows that two skills work together ([MMORPG.com](https://www.mmorpg.com/interviews/interview-path-of-exile-2s-game-director-jonathan-rogers-chats-gameplay-intentions-inclusions-and-improvements-2000130901)). An Epic writeup of the same effort names the old barriers: the game feels like a new language, respec used to be an Orb of Regret, and a loot filter was required before the ground was readable. PoE2 spends gold to respec and tries to put only useful things on the ground ([Epic Games Store](https://store.epicgames.com/en-US/news/path-of-exile-2-the-long-road-to-exceeding-a-decade-of-expectations)).

Early-access players still report a first skill gem with no idea where it sockets, and a first boss that kills them many times. Other posters say a tutorial does stop you and socket the gem unless it was turned off ([Path of Exile forum](https://www.pathofexile.com/forum/view-thread/3775326/page/1)). The fight is not over because a prompt exists.

A Hades teardown says the first run is the real run: one god offers three boons, each boon changes one verb, and duo boons exist but stay invisible until a second god is already on you. It attributes to Greg Kasavin, via an Inverse interview, the goal of taking the sting out of death because dying already feels bad. The first loss is meant to be cheap and to hand something back ([Hades onboarding teardown](https://teemo.dev/game-design/hades/systems/onboarding-and-first-session/)). A separate chapter describes Achilles, after a death, giving spear advice that is also a tutorial and also a conversation ([Socratopia, ch. 24](https://www.socratopia.app/library/game-design-compelling-en/chapter-24)).

A Slay the Spire teardown says the first fight teaches intent and block only. The starter deck has one odd card, Bash, and withholds draw, exhaust, and powers. Later characters and the heart are locked behind finished runs, so a new player cannot be handed the whole card pool ([Slay the Spire onboarding teardown](https://teemo.dev/game-design/slay-the-spire/systems/onboarding-and-first-session/)).

A Hollow Knight teardown says the opening withholds the dash and the claw, grants Vengeful Spirit at the Ancestral Mound, and ends the first session with gates you can see and cannot pass. The Shade rule is taught while the lost geo is still small ([Hollow Knight onboarding teardown](https://teemo.dev/game-design/hollow-knight/systems/onboarding-and-first-session/)).

### Borrow / leave

Same columns as `Docs/canon/DESIGN_ETHOS.md`. This table is research, not an ethos edit.

| Take | Leave | Source |
|------|--------|--------|
| The first place is the real game, smaller. The way out is earned inside it. | Four new powers in one loop. A rail that only pretends you can turn around. | Great Plateau and Great Sky Island, sources in R-01 |
| One toolbox. Harder situations, not new verbs. Hearts back after a safe puzzle. | A shrine menu, a rune wheel, a second gadget per room. | [Montessori Method](https://www.gamedeveloper.com/design/breath-of-the-wild-s-montessori-method) |
| Show the effect. Words after, and few of them. | A paragraph that names a modifier before the player has seen it move. | [Game Maker's Toolkit](https://www.youtube.com/watch?v=-GV814cWiAw) |
| Depth stays. Incidental steps go. The first modifier is one socket on one action, met whichever way you walk. | Loot filters, respec orbs, a gem you cannot find a slot for, a first boss that assumes the build. | Rogers via [Eurogamer](https://www.eurogamer.net/a-date-with-path-of-exile-2-a-new-class-smoother-onboarding-and-the-reason-why-this-had-to-be-a-sequel) and [MMORPG.com](https://www.mmorpg.com/interviews/interview-path-of-exile-2s-game-director-jonathan-rogers-chats-gameplay-intentions-inclusions-and-improvements-2000130901); [Epic](https://store.epicgames.com/en-US/news/path-of-exile-2-the-long-road-to-exceeding-a-decade-of-expectations) |
| One donor, three choices, each choice changes one verb. The combo exists and is not explained yet. | A ten-axis bench on the first visit. A build guide as the way to play. | [Hades teardown](https://teemo.dev/game-design/hades/systems/onboarding-and-first-session/) |
| The starter set is missing pieces on purpose. The rest unlocks after a finished loop. | A full virtue list in the opening. | [Slay the Spire teardown](https://teemo.dev/game-design/slay-the-spire/systems/onboarding-and-first-session/) |
| A gate you can see and cannot pass yet. The first loss is cheap. | A shade that steals the child’s gift. A map you must buy before the yard makes sense. | [Hollow Knight teardown](https://teemo.dev/game-design/hollow-knight/systems/onboarding-and-first-session/) |

---

## R-03 — Teaching without a UI

Outer Wilds is built so the reward is an answer, not a mission or an upgrade. Alex Beachum’s stated goal is curiosity-driven exploration: the player acts to answer a question they already have ([GDC 2021 slides](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/GDC+2021/beachum_gdc_2021(1).pdf)). Kelsey Beachum says a cyclone teaches more than the text that follows it, and that text is the breadcrumb, not the hook ([Game Developer](https://www.gamedeveloper.com/business/explaining-the-value-of-show-don-t-tell-storytelling-in-i-outer-wilds-i-)).

The failed version of that hook matters here. A rock falling from space did not make anyone curious, because the village was still new. Beachum’s lesson: you cannot be curious about one new thing until the immediate place is familiar ([Game Developer, live die repeat](https://www.gamedeveloper.com/design/live-die-repeat-how-i-outer-wilds-i-piques-curiosity-in-an-ambivalent-solar-system)).

A Short Hike’s author uses a cave, a landmark, or a path to pull a lost player back, and treats that as guidance that should not feel like a script. Signs are the last resort, because people skip them ([GDC postmortem transcript](https://gameindustrylibrary.com/documents/crafting-a-tiny-open-world-a-short-hike-postmortem)). The PlayStation Blog post says the island was built so the wrong way still has a pace, and curiosity off the path is rewarded ([PlayStation Blog](https://blog.playstation.com/2021/08/05/crafting-a-tiny-open-world-a-look-behind-the-scenes-at-the-creation-of-a-short-hike/)).

For HomeWorld, “the world announces its purpose” matches these pages when the announcement is a thing you can already see how to use: a door, a gap, a herb in reach, a light that changes. A new mark language dropped into a place the player has not walked yet is the meteor problem.

Journey, Pikmin, and Spiritfarer were named in the task list and were not in this search set. `Docs/canon/DESIGN_ETHOS.md` already records what this project takes and leaves from those three. These notes do not reopen that.

---

## R-04 — Failure that teaches

Celeste tells the player, on a load card, that more deaths mean more learning, and it shows the death count as a record rather than a shame mark. Assist Mode can slow the game, grant stamina or dashes, or skip a chapter. Matt Thorson told Vice the job is to teach, challenge, and support people through failure so they leave feeling capable, and that Assist Mode “breaks the game” on purpose so the person can still play ([Vice](https://www.vice.com/en/article/celeste-difficulty-assist-mode/); [Playback](https://playback.wisc.edu/2018/06/01/celeste-and-the-rhetoric-of-failure/)).

A guidance note puts the contrast in one line: Dark Souls does teach, and it teaches through death rather than text ([VG101](http://www.marty64.net/kb/pages/level-design/guidance-without-handholding.html)). That is the part to leave. HomeWorld’s bonk is closer to the Plateau’s “you are not leaving yet” than to a corpse run, and closer to Celeste’s instant return than to a lost pile of geo. Hollow Knight waits to teach the Shade until the lost money is still small. Hades, per the teardown above, wants the first death cheap and the return to give something back.

The Plateau’s actual edge is harsher than a bonk: without the paraglider you die and return ([GameFAQs](https://gamefaqs.gamespot.com/wii-u/632936-the-legend-of-zelda-breath-of-the-wild/answers/459287-can-you-get-off-the-great-plateau-without-the-paraglider)). The lesson “not yet” does not require the death. The useful part is the boundary and the quick return.

Nothing in this search set describes a readable ongoing cost like spirit-sickness (a dim light, a slower step, stacks that clear at a bed). That cost is already HomeWorld’s, in the vision board. The research constraint on it is: the first time it appears, the player must get back at once, know they are slower, and still be able to finish the beat. Celeste’s line is the test. If the first bonk makes them feel incapable, the cost is too loud for a lesson.

---

## R-05 — A hook that is not a second tutorial

Dan Felder’s tutorial note treats curiosity as the reason to learn the next verb: teach the jump because a chest is on the other side of the gap, not because a prompt arrived. He also says one lesson does not stick, so the same gap should return later in a quieter form ([A Brief Tutorial on Tutorials](https://danfelder.net/2021/06/29/a-brief-tutorial-on-tutorials/)).

The failure mode on the other side is an opening that never hands over the body: minutes of “press X to continue” before a real choice. The counter-pattern in that note is one verb, then a space that asks for that verb, with text optional ([The Endless Tutorial](https://hayao.dev/docs/codex/antipattern-endless-tutorial)).

Outer Wilds says the hook fails if it arrives before the nearby place is familiar (R-03). A Short Hike’s summit is a seen goal, and the off-path rewards are optional. After the summit, the player still has the island ([Medium breakdown](https://alexiamandeville.medium.com/game-design-breakdown-a-short-hike-5a7a17d740e5)). The hook is not a new system lecture at the finish line.

For the four open questions, the research constraint is the same: a mark, a bench motion, a field herb, or a last glimpse only works after the player has already done the walk, the herb, and the heal in a place they know. A hook that adds a second verb, or that explains the seven axes, is the PoE first hour these sources are trying to escape.

---

## What this does not decide

Rounds 6–9 in `.planning/TASK_LIST_TUTORIAL_DESIGN.md` are still open. These notes do not pick them. They only limit the picks: show one change on one familiar thing, keep the first failure cheap and immediate, and do not explain the deep system in the opening.

## Sources

- [Breath of the Wild's Montessori Method](https://www.gamedeveloper.com/design/breath-of-the-wild-s-montessori-method)
- [Zelda Breath of the Wild is a Case Study in Game Tutorials](https://noplatform.wordpress.com/2017/06/30/zelda-breath-of-the-wild-is-a-case-study-in-game-tutorials/) (2017-06-30)
- [Examining Organic Tutorials](https://www.gamedeveloper.com/design/examining-organic-tutorials)
- [Can we Improve Tutorials for Complex Games?](https://www.youtube.com/watch?v=-GV814cWiAw)
- [Guidance Without Hand-Holding](http://www.marty64.net/kb/pages/level-design/guidance-without-handholding.html)
- [Great Sky Island walkthrough](https://www.nintendolife.com/guides/zelda-tears-of-the-kingdom-great-sky-island-walkthrough-shrines-closed-door-quest-abilities)
- [The level design of the Great Sky Island is exquisite](https://www.reddit.com/r/tearsofthekingdom/comments/13ggxhh/the_level_design_of_the_great_sky_island_is/)
- [Tears of the Kingdom Tutorial Sucks Compared to Great Plateau](https://www.escapistmagazine.com/zelda-tears-of-the-kingdom-great-sky-island-tutorial-obtuse-overwhelming-great-plateau/)
- [Can you get off the Great Plateau without the paraglider?](https://gamefaqs.gamespot.com/wii-u/632936-the-legend-of-zelda-breath-of-the-wild/answers/459287-can-you-get-off-the-great-plateau-without-the-paraglider)
- [Great Plateau](https://en.wikipedia.org/wiki/Great_Plateau)
- [Path of Exile forum, new player experience](https://www.pathofexile.com/forum/view-thread/3775326/page/1)
- [Jonathan Rogers interview, MMORPG.com](https://www.mmorpg.com/interviews/interview-path-of-exile-2s-game-director-jonathan-rogers-chats-gameplay-intentions-inclusions-and-improvements-2000130901)
- [Path of Exile 2: the long road](https://store.epicgames.com/en-US/news/path-of-exile-2-the-long-road-to-exceeding-a-decade-of-expectations)
- [A date with Path of Exile 2](https://www.eurogamer.net/a-date-with-path-of-exile-2-a-new-class-smoother-onboarding-and-the-reason-why-this-had-to-be-a-sequel)
- [Hades onboarding teardown](https://teemo.dev/game-design/hades/systems/onboarding-and-first-session/)
- [Socratopia, chapter 24](https://www.socratopia.app/library/game-design-compelling-en/chapter-24)
- [Slay the Spire onboarding teardown](https://teemo.dev/game-design/slay-the-spire/systems/onboarding-and-first-session/)
- [Hollow Knight onboarding teardown](https://teemo.dev/game-design/hollow-knight/systems/onboarding-and-first-session/)
- [Outer Wilds GDC 2021 slides](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/GDC+2021/beachum_gdc_2021(1).pdf)
- [Show don't tell in Outer Wilds](https://www.gamedeveloper.com/business/explaining-the-value-of-show-don-t-tell-storytelling-in-i-outer-wilds-i-)
- [How Outer Wilds piques curiosity](https://www.gamedeveloper.com/design/live-die-repeat-how-i-outer-wilds-i-piques-curiosity-in-an-ambivalent-solar-system)
- [Celeste and the Rhetoric of Failure](https://playback.wisc.edu/2018/06/01/celeste-and-the-rhetoric-of-failure/) (2018-06-01)
- [Why Celeste is fine with you breaking its rules](https://www.vice.com/en/article/celeste-difficulty-assist-mode/)
- [Crafting A Tiny Open World](https://gameindustrylibrary.com/documents/crafting-a-tiny-open-world-a-short-hike-postmortem)
- [A Short Hike, PlayStation Blog](https://blog.playstation.com/2021/08/05/crafting-a-tiny-open-world-a-look-behind-the-scenes-at-the-creation-of-a-short-hike/) (2021-08-05)
- [A Brief Tutorial on Tutorials](https://danfelder.net/2021/06/29/a-brief-tutorial-on-tutorials/) (2021-06-29)
- [The Endless Tutorial](https://hayao.dev/docs/codex/antipattern-endless-tutorial)
- [Game Design Breakdown: A Short Hike](https://alexiamandeville.medium.com/game-design-breakdown-a-short-hike-5a7a17d740e5)
