# SESSION CATALOG — HomeWorld Game Design (2026-10-17)

**Purpose:** Game-design-only handoff for an agent picking up this work. OpenCode/model-rating content has been removed.  
**Created:** 2026-10-17 by Beam (OpenCode plan model).  
**Do not modify existing project files from this document — it is read-only context.**

---

## 0. Repo state at catalog time

- **HEAD:** `804f048c` `chore(tools): add model ratings refresh + /model-for routing` — pushed to `origin/main`.
- **Branch:** `main`.
- **Convention:** `commit_docs: false` (`.planning/STATE.md`). Do not auto-commit.
- **Uncommitted (NOT mine — user's in-flight work):** 21 modified/untracked files (see §5).

---

## 1. Game design audit

Full audit: `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` §3.

**What the game is:** Cozy care-forward 3D action-adventure on UE 5.8 (PC+Steam EA). Day/night form-switching (bed grants spirit form). Care replaces combat. Family stakes (loved one taken at camp). Seven virtue-attribute axes modify encounters. One stroke across all encounters. Authored-hard-form-first. Progression: homestead → field → pine camp → 2nd forest → river → marsh → lair.

**Built vs. designed (honest split):** Logic far ahead of levels. Spirit stealth, spirit-touch table, camp-night strict gate, freedom gate, beast tame, inventory, gather, virtue component, stroke checks, cloud descent, form/day gates all implemented + tested (14 test files, T0 group 19/19). But most `NODE_*` beat actors are not placed in any `.umap`. No playable homestead tutorial map.

**Maps:** `MainMenu`, `EasePad`, `Field`, `SizeTest`, `VS_MVP_Markers`.

**7 strengths:** coherent core fantasy, borrowed-from-best discipline with "leave" columns, one stroke across everything, authored-hard-form-first, process maturity (polish gates, canon map, mutation-tested readiness), scope discipline, diegetic teaching intent.

**14 risks (R1–R14):**
1. No human playtest evidence (G-FEEL RED)
2. World-scale contradiction (island circuit needs 5.6 laps)
3. Onboarding unplayed (5-min tutorial, unplayed)
4. Content breadth thin for Steam EA (1 beast, 1 camp, 6 resources, 3 spirits, 4 zones)
5. Linear progression (camp → 2nd forest → river → marsh → lair)
6. Accessibility unaddressed (no colorblind, remapping, motion-sickness, subtitles, difficulty)
7. Audio unspecified (no audio bible)
8. No telemetry/analytics plan
9. Camera unspecified (6 FEEL tunables are TODO proposals)
10. Virtue onboarding load (7 axes + paradox marks + armor bench)
11. Only one encounter has 4-step ladder (camp ease); others described but not authored
12. Long-horizon hook thematic, not locked
13. Fail-state UX beyond bonk-home unspecified (spirit-sickness stacks untested)
14. Save/recovery design unspecified

---

## 2. Research schedule (all phases DONE)

All 11 phases executed by Beam on 2026-10-17. Full findings in `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` §7.

| Phase | Title | Priority | Status | Key finding | Recommendation |
|-------|-------|----------|--------|-------------|----------------|
| 0 | Resolve now (decisions) | P0 | DONE (decision pending Lead) | Island circuit: 3 readings; Reading 2 (window too long) cheapest/most likely | Park on Lead; recommend Reading 2 |
| 1 | Onboarding & teaching | P1 | DONE | Hands-on/mixed onboarding aligns with Portal/God of War; unplayed is the risk | Adopt + 5-tester playtest; add veteran skip |
| 2 | Camera & movement feel | P1 | DONE | Third-person safer for motion sickness; 6 FEEL tunables unmeasured | Adopt — measure baselines first; add motion-sickness toggles |
| 3 | Day/night loop & pacing | P1 | DONE | Event-gated form change is good; night length + spirit-sickness comprehension untested | Adopt with caution; test spirit-sickness readability |
| 4 | Encounter depth & "one stroke" scalability | P1 | DONE | Hollow Knight charms validate "one stroke + modifiers"; only camp ease has 4-step ladder | Adopt — author step ladders for remaining zones |
| 5 | Progression & content economy | P2 | DONE | "EA launch is your launch"; content thin for EA | Adopt partially — vertical slice + demo; validate depth first |
| 6 | Accessibility | P1 | DONE | XAGs 2026: manual colorblind tweaks > filters; remapping baseline | Adopt — P0 for MVP, P1 for EA, P2 deferred |
| 7 | Audio design | P1 | DONE | No audio bible exists; spatial audio for stealth, adaptive music | Adopt — create audio design brief |
| 8 | Save/telemetry/analytics for EA | P2 | DONE | Instrument in order: session → funnel → attribution | Adopt (P2) — minimal telemetry spec + save design |
| 9 | Art pipeline & blockout discipline | P2 | DONE | S2 art-blockout (Valorant/Icebox) is "the rung never used" | Adopt — formally enforce S2 as gate |
| 10 | Steam EA specifics | P2 | DONE | "EA launch is your launch"; 7000 wishlists; 1000+ reviews = algorithm-blessed | Adopt — vertical slice, near-complete game, demo/Next Fest |

---

## 3. Interview answers (decisions made 2026-10-17)

Full interview: `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md`. All 8 questions answered.

| Q | Decision | Applied? |
|---|----------|----------|
| Q1 (island scale) | Reading 2 — tighten window to ~12–20s | **Yes** — `Docs/canon/FEEL.md` line 15 updated |
| Q2 (polish rename) | Keep "polish" (no change) | N/A (no change needed) |
| Q3 (onboarding) | Approve playtest protocol, schedule first | Protocol created in `.planning/research/ONBOARDING_PLAYTEST_PROTOCOL.md` |
| Q4 (accessibility) | P0 for MVP, P1 for EA, P2 deferred | Recorded in `ACCESSIBILITY_CHECKLIST.md` |
| Q5 (audio) | Approve brief as starting point, assign owner | Brief created in `.planning/research/AUDIO_DESIGN_BRIEF.md` |
| Q6 (EA scope) | Vertical slice for EA (homestead + field + camp + rescue) | Recorded in `EA_LAUNCH_CHECKLIST.md` |
| Q7 (camera tuning) | Measure baselines now, tune after playtest | Baseline doc created in `.planning/research/CAMERA_TUNING_BASELINE.md` |
| Q8 (confirm) | Answered individually | — |

---

## 4. Research deliverables created

All in `.planning/research/`:

| File | Phase | Purpose |
|------|-------|---------|
| `GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | 0–10 | Full audit + research schedule + results log (R-0-1 to R-10-1) |
| `ACCESSIBILITY_CHECKLIST.md` | 6 | P0/P1/P2 accessibility items with HomeWorld-specific notes |
| `AUDIO_DESIGN_BRIEF.md` | 7 | Day/night palette, spatial stealth audio, adaptive music, form-change sting, captions |
| `ONBOARDING_PLAYTEST_PROTOCOL.md` | 1 | 5-tester think-aloud protocol with 12 observed beats + pass criteria |
| `CAMERA_TUNING_BASELINE.md` | 2 | 6 FEEL.md tunables (unmeasured) + motion-sickness mitigation checklist |
| `TELEMETRY_SPEC.md` | 8 | Instrumentation order, custom game events table, save system design, stack recommendation |
| `EA_LAUNCH_CHECKLIST.md` | 5/10 | Pre-launch checklist, scope validation, post-launch |

---

## 5. In-flight work (NOT mine — user's other session)

21 modified/untracked files. Do not touch these.

**18 original in-flight files:**
- `Content/Python/scene_placement.py`
- `Docs/CANON_MAP.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, `Docs/VISION_BOARD.md`
- `Docs/canon/DECISIONS.md`, `Docs/canon/PLAYTEST.md`
- `Docs/context/HOMEWORLD_ROUTE.md`, `PLAY_TASKS.md`, `PRINCIPLE_FIT_LOCK.md`, `SCENE_SETUP.md`
- `Docs/handoffs/research/README.md`
- `Docs/level/L_SizeTest_CONTEXT.md`, `L_SizeTest_METRICS.md`, `L_SizeTest_ROOM_PLAN.md`
- `docs/human-use/taste-profile.md`
- `docs/context/OPENING_TUTORIAL_INTERVIEW.md`, `OPENING_TUTORIAL_TASKS.md`
- `docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`

**3 new untracked (opening reveal feature):**
- `Source/HomeWorld/HomeWorldOpeningReveal.cpp`
- `Source/HomeWorld/HomeWorldOpeningReveal.h`
- `Source/HomeWorld/HomeWorldOpeningRevealTests.cpp`
- (Also modified: `Source/HomeWorld/HomeWorldCharacter.cpp`, `HomeWorldCharacter.h` — wiring)

**2 modified binaries:**
- `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`
- `Content/HomeWorld/Meshes/SizeTest/SM_Size_Island.uasset`

**Context:** The new `HomeWorldOpeningReveal` actor matches the VISION_BOARD opening-tutorial work (2026-10-17). The `.umap`/`.uasset` changes are size-test map work.

---

## 6. Pending actions for the other agent

1. **Phase 1 playtest** is the single highest-leverage next action — nothing should be implemented before it.
2. **Phase 0 island-scale ruling** applied to `Docs/canon/FEEL.md` (window tightened to ~12–20s). Ensure `Docs/qa/TRAVERSAL_BUDGET.md` is updated to match.
3. **Do not touch** the 21 in-flight files in §5 — they belong to the user's other session.
4. Research artifacts in `.planning/research/` are untracked by design (`commit_docs: false`). Commit individually if desired.
5. The other agent should read `Docs/canon/FEEL.md` for the updated island circuit window.

---

## 7. Key files reference (game design)

| File | Role |
|------|------|
| `AGENTS.md` | Lock, build rules, session rules, steer-gate |
| `Docs/VISION_BOARD.md` | Product canon (opening tutorial, principles, shape) |
| `Docs/CANON_MAP.md` | Topic index (441 md files) |
| `Docs/canon/PILLARS.md` | 5 normative gates |
| `Docs/canon/DESIGN_ETHOS.md` | Borrowed/ours/disputed |
| `Docs/canon/FEEL.md` | Tunables (island circuit now ~12–20s) |
| `Docs/canon/PLAYTEST.md` | Playtest log (last known good + played) |
| `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` | 7 virtue axes, spawn, encounters, armor |
| `Docs/01_GDD_MVP.md` | Slice, 8 verbs, 6 resources, out-of-scope |
| `Docs/qa/POLISH_READINESS.md` | Gate state (all RED, by design) |
| `Docs/37_POLISH_PASS_PROCESS.md` | Process + industry sources |
| `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` | 13+4 musts, built vs. unbuilt |
| `Docs/context/PRINCIPLE_FIT_LOCK.md` | Parked vs. next build |
| `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | Interview with all 8 answers filled in |
| `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit + research schedule + results (R-0-1 to R-10-1) |

---

## 8. Session metadata

- **Agent:** Beam (OpenCode plan model)
- **Date:** 2026-10-17
- **Scope:** Game design audit + research schedule (11 phases, all executed). No code changes to game logic. One canon doc edit (`FEEL.md` island circuit window, per Q1 decision). Research artifacts and interview created.
- **Do not:** modify the 21 in-flight files in §5 — they belong to the user's other session.
- **Constraint applied:** steer-gate loaded; taste/scope decisions collected via interview rather than decided by agent. All 8 interview questions answered by user; decisions recorded and applied where safe.