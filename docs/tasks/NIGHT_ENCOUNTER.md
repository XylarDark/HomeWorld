# Optional night encounter (Act 2 prep)

**Purpose:** Design and stub for spawning or triggering encounters when the time-of-day phase is **Night**. Used for Act 2 "by night convert the enemy" (strip sin → loved form; see [VISION.md](../workflow/VISION.md)).

**Combat scope (from VISION):** We avoid going too in-depth with combat mechanics until a full vision board pass. Placeholder abilities, UI, and spawn stubs are fine for now.

**T8 (CURRENT_TASK_LIST):** This doc satisfies the optional "doc or stub for night spawn" criterion for Act 2 prep (day/night Defend at home). **T5 (twelfth list):** Stub and TimeOfDay hook (GetIsNight, OnNightStarted) documented here; DAY12 §4 updated with Defend validation and next step for Act 2.

**See also:** [CONVERSION_NOT_KILL.md](CONVERSION_NOT_KILL.md) (defeat → strip sin → loved form, conversion hook), [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md), [HomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h), [VISION.md](../workflow/VISION.md) § Day and night (night encounters two-part structure).

---

## Vision alignment checklist (three-part structure)

Per [VISION.md](../workflow/VISION.md) § Night encounters: (1) waves at home, (2) packs on planetoid, (3) key-point bosses. Implementation status:

| Part | Vision | Stub/config | How to verify |
|------|--------|-------------|---------------|
| **(1) Waves at home** | Waves spawn against your home; you and family defend and convert. | **Implemented.** Wave 1/2/3 with configurable delay and spawn count (Cube, Sphere, Cylinder); HUD "Wave N". | PIE: `hw.TimeOfDay.Phase 2`; see §2.1. Log: "Night encounter Wave 1 — spawned placeholder at ..."; HUD shows "Wave 1". |
| **(2) Packs on planetoid** | Monsters spawn across the planetoid; explore to find and convert packs. | **Implemented.** Planetoid pack placeholders spawn at `PlanetoidPackSpawnDistance` (default 2000), count `PlanetoidPackCount` (Cone mesh). | PIE: `hw.TimeOfDay.Phase 2` with `PlanetoidPackSpawnDistance` > 0. Log: "Planetoid pack 1/N (away from home) spawned at ...". See §1.1. |
| **(3) Key-point bosses** | Bigger monsters and bosses at key points; convert them. | **Implemented.** One boss placeholder at KeyPoint-tagged actor or at `KeyPointBossSpawnDistance` (scaled mesh). | PIE: place actor with tag `KeyPoint` or set `KeyPointBossSpawnDistance` > 0; set Phase 2. Log: "Key-point boss placeholder spawned at ...". See §1.2. |

---

## 0. Vision: two-part structure and goal

Per [VISION.md](../workflow/VISION.md) **Vanquishing foes** and **Night encounters (two-part structure and goal)**:

- **Conversion, not killing:** Combat **strips foes of their "sin"** and **converts them to their "loved" version**. Converted monsters can become **vendors**, **helpers**, **quest givers**, or **join the homestead as pets or workers**.
- **(1) Waves at home** — A set of **waves** spawn **against your home**; you and your family **defend and convert**.
- **(2) Packs on the planetoid** — **Monsters spawn throughout the planetoid**; you **explore to find and convert** these packs.
- **(3) Key interest places** — At **key points** on the planetoid, **bigger monsters and bosses** you must **convert**.

**Goal:** You have **limited time** each night. You split it between **defending** (waves at home) and **exploring** (packs + bosses). Success depends on **damage/output and strategy**. As you **progress**, you become **powerful enough to clear an entire planetoid in one night** — converting all foes so they can join as vendors, helpers, quest givers, or homestead pets/workers.

