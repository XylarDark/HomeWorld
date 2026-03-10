# MVP: What we have vs. what we need to finalize

**Purpose:** Single evaluation of current state vs. MVP scope so we can prioritize remaining work. **MVP scope** = (1) **MVP tutorial gate** — one-day loop (wake → breakfast → love task → game with child → gather → lunch → dinner → bed → spectral combat → boss → wake to family taken); (2) **Week 1 playtest gate** — crash → scout → boss → claim home; (3) **Vertical slice** — one moment (claim homestead) + one corner (homestead compound) showable; (4) **MVP full scope (Vision-aligned)** per [VISION.md](workflow/VISION.md) § MVP full scope: **packaged build**, **main menu (WBP_MainMenu)**, **full agentic building**, **astral-by-day**, **bed actor**, **in-world meal/love/game triggers**, and everything else in the Vision that applies to the prototype/MVP. The **next 10 task lists** (55–64) focus on this endeavor; see [MVP_FULL_SCOPE_10_LISTS.md](workflow/MVP_FULL_SCOPE_10_LISTS.md). Sources: [VISION.md](workflow/VISION.md), [MVP_TUTORIAL_PLAN.md](workflow/MVP_TUTORIAL_PLAN.md), [MVP_FULL_SCOPE_10_LISTS.md](workflow/MVP_FULL_SCOPE_10_LISTS.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [ACCOMPLISHMENTS_OVERVIEW.md](workflow/ACCOMPLISHMENTS_OVERVIEW.md), [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), [PROJECT_STATE_AND_TASK_LIST.md](workflow/PROJECT_STATE_AND_TASK_LIST.md) §2 Deferred.

**Last updated:** 2026-03-08.

---

## 1. MVP tutorial loop (13 steps) — have vs. need

| Step | Beat | Have | Need to finalize |
|------|------|------|-------------------|
| 1 | Wake up in homestead | Morning state, spawn at start, TimeOfDay morning; console verification. | Optional: bed actor / wake trigger (deferred; **hw.GoToBed** / phase sufficient). |
| 2 | Have breakfast | **hw.Meal.Breakfast** (or ConsumeMealRestore); family-at-table doc; restore/buff hook. | In-game flow: player-triggered meal (optional for MVP; console verification suffices). |
| 3 | One love task with partner | **hw.LoveTask.Complete**; LoveTasksCompletedToday; partner role/tag (FamilySubsystem). | In-game flow: interact with partner NPC (optional; console verification suffices). |
| 4 | Play one game with child | **hw.GameWithChild.Complete**; GamesWithChildToday; child role/tag. | In-game flow: interact with child NPC (optional; console verification suffices). |
| 5 | Collect wood, ore, flowers | Harvest (TryHarvestInFront, GA_Interact); wood verified; ore/flowers stubs or types; **hw.Goods**; Physical on HUD. | Ore/flower harvest in-world if not yet (doc says verify in PIE; placement optional). |
| 6–7 | Lunch, dinner | **hw.Meal.Lunch**, **hw.Meal.Dinner**; time-of-day doc; Restored today. | In-game meal triggers (optional; console suffices). |
| 8 | Go to bed | **hw.GoToBed**; **hw.TimeOfDay.Phase 2** → night; astral ready. | Optional bed actor (deferred); console suffices. |
| 9 | Spectral self — go out | Phase 2 → Night; HUD Phase; **hw.SpiritBurst** / **hw.SpiritShield**; night encounter Wave 1 in log. | Full in-world “go out” moment (optional; stubs + console verification). |
| 10 | Combat with encampment | Night encounter waves (config); HUD Wave; Defend positions; family move to Defend (if State Tree done). | State Tree **Night? / Defend** branch: one-time manual (AUTOMATION_GAPS Gap 2) or GUI automation. |
| 11 | Beat the boss | Key-point boss stub; **hw.GrantBossReward** (Wood). | Boss encounter in-world (placeholder OK per VISION; triggerable via night + key point). |
| 12 | Night ends | **hw.AstralDeath** → dawn + respawn; no death during day. | — |
| 13 | Wake up — family taken | **hw.TutorialEnd** (tutorial complete, inciting incident); Act 1 handoff doc; dawn + spawn. | Optional: objective HUD / “Find your family” (doc or stub). |

**Summary (tutorial):** All 13 steps are **verifiable via console + PIE** (CONSOLE_COMMANDS, MVP_TUTORIAL_PLAN checklist). What’s **not** required for MVP finalization: bed actor, in-world meal/love/game triggers (console is enough), full in-world “spectral go out” moment. What **can** block “MVP finalized”: (1) **State Tree Night?/Defend** still one-time manual (Gap 2) if you want family to move to Defend at night; (2) ensuring **one single-session PIE run** can walk through the full tutorial via console (doc/script exists; run and sign off).

---

## 2. Week 1 playtest (crash → scout → boss → claim home) — have vs. need

| Beat | Have | Need to finalize |
|------|------|-------------------|
| **(1) Crash** | DemoMap/Homestead open; PIE spawns character; pie_test_runner Level + Character. | Sign-off: “crash” = start state documented; no code gap. |
| **(2) Scout** | Move, harvest (E on BP_HarvestableTree); explore loop; optional portal (BP_PortalToPlanetoid, ensure_portal_blueprint). | Portal LevelToOpen: set on Blueprint CDO (ensure_portal_blueprint) or one-time Details (Gap 1). Scout = playable. |
| **(3) Boss** | **hw.TimeOfDay.Phase 2**; key-point boss placeholder / KeyPointBossSpawnDistance; **hw.GrantBossReward**. | Boss encounter triggerable; “reach boss” = night + key point or dungeon entrance. No blocker if placeholder OK. |
| **(4) Claim home** | GA_Place / TryPlaceAtCursor; place (P); building spawns; “claim homestead” moment. | Sign-off: PIE place (P) and confirm; doc in VERTICAL_SLICE_CHECKLIST §3. |

**Summary (Week 1):** All four beats are **implemented and verifiable**. Finalization = **run the Week 1 playtest checklist** (CONSOLE_COMMANDS, PROTOTYPE_SCOPE § Week 1 playtest), document outcome, and optionally capture 1–3 min demo.

---

## 3. Vertical slice (one moment + one corner) — have vs. need

| Item | Have | Need to finalize |
|------|------|-------------------|
| **Moment** | Claim homestead (place first home asset P); verification steps in VERTICAL_SLICE_CHECKLIST §1, §3. | Run pre-demo sequence (§3); confirm moment playable in PIE; optional 1–3 min recording. |
| **Corner** | Homestead compound (DemoMap + placed buildings + resource nodes + PCG); locked in PROTOTYPE_SCOPE. | Pre-demo: Level + PCG + Character + Moment + Corner + Stability (VERTICAL_SLICE_CHECKLIST §3). pie_test_runner covers most; spot-check corner in viewport. |

**Summary (slice):** Moment and corner are **chosen and implemented**. Finalization = **pre-demo run** (open DemoMap → PCG → PIE → pie_test_runner → inspect results + optional stability + optional recording). Fifty-fourth list T6 already ran demo sign-off; slice is demo-ready when PIE is run and corner/moment spot-checked.

---

## 4. MVP full scope (in scope per VISION) and deferred / optional (not required to “finalize MVP”)

| Item | Status | Needed for MVP finalization? |
|------|--------|-------------------------------|
| Full agentic building (family agents build) | Deferred; hw.SimulateBuildOrderActivation observable | No. |
| SaveGame persistence | Implemented (hw.Save / hw.Load) | No. |
| Death-to-spirit (hw.ReportDeath) | Implemented | No. |
| Boss reward (hw.GrantBossReward) | Implemented | No. |
| Astral return on death (night → dawn) | Implemented (hw.AstralDeath) | No. |
| Bed / wake-up trigger | Optional; console suffices | No. |
| State Tree Night?/Defend branch | One-time manual (Gap 2) or GUI automation | Only if you want family to **move to Defend** at night; otherwise “night combat” is playable without it. |
| Portal LevelToOpen (Gap 1) | Blueprint CDO or one-time Details | No for MVP if DemoMap-only; yes if Week 1 “scout” includes planetoid. |
| Packaged build | Run or deferred (doc in KNOWN_ERRORS/AUTOMATION_GAPS) | Optional for “MVP finalized”; required for “ship” or Steam EA. |
| Main menu (WBP_MainMenu) | Gap / create-if-missing | Optional for MVP; needed for “first launch” flow. |

---

## 5. What “finalize MVP” means (recommended)

1. **Tutorial:** Confirm **one full PIE session** can complete the 13-step loop using console commands (and in-world harvest/place where already implemented). Document or run [PIE_TUTORIAL_FLOW.md](tasks/PIE_TUTORIAL_FLOW.md); sign off in MVP_TUTORIAL_PLAN checklist or CONSOLE_COMMANDS.
2. **Week 1 playtest:** Run **crash → scout → boss → claim home** in one session; document outcome (CONSOLE_COMMANDS § Week 1 playtest, PROTOTYPE_SCOPE § Week 1 playtest).
3. **Vertical slice:** Run **pre-demo checklist** (VERTICAL_SLICE_CHECKLIST §3): Level, Character, Moment, Corner, Stability; pie_test_runner + spot-check; optional 1–3 min recording.
4. **Gaps (if blocking):**  
   - **State Tree Defend:** If you want family at Defend at night, do one-time manual (AUTOMATION_GAPS § Gap 2) or run GUI automation once.  
   - **Portal:** If Week 1 “scout” includes planetoid, ensure LevelToOpen set (Blueprint CDO or Details per Gap 1).

**Not required for “MVP finalized”:** Packaged build, main menu, full in-world meal/love/game/bed flows (console verification is enough), full agentic building, astral-by-day.

---

## 7. Suggested next actions (to finalize MVP)

| Priority | Action | Doc / command |
|----------|--------|----------------|
| 1 | Run **single-session PIE tutorial** (13 steps via console + harvest/place); document pass/fail; update MVP_TUTORIAL_PLAN checklist “Playable?” column. | [PIE_TUTORIAL_FLOW.md](tasks/PIE_TUTORIAL_FLOW.md); [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) § Tutorial (List 2–10). |
| 2 | Run **Week 1 playtest** (crash → scout → boss → claim home); document outcome. | [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) § Pre-demo / Week 1; [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Week 1 playtest. |
| 3 | Run **pre-demo checklist** (§3) and optional 1–3 min recording; mark VERTICAL_SLICE_CHECKLIST §3 items done. | [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md) §3. |
| 4 | (Optional) **State Tree Defend:** One-time manual or GUI automation so family moves to Defend at night. | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) § Gap 2; [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md). |
| 5 | (Optional) **Packaged build** run or smoke-test for “ship-ready” beyond MVP. | [NEXT_30_DAY_WINDOW.md](workflow/NEXT_30_DAY_WINDOW.md) § Steam EA prep. |

---

**See also:** [VISION.md](workflow/VISION.md), [MVP_TUTORIAL_PLAN.md](workflow/MVP_TUTORIAL_PLAN.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md), [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md).
