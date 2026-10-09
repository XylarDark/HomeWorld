generated — do not hand-edit

# COMMANDS_AND_LOG_TAGS.md

Every `hw.*` console command, every runtime log prefix, and every input action, indexed from Source. Test packets name the expected log tag from this file.

## Provenance

| Field | Value |
|---|---|
| Extracted from | `Source/` (182 tracked files) and `Config/DefaultInput.ini`, re-greped on this branch after Lead interview #11 3A removed the dawn refill. Base main is `eb22326`; `Source/` is as this PR leaves it. |
| Pack | `Docs/handoffs/CONTEXT_PACK_V1.md`, bite 4 |
| Regenerate | re-grep Source after any `hw.*`, log-prefix, or input change and edit this file in the same commit. There is no generator script. |
| Last regeneration | Two passes, both re-greps. Pass 1 (interview #11 3A) dropped `GATHER: node '%s' replenished at dawn` (was `HomeWorldResourcePile.cpp:57`) and reworded `GATHER: node '%s' depleted until dawn` to `GATHER: node '%s' depleted`. Pass 2 made depletion unconditional in `TryHarvest`, retiring the `bDepleteUntilDawn` and `HarvestCooldownSeconds` switches; that edit is below every `GATHER` literal in this file, so no row here moved and no log tag changed. No `HarvestCooldown` tag was ever emitted, so none had to be dropped. |
| Scope | docs only. No `.uasset`, no `.umap`, no PIE. |

Two things this file cannot know, both stated rather than guessed:

1. **Key-to-action mappings are not in Source.** `Config/DefaultInput.ini` contains no `ActionKeyMappings` or `AxisMappings` section at all — it is Enhanced Input only. The keys live in `/Game/HomeWorld/Input/IMC_Default.IMC_Default`, a `.uasset`. Section 5 lists the action properties, their bound handlers, and the key each C++ comment *claims*; the claimed keys are marked unverified.
2. **Log prefixes are found by convention, not by a registry.** There is no table in Source mapping tags to meanings. The prefix list in section 3 is every leading token that a `UE_LOG` or `LOG_*` macro in Source actually emits. A new tag added to Source is a `closed_fail` here until this file lists it.

## 1. How to verify coverage

Run from the repo root. Both must come back empty.

```powershell
# hw.* commands and variables: every literal must appear in this file
Select-String -Path (git ls-files Source) -Pattern 'TEXT\("hw\.[^"]*"\)' -AllMatches |
  ForEach-Object { $_.Matches.Value } | Sort-Object -Unique

# log prefixes: every leading TAG: token must appear in this file.
# -CaseSensitive is REQUIRED. Without it Select-String also returns lowercase
# words lifted out of prose (http, sanity, allowed) that look like tags and are not.
# The (?:-[A-Za-z0-9]+)? arm catches hyphenated tags such as DS-A and MV-A.
Select-String -Path (git ls-files Source) -Pattern 'TEXT\("([A-Z][A-Za-z0-9_]*(?:-[A-Za-z0-9]+)?):' -CaseSensitive -AllMatches |
  ForEach-Object { $_.Matches.Groups[1].Value } | Sort-Object -Unique
```

Expected at this SHA: the first grep returns **80** literals, the second returns **69** tokens. Every one of the 69 is either a row in section 3 or a declared non-prefix in section 6 — that is the coverage check passing.

The second grep is deliberately over-broad. It also catches prose inside command help text and inside `Docs/`-style references quoted in comments. Section 6 lists the tokens such a grep produces that are **not** runtime log prefixes, so a reviewer can tell a real miss from a known false positive.

## 2. Console commands and console variables

All 77 commands are registered in one `FHomeWorldModule::StartupModule` block. All 80 `hw.*` identifiers in Source are accounted for: 77 commands + 3 variables.

### 2.1 Console commands (`hw.*`)

Flags come from `RegisterConsoleCommand`. `ECVF_Cheat` commands need `~` and are stripped in a shipping build; `ECVF_Default` is available without cheats.

| Command | Flags | Handler | Reg. line | Registered help text (verbatim) |
|---|---|---|---|---|
| `hw.Save` | `ECVF_Cheat` | `CmdSave` | 1447 | Save game (roles + spirit roster) to default slot. Use in PIE for T5 verification. |
| `hw.Load` | `ECVF_Cheat` | `CmdLoad` | 1452 | Load game from default slot. Use in PIE for T5 verification. |
| `hw.Roles` | `ECVF_Cheat` | `CmdRoles` | 1457 | Log current family roles (index → role). Use after hw.Save / hw.Load to verify role persistence. See DAY15_ROLE_PERSISTENCE.md, CONSOLE_COMMANDS.md. |
| `hw.ReportDeath` | `ECVF_Cheat` | `CmdReportDeath` | 1462 | Report player death and add to spirit roster (T5 / Day 21 verification). |
| `hw.Spirits` | `ECVF_Cheat` | `CmdSpirits` | 1467 | List spirit roster: count and spirit IDs. Run hw.ReportDeath then hw.Spirits to verify death-to-spirit (T5 / Day 21). |
| `hw.GrantBossReward` | `ECVF_Cheat` | `CmdGrantBossReward` | 1472 | Grant boss reward (Wood amount, default 100). Use in PIE for T5 / Day 25 verification. |
| `hw.Gather.Ore` | `ECVF_Cheat` | `CmdGatherOre` | 1477 | Add Ore to inventory (default 10). Stub for MVP tutorial List 6 step 5. Use in PIE to verify 'mine some ore' or harvest from BP_HarvestableOre. |
| `hw.Gather.Flowers` | `ECVF_Cheat` | `CmdGatherFlowers` | 1482 | Add Flowers to inventory (default 5). Stub for MVP tutorial List 6 step 5. Use in PIE to verify 'pick some flowers' or harvest from BP_HarvestableFlower. |
| `hw.Gather.Seed` | `ECVF_Cheat` | `CmdGatherSeed` | 1487 | Add Seed to inventory (default 1). D19-B cheat for N1_Crop nurture success-path. Use in PIE: hw.Gather.Seed 1 then night interact at GP_N1_Crop. |
| `hw.Inventory.Dump` | `ECVF_Cheat` | `CmdInventoryDump` | 1492 | T0 #4 / PL-C: inventory open gated by NODE_BACKPACK equip; logs INVENTORY slots when latch set. |
| `hw.PlaceWall` | `ECVF_Cheat` | `CmdPlaceWall` | 1497 | Place PlaceActorClass (e.g. BP_BuildOrder_Wall) at cursor. Requires PIE; run create_bp_build_order_wall.py first. |
| `hw.AstralDeath` | `ECVF_Cheat` | `CmdAstralDeath` | 1502 | Simulate astral death: advance time to dawn and respawn player at start. Use in PIE to test astral-return-on-death. See ASTRAL_DEATH_AND_DAY_SAFETY.md. |
| `hw.EnterAstral` | `ECVF_Cheat` | `CmdEnterAstral` | 1507 | List 61: Enter astral during the day (stub). From Day or Dusk, sets phase to Night; return with hw.AstralDeath restores Day. See ASTRAL_DEATH_AND_DAY_SAFETY.md, CONSOLE_COMMANDS.md. |
| `hw.AstralByDay` | `ECVF_Cheat` | `CmdEnterAstral` | 1512 | Alias for hw.EnterAstral: enter astral during day (List 61). |
| `hw.CompleteBuildOrder` | `ECVF_Cheat` | `CmdCompleteBuildOrder` | 1517 | Complete the nearest incomplete build order (e.g. wall hologram). Use in PIE to test agentic building flow. See DAY10_AGENTIC_BUILDING.md. |
| `hw.SimulateBuildOrderActivation` | `ECVF_Cheat` | `CmdSimulateBuildOrderActivation` | 1522 | Simulate SO_WallBuilder activation on nearest incomplete build order (log + CompleteBuildOrder). Use in PIE so SO activation is triggerable and observable. See DAY10_AGENTIC_BUILDING.md T3. |
| `hw.SpiritualPower` | `ECVF_Cheat` | `CmdSpiritualPower` | 1527 | Log spiritual power collected at night (night collectible stub). Set hw.TimeOfDay.Phase 2, overlap spiritual collectible, then run this to verify. |
| `hw.SpendSpiritualPower` | `ECVF_Cheat` | `CmdSpendSpiritualPower` | 1532 | Spend N spiritual power (e.g. hw.SpendSpiritualPower 5). Deducts from SpiritualPowerCollected if sufficient; logs stub 'upgrade unlocked'. Use in PIE to verify spend path. |
| `hw.Goods` | `ECVF_Cheat` | `CmdGoods` | 1537 | Log physical (day) and spiritual (night) goods counters. Physical = inventory (day harvest); spiritual = night collectible. T5 tagging. |
| `hw.SpiritBurst` | `ECVF_Cheat` | `CmdSpiritBurst` | 1542 | Trigger spirit/night-combat ability (GA_SpiritBurst). Only succeeds when hw.TimeOfDay.Phase 2 (night). Run create_ga_spirit_burst.py to add ability to character. |
| `hw.SpiritShield` | `ECVF_Cheat` | `CmdSpiritShield` | 1547 | Trigger second spirit ability (GA_SpiritShield). Only succeeds when hw.TimeOfDay.Phase 2 (night). Run create_ga_spirit_shield.py to add ability and bind key. |
| `hw.RestoreMeal` | `ECVF_Cheat` | `CmdRestoreMeal` | 1552 | Day restoration: consume meal (day only). Restores Health +25 and sets day buff for next night. At night HUD shows 'Day buff: active' if set. See DAY_RESTORATION_LOOP.md. |
| `hw.Meal.Breakfast` | `ECVF_Cheat` | `CmdMealBreakfast` | 1557 | MVP tutorial step 2: have breakfast (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, AddLovePoints(1), counts Family-tagged actors. Use in morning for List 3 verification. |
| `hw.Meal.Lunch` | `ECVF_Cheat` | `CmdMealLunch` | 1562 | MVP tutorial step 6: have lunch (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, love; counts Family-tagged actors. Use for List 7 verification. |
| `hw.Meal.Dinner` | `ECVF_Cheat` | `CmdMealDinner` | 1567 | MVP tutorial step 7: have dinner (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, love; counts Family-tagged actors. Use for List 7 verification. |
| `hw.LoveTask.Complete` | `ECVF_Cheat` | `CmdLoveTaskComplete` | 1572 | MVP tutorial List 4 step 3: complete one love task with partner. Adds 1 love (HUD Love: N) and increments love tasks completed today (reset at dawn). Use in PIE to verify 'one love task done'. See CONSOLE_COMMANDS.md. |
| `hw.GameWithChild.Complete` | `ECVF_Cheat` | `CmdGameWithChildComplete` | 1577 | MVP tutorial List 5 step 4: complete one game with child. Adds 1 love and increments games with child today (reset at dawn). Use in PIE to verify 'played one game with child'. See CONSOLE_COMMANDS.md, MVP_TUTORIAL_PLAN List 5. |
| `hw.TutorialEnd` | `ECVF_Cheat` | `CmdTutorialEnd` | 1582 | MVP tutorial List 10: mark 'family taken' / tutorial end. Sets bTutorialComplete on PlayerState and logs inciting incident. Use in PIE to verify step 13. See CONSOLE_COMMANDS.md, MVP_TUTORIAL_PLAN List 10. |
| `hw.FamilyTaken` | `ECVF_Cheat` | `CmdTutorialEnd` | 1587 | Alias for hw.TutorialEnd: mark family taken / tutorial complete (inciting incident). MVP tutorial List 10 step 13. |
| `hw.TestGrantSpiritualCollect` | `ECVF_Cheat` | `CmdTestGrantSpiritualCollect` | 1592 | Test-only: grant one spiritual collect using same formula as SpiritualCollectible (base + day buff + love). Night only. For pie_test_runner day-buff-bonus check. |
| `hw.Conversion.Test` | `ECVF_Cheat` | `CmdConversionTest` | 1597 | Trigger conversion hook (ReportFoeConverted) for testing. Logs 'Foe converted (strip sin → loved)' and increments ConvertedFoesThisNight. See CONVERSION_NOT_KILL.md. |
| `hw.RS.CollectDayBonus` | `ECVF_Cheat` | `CmdRSCollectDayBonus` | 1602 | Docs/21 RS-E: collect day special-site bonus that buffs night. Logs RS: day_bonus. Use at GP_RS_SpecialSite. |
| `hw.RS.CollectNightBonus` | `ECVF_Cheat` | `CmdRSCollectNightBonus` | 1607 | Docs/21 RS-E: collect night special-site bonus that buffs day. Logs RS: night_bonus. Use at GP_RS_SpecialSite. |
| `hw.RS.CrossBonusStatus` | `ECVF_Cheat` | `CmdRSCrossBonusStatus` | 1612 | Docs/21 RS-E: log day_bonus_for_night and night_bonus_for_day flags. |
| `hw.CombatStubs` | `ECVF_Cheat` | `CmdCombatStubs` | 1617 | Log DefendCombatMode (Ranged\|GroundAOE), PlanetoidCombatStyle (Combo\|SingleTarget), ComboHitCount. Use in PIE to verify combat stubs. See DEFEND_COMBAT.md, PLANETOID_COMBAT.md. |
| `hw.Planetoid.Complete` | `ECVF_Cheat` | `CmdPlanetoidComplete` | 1622 | Set planetoid-complete flag on GameMode for PIE testing of complete → travel-to-next flow. See PLANETOID_HOMESTEAD.md §5, CONSOLE_COMMANDS.md. |
| `hw.Planetoid.ZoneAlignment` | `ECVF_Cheat` | `CmdPlanetoidZoneAlignment` | 1627 | Get or set current zone alignment (Corrupted \| Neutral \| Positive). No arg = log current; with arg = set. Fight/harvest/empower read at runtime. See PLANETOID_BIOMES.md §3, CONSOLE_COMMANDS.md. |
| `hw.Planetoid.ZoneInfo` | `ECVF_Cheat` | `CmdPlanetoidZoneInfo` | 1632 | Log current zone alignment and biome (GameMode). Use in PIE to verify alignment/biome read at runtime. See PLANETOID_BIOMES.md §3, CONSOLE_COMMANDS.md. |
| `hw.SinVirtue.Pride` | `ECVF_Cheat` | `CmdSinVirtuePride` | 1637 | Log current Pride axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md. |
| `hw.SinVirtue.Greed` | `ECVF_Cheat` | `CmdSinVirtueGreed` | 1642 | Log current Greed axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md. |
| `hw.SinVirtue.Wrath` | `ECVF_Cheat` | `CmdSinVirtueWrath` | 1647 | Log current Wrath axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md. |
| `hw.SinVirtue.Envy` | `ECVF_Cheat` | `CmdSinVirtueEnvy` | 1652 | Log current Envy axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md. |
| `hw.GoToBed` | `ECVF_Cheat` | `CmdGoToBed` | 1657 | Go to bed: Night + GrantSpiritSleepGate. The bed is the form change. Phase-alone (hw.TimeOfDay.Phase 2) stays body (#9). |
| `hw.Sleep` | `ECVF_Cheat` | `CmdGoToBed` | 1662 | Alias for hw.GoToBed: set time-of-day to Night (Phase 2). MVP tutorial List 8 step 8. |
| `hw.Wake` | `ECVF_Cheat` | `CmdWake` | 1667 | Wake: advance time-of-day to Dawn (Phase 3). Only has effect when current phase is Night. Use in PIE for List 56 T3 verification. In-world: interact or overlap bed at night. |
| `hw.Sky.EnsureDefaultDay` | `ECVF_Default` | `CmdSkyEnsureDefaultDay` | 1672 | T0_DEFAULT_SKYBOX_DAY: force Day + ensure Engine stock bright day sky (SKY_DEFAULT_DAY / TOD_DAY / ENV_T0_HOME). Not NF2_B night lookdev. |
| `hw.FieldGather.Collect` | `ECVF_Cheat` | `CmdFieldGatherCollect` | 1677 | T0 #6 NODE_FIELD_GATHER: field herb/seed collect (CAM_T0_FIELD). Not dress/GP_Store/PROXY/plant; not ungated Gather.Flowers. |
| `hw.DayCamp.Eject` | `ECVF_Cheat` | `CmdDayCampEject` | 1687 | T0 #8 NODE_DAY_CAMP: cartoon EJECT_HOME launch->glider->home (TOD_DAY FORM_BODY CAM_T0_CAMP_DAY). StartGlideHome reverse CRUMB; not FALLBACK/PROXY/script-camp/convert. |
| `hw.Planetside.BootHome` | `ECVF_Cheat` | `CmdPlanetsideBootHome` | 1692 | T0 #10 planetside night glider boot home: Night w/o bed FORM_BODY -> EJECT_HOME via StartGlideHome (TOD_NIGHT_HOME NODE_GLIDER). Not day-camp #8; not FALLBACK down; not soft-kidnap. |
| `hw.Bed.SleepSpirit` | `ECVF_Cheat` | `CmdBedSleepSpirit` | 1697 | T0 #11 NODE_BED: the bed grants FORM_SPIRIT (TOD_NIGHT_SPIRIT CAM_T0_BED). Not phase-alone; not soft-kidnap; #9 w/o bed stay FORM_BODY. |
| `hw.Plant.Slot` | `ECVF_Cheat` | `CmdPlantSlot` | 1702 | T0 #3 NODE_PLANT_SLOT: spend RES_HERB -> day plant given herb on N1 slot (TOD_DAY FORM_BODY). Not nurture/PROXY. Same slot identity for #12. |
| `hw.Nurture.Slot` | `ECVF_Cheat` | `CmdNurtureSlot` | 1707 | T0 #12 NODE_PLANT_SLOT: spirit nurture same N1 slot as #3 day plant (TOD_NIGHT_SPIRIT FORM_SPIRIT). Prereq hw.Plant.Slot + hw.Bed.SleepSpirit; RES_SEED via hw.Gather.Seed. Not N2/body/day-plant-alone. |
| `hw.Portal.Camp` | `ECVF_Cheat` | `CmdPortalCamp` | 1712 | T0 #13 NODE_PORTAL_HOME->NODE_PORTAL_CAMP: spirit home->camp portal (TOD_NIGHT_SPIRIT FORM_SPIRIT). Prereq hw.Bed.SleepSpirit. Via HomeWorldShrinePortal*; not home<->planet alone; not body; not dress-as-camp. |
| `hw.CampNight` | `ECVF_Cheat` | `CmdCampNight` | 1717 | T0 #14 camp night: avoid 1 NODE_GUARD + soothe 2 NODE_SLEEPER (TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_CAMP_NIGHT). Prereq hw.Bed.SleepSpirit. Via UHomeWorldSpiritStealthComponent; soothe != convert; not GP_SS_Lit alone; not stealth-alone. |
| `hw.Kettle.Brew` | `ECVF_Cheat` | `CmdKettleBrew` | 1722 | T0 #2 NODE_KETTLE: spend RES_HERB -> tea; tea-gates sprint ~half day (TOD_DAY FORM_BODY). Not PROXY/meal/ungated alone. |
| `hw.Backpack.Equip` | `ECVF_Cheat` | `CmdBackpackEquip` | 1727 | T0 #4 NODE_BACKPACK: equip latch -> inventory open gated (TOD_DAY FORM_BODY). Not inventory-lite alone / not PROXY. |
| `hw.Inventory.Open` | `ECVF_Cheat` | `CmdInventoryOpen` | 1732 | T0 #4 NODE_BACKPACK: inventory open/use requires backpack equip latch. Ungated inventory-lite = closed_fail. |
| `hw.TimeOfDay.SetPhase` | `ECVF_Cheat` | `CmdTimeOfDaySetPhase` | 1737 | Set time-of-day via SetPhase (0=Day, 1=Dusk, 2=Night, 3=Dawn). Runs PersistDawnSnapshot on Dawn. Prefer over raw hw.TimeOfDay.Phase for evidence greps. |
| `hw.Craft.Status` | `ECVF_Cheat` | `CmdCraftStatus` | 1742 | GC-B: log campfire/tent/cottage_unlock progression flags. |
| `hw.Craft.GrantDemo` | `ECVF_Cheat` | `CmdCraftGrantDemo` | 1747 | GC-B: grant demo RES for campfire+tent craft (inventory). |
| `hw.Craft.Campfire` | `ECVF_Cheat` | `CmdCraftCampfire` | 1752 | GC-B: run RECIPE_CAMPFIRE spend + spawn (Stored-first). |
| `hw.Craft.Tent` | `ECVF_Cheat` | `CmdCraftTent` | 1757 | GC-B: run RECIPE_TENT spend + tent stub. |
| `hw.Craft.Torch` | `ECVF_Cheat` | `CmdCraftTorch` | 1762 | GC-B stub: RECIPE_TORCH spend + log. |
| `hw.Craft.TameBait` | `ECVF_Cheat` | `CmdCraftTameBait` | 1767 | GC-B stub: RECIPE_TAME_BAIT spend + log. |
| `hw.Craft.HealSalve` | `ECVF_Cheat` | `CmdCraftHealSalve` | 1772 | GC-B stub: RECIPE_HEAL_SALVE spend + log. |
| `hw.Craft.FishGear` | `ECVF_Cheat` | `CmdCraftFishGear` | 1777 | GC-B stub: RECIPE_FISH_GEAR spend + log. |
| `hw.Move.Mantle` | `ECVF_Cheat` | `CmdMoveMantle` | 1782 | MV-A: try mantle/vault from current facing (grep MOVE: MANTLE / MOVE: VAULT). |
| `hw.Move.Blink` | `ECVF_Cheat` | `CmdMoveBlink` | 1787 | MV-A: spirit blink toward SpiritAnchor/Shrine tag (grep MOVE: SPIRIT_BLINK). Spirit form + anchor in range. |
| `hw.Minigame.Heal` | `ECVF_Cheat` | `CmdMinigameHeal` | 1792 | CD-A: emit MINIGAME:HEAL log (DESKTOP prove). |
| `hw.Minigame.Nurture` | `ECVF_Cheat` | `CmdMinigameNurture` | 1797 | CD-A: emit MINIGAME:NURTURE log. |
| `hw.Minigame.Grow` | `ECVF_Cheat` | `CmdMinigameGrow` | 1802 | CD-A: emit MINIGAME:GROW log. |
| `hw.Minigame.Possess` | `ECVF_Cheat` | `CmdMinigamePossess` | 1807 | CD-A: emit MINIGAME:POSSESS + MOVEMENT possess stub log. |
| `hw.Boss.Status` | `ECVF_Cheat` | `CmdBossStatus` | 1812 | CD-A: log BOSS:STATUS DayBoss/NightBoss flags (after boss volume overlap). |
| `hw.Stealth.Status` | `ECVF_Cheat` | `CmdStealthStatus` | 1817 | SS-A: log STEALTH:STATUS lit/alert (spirit form + lit volumes). |
| `hw.Stealth.ForceLit` | `ECVF_Cheat` | `CmdStealthForceLit` | 1822 | SS-A: force spirit lit stub (0=off, 1=on). Grep STEALTH: LIT enter / ALERT / CLEAR. |
| `hw.Defend.Status` | `ECVF_Cheat` | `CmdDefendStatus` | 1827 | Act 2 prep: log Defend phase status (phase, DefendActive, DefendPosition count, Family count, family-moved-this-night). Use in PIE after hw.TimeOfDay.Phase 2. See DAY12_ROLE_PROTECTOR.md, CONSOLE_COMMANDS.md. |

Count: 77 commands.

### 2.2 Console variables (`hw.*`, not commands)

These are `TAutoConsoleVariable`, not `RegisterConsoleCommand`. Setting one runs `OnChanged`; they take a value, they take no arguments list.

| Variable | Type | Default | Flags | File:line | Registered help text (verbatim) |
|---|---|---|---|---|---|
| `hw.TimeOfDay.Phase` | `int32` | `0` | `ECVF_Cheat` (implicit) | `Source/HomeWorld/HomeWorldTimeOfDaySubsystem.cpp:42` | Override time-of-day phase for testing: 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = default (Day). Calls SetPhase side effects when changed externally. |
| `hw.TimeOfDay.NightDurationSeconds` | `float` | `120.f` | `ECVF_Cheat` (implicit) | `Source/HomeWorld/HomeWorldTimeOfDaySubsystem.cpp:47` | Night phase duration in seconds for stub countdown (Dawn in Ns). Used when phase is set to Night. |
| `hw.Portal.RequireNight` | `int32` | `-1` | `ECVF_Default` | `Source/HomeWorld/HomeWorldShrinePortalComponent.cpp:12` | Override shrine portal night gate: -1=use component bRequireNight, 0=allow day, 1=require night |

Note the default flags on the two `HomeWorldTimeOfDaySubsystem` variables: they are declared without an explicit `ECVF_` argument, so UE gives them `ECVF_Cheat`. `hw.Portal.RequireNight` passes `ECVF_Default` explicitly.

### 2.3 Entry points that are not `hw.*`

For completeness, so a grep for entry points does not report these as misses.

Neither is an `hw.*` command and neither runs in PIE. The invocation is `-run=HomeWorldEditor.<ClassName>`; the module prefix matters and is what the editor module name (`HomeWorldEditor`) supplies.

| Commandlet class | Kind | Header | Implementation |
|---|---|---|---|
| `UApplyPCGSetupCommandlet` | editor commandlet | `Source/HomeWorldEditor/ApplyPCGSetupCommandlet.h:15` | `Source/HomeWorldEditor/ApplyPCGSetupCommandlet.cpp:30` |
| `UCreateMECCommandlet` | editor commandlet | `Source/HomeWorldEditor/CreateMECCommandlet.h:13` | `Source/HomeWorldEditor/CreateMECCommandlet.cpp:24` |

The only literal `-run=` string in Source is inside `ApplyPCGSetupCommandlet.cpp:51`, and it reads `-run=HomeWorldEditor.ApplyPCGSetup`. The commandlet's own class is `UApplyPCGSetupCommandlet`, so that literal is a third spelling again; the class name is the authoritative one.

## 3. Log prefixes

43 runtime prefixes. Each row is the literal prefix a log line starts with. `First emit` is the first such line in Source, so a reviewer can jump straight to it. `Emitted from` counts the Source files that emit the prefix; `Kind` says whether the prefix is written inline or supplied by a macro.

Four prefixes are produced by a macro rather than written inline. Those are marked, because a grep for `TEXT("FALLBACK: ` finds nothing while the tag is still real:

| Macro | File:line | Literal prefix it emits |
|---|---|---|
| `LOG_FALLBACK` | `Source/HomeWorld/HomeWorldFallbackGlideComponent.cpp:26` | `FALLBACK: ` |
| `LOG_PORTAL_FALLBACK` | `Source/HomeWorld/HomeWorldShrinePortalComponent.cpp:20` | `FALLBACK: Portal ` |
| `LOG_BOUNDS` | `Source/HomeWorld/HomeWorldSoftBoundsComponent.cpp:8` | `BOUNDS: ` |
| `LOG_MOVE` | `Source/HomeWorld/HomeWorldTraversalComponent.cpp:13` | `MOVE: ` |

`FALLBACK: Portal ` is the compound prefix the pack names. Its sub-lines are `ready`, `cooldown - skip transit`, `blocked - night gate closed`, `failed - destination ... not found in level`, `transit %s -> %s @ %s`, `failed -- OverrideDestinationLabel none`, and `T0 camp transit via override ...`.

| Prefix | Kind | First emit | Known sub-tags | Emitted from |
|---|---|---|---|---|
| `BOUNDS` | macro `LOG_BOUNDS` | `Source/HomeWorld/HomeWorldSoftBoundsComponent.cpp:8` | soft walk-bounds active; soft pushback toward hub | 1 file |
| `BOSS` | direct | `HomeWorld.cpp:359` | `STATUS` (from `hw.Boss.Status`), `PHASE_NIGHT`, `PHASE_DAY`, `SEAL` | 4 files |
| `CAMP` | direct | `HomeWorldCampActor.cpp:127` | actor present, ease skip/fail/ok, `WOKE`, `KILLED`, `CONVERTED`, `SOFT_LATCH_ONLY`, captive free/refused/`CAPTIVE FREED` | 2 files |
| `CLOUD` | direct | `HomeWorldCloud.cpp:56` | master-not-loaded warning, surface wisp placed | 1 file |
| `CLOUD_DESCENT` | direct | `HomeWorldCharacter.cpp:800` | `refused`, `active`, `landed`; plus `glide mode entered` from `HomeWorldGlideMovementComponent.cpp:33` | 2 files |
| `CLOUD_FIELD` | direct | `HomeWorldCloudField.cpp:33` | `needs` (too few layers), `built` | 1 file |
| `CLOUD_WISP` | direct | `HomeWorldCloudWisp.cpp:28` | `collected` | 1 file |
| `CRAFT` | direct | `HomeWorld.cpp:233` | `status`, `spend`, `fail`, campfire, tent, torch, kitchen rebind | 4 files |
| `DAWN` | direct | `HomeWorldSaveGameSubsystem.cpp:125` | `persist` skipped, `persisted` | 1 file |
| `DS-A` | direct | `HomeWorldCraftSubsystem.cpp:279` | cottage revealed, spawn failed, runtime blockout spawned | 1 file |
| `EJECT_HOME` | direct | `HomeWorldFallbackGlideComponent.cpp:225` | `StartGlideHome` skip/fail/`launch→glider→home`, `reached home` | 1 file |
| `FALLBACK` | macro + direct | `HomeWorldCharacter.cpp:906` | `TryStartFallbackGlide`, plus the `FALLBACK: Portal ` compound from `LOG_PORTAL_FALLBACK` | 3 files |
| `FORM` | direct | `HomeWorldCharacter.cpp:587` | day verb rejected (sprint/mantle), form switch, `rune gate`, `sleep gate` | 1 file |
| `GATHER` | direct | `HomeWorld.cpp:184` | grant, blocked, harvest, treasure, pile/yield-node, inventory full/stack full; pile sub-tags `depleted` and `has no valid site→RES mapping` from `HomeWorldResourcePile.cpp:90` and `:98`; `YieldNode '%s' produced` from `HomeWorldYieldNode.cpp:80` | 5 files |
| `HEAL` | direct | `HomeWorldCharacter.cpp:1013` | component ready, ability, soft fail/success, night-only guard | 3 files |
| `HomeWorld:` | direct | `HomeWorld.cpp:39` | the generic prefix. Every `hw.*` command echoes its own name this way, plus subsystem and widget chatter. Cheapest possible smoke grep. | 21 files |
| `INTERACT` | direct | `HomeWorldCharacter.cpp:2719` | single verb-result line | 1 file |
| `INVENTORY` | direct | `HomeWorldCharacter.cpp:1859` | `slot[n]=...` per-slot dump | 1 file |
| `MINIGAME` | direct + tag helper | `HomeWorldCharacter.cpp:1102` | `HEAL`, `NURTURE`, `GROW`, `POSSESS`, `UNKNOWN`. Emitted by `HomeWorldCombatDream::GetMinigameLogTag` (`HomeWorldCombatDreamTypes.cpp:11`), not inline. | 3 files |
| `MOVEMENT` | direct | `HomeWorld.cpp:291` | `POSSESS` stub | 2 files |
| `MOVE` | macro `LOG_MOVE` | `Source/HomeWorld/HomeWorldTraversalComponent.cpp:13` | `MANTLE`, `VAULT`, `SPIRIT_BLINK`, `soft_reset`, `mount_boost`, `form_tune` | 1 file |
| `NF2` | direct | `HomeWorldCharacter.cpp:2645` | `soft_feedback` form/phase/sound/particles | 1 file |
| `NODE_BACKPACK` | direct | `HomeWorldCharacter.cpp:1765` | equip skip/ok, inventory rejected/`gated open` | 1 file |
| `NODE_BED` | direct | `HomeWorldCharacter.cpp:1350` | sleep gate, sleep-spirit skip/grant, granted-but-FORM_BODY | 2 files |
| `NODE_DAY_CAMP` | direct | `HomeWorldCharacter.cpp:2031` | eject skipped, `EJECT_HOME` latch/pending/done | 1 file |
| `NODE_FIELD_GATHER` | direct | `HomeWorldCharacter.cpp:1887` | collect skipped/failed, `field collect` ok | 1 file |
| `NODE_GLIDER` | direct | `HomeWorldCharacter.cpp:2113` | planetside boot skipped, `EJECT_HOME` latch/pending/done | 1 file |
| `NODE_GUARD` | direct | `HomeWorldCharacter.cpp:2425` | camp-night skipped/failed/incomplete, `ease failed` | 1 file |
| `NODE_KETTLE` | direct | `HomeWorldCharacter.cpp:594` | sprint rejected without tea, `tea-gated sprint`, brew skipped/failed/ok, gate cleared | 1 file |
| `NODE_PLANT_SLOT` | direct | `HomeWorldCharacter.cpp:1068` | plant skip/fail/ok, nurture skip/fail/ok, slot day-planted marker | 2 files |
| `NODE_PORTAL_HOME` | direct | `HomeWorldCharacter.cpp:2230` | portal-camp skipped, `NODE_PORTAL_CAMP` transit, soft-arrive | 1 file |
| `NODE_SLEEPER` | direct | `HomeWorldCharacter.cpp:2475` | `ease failed (soothe != convert)` | 1 file |
| `NODE_WAKE` | direct | `HomeWorldCharacter.cpp:1438` | start-day beat | 1 file |
| `NURTURE` | direct | `HomeWorldCharacter.cpp:1048` | night-only guard, need/spend failures, success, visual applied | 2 files |
| `PLACEHOLDER` | tag helper + direct | `HomeWorldGcPlaceholderTypes.cpp:12` | `WOODSHOP`, `TEXTILE`, `RESEARCH`, `COTTAGE_KITCHEN`, `COTTAGE_BEDROOM`, `CAULDRON`, `UNKNOWN`, plus `COTTAGE_KITCHEN locked` | 2 files |
| `PROGRESS` | direct | `HomeWorldCharacter.cpp:1181` | `COTTAGE_UNLOCK` | 2 files |
| `RS` | direct | `HomeWorld.cpp:869` | `day_bonus`, `night_bonus`, cross-bonus active, `status`, `cross_bonuses cleared at dawn` | 2 files |
| `SKY_DEFAULT_DAY` | direct | `HomeWorldTimeOfDaySubsystem.cpp:234` | `skipped`, `soft stack incomplete`, `bright day defaults`, `re-ensure` | 1 file |
| `STEALTH` | direct | `HomeWorldSpiritStealthComponent.cpp:105` | `LIT enter`, `CLEAR`, `ALERT`, `STATUS`, `QUICK_WINDOW`, `feel`, `ForceLit`, HUD tick, torch carrier | 4 files |
| `STORE` | direct | `HomeWorldCharacter.cpp:1205` | blocked, `transfer ok`, deposit/withdraw ok/fail/soft | 2 files |
| `TAME` | direct | `HomeWorldBeastTameComponent.cpp:56` | component ready, bond complete, radius exit, offer accepted/blocked, promotion | 2 files |
| `TOUCH` | direct | `HomeWorldSpiritStealthComponent.cpp:813` | target/form/verdict verdict line | 1 file |

Count: 43 runtime prefixes.

### 3.1 The `STEALTH` sub-tags Test packets use

`hw.Stealth.Status` and `hw.Stealth.ForceLit` exist to make these lines greppable. All of them live in `HomeWorldSpiritStealthComponent.cpp`:

- `STEALTH:STATUS lit=%d alert=%.2f overlaps=%d force=%d feel=%s` (`:155`)
- `STEALTH: LIT enter (%s)` (`:105`) and `STEALTH: LIT enter (ForceLit)` (`:144`)
- `STEALTH: ALERT` (`:283`)
- `STEALTH: CLEAR` (`:121` and `:291`)

`hw.Stealth.ForceLit` itself logs `STEALTH: ForceLit %d` from `HomeWorld.cpp:341`. Note the space: that one is `ForceLit %d`, while the component emits `ForceLit)` with a closing paren. A packet grepping for `ForceLit` matches both; a packet grepping for the full `STEALTH: ForceLit %d` matches only the command.

### 3.2 Log categories

The prefix above is the text inside the message. The category is the UE channel that carries it, and it is the thing `Log`/`Display:` filtering in the console keys off. Most evidence lines use the engine `LogTemp`; only these are project categories:

| Category | Declaration | Kind |
|---|---|---|
| `LogHomeWorld` | `Source/HomeWorld/HomeWorldGameMode.h:10` | `DECLARE_LOG_CATEGORY_EXTERN`, default verbosity `Log`, compiled for all |
| `LogHomeWorldPlayerState` | `Source/HomeWorld/HomeWorldPlayerState.cpp:6` | `DEFINE_LOG_CATEGORY_STATIC` |
| `LogBuildOrder` | `Source/HomeWorld/HomeWorldBuildOrder.cpp:8` | `DEFINE_LOG_CATEGORY_STATIC` |
| `LogApplyPCGSetup` | `Source/HomeWorldEditor/ApplyPCGSetupCommandlet.cpp:12` | `DEFINE_LOG_CATEGORY_STATIC` |
| `LogCreateMEC` | `Source/HomeWorldEditor/CreateMECCommandlet.cpp:11` | `DEFINE_LOG_CATEGORY_STATIC` |

## 4. Commands that name their own log tag

These registrations carry a grep target in their help text, so the command-to-tag link is Source's own statement and not an inference. A Test packet can pair the command with the tag without reading the handler.

| Command | Tag named in its registered help text |
|---|---|
| `hw.Boss.Status` | `BOSS:STATUS` |
| `hw.Stealth.Status` | `STEALTH:STATUS` |
| `hw.Stealth.ForceLit` | `STEALTH: LIT enter`, `ALERT`, `CLEAR` |
| `hw.Minigame.Heal` | `MINIGAME:HEAL` |
| `hw.Minigame.Nurture` | `MINIGAME:NURTURE` |
| `hw.Minigame.Grow` | `MINIGAME:GROW` |
| `hw.Minigame.Possess` | `MINIGAME:POSSESS` and a `MOVEMENT` possess stub |
| `hw.Move.Mantle` | `MOVE: MANTLE` or `MOVE: VAULT` |
| `hw.Move.Blink` | `MOVE: SPIRIT_BLINK` |
| `hw.RS.CollectDayBonus` | `RS: day_bonus` |
| `hw.RS.CollectNightBonus` | `RS: night_bonus` |
| `hw.Inventory.Dump` | `INVENTORY slots` |
| `hw.Craft.Status` | campfire / tent / `cottage_unlock` flags |
| `hw.CombatStubs` | `DefendCombatMode`, `PlanetoidCombatStyle`, `ComboHitCount` |
| `hw.Defend.Status` | `Phase`, `DefendActive`, `DefendPosition` count, `Family` count |

The other **62** commands have no grep target in their registered help text. Nearly all of their handlers log unprefixed `HomeWorld: <command name> ...` text, so grep the command name itself. Two of them also emit a real prefix from the handler body:

| Command | Prefix its handler also emits |
|---|---|
| `hw.Gather.Ore` | `GATHER` (`GATHER: RES_STONE (flint)`, `HomeWorld.cpp:184`) |
| `hw.RS.CrossBonusStatus` | `RS` (`RS: status ...`, `HomeWorld.cpp:901`) |

`hw.TimeOfDay.SetPhase` is not one of them — it logs only `HomeWorld:` lines. The `Wake:` and `T0_DEFAULT_SKYBOX_DAY:` strings near it are help text for `hw.Wake` and `hw.Sky.EnsureDefaultDay`, not output from this handler.

The `hw.Craft.*` run commands (`hw.Craft.Campfire`, `.Tent`, `.Torch`, `.TameBait`, `.HealSalve`, `.FishGear`) all delegate to one shared `CmdCraftRun` helper and emit no tag of their own; only `hw.Craft.Status` logs `CRAFT:`. The `hw.SinVirtue.*` commands do name their axis, in the form `HomeWorld: Pride: %g (stub; sin/virtue axis -1..0..+1)`, so grep the axis word rather than `hw.`.

## 5. Input

Enhanced Input end to end. `Config/DefaultInput.ini` sets `DefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput` and `DefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent`, and declares **no** key bindings.

### 5.1 Input actions declared in Source

All on `AHomeWorldCharacter`. `Property` is the `UPROPERTY` holding the `UInputAction`; `Claimed key` is what the C++ doc comment says, not a verified binding.

| Action property | Declared | Bound handler | Trigger events | Claimed key |
|---|---|---|---|---|
| `MoveAction` | `HomeWorldCharacter.h:441` | `Move` (Axis2D fallback) | `Triggered` | none claimed; "Axis2D fallback" |
| `LookAction` | `HomeWorldCharacter.h:445` | `Look` | `Triggered` | "Mouse delta" |
| `MoveForwardAction` | `HomeWorldCharacter.h:449` | `OnMoveForwardPressed` / `OnMoveForwardReleased` | `Triggered` / `Completed` | W |
| `MoveBackAction` | `HomeWorldCharacter.h:453` | `OnMoveBackPressed` / `OnMoveBackReleased` | `Triggered` / `Completed` | S |
| `StrafeLeftAction` | `HomeWorldCharacter.h:457` | `OnStrafeLeftPressed` / `OnStrafeLeftReleased` | `Triggered` / `Completed` | A |
| `StrafeRightAction` | `HomeWorldCharacter.h:461` | `OnStrafeRightPressed` / `OnStrafeRightReleased` | `Triggered` / `Completed` | D |
| `PrimaryAttackAction` | `HomeWorldCharacter.h:469` | `OnPrimaryAttackTriggered` | `Triggered` | Left Mouse |
| `DodgeAction` | `HomeWorldCharacter.h:473` | `OnSprintStarted` / `OnSprintCompleted` / `OnDodgeTriggered` | `Started` / `Completed` / `Triggered` | Shift |
| `InteractAction` | `HomeWorldCharacter.h:477` | `OnInteractTriggered` | `Triggered` | E |
| `PlaceAction` | `HomeWorldCharacter.h:481` | `OnPlaceTriggered` | `Triggered` | P |
| `AstralDeathAction` | `HomeWorldCharacter.h:485` | `OnAstralDeathTriggered` | `Triggered` | optional, "assign IA_AstralDeath or leave null" |
| `SpiritShieldAction` | `HomeWorldCharacter.h:489` | `OnSpiritShieldTriggered` | `Triggered` | R |

Bindings are guarded, but not uniformly. `HomeWorldCharacter.cpp:391` returns early unless `EnhancedInput`, `DefaultMappingContext`, `MoveAction`, and `LookAction` are all set, which is what protects the unguarded `LookAction` bind at `:425`. Below that, `MoveForwardAction`/`MoveBackAction`/`StrafeLeftAction`/`StrafeRightAction` are gated together at `:409`, `PrimaryAttackAction`, `InteractAction`, and `PlaceAction` are gated on **both** the action and its ability class, and `DodgeAction`, `AstralDeathAction`, and `SpiritShieldAction` are gated on the action pointer alone. An unassigned action is inert, not a crash.

### 5.2 Mapping context

| Item | Value | Source |
|---|---|---|
| Mapping context asset | `/Game/HomeWorld/Input/IMC_Default.IMC_Default` | hard-coded `LoadObject` at `Source/HomeWorld/HomeWorldCharacter.cpp:349` |
| C++ property | `DefaultMappingContext` (`UInputMappingContext`) | `Source/HomeWorld/HomeWorldCharacter.h:465` |
| Fallback | when unset, `HomeWorldCharacter.cpp:347-349` loads the same asset from the project | `Source/HomeWorld/HomeWorldCharacter.cpp:349` |
| Look sensitivity | `LookSensitivity`, default `1.0f`, editor clamp 0.01–10.0 | `Source/HomeWorld/HomeWorldCharacter.h:519-520`, applied at `HomeWorldCharacter.cpp:2710-2712` |
| Console key | `Tilde` (`+ConsoleKeys=Tilde`), the only key in the whole config | `Config/DefaultInput.ini:83` |
| User settings | `bEnableUserSettings=False`, so no rebinding UI persists | `Config/DefaultInput.ini:92` |

**Unverified and not verifiable from the repo:** the actual key each action is bound to. That lives in `IMC_Default`, a Git-LFS `.uasset` this bite does not open. The `Claimed key` column is the C++ comment's intent, restated, not read back from the asset. If a packet depends on a real key, open `IMC_Default` in the editor and confirm before writing the expectation.

## 6. Known false positives and non-prefixes

The over-broad prefix grep in section 1 also matches these. Each is in Source, and none is a runtime log prefix. A reviewer should not file a miss on them.

The grep returns **69** tokens. Of those, **43** are the section 3 prefixes above and **26** are the ones listed here. There are no others.

| Token | What it actually is |
|---|---|
| `Anti` | a test assertion label in `HomeWorldFormGateTests.cpp:149` and `:151`, not a runtime tag |
| `Converted`, `Envy`, `Greed`, `Love`, `Phase`, `Physical`, `Pride`, `Spirit`, `Spiritual`, `Wrath` | HUD line labels built with `FString::Printf` in `HomeWorldHUD.cpp` (`:74`, `:75`, `:76`, `:139`, `:142`, `:145`, `:148`, `:259`). Real output, but HUD vocabulary, not tag vocabulary. |
| `MeshList`, `Saved` | commandlet output, `ApplyPCGSetupCommandlet.cpp:110` and `CreateMECCommandlet.cpp:119`. Editor-only, so they never appear in a PIE log. |
| `Shield`, `SpiritBurst`, `SpiritShield` | ability feedback strings, `HomeWorldSpiritShieldAbility.cpp:54` and `HomeWorldHUD.cpp:342`/`:359` |
| `Wake` | sentence-initial word in the registered help text for `hw.Wake`, `HomeWorld.cpp:1669` |
| `Test-only` | the first word of the registered help text for `hw.TestGrantSpiritualCollect`, `HomeWorld.cpp:1594`. Sentence-initial, not a tag. |
| `MV-A`, `SS-A`, `CD-A`, `GC-B` | gate ids inside registered help text, `HomeWorld.cpp:1784`/`:1819`/`:1794`/`:1744`. `DS-A` is the one hyphenated gate id that really is emitted, see section 3. |
| `M2`, `M4`, `M9` | milestone ids in test assertion labels, `HomeWorldDayGateTests.cpp:199`/`:162` and `HomeWorldFormGateTests.cpp:140` |
| `T0_DEFAULT_SKYBOX_DAY` | a milestone label in the registered help text for `hw.Sky.EnsureDefaultDay`, `HomeWorld.cpp:1674`, and in comments. The runtime prefix for that beat is `SKY_DEFAULT_DAY`, which is a real prefix in section 3. |

Two categories that are worth naming but that the section 1 grep does **not** return, because it requires a colon immediately after the token inside a `TEXT("` literal:

- `RES_*`, `RECIPE_*`, `TOD_*`, `FORM_BODY`, `FORM_SPIRIT`, `CRUMB_*`, `NODE_*` are enum members, actor labels, and identifiers. They are not tags and never produce a grep hit.
- `MVP`, `T0`, `Docs`, `M14`, `M15`, `M16` appear in prose, comments, and test names mid-sentence, with no colon directly after them.

## 7. Relationship to `docs/CONSOLE_COMMANDS.md`

Not a dangling reference. Thirteen registered help strings name `CONSOLE_COMMANDS.md`, and that doc does exist on `main` at `docs/CONSOLE_COMMANDS.md` (373 lines). The referencing commands are `hw.Roles`, `hw.EnterAstral`, `hw.LoveTask.Complete`, `hw.GameWithChild.Complete`, `hw.TutorialEnd`, `hw.Planetoid.Complete`, `hw.Planetoid.ZoneAlignment`, `hw.Planetoid.ZoneInfo`, `hw.SinVirtue.Pride`, `hw.SinVirtue.Greed`, `hw.SinVirtue.Wrath`, `hw.SinVirtue.Envy`, and `hw.Defend.Status`, all in `Source/HomeWorld/HomeWorld.cpp`.

The two files do not overlap, which is why both are worth having:

| | `docs/CONSOLE_COMMANDS.md` (existing) | this file |
|---|---|---|
| What a command *does* | yes — prose run order, per-beat PIE steps, what outcome to expect | no |
| Expected log line for a beat | no | yes — sections 3, 3.1, 4 |
| Input bindings | no | yes, section 5, minus the unverified keys |
| Completeness guarantee | hand-maintained | every `hw.*` literal and prefix in Source, with the grep in section 1 |

It mentions none of `STEALTH`, `BOSS:`, `MOVE:`, `MINIGAME`, or log-prefix vocabulary at all. A packet that needs to know *what to run* reads that doc; a packet that needs to know *what to grep* reads this one. Neither replaces the other.

Note for anyone extending this file: `Docs/` and `docs/` are the same directory on Windows (DEC-0029), so the tracked path is lowercase `docs/` even though commands are commonly written as `Docs/`. Do not add a second copy.

## Header

Bite 4 asks the file to carry the header `generated — do not hand-edit`. It is line 1 of this file, unadorned, so the check is a literal read of the first line.