**Combat variety (from VISION):** **Defend (waves at home):** Defenses around your homestead; you can use **ranged attacks** (from defenses) or **go on the ground** and use **area-of-effect (AOE)** attacks. **Planetoid (away from home):** **Combos** and **single-target damage**. Variety lets you progress without building both at once; **end-game** = use AOE or single-target in either situation. See [VISION.md](../workflow/VISION.md) § Combat variety. Defend combat mode (ranged vs ground AOE) is documented and stubbed in [DEFEND_COMBAT.md](DEFEND_COMBAT.md). Defense positions (turrets, walls, placeholder slots) around the homestead are described in [DEFEND_DEFENSES.md](DEFEND_DEFENSES.md). Planetoid combat style (combo vs single-target) is documented and stubbed in [PLANETOID_COMBAT.md](PLANETOID_COMBAT.md).

Current implementation (below) is a **stub for waves at home** (spawn placeholders at/near home). Planetoid packs and key-point bosses are future work; design is documented here and in VISION.

---

## 1. Design

- **Trigger:** When `UHomeWorldTimeOfDaySubsystem::GetIsNight()` is true (or when phase transitions to Night), game code can spawn enemy actors or fire an encounter event.
- **Options:**
  - **Poll:** In GameMode Tick or a dedicated actor, call `GetIsNight()` each frame; when true, spawn a wave or enable a spawner.
  - **Delegate (stub):** Subscribe to `UHomeWorldTimeOfDaySubsystem::OnNightStarted`. When phase-change detection is implemented, this will broadcast once when phase becomes Night so spawn logic runs once per night transition instead of every frame.
- **Placement:** Spawn at configurable positions (e.g. from `demo_map_config.json` or a dedicated `night_encounter_config.json`), or use a volume/POI. Avoid overlapping family Defend rally points.

### 1.1 Planetoid packs (away from home)

Per [VISION.md](../workflow/VISION.md): the homestead **lands on the planetoid**; you **venture out** to explore. Night has **(1) waves at home** (defend) and **(2) packs across the planetoid** (explore to find and convert).

- **Goal:** "Defend then explore" — after (or while) defending waves at home, the player **explores the planetoid** to find **packs** of monsters, **convert** them (strip sin → loved form). Converted foes can become vendors, helpers, quest givers, or homestead pets/workers.
- **Spawn:** Packs spawn **away from home** (e.g. at a configurable distance or at POIs/volumes), so the player must leave the homestead to find them. One minimal stub: when night starts, spawn one placeholder "pack" at a configurable offset from home (e.g. 2000 units) so the loop has a first hook.
- **Home reference:** "Home" is the defend position (e.g. player/homestead location when night starts, or a tagged Home actor). Pack spawn positions are computed relative to home so they are clearly "out in the planetoid."
- **Finding and converting:** Player moves toward pack locations; conversion (strip sin → loved) is placeholder until combat/ability pass. This doc and the stub establish the **first step** toward packs on planetoid.

### 1.2 Key-point / boss (bigger monsters at key points)

Per [VISION.md](../workflow/VISION.md): at **key points** on the planetoid there are **bigger monsters and bosses** you must **convert** (strip sin → loved form); converted can become vendors, helpers, quest givers, or homestead pets/workers.

- **Trigger:** When it is **night** and a **key point** is present (e.g. an actor or volume in the level tagged `KeyPoint`), the game can spawn one **boss placeholder** at that point. Key points are interest places (dungeon entrance, shrine, landmark) where a stronger encounter is expected.
- **Placement:** Spawn one "boss" placeholder at the key point's location (or at a small offset). If no key-point actors exist in the level, a fallback is configurable distance from home (e.g. `KeyPointBossSpawnDistance` > 0) so the stub is testable in PIE without placing tagged actors.
- **Boss placeholder:** One larger or distinct actor (e.g. scaled-up mesh) so it reads as "bigger monster" vs wave/pack placeholders. Conversion outcome is the same as waves and packs: strip sin → loved form (placeholder until full combat/ability pass).
- **Conversion:** Same as waves and packs — convert, do not kill; converted boss can thematically become vendor, helper, quest giver, or homestead ally. No full implementation required for stub.

