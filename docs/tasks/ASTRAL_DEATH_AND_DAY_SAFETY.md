# Astral death and day safety (night combat)

**Purpose:** Design for "astral death" during night combat: when the player's astral body is defeated, they return to their physical body and wake at dawn with no permanent death. Distinct from succession/permanent death (`ReportDeathAndAddSpirit`, `hw.ReportDeath`).

**See also:** [VISION.md](../workflow/VISION.md) (Day and night: physical and spiritual worlds), [PROTOTYPE_SCOPE.md](../workflow/PROTOTYPE_SCOPE.md) § Day/night and astral, [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md), [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md).

---

## 1. Design (MVP scope)

- **Night = astral combat.** The player (and optionally family) operates in **astral form** at night; combat happens in the spiritual world.
- **Astral "death":** If the player's astral body is defeated (HP to zero, or equivalent defeat condition), that is **not** permanent death. The player **returns to their physical body** and **wakes at dawn**.
- **No permanent death from night combat.** No succession, no game over, no `ReportDeathAndAddSpirit`. Day is safe; night death is "knocked out of astral form" only.
- **Permanent death** (succession, `hw.ReportDeath`) applies to **physical-world death** (e.g. later when "enter astral during the day" is unlocked, or other day-phase lethal mechanics if ever added). Not in MVP.

---

## 2. Flow

1. **During night:** Player is in astral form (or representation thereof); combat and spirit abilities apply.
2. **Astral body defeated:** Trigger "astral death" (e.g. astral HP → 0, or a dedicated OnAstralDefeated event).
3. **Return to body:** Exit astral mode; character is back in physical world (e.g. in bed at homestead).
4. **Wake at dawn:** Time advances to **Dawn** (or Day) so the next playable state is morning. No penalty other than narrative (e.g. "you were driven back to your body"). **Health and other losses are not restored automatically at dawn** — per [VISION.md](../workflow/VISION.md), restoration happens **during the day** through eating food, taking care of yourself and family, and wholesome living; day activities can also grant buffs for the next astral fight.

---

## 3. Optional implementation hook (stub)

For implementation, a clear contract keeps astral death separate from permanent death:

- **OnAstralDeath** (or **OnAstralDefeated**): Fired when the player's astral form is defeated at night. Game code should:
  1. **Advance time to dawn** — e.g. `UHomeWorldTimeOfDaySubsystem::SetPhase(Dawn)` or `AdvanceToDawn()` (to be added when DaySequence/time is driven). For now, console `hw.TimeOfDay.Phase 0` or `3` can be used for testing.
  2. **Respawn player in bed** — e.g. teleport to "bed" or homestead spawn; no permanent death flow.
  3. **Do not** call `ReportDeathAndAddSpirit()` — that is for succession/permanent death only.

- **Where to hook:** GameMode, a dedicated AstralDeathSubsystem, or the character/ability that represents "astral form defeated." When astral combat is implemented, the ability or component that manages astral HP (or defeat state) should invoke this hook instead of any permanent-death path.

**Status (T1 implemented):** C++ implementation added. `AHomeWorldGameMode::OnAstralDeath(APlayerController*)` advances time to dawn via `UHomeWorldTimeOfDaySubsystem::AdvanceToDawn()` and respawns the player at start. **In-game wiring:** (1) `AHomeWorldGameMode::RequestAstralDeath(WorldContextObject)` static — call from any code with a world context. (2) `AHomeWorldCharacter::RequestAstralDeath()` — call from character/Blueprint or bind to input. (3) **IA_AstralDeath** (F8): run `setup_enhanced_input.py` (or let `init_unreal.py` run it) to create the action and add F8 to IMC_Default; in PIE press **F8** to trigger astral death without the console. Console **`hw.AstralDeath`** still works. (4) **Lethal astral damage:** When the player's Health (GAS attribute) reaches 0 during night phase, `AHomeWorldCharacter::OnHealthChanged` calls `RequestAstralDeath`, so dawn + respawn triggers without F8 or console. Any damage source that reduces Health to 0 at night (e.g. GameplayEffect, future night encounter damage) will trigger astral return. Do not call `ReportDeathAndAddSpirit` for astral death.

