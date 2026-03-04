# Day 12 [2.2]: Role — Attack/Defend (Protector)

**Goal:** Add **Protector** role behavior: State Tree combat branch (e.g. defend at night, move to enemy) and GAS combat abilities so a family agent can attack/defend.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 12, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).

---

## 1. Prerequisites

- **Day 11 done:** MEC_FamilyGatherer, ST_FamilyGatherer, Mass Spawner on DemoMap; agents spawn and are visible (and move if ZoneGraph is set up). See [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).
- **IsNight:** [UHomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h) provides `GetIsNight()` and `GetCurrentPhase()`. Use console **hw.TimeOfDay.Phase** to test night (see below).

**Testing IsNight (no DaySequence yet):** In PIE or Editor, open the **Output Log** or **Console** and run: `hw.TimeOfDay.Phase 2` to force **Night** (0=Day, 1=Dusk, 2=Night, 3=Dawn). Set back to day with `hw.TimeOfDay.Phase 0`. The State Tree Blackboard **IsNight** must be set from Blueprint or a Mass processor that reads `UHomeWorldTimeOfDaySubsystem::GetIsNight()`.

---

## 2. State Tree — Defend / Attack branch

Per [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) Step 3.2 and Step 5:

1. **ST_FamilyGatherer** (or a dedicated ST_FamilyProtector if you split by role): ensure the root **Selector** has a **Night?** (or **Threat?**) branch as the **first** child (highest priority), above Idle/Gather.
2. **Condition:** Blackboard **IsNight** (Bool). Set IsNight from Blueprint or a Mass processor using `TimeOfDaySubsystem::GetIsNight()` (subsystem is not directly exposed in State Tree editor). Optional: "enemy in range" from “enemy in range” from Blackboard / EQS.
3. **Task:** Defend — e.g. **MoveTo** (rally point or enemy actor); optionally **Play Anim Montage** (guard/attack idle).
4. **Blackboard:** Add **IsNight** (Bool) and optionally **DefendTarget** (Vector or Object). Wire IsNight from game code: get the world's `UHomeWorldTimeOfDaySubsystem` and call `GetIsNight()` each tick or from a Mass processor, and write the result to the State Tree blackboard.

---

## 3. GAS combat abilities (Protector)

- **C++:** `UHomeWorldProtectorAttackAbility` ([Source/HomeWorld/HomeWorldProtectorAttackAbility.h](../../Source/HomeWorld/HomeWorldProtectorAttackAbility.h)) — commit + log; add montage/effects in Blueprint. **Blueprint:** Run `Content/Python/create_ga_protector_attack.py` to create **GA_ProtectorAttack** and add to **BP_HomeWorldCharacter → Default Abilities**. Trigger via `TryActivateAbilityByClass` or add IA_ProtectorAttack for testing. **Granting:** For Mass agents with ASC, grant this ability; State Tree task can trigger by class or tag in Defend state.’s “family member” ASC if you use one; document how the State Tree or a task triggers the ability (e.g. “When in Defend state, fire ability by tag”).

---

## 4. Validation

- **PIE:** Run **hw.TimeOfDay.Phase 2** in console to force Night; agents using ST_FamilyGatherer should switch to the Defend branch. Use **hw.TimeOfDay.Phase 0** to return to day. Alternatively, with day/night or a test “night” trigger, agents switch to Defend (e.g. move toward enemy or rally point).
- **Combat:** After running `create_ga_protector_attack.py`, GA_ProtectorAttack is on the player Default Abilities. Trigger via `TryActivateAbilityByClass` or add input; check Output Log for "ProtectorAttack ability activated" and "committed successfully".

---

## 5. After Day 12

- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 12 (Protector); Today = Day 13 (Healer). Append [SESSION_LOG.md](../SESSION_LOG.md).
