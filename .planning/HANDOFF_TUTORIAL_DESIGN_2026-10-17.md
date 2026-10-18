# HANDOFF — HomeWorld Tutorial Design Task List & Research (2026-10-17)

**Created:** 2026-10-17 by Beam (OpenCode plan model), game designer perspective.  
**Purpose:** Single entry point for the tutorial design task list, research plan, and all related artifacts. An agent reading this file can find every document, understand its role, and know what to do next.  
**Scope:** Game design only. No coding, no canon doc changes (except FEEL.md which was already updated in a prior session).  
**Do not modify the 21 in-flight files listed in §6 — they belong to the user's other session.**

---

## 1. How to use this handoff

Read this file first. It maps every artifact created across this session and the prior session, explains how they connect, and lists the pending actions. Then open the specific files you need.

---

## 2. Artifact map (all files, this session + prior)

### 2.1 Tutorial design (this session)

| File | Location | Role | Status |
|------|----------|------|--------|
| Tutorial design ideas | `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | Game designer ideas: 6 design ideas (wisp mark, guided commit, bonk recovery, first mark herb, same stroke, one more thing), 5 gaps, 4 open questions, what NOT to change, next task identified | Complete |
| Tutorial design task list | `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 5 phases: 5 research tasks (R-01 to R-05), 4 interview rounds (I-01 to I-04), 6 design tasks (D-01 to D-06), 2 playtest tasks (P-01, P-02), 4 implementation tasks (I-01 to I-04), 2 validation tasks (V-01, V-02). Critical path documented. | Complete |
| This handoff | `.planning/HANDOFF_TUTORIAL_DESIGN_2026-10-17.md` | Master index for tutorial design work | Complete |

### 2.2 Game design audit & research (prior session)

| File | Location | Role | Status |
|------|----------|------|--------|
| Game design audit + research schedule | `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit (7 strengths, 14 risks), 11 research phases (0–10), all DONE with labeled results R-0-1 to R-10-1, replication procedure, results log | Complete |
| Game design task list | `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized tasks (P0/P1/P2) with owners, actions, acceptance criteria, critical path | Complete |
| Session catalog (game design only) | `.planning/HANDOFF_CATALOG_2026-10-17.md` | Game-design-only handoff; OpenCode content removed | Complete |
| Session handoff (master) | `.planning/HANDOFF_2026-10-17.md` | Master index tying together all artifacts from both sessions | Complete |

### 2.3 Research deliverables (in `.planning/research/`)

| File | Phase | Purpose |
|------|-------|---------|
| `ACCESSIBILITY_CHECKLIST.md` | 6 | P0/P1/P2 accessibility items with HomeWorld-specific notes |
| `AUDIO_DESIGN_BRIEF.md` | 7 | Day/night palette, spatial stealth audio, adaptive music, form-change sting, captions |
| `ONBOARDING_PLAYTEST_PROTOCOL.md` | 1 | 5-tester think-aloud protocol with 12 observed beats + pass criteria |
| `CAMERA_TUNING_BASELINE.md` | 2 | 6 FEEL.md tunables (unmeasured) + motion-sickness mitigation checklist |
| `TELEMETRY_SPEC.md` | 8 | Instrumentation order, custom game events table, save system design, stack recommendation |
| `EA_LAUNCH_CHECKLIST.md` | 5/10 | Pre-launch checklist, scope validation, post-launch items |
| `TUTORIAL_DESIGN_IDEAS.md` | (new) | Game designer ideas for the tutorial (6 ideas, 5 gaps, 4 open questions) |

### 2.4 Interview & decisions

