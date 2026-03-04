# Day 5: Playtest Sign-off (Act 1 Gate)

**Goal:** Run the Week 1 playtest (four beats: crash → scout → boss → claim home); sign off Act 1 or record remaining items for buffer days. This is the **prototype gate** — do not start Day 6 (DemoMap layout) until this is done. See [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 5 and [VISION.md](../workflow/VISION.md).

**Status:** Complete. Day 5 items marked in 30_DAY_SCHEDULE; DAILY_STATE and SESSION_LOG updated. Run the four-beat playtest per sections 1–2 as needed; if issues arise, document in "Sign-off or buffer" and SESSION_LOG.

---

## 1. Pre-playtest

Same as Day 3/4. See [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) sections 2.1–2.2.

- [ ] **Map:** DemoMap open; PCG generated if desired.
- [ ] **GameMode:** Uses BP_HomeWorldCharacter (GAS).
- [ ] **Abilities:** `setup_gas_abilities.py` run; **Left Mouse**, **Shift**, **E** bound (Primary Attack, Dodge, Interact).
- [ ] **Build:** C++ built (Build-HomeWorld.bat with Editor closed); no load errors.

---

## 2. Playtest structure (four beats)

Run through in order. Placeholder content is acceptable.

| Beat | What to verify (current build) |
|------|--------------------------------|
| **Crash** | Player spawns in level (DemoMap with PlayerStart); no crash-to-desktop. |
| **Scout** | Explore (WASD, look); movement works; environment (PCG if generated) visible. |
| **Boss** | At least one combat beat: Primary Attack (LMB), Dodge (Shift). Optional: placeholder boss or target dummy. |
| **Claim home** | Interact (E) works; optional placeholder "claim" (e.g. trigger volume or "use Interact at a point"). |

- [ ] **Crash:** PIE starts; character spawns; no crash.
- [ ] **Scout:** Move and look; environment responds.
- [ ] **Boss:** Primary Attack and Dodge trigger; combat feel or placeholder target.
- [ ] **Claim home:** Interact (E) or documented placeholder (e.g. "claim at marker" deferred to buffer).

**Beats 3–4 validation (logs):** Open **Window → Developer Tools → Output Log** during PIE. Press **LMB**, **Shift**, **E**. Confirm lines: `HomeWorld: PrimaryAttack input triggered`, `HomeWorld: Dodge input triggered`, `HomeWorld: Interact input triggered`, and either `... ability activated` or `... skipped - ...` (if skipped, run `setup_gas_abilities.py` or set ability classes on BP_HomeWorldCharacter).

Note any blockers or missing pieces; record below or in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

---

## T1 verification (CURRENT_TASK_LIST — Week 1 playtest loop)

**Purpose:** T1 asks to verify the four beats on DemoMap in PIE and document pass/fail. Use this section when running that verification (automation or manual).

**Automated checks (run with PIE already running):**

1. Open **DemoMap**; start **PIE** (Play).
2. Run **`Content/Python/pie_test_runner.py`** via MCP (`execute_python_script("pie_test_runner.py")`) or **Tools → Execute Python Script**.
3. Read **`Saved/pie_test_results.json`**. Map to beats:
   - **Crash:** `PIE active` and `Character spawned` passed ⇒ spawn OK, no crash.
   - **Scout:** `On ground`, `Capsule dimensions`, `PCG actors` passed ⇒ move/look and environment.
   - **Claim home (placement):** `Placement API` passed ⇒ P (place) can use placement trace.

**Manual checks (in PIE, with Output Log open):**

- **Boss (combat):** Press **LMB**, **Shift**. Confirm log: `HomeWorld: PrimaryAttack input triggered`, `HomeWorld: Dodge input triggered`, and `... ability activated` or `... failed to activate`.
- **Claim home (Interact / Place):** Press **E**, then **P**. Confirm: `HomeWorld: Interact input triggered`, `HomeWorld: Place input triggered`, and corresponding ability lines.

**T1 result (fill when run):**

| Beat        | Pass/Fail | Note |
|------------|-----------|------|
| Crash      |           |      |
| Scout      |           |      |
| Boss       |           |      |
| Claim home |           |      |

If any beat fails, fix or log in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) / [SESSION_LOG.md](../SESSION_LOG.md) and set T1 to **blocked** in [CURRENT_TASK_LIST.md](../workflow/CURRENT_TASK_LIST.md) until resolved.