---

## 2. Implementation stub

- **C++:** [UHomeWorldTimeOfDaySubsystem](../../Source/HomeWorld/HomeWorldTimeOfDaySubsystem.h) exposes:
  - `GetIsNight()` — use to gate spawn logic (poll).
  - `OnNightStarted` (BlueprintAssignable multicast delegate) — reserved for future use when phase transitions are detected; currently not broadcast (poll `GetIsNight()` for now).
- **Console:** `hw.TimeOfDay.Phase 2` forces Night for testing; `hw.TimeOfDay.Phase 0` returns to Day.

### 2.1 Triggering one spawn at night (testing)

To trigger **at least one** night encounter spawn for PIE testing or automation:

1. Start PIE (DemoMap or any level using `AHomeWorldGameMode`).
2. In the in-game console, run: **`hw.TimeOfDay.Phase 2`**.
3. On the next GameMode Tick, `TryTriggerNightEncounter()` runs: when `GetIsNight()` is true and not yet triggered this night, it spawns **Wave 1** — one placeholder (Cube mesh) in front of the player at `NightEncounterSpawnDistance` (default 500).
4. **Log confirmation:** In Output Log, look for: `HomeWorld: Night encounter Wave 1 — spawned placeholder at X=... Y=... Z=... (distance=500)` (or your configured distance). The HUD shows "Wave 1" and "Phase: Night".
5. To trigger again: run `hw.TimeOfDay.Phase 0`, then `hw.TimeOfDay.Phase 2` again (resets `bNightEncounterTriggered`).

**Config (optional):** In BP_GameMode (or GameMode defaults), Category "HomeWorld|NightEncounter": `NightEncounterSpawnDistance`, `NightEncounterSpawnHeightOffset`. No console command is required to force a spawn — setting Phase to 2 is sufficient; spawn runs automatically once per night.

---

## 3. When implementing

1. Add spawn logic (e.g. in GameMode or a BP_NightEncounterManager): on Tick or when receiving a future OnNightStarted broadcast, spawn enemy actors or trigger an encounter event.
2. Optionally add phase-change detection in TimeOfDaySubsystem (e.g. Tick or from DaySequence) and call `OnNightStarted.Broadcast()` when phase transitions to Night.
3. Configure spawn count, class, and positions via config or Blueprint defaults.

---

## 4. Implementation status

