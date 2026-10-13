# Tooling build vs use

PROPOSAL. `HomeWorld.uproject:3` is EngineAssociation `5.8`. Nothing here changes the route, the GDD, or a build until Lead accepts the wording. Glider-perch lines `Docs/01_GDD_MVP.md:32`, `:66`, `:75`, `:78`, `:210` are cut and have no row.

Index: [PCG 5.8](https://dev.epicgames.com/documentation/unreal-engine/procedural-content-generation-overview?lang=en-US), [editor Python 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/introduction), [Automation 5.8](https://dev.epicgames.com/documentation/unreal-engine/run-automation-tests-in-unreal-engine?lang=en-US), [Functional Testing 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine), [Gauntlet 5.8](https://dev.epicgames.com/documentation/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine), [World Partition Python 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/WorldPartitionBlueprintLibrary), [Blender FBX](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_fbx.html). Data Validation, Level Snapshots, and every Fab plugin: no 5.8 check on this project, so UNVERIFIED, not recommended. TripoSR and any AI mesh generator conflict with `Docs/40_BLENDER_AI_WORKFLOW_RESEARCH.md:144` and are not recommended.

## Requirements

| Requirement | Dev task | Already have | Alternatives | Verdict |
|---|---|---|---|---|
| Walk named POIs, soft bound, ~15–90s (`01_GDD_MVP.md:65`, `:67–69`) | Place from the metrics sheet | `scene_placement.py:1–5`, pin `:314–334`. Walk is the engine CMC (`HomeWorldGlideMovementComponent.h:22–25`) | Modeling Tools on (`HomeWorld.uproject:20–22`). PCG on (`:24–26`); `SCENE_SETUP.md:47` saves it for later copies. No POI PCG run: UNVERIFIED | KEEP |
| Steered 30s descent, field landing, no flight HUD (`:76–77`, `:79`, `:211–214`, `:271`) | Keep one glide | 3000/1500 cm/s (`HomeWorldGlideMovementComponent.h:44–51`); no rail (`:18–20`); no engine glide mode (`:9`). Day wisp returns false (`HomeWorldCharacter.cpp:974–976`); route `:98` revises `:212` | Marketplace flight kit unverified on 5.8: UNVERIFIED, not recommended | KEEP |
| FALLBACK stays separate (`:218`) | Keep the second component | `HomeWorldCharacter.cpp:1081` | None that keep it separate | KEEP |
| Six resources, +1, full fails (`:85–88`, `:147–154`) | Keep the pile | `HomeWorldResourcePile.h:16`; `TryHarvest` `.cpp:88–118` | PCG 5.8 scatters meshes and skips this law. No pile-point graph was run: UNVERIFIED | KEEP |
| Pool, no cooldown; dawn does not refill; fertilizer does (`:156`) | Leave a spawner unbuilt | Cooldown unread (`.cpp:116–118`). Spread spawns nothing (`HomeWorldCharacter.cpp:2084–2099`). Route `:116`: no morning pile | A spawner is new gameplay | KEEP. Spawner waits for Lead |
| Homestead store, visual (`:149–152`, `:158`) | Keep store props | `place_vs_mvp_store_transfer.py:1–2` | Data Validation: UNVERIFIED, not recommended | KEEP |
| Six slots, stack 9 (`:232–236`, `:278`) | Keep the subsystem | `HomeWorldInventoryTests.cpp:27–30`, cap `:103–112` | No inventory plugin verified on 5.8 | KEEP |
| Bull: herb, threat, tame, ride, boot, no combat (`:95–98`, `:170–175`) | Keep the encounter | `HomeWorldBeastEncounterTests.cpp:24–29`; boot `HomeWorldCharacter.h:468–477` | None verified | KEEP |
| Spirit only after sleep and rune (`:34`) | Keep one form gate | Bed `HomeWorldCharacter.h:479–485`. `HomeWorld.T0.M9.NightWithoutGatesStaysBody` (`HomeWorldFormGateTests.cpp:109–111`). Route `:81`, `:89`: rune removed, sleep is the change | A second gate forks the law | KEEP route-matching code. GDD wording is a PROPOSAL |
| Portal both ways; no third map; no night flight (`:105–108`, `:222–224`) | Keep the shrine. Leave the 1560 m edge out | Home return `HomeWorldShrinePortalComponent.cpp:201`. Route `:71–75`, `:86`, `:92`, `:109` and `WORLD_METRICS.md:29–31` add night glide and a straight-only plains edge. No 1560 m clamp in Source | WP Python is 5.8. `get_editor_world_bounds` was not called here: UNVERIFIED, not recommended | KEEP unrestricted glide. A clamp rewrites `:76`, `:211`, `:224` and waits |
| Heal three (`:115–117`, `:185–187`) | Keep three wisps | `place_vs_mvp_spirit_heal.py:1–2` | None verified | KEEP |
| Nurture crop and one stored pile (`:125–127`, `:198–200`) | Keep two targets | `place_vs_mvp_nurture.py:1–2`. Prove requests begin-play `t0_m12_nurture_slot_prove.py:18–21` and does not tick | Automation, same proof as the PIE row | KEEP actors. USE Automation to prove |
| Camp tend and rescue; heal, calm, or convert (`:35`, `:53`) | Keep soothe | `HomeWorldCampNightTests.cpp:258–260`; gaps `HomeWorldCharacter.cpp:1742–1750` | None verified | KEEP |
| Dawn returns body (`:135–137`) | Keep the phase swap | Same M9 test (`HomeWorldFormGateTests.cpp:109–111`) | None verified | KEEP |
| Lookout points at landing, portal, harvest, home (`:38`, `:248`) | Read the level | `level_manifest.py:1–8` | Level Snapshots: UNVERIFIED. Metrics file is the layout (`SCENE_SETUP.md:45–47`) | KEEP |
| Hub; planet is the same slice (`:36`) | One markers level | `level_manifest.py:50–51` `L_VS_MVP_Markers` | A second map leaves `:224` | KEEP |
| Dual sites: trees, rocks, flowers, den, camp, special (`:46–51`) | Greybox at locked meters | `SCALE.md:9–16`. Measured blocks `SIZE_TEST_TASKS.md:20`, `GREYBOX_T0_CATALOG.md:13`, `:37`. TripoSR named `SIZE_TEST_TASKS.md:19` | TripoSR conflicts with `40_BLENDER…:144`: not recommended for LIB. FBX addon `40_…:170`. Mixar only (`:139`) | KEEP measured blocks |
| Shots teach by a successful verb (`:244`, `:250–254`). PIE gap: M8, M10–M14 | Prove in a world that ticks | Begin-play at `t0_m8_day_camp_eject_prove.py:18–21`, `t0_m10_planetside_boot_prove.py:18–21`, `t0_m11_bed_spirit_prove.py:18–21`, `t0_m12_nurture_slot_prove.py:18–21`, `t0_m13_portal_camp_prove.py:18–21`, `t0_m14_camp_night_prove.py:18–21`. `-ExecutePythonScript` quits first (`docs/KNOWN_ERRORS.md:703`). | USE Automation on 5.8 (index). Proof: `run_ue_automation.py --filter HomeWorld.T0` success, exit 0, on 5.8 (`KNOWN_ERRORS.md:751`). Re-proof: Safe-Build, same filter, duration must match a world test (`:720–726`). Gauntlet is 5.8; this repo never names it. One RunUnreal tick-and-exit smoke is the proof. Until then UNVERIFIED, not recommended. | USE Automation |
| Pocket kit for care surfaces (`:249`) | One-off or reusable tool? | `place_pocket_kit_once.py` calls `scene_placement.place_static` (`scene_placement.py:73`). Missing on disk and origin/main. `check_pocket_kit.py:1–7` on `size/pocket-kit` measures a hardcoded path | Editor Python 5.8, plugin on (`uproject:51–53`). Proof: pin errors past 2 cm (`scene_placement.py:333–334`) and refuses the save (`:1–5`) | KEEP the one-off. Reusable tool is `scene_placement.py` |
| Bounds: no combat, extra beast, biome, resource, or free-flight (`:261–279`) | Add no system for these | Tests above; glide is a trimmed descent (`HomeWorldGlideMovementComponent.h:16–20`) | Those systems would leave the GDD | KEEP |

## Pipeline

Order: meters, a texture-off walk, then polish (`SIZE_TEST_TASKS.md:3`; `GREYBOX_T0_CATALOG.md:3`; `SCALE.md:9`). Cottage and island stay measured blocks (`SIZE_TEST_TASKS.md:20`; `GREYBOX_T0_CATALOG.md:13`). The placer refuses a bad save (`scene_placement.py:1–5`; `SCENE_SETUP.md:47`). Verb laws run in C++ worlds (`HomeWorldDayGateTests.cpp:32–40`). One route fact per Lead yes (`HOMEWORLD_ROUTE.md:17`).

The Level Design Book: playtest a blockout, because a document cannot be playtested, and scale is the usual miss ([Blockout](https://book.leveldesignbook.com/process/blockout)). Epic prototyped with BSP and same-named placeholders, then started art ([Design Workflow](https://docs.unrealengine.com/udk/Three/DesignWorkflow.html), UDK-era). The UEFN greybox note adds art after the level plays ([Greyboxing](https://dev.epicgames.com/documentation/en-us/fortnite/greyboxing-in-unreal-editor-for-fortnite)). A vertical slice proves production after prototypes ([Rami Ismail](https://ltpf.ramiismail.com/prototypes-and-vertical-slice/); [scope](https://book.leveldesignbook.com/process/preproduction/scope.md)).

The meter-first walk matches that. TripoSR before the walk (`SIZE_TEST_TASKS.md:19`) spends a mesh early and conflicts with the LIB rule. Human PIE was waived (`Docs/16_PLAYABLE_LOOP.md:106`) while M8 and M10–M14 still quit before a tick (`KNOWN_ERRORS.md:703`).

## Top 5

1. USE Automation already run on 5.8 for M8 and M10–M14. Proof: recorded `HomeWorld.T0` success, then a fresh Safe-Build rerun. Gauntlet stays UNVERIFIED until a one-tick smoke. A new PIE driver stays unbuilt.
2. Keep `place_pocket_kit_once.py` a one-sitting caller of `scene_placement.place_static`.
3. Keep measured blocks for cottage, island, bed, shrine, and windows. TripoSR is not recommended for any LIB mesh.
4. Keep pile, inventory, bull, shrine, and glide. PCG stays later dressing (`SCENE_SETUP.md:47`): enabled, UNVERIFIED as their stand-in.
5. Leave rune removal, night glide, the 1560 m edge, and the morning pile unbuilt. The GDD and `HOMEWORLD_ROUTE.md:71–116` disagree; the wording is Lead’s.
