# Day restoration loop (design)

**Purpose:** Design for how the player restores what was lost in the astral and gains buffs for the next night. Aligned with [VISION.md](../../../VisionBoard/Core/VISION.md) (Day as restoration) and [ASTRAL_DEATH_AND_DAY_SAFETY.md](ASTRAL_DEATH_AND_DAY_SAFETY.md).

**See also:** [PROTOTYPE_SCOPE.md](../../../VisionBoard/PROTOTYPE_SCOPE.md) § Day/night and astral.

---

## 1. Design principles

- **No automatic Health restore at dawn.** When the time-of-day phase changes to Dawn (or Day), the game must **not** apply any automatic Health (or other attribute) restoration. Restoration happens **only** through day activities (food, care, family, wholesome choices). This makes the day meaningful: how you spend the day directly determines how restored you are and what buffs you have for the next night.
- **Day activities are the restoration path.** Eating food, taking care of yourself and your family, and living a wholesome, loving life:
  1. **Restore** health and other losses from the previous night’s astral combat.
  2. Can **grant buffs** that carry into the next night’s astral combat (e.g. stronger spirit abilities, extra protection).
- **Night uses day state.** At night, the game may read “day restoration” state (e.g. did the player eat well? care for family?) to show buffs on HUD or to apply gameplay effects during astral combat.

---

## 2. No Health restore at dawn (explicit rule)

- On **phase transition to Dawn** (or Day): do **not** call any logic that sets Health (or Stamina, etc.) to a value or adds a flat restore. The TimeOfDay subsystem and GameMode must not apply automatic healing when phase becomes Dawn.
- **Respawn after astral death** is a separate flow: the player is respawned at start (e.g. in bed). A respawned pawn may start with default attributes (e.g. 100 Health) as a new body; that is independent of “no auto restore at dawn.” If the design later chooses “wake in place with current Health” (no respawn), then Health must still not be auto-restored on the phase change.
- **Stub / implementation check:** Ensure `UHomeWorldTimeOfDaySubsystem::SetPhase` / `AdvanceToDawn()` and any dawn-tick or phase-change handlers do not modify player Health. Restoration only via explicit day actions (e.g. ConsumeMeal, future care/family hooks).

---

## 3. Day activities (restoration and buffs)

| Activity        | Restoration effect (stub / future) | Buff for next night (stub / future) |
|----------------|-------------------------------------|--------------------------------------|
| **Food / meal**| Restore Health (e.g. +25 or to cap) | Set “day buff” flag; future: potency/duration |
| **Care**       | Future: restore Stamina / morale    | Future: small defensive or regen buff |
| **Family**     | Future: bond restoration            | Future: family-assisted astral buff |
| **Wholesome**  | Future: virtue-aligned restore       | Future: virtue buff for astral |

**Stub (T1):** One minimal path is enough to validate the loop: **consume a meal** (or “restore” interaction) that (1) restores Health by a fixed amount (or to MaxHealth), and (2) sets a **day restoration buff** flag on the player. At night, the HUD (or log) can show that the buff is active so the flow is testable in PIE.

---

**Caretaker stub (T2):** When the player uses `hw.RestoreMeal` / `ConsumeMealRestore` and there are actors with tag **Family** in the level, the meal counts as a "meal with family." PlayerState tracks **MealsWithFamilyToday** (incremented in that case, reset at dawn). HUD shows "Meals with family: N" during day. This stub feeds into love/buff later: caretaker role (cooking, meals with family) will contribute to love level and day buff potency (see [DAY_LOVE_OR_BOND.md](DAY_LOVE_OR_BOND.md)).

---

## 4. Implementation hooks (stub)

- **PlayerState (or subsystem):** A **day restoration buff** flag (e.g. `HasDayRestorationBuff`) that is set when the player performs a qualifying day activity (e.g. consume meal) and cleared at dawn so it must be earned again each day. At night, this flag can be shown on the HUD and used later to apply actual buffs.
- **Consume meal / restore:** A function (e.g. `ConsumeMealRestore`) that:
  - Is only valid during the **day** (not night phase).
  - Restores Health (e.g. +25 or set to MaxHealth; configurable later).
  - Sets the day restoration buff flag on the player’s PlayerState.
  - Can be invoked by a console command (e.g. `hw.RestoreMeal`) for testing, and later by an interactable (e.g. “eat at table”) or inventory consume.
- **Dawn:** When advancing to dawn (e.g. after astral death or time advance), clear the day restoration buff flag so the next day the player must perform day activities again to get the buff.
- **HUD at night:** When phase is Night, if the day restoration buff is set, show a line such as “Day buff: active” so the stub is visible in PIE.

---

## 5. Success criteria (T1)

- Design doc (this file) states: no Health restore at dawn; day activities are the restoration path; day activities can grant buffs for astral.
- **Stub:** (1) Consume meal (or `hw.RestoreMeal`) restores Health and sets day buff flag. (2) At night, HUD or log shows that the day buff is active. (3) At dawn, the day buff flag is cleared.
- **Day buff gameplay effect at night:** When the player has the day restoration buff and is at night, collecting a spiritual collectible grants **bonus** spiritual power (base 1 + 1 bonus = 2 per collectible). Without the buff, they get 1 per collectible. Implemented in `AHomeWorldSpiritualCollectible::OnCollectVolumeOverlap`; log line includes "day buff bonus" when applied. Test: set phase to night, set day buff (e.g. `hw.RestoreMeal` during day then `hw.TimeOfDay.Phase 2`), overlap collectible and check log / `hw.SpiritualPower`.
- **Persistence:** Day buff is persisted in `UHomeWorldSaveGame` (`bSavedHasDayRestorationBuff`). On `hw.Save` the current `HasDayRestorationBuff` is written; on `hw.Load` it is restored to PlayerState. Old saves without the field load with buff false.
- T1 status set to completed in CURRENT_TASK_LIST.

---

## 6. Relation to existing systems

| System | Use |
|--------|-----|
| **UHomeWorldTimeOfDaySubsystem** | Phase (Day/Dusk/Night/Dawn). Do **not** restore Health in SetPhase / AdvanceToDawn. Clear day buff when advancing to dawn. |
| **AHomeWorldPlayerState** | Hold `HasDayRestorationBuff`; provide Set/Get and clear-at-dawn (called from GameMode or TimeOfDay when advancing to dawn). |
| **AHomeWorldCharacter** | `ConsumeMealRestore()`: day-only, restore Health, set PlayerState day buff, log. |
| **AHomeWorldGameMode** | When advancing to dawn (e.g. OnAstralDeath), clear player’s day restoration buff. |
| **AHomeWorldHUD** | At night, if player has day buff, draw “Day buff: active” (or similar). |
