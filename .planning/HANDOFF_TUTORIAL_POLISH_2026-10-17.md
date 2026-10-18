# HANDOFF — Tutorial Polish Gap Analysis (2026-10-17)

**Created:** 2026-10-17 by Beam (OpenCode plan model), game designer perspective.  
**Purpose:** Single entry point for the tutorial polish gap analysis and all related artifacts.  
**Scope:** Game design only. No coding, no canon doc changes.

**Status after this file was written.** Research notes and interview rounds 6–9 are done. The second end hook is closed. The Love heart, the one bench use, and the marked herb are decided and not built. The next action is still the unplayed walk in `Docs/qa/TUTORIAL_ISLAND_PLAYTEST.md`.

---

## 1. How to use this handoff

Read this file first. It maps every artifact, explains how they connect, and lists pending actions. Then open the specific files you need.

**Do not modify the 21 in-flight files listed in §5 — they belong to the user's other session.**

---

## 2. Artifact map (all files, this session + prior)

### This session

| File | Location | Role | Status |
|------|----------|------|--------|
| Tutorial polish gap analysis | `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md` | Cross-analysis of 14 gaps against 10 polished tutorial requirements. 3-tier gap closure plan. What "done" looks like. | Complete |
| This handoff | `.planning/HANDOFF_TUTORIAL_POLISH_2026-10-17.md` | Master index for tutorial polish work | Complete |

### Prior session (tutorial design)

| File | Location | Role | Status |
|------|----------|------|--------|
| Tutorial design ideas | `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | 6 design ideas, 5 gaps, 4 open questions, what NOT to change | Complete |
| Tutorial design task list | `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 23 tasks across 5 phases (research -> interviews -> design -> playtest -> impl -> validation) | Complete |
| Tutorial design handoff | `.planning/HANDOFF_TUTORIAL_DESIGN_2026-10-17.md` | Master index for tutorial design work | Complete |

### Prior session (game design audit)

| File | Location | Role | Status |
|------|----------|------|--------|
| Game design audit + research | `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit (7 strengths, 14 risks), 11 research phases (all DONE), results R-0-1 to R-10-1 | Complete |
| Game design task list | `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized tasks (P0/P1/P2) | Complete |
| Session catalog | `.planning/HANDOFF_CATALOG_2026-10-17.md` | Game-design-only catalog | Complete |
| Master handoff | `.planning/HANDOFF_2026-10-17.md` | Master index tying all artifacts | Complete |

### Research deliverables (in `.planning/research/`)

| File | Phase | Purpose |
|------|-------|---------|
| `ACCESSIBILITY_CHECKLIST.md` | 6 | P0/P1/P2 accessibility items |
| `AUDIO_DESIGN_BRIEF.md` | 7 | Day/night palette, spatial stealth audio, adaptive music, captions |
| `ONBOARDING_PLAYTEST_PROTOCOL.md` | 1 | 5-tester think-aloud protocol with 12 observed beats |
| `CAMERA_TUNING_BASELINE.md` | 2 | 6 FEEL.md tunables + motion-sickness mitigation |
| `TELEMETRY_SPEC.md` | 8 | Instrumentation order, custom game events, save system design |
| `EA_LAUNCH_CHECKLIST.md` | 5/10 | Pre-launch checklist, scope validation, post-launch |
| `TUTORIAL_DESIGN_IDEAS.md` | (new) | 6 design ideas, 5 gaps, 4 open questions |
| `TUTORIAL_POLISH_GAP_ANALYSIS.md` | (new) | 14 gaps x 10 polished tutorial requirements |

### Interview and canon

