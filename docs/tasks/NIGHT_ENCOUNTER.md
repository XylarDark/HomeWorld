# Optional night encounter (Act 2 prep)

**Purpose:** Design and stub for spawning or triggering encounters when the time-of-day phase is **Night**. Used for Act 2 "by night vanquish the enemy" (see [VISION.md](../workflow/VISION.md)).

**T8 (CURRENT_TASK_LIST):** This doc satisfies the optional "doc or stub for night spawn" criterion for Act 2 prep (day/night Defend at home).

**See also:** [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md), [HomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h).

---

## 1. Design

- **Trigger:** When `UHomeWorldTimeOfDaySubsystem::GetIsNight()` is true (or when phase transitions to Night), game code can spawn enemy actors or fire an encounter event.
- **Options:**
  - **Poll:** In GameMode Tick or a dedicated actor, call `GetIsNight()` each frame; when true, spawn a wave or enable a spawner.
  - **Delegate (stub):** Subscribe to `UHomeWorldTimeOfDaySubsystem::OnNightStarted`. When phase-change detection is implemented, this will broadcast once when phase becomes Night so spawn logic runs once per night transition instead of every frame.
- **Placement:** Spawn at configurable positions (e.g. from `demo_map_config.json` or a dedicated `night_encounter_config.json`), or use a volume/POI. Avoid overlapping family Defend rally points.

---

## 2. Implementation stub

- **C++:** [UHomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h) exposes:
  - `GetIsNight()` — use to gate spawn logic (poll).
  - `OnNightStarted` (BlueprintAssignable multicast delegate) — reserved for future use when phase transitions are detected; currently not broadcast (poll `GetIsNight()` for now).
- **Console:** `hw.TimeOfDay.Phase 2` forces Night for testing; `hw.TimeOfDay.Phase 0` returns to Day.

---

## 3. When implementing

1. Add spawn logic (e.g. in GameMode or a BP_NightEncounterManager): on Tick or when receiving a future OnNightStarted broadcast, spawn enemy actors or trigger an encounter event.
2. Optionally add phase-change detection in TimeOfDaySubsystem (e.g. Tick or from DaySequence) and call `OnNightStarted.Broadcast()` when phase transitions to Night.
3. Configure spawn count, class, and positions via config or Blueprint defaults.

---

## 4. Implementation status (stub / deferred)

- **CURRENT_TASK_LIST T4:** This section satisfies the "implement or document stub" criterion; implementation is deferred with next steps below.
- **Scope:** Optional night-phase encounter for Act 2 "by night vanquish the enemy." Design and C++ API are in place; no spawn or trigger is implemented in-code.
- **Status:** **Stub / deferred.** Use `GetIsNight()` (or console `hw.TimeOfDay.Phase 2`) to gate future spawn logic; `OnNightStarted` is reserved for when phase-change detection is added.
- **Next steps when implementing:**
  1. Add spawn logic in GameMode Tick or a dedicated actor (e.g. BP_NightEncounterManager): when `GetIsNight()` is true, spawn enemy actors or fire an encounter event (optionally once per night via `OnNightStarted` when implemented).
  2. Optionally add phase-change detection in `UHomeWorldTimeOfDaySubsystem` (e.g. from DaySequence or Tick) and call `OnNightStarted.Broadcast()` when phase transitions to Night.
  3. Configure spawn count, class, and positions via `night_encounter_config.json` or Blueprint defaults.

---

## 5. Validation

- PIE with `hw.TimeOfDay.Phase 2`; confirm spawn logic runs (e.g. enemies appear or event fires). Set `hw.TimeOfDay.Phase 0` to confirm day behavior (no spawn or different behavior).