**List 61 — Astral-by-day entry (stub):** **Enter astral during the day** is implemented as a stub. (1) **Console:** **`hw.EnterAstral`** or **`hw.AstralByDay`** — when phase is Day (0) or Dusk (1), sets phase to Night (2) and sets `bAstralByDay` so that when the player returns (F8 or **`hw.AstralDeath`**), phase is restored to **Day** (0) and day restoration state (meals, love, etc.) is not cleared. (2) **C++:** `AHomeWorldGameMode::EnterAstralByDay()` — call from Blueprint or in-world trigger. (3) **PIE verification:** Run **`hw.TimeOfDay.Phase 0`** (day), then **`hw.EnterAstral`**; confirm phase becomes Night and Output Log shows "Enter astral during day". Run **`hw.AstralDeath`** (or F8); confirm phase becomes Day and "Return from astral-by-day — phase restored to Day" in log. See CONSOLE_COMMANDS.md § Commands and § Key PIE-test usage.

**Progression gate (T2 List 61):** **What unlocks** astral-by-day for MVP is **no gate** (always-on stub). The entry path calls `CanEnterAstralByDay(PlayerController)` before switching phase; for MVP it always returns **true**. **Future options:** (1) Tutorial complete — `AHomeWorldPlayerState::GetTutorialComplete()` (e.g. set by `hw.TutorialEnd`). (2) Love level threshold — `GetLoveLevel() >= N` (config or Blueprint). (3) Config flag — e.g. DefaultGame.ini or GameMode Blueprint property. When adding a real gate, implement the condition in `AHomeWorldGameMode::CanEnterAstralByDay()` and the entry path (console, in-world trigger, UI) will respect it without further changes.

**Day/time integration (astral-by-day, List 61 / T4):** Entering astral during the day does not break day/night or time-of-day. Assumptions and behaviour:

- **Time-of-day is phase-based (stub).** MVP uses `UHomeWorldTimeOfDaySubsystem` with explicit phases (Day, Dusk, Night, Dawn). There is no running in-world clock; phase is set by console, `EnterAstralByDay`, `AdvanceToDawn`, or future DaySequence. So "time continues or is paused" for astral-by-day is expressed as: on return we restore **phase** to Day so the same day continues.
- **Enter astral during day:** Allowed only when phase is Day or Dusk. GameMode sets phase to Night and sets `bAstralByDay` so the return path knows to restore Day instead of advancing to Dawn.
- **Return from astral-by-day:** `OnAstralDeath` sees `bAstralByDay`; it calls `TimeOfDay->SetPhase(Day)` and clears `bAstralByDay`. **Day restoration state is not cleared** (meals, love, buff) — the same day continues; only the player is respawned at start.
- **Normal night astral death** (player went to bed or `hw.TimeOfDay.Phase 2`, not via EnterAstralByDay): `OnAstralDeath` calls `AdvanceToDawn()` and clears day restoration (meals, love, etc.) so the next day cycle applies.
- **Consistency:** All phase changes go through `UHomeWorldTimeOfDaySubsystem::SetPhase` or `AdvanceToDawn()`. HUD, night encounter, spirit abilities, and save/load all query the same subsystem, so astral-by-day stays consistent with the rest of the time-of-day flow.

---

## 4. Relation to existing systems

| System | Use |
|--------|-----|
| **ReportDeathAndAddSpirit** / **hw.ReportDeath** | Permanent death (succession); do **not** use for astral death. |
| **UHomeWorldTimeOfDaySubsystem** | `GetIsNight()`, `SetPhase(Phase)`, `AdvanceToDawn()` (calls SetPhase(Dawn)). Console: `hw.TimeOfDay.Phase 0` (Day), `1` (Dusk), `2` (Night), `3` (Dawn); `hw.AstralDeath` runs full astral-return flow. |
| **NIGHT_ENCOUNTER.md** | Night-phase spawn/encounter; astral death is the **player** outcome when defeated in that encounter. |

---

## 5. Success criteria and PIE test

- Design documented: night-phase astral death → return to body → wake at dawn; no permanent death.
- **Implemented (T1):** `OnAstralDeath` → `AdvanceToDawn()` + `RestartPlayer`; console `hw.AstralDeath` or in-game **F8** (IA_AstralDeath) for testing.
- **Astral health on HUD (T1):** When TimeOfDay is Phase 2 (night), `AHomeWorldHUD` draws **Astral HP: &lt;Health&gt; / &lt;MaxHealth&gt;** from the player's GAS attribute set so the player can see astral HP and that lethal damage will trigger RequestAstralDeath. In PIE: run `hw.TimeOfDay.Phase 2`, then confirm the line "Astral HP: 100 / 100" (or current values) appears on the HUD; Output Log shows "HomeWorld HUD: Night phase — Astral HP ... (lethal damage triggers RequestAstralDeath)."
- **PIE validation:** In PIE, run `hw.TimeOfDay.Phase 2` (night), then press **F8** or run `hw.AstralDeath`; expect time phase 3 (dawn) and player respawned at start. Cross-links: VISION, PROTOTYPE_SCOPE, DAY12.
