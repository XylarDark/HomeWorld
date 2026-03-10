# MVP full scope: 10 task-list phases (Vision-aligned)

**Purpose:** Focus the **next 10 task lists** (fifty-fifth through sixty-fourth) on implementing the **MVP full scope** as defined in [VISION.md](VISION.md) § MVP full scope (Vision-aligned). Everything in the Vision that applies to the prototype and MVP is to be developed; this plan breaks that into 10 list phases.

**Source:** [VISION.md](VISION.md) § MVP full scope; user directive to include packaged build, main menu (WBP_MainMenu), full agentic building, astral-by-day, bed actor, and in-world meal/love/game triggers in MVP, and to develop everything else from the Vision for MVP.

**Last updated:** 2026-03-09.

---

## List 64: MVP full-scope verification (current state and gaps)

**Purpose (T3 sixty-fourth list):** Record current state vs MVP full scope (Lists 55–63) and identify gaps for post–List 64 work. When Editor/MCP is connected, run through MVP checklist (tutorial loop, Week 1 playtest, pre-demo) per [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § List 63 integration and [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3; document outcome in SESSION_LOG or here.

**Verification run this round:** Deferred (Editor/MCP not connected). Current state and gaps are documented below from prior list outcomes and docs.

### Current state vs Lists 55–64

| List | Focus | Current state |
|------|--------|----------------|
| **55** | Packaged build; main menu (WBP_MainMenu) | Packaged build: deferred (run when Editor closed; see KNOWN_ERRORS Package-HomeWorld). Main menu: WBP_MainMenu create/wire and first-launch flow documented; vertical slice §4 fifty-fifth. |
| **56** | Bed actor — go-to-bed and wake in-world | Bed actor (BP_Bed), go-to-bed and wake via interact (E) or overlap; CONSOLE_COMMANDS § Tutorial (List 8)/(List 10); place_bed.py, place_defend_gather_positions. |
| **57** | In-world meal triggers (breakfast/lunch/dinner) | Meal triggers (BP_MealTrigger_Breakfast/Lunch/Dinner), interact or overlap; CONSOLE_COMMANDS § Tutorial (List 3)/(List 7); place_meal_triggers.py. |
| **58** | In-world love task (partner interact) | Partner tag, interact (E) completes one love task; CONSOLE_COMMANDS § Tutorial (List 4); place_partner.py. |
| **59** | In-world game-with-child (child interact) | Child tag, interact (E) completes one game; CONSOLE_COMMANDS § Tutorial (List 5); place_child.py. |
| **60** | Full agentic building | **Path 1:** hw.PlaceWall, hw.CompleteBuildOrder, hw.SimulateBuildOrderActivation — implemented and verifiable. **Path 2 (full agent):** Deferred; State Tree BUILD branch per AGENTIC_BUILDING; no Python/MCP API for full flow (AUTOMATION_GAPS). |
| **61** | Astral-by-day | hw.EnterAstral / hw.AstralByDay (day → Night); return (hw.AstralDeath or F8) restores Day; CONSOLE_COMMANDS § Astral-by-day (List 61). |
| **62** | Defend-at-night | place_defend_gather_positions.py; Family tag; hw.TimeOfDay.Phase 2 → family to DefendPosition, Phase 0/3 → return; hw.Defend.Status; CONSOLE_COMMANDS § Defend-at-night (List 62). |
| **63** | Integration (tutorial + Week 1 playtest + pre-demo) | Run order and checklists in CONSOLE_COMMANDS § List 63 integration; tutorial loop and Week 1 playtest runs deferred (Editor/MCP not connected in recent lists); pre-demo §3 steps 1–8 documented. |
| **64** | Packaged build smoke-test; demo sign-off; MVP full-scope verification; buffer | T1 completed (pre-demo entry point); T2 completed (demo sign-off deferred, reason in VERTICAL_SLICE_CHECKLIST §3); T3 = this verification (doc update). |

### Gaps for post–List 64

- **Packaged build:** Run Package Game (or Package-HomeWorld.bat) when Editor is closed; smoke-test staged exe. Document outcome in SESSION_LOG or KNOWN_ERRORS. See List 55 scope and KNOWN_ERRORS Package-HomeWorld.
- **Full agentic building (Path 2):** Family agent claims and completes build order via State Tree BUILD branch; requires manual or GUI automation for State Tree/Mass (AUTOMATION_GAPS). Do not re-add "verify agentic building" unless implementing or re-verifying (PROJECT_STATE_AND_TASK_LIST §2).
- **Tutorial loop single-session run:** When Editor/MCP available, run [MVP_TUTORIAL_PLAN](MVP_TUTORIAL_PLAN.md) 13 steps in one PIE session; document pass/fail in SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3.
- **Week 1 playtest single-session run:** When Editor/MCP available, run Week 1 playtest checklist (crash → scout → boss → claim home) per CONSOLE_COMMANDS § Pre-demo verification; document in SESSION_LOG or DAY5_PLAYTEST_SIGNOFF § T1.
- **Pre-demo checklist run:** When Editor/MCP available, open DemoMap, PCG generated, start PIE, run pie_test_runner.py, inspect Saved/pie_test_results.json; document in SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3.
- **Next lists:** After List 64, MVP full scope (10 lists) is complete; next lists per [VISION.md](VISION.md) and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Generate next list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md). **Phased path to 100% MVP (asset-ready):** [MVP_100_PHASED_APPROACH.md](MVP_100_PHASED_APPROACH.md).

---

## MVP full scope (from VISION)

- **Packaged build** — Ship-ready packaged build (run or smoke-test).
- **Main menu (WBP_MainMenu)** — Play, Character, Options, Quit; first-launch flow.
- **Full agentic building** — Family agents fulfilling build orders (State Tree/Blueprint flow).
- **Astral-by-day** — Enter the astral during the day (progression unlock or stub).
- **Bed actor** — Bed or wake-up trigger in-world (go-to-bed / wake).
- **In-world meal, love, and game triggers** — Player-triggered breakfast/lunch/dinner, love task with partner, game with child in-world.
- **All other Vision systems** that touch opening, tutorial, day/night, combat, conversion, planetoids, moral system, Act 1.

---

## 10 task-list phases (high-level focus)

| List | Focus (one-line) |
|------|-------------------|
| **55** | Packaged build run or smoke-test; main menu (WBP_MainMenu) create or wire — first-launch flow. |
| **56** | Bed actor — in-world go-to-bed and wake trigger; optional interact. |
| **57** | In-world meal triggers — player-triggered breakfast/lunch/dinner (interact or zone). |
| **58** | In-world love task trigger — player interact with partner to complete one love task. |
| **59** | In-world game-with-child trigger — player interact with child to complete one game. |
| **60** | Full agentic building — State Tree/Blueprint build-order flow (family agents claim and complete). |
| **61** | Astral-by-day — progression unlock or stub (enter astral during day). |
| **62** | State Tree Night?/Defend — family move to Defend at night (manual or automation); conversion/defend polish. |
| **63** | Integration — tutorial + Week 1 playtest single-session run; vertical slice pre-demo. |
| **64** | Packaged build smoke-test; demo sign-off; MVP full-scope verification and buffer. |

---

## List 55 scope (first of 10)

- **Packaged build:** Run Package Game (or project package script); document outcome; if deferred, document in KNOWN_ERRORS/AUTOMATION_GAPS. Optional: smoke-test (launch packaged exe, load map or main menu).
- **Main menu (WBP_MainMenu):** Create or wire WBP_MainMenu in /Game/HomeWorld/UI with Play, Character, Options, Quit; first-launch flow (game starts on MainMenu, Play loads DemoMap or default map). See AUTOMATION_GAPS (WBP_MainMenu create-if-missing); [CHARACTER_GENERATION_AND_CUSTOMIZATION.md](../CHARACTER_GENERATION_AND_CUSTOMIZATION.md).
- **Deliverables:** Packaged build outcome doc; WBP_MainMenu present and wired (or doc + next step); vertical slice §4 fifty-fifth; docs and cycle; verification; buffer.

---

## How to generate each list

- Read this doc for the **list phase** (55–64) and its one-line focus.
- Fill T1–T7 with **implementation** tasks that advance that focus (and Vision-aligned MVP scope).
- T8 = Docs and cycle (combined); T9 = Verification (combined); T10 = Buffer. See [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) § Consolidate overhead.
- After list 64, MVP full scope (Vision-aligned) block is complete; next lists per VISION and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md).

---

**See also:** [VISION.md](VISION.md) § MVP full scope, [MVP_HAVE_VS_NEED.md](../MVP_HAVE_VS_NEED.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
