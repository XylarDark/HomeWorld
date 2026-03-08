# MVP full scope: 10 task-list phases (Vision-aligned)

**Purpose:** Focus the **next 10 task lists** (fifty-fifth through sixty-fourth) on implementing the **MVP full scope** as defined in [VISION.md](VISION.md) § MVP full scope (Vision-aligned). Everything in the Vision that applies to the prototype and MVP is to be developed; this plan breaks that into 10 list phases.

**Source:** [VISION.md](VISION.md) § MVP full scope; user directive to include packaged build, main menu (WBP_MainMenu), full agentic building, astral-by-day, bed actor, and in-world meal/love/game triggers in MVP, and to develop everything else from the Vision for MVP.

**Last updated:** 2026-03-08.

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