- **T2 (CURRENT_TASK_LIST) implemented:** Night-phase spawn stub is in place. `AHomeWorldGameMode::TryTriggerNightEncounter()` runs each Tick: when `GetIsNight()` is true and not yet triggered this night, it spawns one `AStaticMeshActor` placeholder with Engine cube mesh (visible in PIE) in front of the player or at (500,0,100), and logs `HomeWorld: Night encounter triggered (Phase 2); spawned placeholder at ...`. When phase leaves night, the trigger resets so setting Phase 2 again spawns again. **T6 (seventeenth list):** Placeholder mesh set to `/Engine/BasicShapes/Cube` so the encounter is clearly observable in the viewport.
- **T6 (eighteenth list) implemented:** Night encounter spawn is **configurable** via GameMode (Blueprint/Editor): `NightEncounterSpawnDistance` (default 500, 50–5000), `NightEncounterSpawnHeightOffset` (default 50). Optional **second encounter type**: set `NightEncounterSecondSpawnDistance` > 0 in BP_GameMode (or defaults) to spawn a second placeholder at a different offset (forward+right); logs "Night encounter second spawn at ...". Success: in PIE at night, spawn distance/height and second spawn are configurable and testable.
- **T6 (nineteenth list) implemented:** **Wave stub** added. Set `NightEncounterWave2DelaySeconds` > 0 (e.g. 5) in BP_GameMode or defaults; when night starts, wave 1 spawns (first + optional second placeholder), then after the delay a **wave 2** spawns one more placeholder at a different offset (forward-left). Logs: "Night encounter wave 2 scheduled in X.Xs" and "Night encounter wave 2 spawned at ...". Timer is cleared when phase leaves night. Success: in PIE at night, wave 2 is observable after the configured delay.
- **T5 (twentieth list) implemented:** **Wave counter** — when a night encounter spawns, `CurrentNightEncounterWave` is 1 (wave 1) or 2 (after wave 2 spawns); reset to 0 when leaving night. Logs include "Wave 1" and "Wave 2". HUD shows "Wave N" when at night and wave > 0 (below phase label / above "Dawn in Ns"). `GetCurrentNightEncounterWave()` on GameMode for Blueprint/log. Success: in PIE at night, wave number visible on HUD and in Output Log when encounter triggers.
- **T5 (twenty-first list) implemented:** **Wave 2 difficulty stub** — Wave 2 now spawns **more** placeholders (configurable `NightEncounterWave2SpawnCount`, default 2) and uses **Sphere** mesh as a "different type" stub (Wave 1 = Cube). Positions are spread by index so wave-2 actors are distinguishable. Log: "Night encounter Wave 2 (difficulty stub): N enemies spawned (different type/count from Wave 1)." Success: in PIE at night with `NightEncounterWave2DelaySeconds` > 0 (e.g. 5), wave 2 results in different count and mesh type observable in world and log.
- **T5 (twenty-second list) implemented:** **Wave 3 and configurable spawn count per wave** — Wave 3 fires after `NightEncounterWave3DelaySeconds` (seconds after wave 2 spawns; 0 = disabled). Spawn count per wave: Wave 2 = `NightEncounterWave2SpawnCount`, Wave 3 = `NightEncounterWave3SpawnCount` (default 3). Wave 3 uses **Cylinder** mesh (distinct from Cube/Sphere), spawns farther (1.5× base distance). HUD shows "Wave 3" when wave 3 has spawned. Log: "Night encounter Wave 3 scheduled in X.Xs" and "Night encounter Wave 3 (configurable spawn count): N enemies spawned (Cylinder mesh, distinct from Wave 1/2)." Success: in PIE at night with Wave 2 and Wave 3 delays > 0, wave 3 results in config-driven count and distinct behavior observable in world and log.
- **T3 (twenty-third list) implemented:** **Planetoid pack stub (spawn away from home).** When night starts and `PlanetoidPackSpawnDistance` > 0 (default 2000), one placeholder "pack" is spawned at that distance from the player (home reference), in the player's forward direction, so it is clearly "away from home" and observable when venturing out. Uses Cone mesh to distinguish from waves (Cube/Sphere/Cylinder). Log: "HomeWorld: Planetoid pack (away from home) spawned at ... (distance=...)". 0 = disabled. Gives the "defend then explore" loop a first hook. See §1.1.
- **T5 (twenty-fourth list) implemented:** **Planetoid pack count (configurable).** `PlanetoidPackCount` (1–10, default 1) on GameMode: at night that many "pack" placeholders are spawned away from home at `PlanetoidPackSpawnDistance`, spread by angle (even circle). Set in Blueprint/Editor (Category "HomeWorld|NightEncounter"). Log: "Planetoid pack 1/N (away from home) spawned at ..." per pack and "Planetoid packs (away from home): N of M spawned at distance=...". Success: at night, more than one away-from-home spawn is configurable and observable in PIE.
- **T5 (twenty-third list) implemented:** **Key-point / boss placeholder stub.** When night and (a) an actor with tag `KeyPoint` exists in the level, one "boss" placeholder is spawned at that actor's location (scaled-up mesh so it reads as bigger); or (b) no KeyPoint actors but `KeyPointBossSpawnDistance` > 0, one boss placeholder is spawned at that distance from the player (fallback for testing). Conversion outcome: same as waves/packs (strip sin → loved; placeholder). See §1.2.
- **Scope:** Optional night-phase encounter for Act 2 "by night convert the enemy" (strip sin → loved form). Design and C++ API are in place; one-time spawn per night plus optional delayed wave 2 and wave 3; spawn distance, second type, wave-2/3 delay and spawn count per wave are configurable; wave counter on HUD and in log; **planetoid pack** spawn away from home (configurable distance); **key-point boss** spawn at KeyPoint-tagged actor or at configurable distance.
- **Defeat → convert (placeholder requirement):** All night encounter placeholders (wave, planetoid pack, boss) must support **defeat** so conversion runs. Spawned actors use **`AHomeWorldNightEncounterPlaceholder`**: overlap with the player pawn while `GetIsNight()` triggers `ReportFoeConverted(this)` and removal. See [CONVERSION_NOT_KILL.md](CONVERSION_NOT_KILL.md) §1 for the defeat trigger (overlap or future damage stub) and the requirement that placeholders call `ReportFoeConverted` when defeated.
- **Status:** **Stub implemented; configurable.** Use `hw.TimeOfDay.Phase 2` in PIE to observe spawn, "Wave 1" on HUD and in log; set `NightEncounterWave2DelaySeconds` > 0 to see "Wave 2"; set `NightEncounterWave3DelaySeconds` > 0 to see "Wave 3". Wave 2 spawns `NightEncounterWave2SpawnCount` placeholders (Sphere); Wave 3 spawns `NightEncounterWave3SpawnCount` (Cylinder). Set `PlanetoidPackSpawnDistance` > 0 (default 2000) and `PlanetoidPackCount` (1–10, default 1) to spawn that many "pack" placeholders away from home at angular spread (Cone mesh). **Key-point boss:** Place an actor with tag `KeyPoint` in the level and go to night to spawn one boss placeholder at that location; or set `KeyPointBossSpawnDistance` > 0 (no KeyPoint actors) to spawn one boss at that distance (larger mesh). Tune in Blueprint: GameMode defaults or BP_GameMode → Category "HomeWorld|NightEncounter". `OnNightStarted` remains reserved for when phase-change detection is added.
- **Next steps when expanding:**
  1. Replace placeholder with enemy class or configure via `night_encounter_config.json` / Blueprint defaults.
  2. Optionally add phase-change detection in `UHomeWorldTimeOfDaySubsystem` and call `OnNightStarted.Broadcast()` when phase transitions to Night.
  3. Configure spawn count, class, and positions via config or Blueprint.

