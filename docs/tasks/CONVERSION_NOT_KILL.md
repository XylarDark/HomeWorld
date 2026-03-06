# Conversion not kill: strip sin → loved form

**Purpose:** Design for how "defeat" in HomeWorld triggers **conversion** (strip sin → loved form), not death. Per [VISION.md](../workflow/VISION.md): we do not kill foes; combat strips them of their sin and converts them to their "loved" version. Converted foes can become vendors, helpers, quest givers, or homestead pets/workers.

**See also:** [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (waves at home, planetoid packs, key-point bosses), [VISION.md](../workflow/VISION.md) § Vanquishing foes and Night encounters.

**Combat variety (defend vs planetoid):** Per [VISION.md](../workflow/VISION.md) § Combat variety: **at home (defend)** you use **ranged attacks** (from defenses) or **ground AOE**; **on planetoid** (away from home) combat uses **combos** and **single-target** damage; **end-game** you can use either style in either situation. See [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) §0 for the same breakdown and [DEFEND_COMBAT.md](DEFEND_COMBAT.md) / [PLANETOID_COMBAT.md](PLANETOID_COMBAT.md) for design stubs.

---

## 1. Defeat triggers conversion

**When is a foe "defeated"?** One of:

- **Placeholder (current):** A night-encounter placeholder (Cube/Sphere/Cylinder/Cone mesh) is removed from the world (e.g. destroyed, or tagged "Defeated"). The game treats that as "defeated" and runs the conversion flow.
- **Future combat:** When a foe's **sin value** (or equivalent health/resistance tied to sin) is reduced to **zero** by player damage or abilities, the foe is considered "defeated" and conversion runs. No death/kill; the transition is strip sin → loved form.

**Placeholder requirement:** Night encounter placeholders (wave, planetoid pack, boss) **must** support a defeat trigger so conversion runs. Current implementation: use **`AHomeWorldNightEncounterPlaceholder`** (C++), which has an overlap volume; when the player pawn overlaps it and `GetIsNight()` is true, it calls `ReportFoeConverted(this)` and destroys itself. Alternative for future placeholders: a minimal damage/health stub that on "death" (e.g. health → 0 or removal) calls `ReportFoeConverted`. Any new night-encounter actor that should count as "converted when defeated" must either be this class or invoke `ReportFoeConverted` when its defeat condition is met. See [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) §4 for spawn and placeholder usage.

**Hook in code:** When any system determines a foe is defeated (placeholder removed, sin reduced to zero, or ability/applied effect), it calls **`AHomeWorldGameMode::ReportFoeConverted(AActor* Foe)`**. That function:

- Logs that a foe was converted (strip sin → loved) for validation and debugging.
- Increments a per-night counter `ConvertedFoesThisNight` (reset when phase leaves Night) so the flow can be extended (e.g. HUD, rewards, role assignment).

No full implementation is required for the stub: the hook is triggerable via:

- **Combat/ability code** (when implemented): call `ReportFoeConverted(Foe)` when the foe is "defeated" (sin stripped).
- **Console:** `hw.Conversion.Test` in PIE calls the hook with no actor to verify the log and counter (testable without combat).

---

## 2. What happens after conversion (loved form, role stub)

After a foe is converted:

1. **Loved form:** The foe is replaced or transformed into their "loved" version (no death state). Placeholder: the encounter actor may be destroyed or replaced by a neutral/friendly placeholder; full implementation is later.
2. **Role assignment (stub):** Converted foes can later be assigned a **role**: vendor, helper, quest giver, or homestead pet/worker. **Implemented (T2):** When `ReportFoeConverted` is called, the game assigns a stub role round-robin (`EConvertedFoeRole`: Vendor, Helper, QuestGiver, Pet, Worker) and stores it in `ConvertedFoeRolesThisNight`. Role is readable via `GetConvertedFoeRole(int32 Index)` (0-based index for conversions this night). List is cleared when phase leaves Night. No persistence or full behavior yet.
   - When expanding: use the role for spawning vendors, helpers, quest givers, or homestead NPCs.

**Current scope:** Design doc + conversion hook + role stub. Full loved-form spawn and role-driven behavior are future work.

---

## 3. Validation

- **Design:** This doc exists and defines defeat → conversion and post-conversion (loved form, role stub).
- **Hook:** In PIE, run `hw.Conversion.Test`; Output Log should show a "Foe converted (strip sin → loved)" message and the conversion path is triggerable. Optional: verify `GetConvertedFoesThisNight()` increases (e.g. call twice, then check value or log).

### 3.1 Testing defeat → conversion in PIE

**Defeat path (two ways to trigger conversion in PIE):**

1. **Console (no combat):** With PIE running, open the in-game console (`~`), run:
   - `hw.Conversion.Test`
   - Output Log shows: `HomeWorld: Foe converted (strip sin → loved); Foe=...; ConvertedFoesThisNight=N; role: ...` and `HomeWorld: hw.Conversion.Test executed (conversion hook triggered; ConvertedFoesThisNight=N; Role=N)`.
   - At night, the HUD shows "Converted: N" (updates each time you run the command or convert a placeholder).

2. **Overlap (placeholder defeat):** Set night with `hw.TimeOfDay.Phase 2` so night encounter placeholders spawn (or place an `AHomeWorldNightEncounterPlaceholder` in the level). Move the player pawn so it **overlaps** a placeholder; the placeholder calls `ReportFoeConverted(this)` and is destroyed. Same log lines and `ConvertedFoesThisNight` increment; HUD "Converted: N" updates.

**Automated check:** `pie_test_runner.py` includes **"Conversion test (hw.Conversion.Test)"**: it runs `hw.Conversion.Test` via the Editor/PIE console and, when the GameMode is readable from Python, asserts `ConvertedFoesThisNight` incremented by one. Run with PIE active via **MCP** (`execute_python_script("pie_test_runner.py")`) or **Editor: Tools > Execute Python Script**; results in `Saved/pie_test_results.json`. No manual step required for the console path when using the test runner.

---

## 4. Implementation status

- **T1 (twenty-fourth list):** Design doc added (this file). Minimal conversion hook: `ReportFoeConverted(AActor* Foe)` on `AHomeWorldGameMode` logs conversion and increments `ConvertedFoesThisNight`; counter reset when phase leaves Night. Console command `hw.Conversion.Test` invokes the hook for testing. Success: design doc exists and conversion hook is triggerable (log or flag).
- **T1 (twenty-fifth list) — defeat trigger:** Night encounter placeholders are now `AHomeWorldNightEncounterPlaceholder` (C++). On overlap with the player pawn while `GetIsNight()` is true, the placeholder calls `ReportFoeConverted(this)` and destroys itself. All wave, planetoid pack, and boss placeholders use this class. Validation: in PIE, set night (`hw.TimeOfDay.Phase 2`), walk into a spawned placeholder; log shows "Foe converted (strip sin → loved)" and `ConvertedFoesThisNight` increments.