| File | Location | Role |
|------|----------|------|
| Game design research interview | `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | 8 questions (Q1-Q8), all answered |
| FEEL.md (canon) | `Docs/canon/FEEL.md` | Island circuit window tightened to ~12-20s (Q1 decision) |

---

## 3. Gap analysis summary

Full analysis: `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md`.

**10 polished tutorial requirements scored:** 1 satisfied (emotional arc), 4 partial (teaching completeness, failure teaching, pacing, visual language), 5 missing (feedback loops, accessibility, audio, transition to game, replayability).

**Prioritized gap closure plan (3 tiers):**

- **Tier 1 (6 items, must have):** First mark moment, guided commit, failure-recoverability teaching, audio design, accessibility P0, "one more thing" hook.
- **Tier 2 (5 items, strongly recommended):** Camp ease preview, "same stroke" teaching map, VFX design, skip for returning players, NPC dialogue system.
- **Tier 3 (4 items, nice to have):** 4-step ladders for other zones, "help" system, HUD design, settings menu design.

**What we have vs. what we need:** 8/12 teaching beats done. 4 more needed (mark, failure recovery, first mark, one more thing). Feedback loops: visual only (need audio, VFX). Accessibility: nothing (need full P0). Audio: nothing (need bible + first assets). Visual language: runes/poles defined (need first mark connection + shoulder spirit light). Transition: glide only (need first mark bridge, camp preview, one more thing). Replayability: nothing (need skip option).

---

## 4. Key decisions made (interview answers)

| Q | Decision | Applied? |
|---|----------|----------|
| Q1 (island scale) | Reading 2 -- tighten window to ~12-20s | Yes -> `Docs/canon/FEEL.md` |
| Q2 (polish rename) | Keep "polish" (no change) | N/A |
| Q3 (onboarding) | Approve playtest protocol, schedule first | Protocol created |
| Q4 (accessibility) | P0 for MVP, P1 for EA, P2 deferred | Recorded in `ACCESSIBILITY_CHECKLIST.md` |
| Q5 (audio) | Approve brief as starting point, assign owner | Brief created in `AUDIO_DESIGN_BRIEF.md` |
| Q6 (EA scope) | Vertical slice for EA | Recorded in `EA_LAUNCH_CHECKLIST.md` |
| Q7 (camera tuning) | Measure baselines now, tune after playtest | Baseline doc created |
| Q8 (confirm) | Answered individually | -- |

---

## 5. In-flight work (NOT mine -- do not touch)

21 modified/untracked files belonging to the user's other session:

- 18 original in-flight: `Content/Python/scene_placement.py`, `Docs/CANON_MAP.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, `Docs/VISION_BOARD.md`, `Docs/canon/DECISIONS.md`, `Docs/canon/PLAYTEST.md`, `Docs/context/HOMEWORLD_ROUTE.md`, `PLAY_TASKS.md`, `PRINCIPLE_FIT_LOCK.md`, `SCENE_SETUP.md`, `Docs/handoffs/research/README.md`, `Docs/level/L_SizeTest_CONTEXT.md`, `L_SizeTest_METRICS.md`, `L_SizeTest_ROOM_PLAN.md`, `docs/human-use/taste-profile.md`, `docs/context/OPENING_TUTORIAL_INTERVIEW.md`, `OPENING_TUTORIAL_TASKS.md`, `docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`.
- 3 new untracked (opening reveal feature): `Source/HomeWorld/HomeWorldOpeningReveal.{cpp,h,Tests.cpp}` (plus modified `HomeWorldCharacter.cpp/.h`).
- 2 modified binaries: `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`, `Content/HomeWorld/Meshes/SizeTest/SM_Size_Island.uasset`.

---

## 6. Pending actions for the next agent

1. **Phase 1 playtest** -- single highest-leverage next action. Nothing should be implemented before it.
2. **TRAVERSAL_BUDGET.md update** -- ensure it matches the tightened FEEL.md window (~12-20s).
3. **DECISIONS.md entry** -- record Q1 decision (Reading 2, window tightened) per canon convention.
4. **Do not touch** the 21 in-flight files in §5.
5. **Research tasks R-01 to R-05** (from TASK_LIST_TUTORIAL_DESIGN.md) -- online research to hone tutorial ideas. Not started.
6. **Interview rounds I-01 to I-04** -- 4 taste questions for the Lead. Not yet opened.
7. **Tier 1 gap closure** (6 items from TUTORIAL_POLISH_GAP_ANALYSIS.md §4) -- first mark moment, guided commit, failure-recoverability, audio, accessibility P0, "one more thing" hook.
8. **Audio brief** needs an owner assigned (Q5 decision).
9. **EA scope** needs Lead/business decision (Q6 decision recorded but not executed).

---

## 7. Key files reference (game design)

| File | Role |
|------|------|
| `AGENTS.md` | Lock, build rules, session rules, steer-gate |
| `Docs/VISION_BOARD.md` | Product canon (opening tutorial, principles, shape) |
| `Docs/CANON_MAP.md` | Topic index (441 md files) |
| `Docs/canon/PILLARS.md` | 5 normative gates |
| `Docs/canon/DESIGN_ETHOS.md` | Borrowed/ours/disputed |
| `Docs/canon/FEEL.md` | Tunables (island circuit now ~12-20s) |
| `Docs/canon/PLAYTEST.md` | Playtest log |
| `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` | 7 virtue axes, spawn, encounters, armor |
| `Docs/01_GDD_MVP.md` | Slice, 8 verbs, 6 resources, out-of-scope |
| `Docs/qa/POLISH_READINESS.md` | Gate state (all RED, by design) |
| `Docs/37_POLISH_PASS_PROCESS.md` | Process + industry sources |
| `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` | 13+4 musts, built vs. unbuilt |
| `Docs/context/PRINCIPLE_FIT_LOCK.md` | Parked vs. next build |
| `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | Interview with all 8 answers filled in |
| `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit + research schedule + results |
| `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized game design tasks |
| `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | 6 design ideas, 5 gaps, 4 open questions |
| `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 23 tasks across 5 phases |
| `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md` | 14 gaps x 10 polished tutorial requirements |
| `.planning/research/` | 7 research deliverables (accessibility, audio, onboarding, camera, telemetry, EA, tutorial) |

---

## 8. Session metadata

- **Agent:** Beam (OpenCode plan model)
- **Date:** 2026-10-17
- **Scope:** Game designer perspective. Investigated the project, identified the "first mark" bridge as the next task, created 6 design ideas, 5 gaps, 4 open questions, task list (23 tasks, 5 phases), polish gap analysis (14 gaps x 10 requirements), and this handoff.
- **Constraint applied:** No coding, no doc changes (except creating new files). Research and interviews prioritized over implementation. Taste/scope decisions deferred to Lead via interview rounds. Steer-gate loaded.
- **Do not:** modify the 21 in-flight files. Do not decide taste, scope, or "done." Do not implement without completing Phase 0 research and Phase 1 interviews. Do not change canon docs without Lead decision recorded in `Docs/canon/DECISIONS.md`.