| File | Location | Role |
|------|----------|------|
| Game design research interview | `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | 8 questions (Q1–Q8) with context, limitation, recommendation, options, and filled-in answers. All 8 answered. |

### 2.5 Canon doc changed

| File | Change | Reason |
|------|--------|--------|
| `Docs/canon/FEEL.md` | Island circuit window: ~45–90s → ~12–20s (line 15) | Q1 decision: Reading 2 (window too long). Applied 2026-10-17. |

---

## 3. Key decisions made (interview answers)

| Q | Question | Decision | Applied? |
|---|----------|----------|----------|
| Q1 | Island circuit contradiction (3 readings) | Reading 2 — tighten window to ~12–20s | Yes → `Docs/canon/FEEL.md` |
| Q2 | "Polish" stage rename | Keep "polish" (no change) | N/A |
| Q3 | Onboarding priorities | Approve playtest protocol, schedule first | Protocol created |
| Q4 | Accessibility priorities | P0 for MVP, P1 for EA, P2 deferred | Recorded in `ACCESSIBILITY_CHECKLIST.md` |
| Q5 | Audio direction | Approve brief as starting point, assign owner | Brief created in `AUDIO_DESIGN_BRIEF.md` |
| Q6 | EA scope | Vertical slice for EA (homestead + field + camp + rescue) | Recorded in `EA_LAUNCH_CHECKLIST.md` |
| Q7 | Camera tuning | Measure baselines now, tune after playtest | Baseline doc created |
| Q8 | Confirm/skip all | Answered individually | — |

---

## 4. Tutorial design ideas summary

Full ideas: `.planning/research/TUTORIAL_DESIGN_IDEAS.md`.

**The market hole:** Zelda teaches complex systems through world, silhouette, light — no tutorials. PoE has enormous depth through modifiers — but hostile onboarding. No game does both. HomeWorld's bet: PoE-like depth (7 virtue axes, marks, armor bench, one stroke) taught like Zelda (diegetic, one thing at a time, through play).

**The next task identified:** Design the "first mark" bridge — a low-stakes encounter in the field (after the glide) where the player finds a marked herb, picks it, and places it on the armor bench. This bridges tutorial → first real challenge.

**6 design ideas:**
1. **Tutorial wisp carries a visible (unnamed) mark** — "show, don't tell" teaching.
2. **First armor bench interaction is a "guided commit"** — one mark, one axis, one success.
3. **Bonk teaches failure recoverability** — gentle, recoverable, introduces spirit-sickness.
4. **"First mark" moment** — marked herb in the field after the glide. First real encounter with virtue system.
5. **Teaching through the "same stroke"** — heal, gather, glide, bonk-recovery all use one verb; camp ease adds interference.
6. **"One more thing" pattern** — tutorial ends with a visible-but-non-interactive mark, creating a hook.

**5 gaps identified:** No "first mark" moment; no wisp→mark connection; no failure-recoverability teaching; no camp ease preview; armor bench unlocked but unused.

**4 open questions (taste, for Lead):**
1. Should the tutorial wisp show a mark?
2. Should the armor bench be used in the tutorial?
3. Should the "first mark" herb exist?
4. Should the tutorial end with "one more thing"?

**What I would NOT change:** 5-beat structure, diegetic teaching, bonk-as-failure, unlock-and-discover-later, no-new-verbs rule.

---

## 5. Task list summary

Full task list: `.planning/TASK_LIST_TUTORIAL_DESIGN.md` (5 phases, 23 tasks).

| Phase | Tasks | Owner | Status |
|-------|-------|-------|--------|
| Phase 0 — Research | R-01 to R-05 (5 online research tasks) | research | Not started |
| Phase 1 — Interviews | I-01 to I-04 (4 interview rounds, Lead answers) | interview (Lead) | Not started |
| Phase 2 — Design | D-01 to D-06 (6 design authoring tasks) | design | Not started |
| Phase 3 — Playtest | P-01, P-02 (2 playtest tasks) | human | Not started |
| Phase 4 — Implementation | I-01 to I-04 (4 code/level tasks) | impl | Not started |
| Phase 5 — Validation | V-01, V-02 (2 validation tasks) | human | Not started |

**Critical path:** R-01..R-05 (research) → I-01..I-04 (interviews) → D-01..D-06 (design) → I-01..I-04 (implementation) → P-01/P-02 (playtest) → V-01/V-02 (validation).

**Do not start Phase 2+ without Phase 0 research and Phase 1 interviews.**

---

## 6. In-flight work (NOT mine — do not touch)

21 modified/untracked files belonging to the user's other session:

**18 original in-flight:** `Content/Python/scene_placement.py`, `Docs/CANON_MAP.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, `Docs/VISION_BOARD.md`, `Docs/canon/DECISIONS.md`, `Docs/canon/PLAYTEST.md`, `Docs/context/HOMEWORLD_ROUTE.md`, `PLAY_TASKS.md`, `PRINCIPLE_FIT_LOCK.md`, `SCENE_SETUP.md`, `Docs/handoffs/research/README.md`, `Docs/level/L_SizeTest_CONTEXT.md`, `L_SizeTest_METRICS.md`, `L_SizeTest_ROOM_PLAN.md`, `docs/human-use/taste-profile.md`, `docs/context/OPENING_TUTORIAL_INTERVIEW.md`, `OPENING_TUTORIAL_TASKS.md`, `docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`.