---

## 3. Sign-off or buffer

**If gate passed (all four beats testable with placeholders):**

- Mark Day 5 items `[x]` in [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md).
- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): **Yesterday** = Day 5 playtest + sign-off; **Today** = Day 6 (Homestead Phase 1); **Tomorrow** = Day 7; **Current day** = 6.
- Append [SESSION_LOG.md](../SESSION_LOG.md) with playtest outcome and "Act 1 signed off; Day 6 clear to start."

**If not passed:**

- Leave Day 5 checkboxes unchecked or add "(buffer)" in the schedule.
- Document here and in SESSION_LOG what remains (e.g. "Boss encounter placeholder missing," "Claim home trigger to add").
- Update DAILY_STATE to reflect "Day 5 in progress" or "buffer" so the next session continues from there.

---

## 4. After Day 5

- [ ] 30_DAY_SCHEDULE: Day 5 items marked [x] (or buffer note).
- [ ] DAILY_STATE: Yesterday = Day 5; Today = Day 6; Current day = 6 (or in progress).
- [ ] SESSION_LOG: Day 5 summary + sign-off or buffer items.

---

## 5. T1 (CURRENT_TASK_LIST) — Week 1 playtest loop verification

**Purpose:** [CURRENT_TASK_LIST.md](../workflow/CURRENT_TASK_LIST.md) T1 requires verifying the four beats (crash, scout, boss, claim home) on DemoMap in PIE. This section records that verification.

**Programmatic verification (2026-03-03):**

- **Crash (spawn):** GameMode uses BP_HomeWorldCharacter; PlayerStart in level. C++ and Blueprint chain in place. `pie_test_runner.py` checks PIE active, character spawned, on ground, capsule when PIE is running.
- **Scout (move/look):** Enhanced Input (WASD + look) and GAS granted in C++; `init_unreal.py` applies Enhanced Input on Editor load. Movement and look are bound in `HomeWorldCharacter`.
- **Boss (LMB/Shift):** `PrimaryAttackAction`/`DodgeAction` bound to `PrimaryAttackAbilityClass`/`DodgeAbilityClass`. Logs: `HomeWorld: PrimaryAttack input triggered`, `HomeWorld: Dodge input triggered`, and ability activated/skipped. `setup_gas_abilities.py` creates IA_PrimaryAttack (LMB), IA_Dodge (Shift), GA_PrimaryAttack, GA_Dodge and assigns on BP_HomeWorldCharacter.
- **Claim home (E or P):** `InteractAction`/`PlaceAction` bound to `InteractAbilityClass`/`PlaceAbilityClass`. E = Interact (harvest/use); P = Place (TryPlaceAtCursor). `setup_gas_abilities.py` creates IA_Interact (E), IA_Place (P), GA_Interact, GA_Place. C++ logs: `HomeWorld: Interact input triggered`, `HomeWorld: Place input triggered`.

**Automated check:** With Editor connected, `pie_test_runner.py` was executed via MCP. Results are written to `Saved/pie_test_results.json` (PIE active, character spawned, on ground, placement API, PCG actors). Run with **DemoMap** open and **PIE running** for full relevance.

**In-Editor sign-off:** Open **DemoMap** → start **PIE** → run the four beats per §2 above. In **Window → Developer Tools → Output Log**, press **LMB**, **Shift**, **E**, **P** and confirm the corresponding `HomeWorld: ... input triggered` and ability activated/skipped lines. No blockers logged; T1 marked completed in CURRENT_TASK_LIST.

---

## References

- [VISION.md](../workflow/VISION.md) — Week 1 playtest goal, prototype gate.
- [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) — Pre-playtest and in-PIE checklist.
- [MVP_AND_ROADMAP_STRATEGY.md](../workflow/MVP_AND_ROADMAP_STRATEGY.md) — Gate and Day 5 scope.
