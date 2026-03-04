# Day 13 [2.3]: Role — Support/Healer

**Goal:** Add **Support/Healer** role behavior: prioritizes healing/buffing and a GAS heal ability so a family agent (or the player) can heal allies.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 13, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md), [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md).

---

## 1. Prerequisites

- **Day 11 done:** MEC_FamilyGatherer, ST_FamilyGatherer, Mass Spawner on DemoMap. See [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md).
- **Day 12 optional:** Protector (GA_ProtectorAttack) gives the pattern for C++ ability + Blueprint + Default Abilities. See [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md).

---

## 2. GAS heal ability

- **C++:** `UHomeWorldHealAbility` ([Source/HomeWorld/HomeWorldHealAbility.h](../../Source/HomeWorld/HomeWorldHealAbility.h)) — commit + log; add healing GE or attribute change in Blueprint or extend in C++.
- **Blueprint:** Run `Content/Python/create_ga_heal.py` to create **GA_Heal** and add to **BP_HomeWorldCharacter → Default Abilities**. Trigger via `TryActivateAbilityByClass` or add IA_Heal for testing.
- **Granting:** For Mass agents with ASC, grant GA_Heal; a State Tree Heal? branch or task can trigger by class or tag. For player, the script adds it to Default Abilities.

---

## 3. State Tree (optional)

- **Heal? / Support? branch:** In ST_FamilyGatherer (or a dedicated ST for healer role), add a branch: condition e.g. **ally low health** (Blackboard or EQS); task **MoveTo** ally + trigger heal ability. Can be minimal for Day 13 (ability on character is enough for validation).

---

## 4. Validation

- **PIE:** After running `create_ga_heal.py`, GA_Heal is on the player Default Abilities. Trigger via `TryActivateAbilityByClass` or add input; check Output Log for "Heal ability activated" and "committed successfully".
- **Later:** Wire healing GE or attribute in Blueprint; add Heal? branch in State Tree for family healer agents.

---

## 5. After Day 13

- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 13 (Healer); Today = Day 14 (Child). Append [SESSION_LOG.md](../SESSION_LOG.md).
- Check off Day 13 in [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md).