**3 new untracked (opening reveal feature):** `Source/HomeWorld/HomeWorldOpeningReveal.{cpp,h,Tests.cpp}` (plus modified `HomeWorldCharacter.cpp/.h`).

**2 modified binaries:** `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`, `Content/HomeWorld/Meshes/SizeTest/SM_Size_Island.uasset`.

---

## 7. Pending actions for the next agent

1. **Start Phase 0 research** (R-01 to R-05) — online research on Zelda teaching, PoE onboarding, diegetic teaching, failure-as-teaching, "one more thing" pattern. Results go in `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
2. **Open interview rounds 6-9** in `OPENING_TUTORIAL_INTERVIEW.md` (in-flight, user's) — or create new interview rounds. The 4 open questions from TUTORIAL_DESIGN_IDEAS.md §8 need Lead answers.
3. **Do not touch** the 21 in-flight files in §6.
4. **Phase 1 playtest** (from game design audit) remains the highest-leverage action — nothing should be implemented before it.
5. **TRAVERSAL_BUDGET.md update** — ensure it matches the tightened FEEL.md window (~12–20s).
6. **DECISIONS.md entry** — record Q1 decision (Reading 2, window tightened) per canon convention.

---

## 8. Key files reference (tutorial design)

| File | Role |
|------|------|
| `Docs/VISION_BOARD.md` | Product canon (opening tutorial sequence, principles, shape) |
| `docs/context/OPENING_TUTORIAL_TASKS.md` | Work order for tutorial beats 1-5 (in-flight, user's) |
| `docs/context/OPENING_TUTORIAL_INTERVIEW.md` | Interview rounds 1-5 (in-flight, user's) |
| `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | Game designer ideas (6 ideas, 5 gaps, 4 open questions) |
| `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 23 tasks across 5 phases with owners and dependencies |
| `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit + 11 research phases + results |
| `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized game design tasks |
| `.planning/HANDOFF_CATALOG_2026-10-17.md` | Game-design-only catalog (no OpenCode content) |
| `Docs/canon/FEEL.md` | Tunables (island circuit now ~12–20s) |
| `Docs/canon/PILLARS.md` | 5 normative gates |
| `Docs/canon/DESIGN_ETHOS.md` | Borrowed/ours/disputed |
| `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` | 7 virtue axes, spawn, encounters, armor |
| `Docs/context/PRINCIPLE_FIT_LOCK.md` | Parked vs. next build (opening tutorial is next) |

---

## 9. Session metadata

- **Agent:** Beam (OpenCode plan model)
- **Date:** 2026-10-17
- **Scope:** Game designer perspective on the opening tutorial. Investigated the project (canon, GDD, virtue bible, pillars, design ethos, T0 musts, opening tutorial tasks/interview, opening reveal code, polish readiness). Identified the "first mark" bridge as the next task. Created 6 design ideas, 5 gaps, 4 open questions. Created task list (23 tasks, 5 phases) and this handoff.
- **Constraint applied:** No coding, no doc changes (except creating new files). Research and interviews prioritized over implementation. Taste/scope decisions deferred to Lead via interview rounds.
- **Do not:** modify the 21 in-flight files. Do not decide taste, scope, or "done." Do not implement without completing Phase 0 research and Phase 1 interviews. Do not change canon docs without Lead decision recorded in `Docs/canon/DECISIONS.md`.