---

## 5. Validation

- PIE with `hw.TimeOfDay.Phase 2`; confirm spawn logic runs (e.g. enemies appear or event fires). Set `hw.TimeOfDay.Phase 0` to confirm day behavior (no spawn or different behavior).
- **Defeat → conversion:** To test conversion (strip sin → loved) in PIE: **(1) Console:** run `hw.Conversion.Test` in the in-game console; **(2) Overlap:** at night, walk into a spawned placeholder — overlap triggers `ReportFoeConverted` and the placeholder is removed. See [CONVERSION_NOT_KILL.md](CONVERSION_NOT_KILL.md) §3.1 for full steps and automated `pie_test_runner` check.
- **Planetoid pack:** With `PlanetoidPackSpawnDistance` > 0 (default 2000) and `PlanetoidPackCount` (1–10, default 1), at night that many Cone-shaped placeholders appear at that distance, spread by angle ("away from home"); log "Planetoid pack 1/N (away from home) spawned at ..." and "Planetoid packs (away from home): N of M spawned at distance=...". Set PlanetoidPackSpawnDistance to 0 to disable.
- **Key-point boss:** With an actor tagged `KeyPoint` in the level, at night one larger (scaled) boss placeholder spawns at that actor's location; log "Key-point boss placeholder spawned at ...". With no KeyPoint actors, set `KeyPointBossSpawnDistance` > 0 to spawn one boss at that distance from the player (fallback for testing).
