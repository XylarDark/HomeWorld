# HomeWorld – Console commands reference

Short reference for all `hw.*` and related console commands used in PIE testing and automation. All commands require a **play world** (PIE or packaged game); they are registered as cheat commands (`ECVF_Cheat`). Source: `Source/HomeWorld/HomeWorld.cpp`, `Source/HomeWorld/HomeWorldTimeOfDaySubsystem.cpp`.

---

## Pre-demo verification (entry point)

**How to run the pre-demo checklist:** Use a single sequence before recording or showing the slice.

1. **Step-by-step run sequence** — Follow [Vertical Slice Checklist §3](workflow/VERTICAL_SLICE_CHECKLIST.md) (Pre-demo checklist). §3 gives the ordered steps: open DemoMap, ensure PCG generated, start PIE, run `pie_test_runner.py`, inspect `Saved/pie_test_results.json`, and optional stability check.
2. **Console commands** — The `hw.*` commands you need during that run (time-of-day, save/load, place, harvest, conversion, etc.) are listed in this document: see [Commands (hw.*)](#commands-hw) and [Key PIE-test usage](#key-pie-test-usage).

Opening this doc gives you both: the link to §3 for the run sequence and the command reference in the sections below.

---

## Commands (hw.*)

| Command | Description |
|--------|-------------|
| **hw.Save** | Save game (roles, spirit roster, phase, etc.) to default slot. Use in PIE for SaveGame verification (e.g. DAY15 §4). |
| **hw.Load** | Load game from default slot. Use in PIE for SaveGame verification. |
| **hw.ReportDeath** | Report player death and add player to spirit roster (T5 / Day 21). Verifiable via `pie_test_runner` check_report_death. |
| **hw.GrantBossReward** [*amount*] | Grant boss reward (Wood). Default amount 100; e.g. `hw.GrantBossReward 50`. Use in PIE for Day 25 verification. |
| **hw.PlaceWall** | Place build-order actor (e.g. BP_BuildOrder_Wall) at cursor. Requires PIE; run build-order setup script first. |
| **hw.AstralDeath** | Simulate astral death: advance time to dawn and respawn player at start. Use in PIE to test astral-return-on-death (ASTRAL_DEATH_AND_DAY_SAFETY.md). |
| **hw.CompleteBuildOrder** | Complete the nearest incomplete build order (e.g. wall hologram). Use in PIE to test agentic building (DAY10_AGENTIC_BUILDING.md). |
| **hw.SimulateBuildOrderActivation** | Simulate SO_WallBuilder activation on nearest incomplete build order (log + CompleteBuildOrder). Use in PIE so activation is triggerable and observable. |
| **hw.SpiritualPower** | Log spiritual power and spiritual artefacts counts (PlayerState). Set `hw.TimeOfDay.Phase 2`, overlap spiritual collectible, then run to verify. |
| **hw.SpendSpiritualPower** [*N*] | Spend N spiritual power (e.g. `hw.SpendSpiritualPower 5`). Deducts from SpiritualPowerCollected; logs stub "upgrade unlocked". Use in PIE to verify spend path. |
| **hw.Goods** | Log physical (day) and spiritual (night) goods: physical total from InventorySubsystem, spiritual power and spiritual artefacts from PlayerState. |
| **hw.SpiritBurst** | Trigger GA_SpiritBurst ability. Only succeeds when `hw.TimeOfDay.Phase 2` (night). Run create_ga_spirit_burst.py to add ability to character. |
| **hw.SpiritShield** | Trigger GA_SpiritShield ability. Only succeeds when `hw.TimeOfDay.Phase 2` (night). Run create_ga_spirit_shield.py to add ability and bind key. |
| **hw.RestoreMeal** | Day restoration: consume meal (day only). Restores Health +25 and sets day buff for next night. At night HUD shows "Day buff: active" if set (DAY_RESTORATION_LOOP.md). |
| **hw.TestGrantSpiritualCollect** | Test-only: grant one spiritual collect using same formula as SpiritualCollectible (base + day buff + love). **Night only.** For pie_test_runner day-buff-bonus and love-bonus checks. |
| **hw.Conversion.Test** | Trigger conversion hook (ReportFoeConverted) for testing. Logs conversion and increments ConvertedFoesThisNight (CONVERSION_NOT_KILL.md). |
| **hw.CombatStubs** | Log DefendCombatMode (Ranged \| GroundAOE), PlanetoidCombatStyle (Combo \| SingleTarget), and ComboHitCount to Output Log. Use in PIE to verify combat stubs. See [DEFEND_COMBAT.md](tasks/DEFEND_COMBAT.md), [PLANETOID_COMBAT.md](tasks/PLANETOID_COMBAT.md). |

---

## Console variables (cvars)

| Cvar | Default | Description |
|------|---------|-------------|
| **hw.TimeOfDay.Phase** | 0 | Override time-of-day phase: **0** = Day, **1** = Dusk, **2** = Night, **3** = Dawn. **-1** = use default (Day). Set in PIE with e.g. `hw.TimeOfDay.Phase 2` for night; used by Defend branch, spirit abilities, spiritual collectibles. |
| **hw.TimeOfDay.NightDurationSeconds** | 120 | Night phase duration in seconds for stub countdown ("Dawn in Ns"). Used when phase is set to Night. |

---

## Key PIE-test usage

- **TimeOfDay:** Use `hw.TimeOfDay.Phase 0` for day, `hw.TimeOfDay.Phase 2` for night. Many checks (Defend, spirit abilities, spiritual collectibles, day buff at night) require Phase 2.
- **Save/Load:** In PIE run `hw.Save` then `hw.Load`; confirm success and counts in Output Log. `pie_test_runner` includes `check_save_load_persistence` and related checks.
- **Death and boss reward:** `hw.ReportDeath` (spirit roster); `hw.GrantBossReward` or `hw.GrantBossReward 50`. Validated by `check_report_death` and `check_grant_boss_reward` in pie_test_runner.
- **Day restoration:** `hw.RestoreMeal` (day only); then set Phase 2 and use `hw.TestGrantSpiritualCollect` to verify day-buff bonus; `hw.SpiritualPower` or `hw.Goods` to confirm counters.
- **Conversion:** `hw.Conversion.Test` to trigger one conversion and see ConvertedFoesThisNight / role in Output Log.
- **Astral death:** Set `hw.TimeOfDay.Phase 2`, run `hw.AstralDeath`; expect dawn + respawn at start (pie_test_runner has check_astral_death).
- **Spirit abilities:** Set `hw.TimeOfDay.Phase 2`, then `hw.SpiritBurst` or `hw.SpiritShield` (abilities must be granted to character).
- **Night encounter (one spawn at Phase 2):** Set `hw.TimeOfDay.Phase 2` in PIE; Wave 1 spawns one placeholder (Cube) in front of the player. Output Log: `HomeWorld: Night encounter Wave 1 — spawned placeholder at ...`. HUD shows "Wave 1" and "Phase: Night". See [NIGHT_ENCOUNTER.md](tasks/NIGHT_ENCOUNTER.md) §2.1.
- **Combat stubs (DefendCombatMode, PlanetoidCombatStyle, ComboHitCount):** In PIE, run **`hw.CombatStubs`** to print current values to the Output Log (e.g. `DefendCombatMode=Ranged`, `PlanetoidCombatStyle=SingleTarget`, `ComboHitCount=0`). To change DefendCombatMode or PlanetoidCombatStyle, select the player's **PlayerState** in the World Outliner, then in the Details panel use **HomeWorld|Defend** and **HomeWorld|Planetoid**; run `hw.CombatStubs` again to confirm. See [DEFEND_COMBAT.md](tasks/DEFEND_COMBAT.md) and [PLANETOID_COMBAT.md](tasks/PLANETOID_COMBAT.md) "Testing in PIE".

**Running checks:** With Editor open and PIE running, execute `pie_test_runner.py` via MCP (`execute_python_script("pie_test_runner.py")`) or Tools → Execute Python Script; read `Saved/pie_test_results.json` for pass/fail and detail. See [VERTICAL_SLICE_CHECKLIST](workflow/VERTICAL_SLICE_CHECKLIST.md) §3 for pre-demo checklist.

---

## Reading Saved/pie_test_results.json

After running `pie_test_runner.py`, results are written to **`Saved/pie_test_results.json`**. Use this section to interpret the file.

**Top-level keys:**

| Key | Meaning |
|-----|--------|
| **pie_was_running** | `true` if PIE was active when the script ran; many checks require PIE. |
| **note** | Present when PIE was not running (e.g. "PIE not running. Start PIE first for full validation."). |
| **summary** | One-line result, e.g. `"25/35 passed"`. |
| **all_passed** | `true` only when every check passed. |
| **checks** | Array of per-check results (see below). |

**Each item in `checks`** has:

- **name** — Short label for the check (e.g. "PIE active", "Character spawned", "On ground").
- **passed** — `true` or `false`; use this for pass/fail.
- **detail** — Human-readable explanation (e.g. movement mode, actor count, or error message).

**Pass/fail:** A run is successful when `all_passed` is `true`. If not, inspect `checks` and look for entries with `"passed": false`; use **detail** to see why (e.g. "PIE not running", "No controlled pawn", "No actor with tag Portal_To_Planetoid").

**Check names (what they mean):**

| Check name | What it verifies |
|------------|------------------|
| PIE active | Play-in-Editor was running when the script ran. |
| Character spawned | Controlled pawn is present (e.g. BP_HomeWorldCharacter). |
| On ground | Character movement is not falling (on ground or walking). |
| Capsule dimensions | Character capsule has valid half-height and radius. |
| Skeletal mesh | Character mesh component has a skeletal mesh assigned. |
| AnimInstance | Character has an active animation instance. |
| PlaceActorClass set | BP_HomeWorldCharacter has a build-order class set for placement. |
| Placement API | GetPlacementHit/GetPlacementTransform (BuildPlacementSupport) works. |
| Place flow (PIE) | hw.PlaceWall and BuildOrder count (key P / placement). |
| Harvest flow (PIE) | TryHarvestInFront / Wood (E on harvestable). |
| PCG actors | Level has many static mesh actors (e.g. > 100 from PCG). |
| Portal configured | Level has an actor tagged Portal_To_Planetoid with LevelToOpen set. |
| Dungeon entrance configured | Level has an actor tagged Dungeon_POI. |
| Planetoid / HomesteadLandedOnPlanetoid | On planetoid/DemoMap, GameMode set HomesteadLandedOnPlanetoid. |
| TimeOfDay Phase 2 | After hw.TimeOfDay.Phase 2, GetIsNight() is true. |
| Astral death flow | hw.AstralDeath advances to Dawn and respawn. |
| Spirit ability (Phase 2) | hw.SpiritBurst at night runs without error. |
| Night collectible counters | Spiritual power/artefact counters readable at Phase 2. |
| ReportDeath | hw.ReportDeath and spirit roster. |
| GrantBossReward | hw.GrantBossReward and Wood. |
| Conversion test (hw.Conversion.Test) | ConvertedFoesThisNight and converted role. |
| Save/Load persistence | hw.Save / hw.Load and basic round-trip. |
| SaveGame round-trip (phase, LoveLevel, spiritual) | Phase, LoveLevel, spiritual power restored after save/load. |
| LoveLevel persistence (save/load) | LoveLevel restored after hw.Save then hw.Load. |
| TimeOfDay phase persistence (save/load) | Phase 2 (night) restored after save/load. |
| Spiritual power persistence (save/load) | Spiritual power count restored after save/load. |
| SpendSpiritualPower / astral HUD | hw.SpendSpiritualPower decreases power at Phase 2. |
| Day restoration (RestoreMeal) | hw.RestoreMeal sets day buff or meals count. |
| Day buff persistence (save/load) | Day buff still set after save/load. |
| Day buff bonus at night (collect) | At night, day buff gives +1 spiritual power per collect. |
| Love bonus at night (collect) | At night, LoveLevel adds bonus to spiritual collect. |

**One-line summary in Output Log:** When you run `pie_test_runner.py` from the Editor (MCP or Tools → Execute Python Script), the script also prints a one-line summary to the **Output Log** (e.g. "PIE validation: 25/35 passed" or "PIE validation failed: 25/35 (see Saved/pie_test_results.json)"). Use that for a quick pass/fail; use the JSON file for which checks failed and why.
