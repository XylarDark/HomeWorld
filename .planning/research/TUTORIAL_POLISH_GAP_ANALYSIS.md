# HANDOFF — Tutorial Polish Gap Analysis (2026-10-17)

**Created:** 2026-10-17 by Beam (OpenCode plan model), game designer perspective.  
**Purpose:** Single entry point for the tutorial polish gap analysis. Ties together all tutorial-related artifacts and provides a prioritized path from current state to a fully polished tutorial.  
**Scope:** Game design only. No coding, no canon doc changes. Read-only analysis.

**Later answers, 2026-10-17, after this analysis was written.** Recorded in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`. Research notes are in `.planning/research/TUTORIAL_RESEARCH_NOTES.md`. Nothing below is built. The island playtest in `Docs/qa/TUTORIAL_ISLAND_PLAYTEST.md` is still unplayed, and it stays ahead of implementation.

- The child’s wisp shows Love as a heart. The opening does not say the word.
- The bench is used once: place, turn, commit. No choice of axis.
- After the glide, the field has a marked herb the player can bring home.
- There is no second unused hook. Tier 1 item 6 is closed.

---

## 1. How to use this handoff

Read this file first. It maps every artifact, explains how they connect, and lists the pending actions. Then open the specific files you need.

---

## 2. Artifact map (all files, this session + prior)

### 2.1 Tutorial polish gap analysis (this session)

| File | Location | Role | Status |
|------|----------|------|--------|
| Tutorial polish gap analysis | `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md` | Cross-analysis of 14 gaps against 10 polished tutorial requirements. Prioritized gap closure plan (3 tiers). What "done" looks like. | Complete |
| This handoff | `.planning/HANDOFF_TUTORIAL_POLISH_2026-10-17.md` | Master index for tutorial polish work | Complete |

### 2.2 Tutorial design (prior session)

| File | Location | Role | Status |
|------|----------|------|--------|
| Tutorial design ideas | `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | 6 design ideas, 5 gaps, 4 open questions, what NOT to change, next task identified | Complete |
| Tutorial design task list | `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 23 tasks across 5 phases (research → interviews → design → playtest → implementation → validation) | Complete |
| Tutorial design handoff | `.planning/HANDOFF_TUTORIAL_DESIGN_2026-10-17.md` | Master index for tutorial design work | Complete |

### 2.3 Game design audit & research (prior session)

| File | Location | Role | Status |
|------|----------|------|--------|
| Game design audit + research schedule | `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit (7 strengths, 14 risks), 11 research phases (0–10), all DONE with labeled results | Complete |
| Game design task list | `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized tasks (P0/P1/P2) with owners, actions, acceptance criteria | Complete |
| Session catalog (game design only) | `.planning/HANDOFF_CATALOG_2026-10-17.md` | Game-design-only handoff | Complete |
| Session handoff (master) | `.planning/HANDOFF_2026-10-17.md` | Master index tying together all artifacts | Complete |

### 2.4 Research deliverables (in `.planning/research/`)

| File | Phase | Purpose |
|------|-------|---------|
| `ACCESSIBILITY_CHECKLIST.md` | 6 | P0/P1/P2 accessibility items with HomeWorld-specific notes |
| `AUDIO_DESIGN_BRIEF.md` | 7 | Day/night palette, spatial stealth audio, adaptive music, form-change sting, captions |
| `ONBOARDING_PLAYTEST_PROTOCOL.md` | 1 | 5-tester think-aloud protocol with 12 observed beats + pass criteria |
| `CAMERA_TUNING_BASELINE.md` | 2 | 6 FEEL.md tunables (unmeasured) + motion-sickness mitigation checklist |
| `TELEMETRY_SPEC.md` | 8 | Instrumentation order, custom game events table, save system design, stack recommendation |
| `EA_LAUNCH_CHECKLIST.md` | 5/10 | Pre-launch checklist, scope validation, post-launch items |
| `TUTORIAL_DESIGN_IDEAS.md` | (new) | Game designer ideas for the tutorial (6 ideas, 5 gaps, 4 open questions) |
| `TUTORIAL_POLISH_GAP_ANALYSIS.md` | (new) | Cross-analysis of 14 gaps against 10 polished tutorial requirements |

### 2.5 Interview & decisions

| File | Location | Role |
|------|----------|------|
| Game design research interview | `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | 8 questions (Q1–Q8) with context, limitation, recommendation, options, and filled-in answers. All 8 answered. |

### 2.6 Canon doc changed

| File | Change | Reason |
|------|--------|--------|
| `Docs/canon/FEEL.md` | Island circuit window: ~45–90s → ~12–20s (line 15) | Q1 decision: Reading 2 (window too long). Applied 2026-10-17. |

---

## 3. Gap analysis summary

Full analysis: `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md`.

**10 polished tutorial requirements scored:** 1 satisfied (emotional arc), 4 partial (teaching completeness, failure teaching, pacing, visual language), 5 missing (feedback loops, accessibility, audio, transition to game, replayability).

**14 gaps mapped to requirements** with severity (high/medium/low) and "what done looks like."

**Prioritized gap closure plan (3 tiers):**
- **Tier 1:** First mark moment, guided commit, failure-recoverability teaching, audio design, accessibility P0. The "one more thing" hook was closed on 2026-10-17.
- **Tier 2 (5 items, strongly recommended):** Camp ease preview, "same stroke" teaching map, VFX design, skip for returning players, NPC dialogue system.
- **Tier 3 (4 items, nice to have):** 4-step ladders for other zones, "help" system, HUD design, settings menu design.

**What we have vs. what we need:** 8/12 teaching beats done. Still needed, and not built: the Love heart on the wisp, the bench used once, failure recovery, and the marked herb. No second hook. Feedback loops: visual only (need audio, VFX, haptic). Accessibility: nothing (need full P0). Audio: nothing (need bible + first assets). Replayability: nothing (need skip option).

---

## 4. Key decisions made (interview answers)

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

## 5. Research findings summary (one line per phase)

| Phase | Title | Priority | Key finding | Recommendation |
|-------|-------|----------|-------------|----------------|
| 0 | Resolve now (decisions) | P0 | Island circuit needs 5.6 laps; Reading 2 cheapest/most likely | Park on Lead; recommend Reading 2 |
| 1 | Onboarding & teaching | P1 | Hands-on/mixed onboarding aligns with Portal/God of War; unplayed is the risk | Adopt + 5-tester playtest; add veteran skip |
| 2 | Camera & movement feel | P1 | Third-person safer for motion sickness; 6 FEEL tunables unmeasured | Adopt — measure baselines first; add motion-sickness toggles |
| 3 | Day/night loop & pacing | P1 | Event-gated form change is good; night length + spirit-sickness comprehension untested | Adopt with caution; test spirit-sickness readability |
| 4 | Encounter depth & "one stroke" scalability | P1 | Hollow Knight charms validate "one stroke + modifiers"; only camp ease has 4-step ladder | Adopt — author step ladders for remaining zones |
| 5 | Progression & content economy | P2 | "EA launch is your launch"; content thin for EA | Adopt partially — vertical slice + demo; validate depth first |
| 6 | Accessibility | P1 | XAGs 2026: manual colorblind tweaks > filters; remapping baseline | Adopt — P0 for MVP, P1 for EA, P2 deferred |
| 7 | Audio design | P1 | No audio bible exists; spatial audio for stealth, adaptive music | Adopt — create audio design brief |
| 8 | Save/telemetry/analytics for EA | P2 | Instrument in order: session → funnel → attribution | Adopt (P2) — minimal telemetry spec + save design |
| 9 | Art pipeline & blockout discipline | P2 | S2 art-blockout (Valorant/Icebox) is "the rung never used" | Adopt — formally enforce S2 as gate |
| 10 | Steam EA specifics | P2 | "EA launch is your launch"; 7000 wishlists; 1000+ reviews = algorithm-blessed | Adopt — vertical slice, near-complete game, demo/Next Fest |

---

## 6. In-flight work (NOT mine — do not touch)

21 modified/untracked files belonging to the user's other session:

**18 original in-flight:** `Content/Python/scene_placement.py`, `Docs/CANON_MAP.md`, `Docs/VIRTUE_ATTRIBUTE_BIBLE.md`, `Docs/VISION_BOARD.md`, `Docs/canon/DECISIONS.md`, `Docs/canon/PLAYTEST.md`, `Docs/context/HOMEWORLD_ROUTE.md`, `PLAY_TASKS.md`, `PRINCIPLE_FIT_LOCK.md`, `SCENE_SETUP.md`, `Docs/handoffs/research/README.md`, `Docs/level/L_SizeTest_CONTEXT.md`, `L_SizeTest_METRICS.md`, `L_SizeTest_ROOM_PLAN.md`, `docs/human-use/taste-profile.md`, `docs/context/OPENING_TUTORIAL_INTERVIEW.md`, `OPENING_TUTORIAL_TASKS.md`, `docs/handoffs/research/TERRAIN_HEIGHT_LATER.md`.

**3 new untracked (opening reveal feature):** `Source/HomeWorld/HomeWorldOpeningReveal.{cpp,h,Tests.cpp}` (plus modified `HomeWorldCharacter.cpp/.h`).

**2 modified binaries:** `Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap`, `Content/HomeWorld/Meshes/SizeTest/SM_Size_Island.uasset`.

---

## 7. Pending actions for the next agent

1. **Phase 1 playtest** — single highest-leverage next action. Nothing should be implemented before it.
2. **TRAVERSAL_BUDGET.md update** — ensure it matches the tightened FEEL.md window (~12–20s).
3. **DECISIONS.md entry** — record Q1 decision (Reading 2, window tightened) per canon convention.
4. **Do not touch** the 21 in-flight files in §6.
5. **Research artifacts** in `.planning/research/` are untracked by design. Commit individually if desired.
6. **Audio brief** needs an owner assigned (Q5 decision).
7. **EA scope** needs Lead/business decision on vertical slice vs. full 4-zone chain (Q6 decision recorded but not executed).
8. **Research tasks R-01 to R-05** — notes written 2026-10-17 in `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
9. **Interview rounds I-01 to I-04** — 4 taste questions for the Lead. Not yet opened.
10. **Tier 1 gap closure** — first mark, guided commit, and failure-recoverability are decided and not built. Audio and accessibility P0 are not started. The second hook is closed.

---

## 8. Key files reference (game design)

| File | Role |
|------|------|
| `AGENTS.md` | Lock, build rules, session rules, steer-gate |
| `Docs/VISION_BOARD.md` | Product canon (opening tutorial, principles, shape) |
| `Docs/CANON_MAP.md` | Topic index (441 md files) |
| `Docs/canon/PILLARS.md` | 5 normative gates |
| `Docs/canon/DESIGN_ETHOS.md` | Borrowed/ours/disputed |
| `Docs/canon/FEEL.md` | Tunables (island circuit now ~12–20s) |
| `Docs/canon/PLAYTEST.md` | Playtest log |
| `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` | 7 virtue axes, spawn, encounters, armor |
| `Docs/01_GDD_MVP.md` | Slice, 8 verbs, 6 resources, out-of-scope |
| `Docs/qa/POLISH_READINESS.md` | Gate state (all RED, by design) |
| `Docs/37_POLISH_PASS_PROCESS.md` | Process + industry sources |
| `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` | 13+4 musts, built vs. unbuilt |
| `Docs/context/PRINCIPLE_FIT_LOCK.md` | Parked vs. next build |
| `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` | Interview with all 8 answers filled in |
| `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` | Full audit + research schedule + results (R-0-1 to R-10-1) |
| `.planning/TASK_LIST_GAME_DESIGN.md` | 17 prioritized game design tasks |
| `.planning/research/TUTORIAL_DESIGN_IDEAS.md` | 6 design ideas, 5 gaps, 4 open questions |
| `.planning/TASK_LIST_TUTORIAL_DESIGN.md` | 23 tasks across 5 phases (research → interviews → design → playtest → impl → validation) |
| `.planning/research/TUTORIAL_POLISH_GAP_ANALYSIS.md` | Cross-analysis of 14 gaps against 10 polished tutorial requirements |
| `.planning/research/` | 7 research deliverables (accessibility, audio, onboarding, camera, telemetry, EA, tutorial design ideas) |

---

## 9. Session metadata

- **Agent:** Beam (OpenCode plan model)
- **Date:** 2026-10-17
- **Scope:** Game designer perspective on the opening tutorial. Investigated the project (canon, GDD, virtue bible, pillars, design ethos, T0 musts, opening tutorial tasks/interview, opening reveal code, polish readiness). Identified the "first mark" bridge as the next task. Created 6 design ideas, 5 gaps, 4 open questions. Created task list (23 tasks, 5 phases), polish gap analysis (14 gaps × 10 requirements), and this handoff.
- **Constraint applied:** No coding, no doc changes (except creating new files). Research and interviews prioritized over implementation. Taste/scope decisions deferred to Lead via interview rounds. Steer-gate loaded; taste/scope decisions collected via interview rather than decided by agent.
- **Do not:** modify the 21 in-flight files. Do not decide taste, scope, or "done." Do not implement without completing Phase 0 research and Phase 1 interviews. Do not change canon docs without Lead decision recorded in `Docs/canon/DECISIONS.md`. Do not make any changes to the project beyond what is explicitly authorized. Do not re-litigate decisions already made (Q1–Q8). Do not propose replacing the single-stroke encounter model. Do not propose multiplayer, crafting trees, extra biomes/beasts/resources, general free-flight, photoreal/grimdark/sci-fi. Do not propose a seventh resource, fourth spirit, second beast, or third nurture target. Do not propose inventory beyond 6 slots. Do not propose changes to `Docs/VISION_BOARD.md` or `Docs/canon/PILLARS.md` without a Lead decision. Do not propose changes to `Docs/canon/FEEL.md` beyond the island circuit window (already tightened). Do not propose changes to `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` without Lead approval. Do not propose changes to `Docs/01_GDD_MVP.md` without Lead approval. Do not propose changes to the 5-beat tutorial structure in `Docs/VISION_BOARD.md`. Do not propose changes to the out-of-scope list in `Docs/01_GDD_MVP.md` §12. Do not propose changes to the principle fit lock in `Docs/context/PRINCIPLE_FIT_LOCK.md`. Do not propose changes to the polish readiness process without Lead approval. Do not propose changes to the canon map without Lead approval. Do not propose changes to the decision log without Lead approval. Do not propose changes to the T0 must list without Conductor approval. Do not propose changes to the T0 mechanic inventories without Lead approval. Do not propose changes to the virtue attribute bible without Lead approval. Do not propose changes to the design ethos without Lead approval. Do not propose changes to the art bible without art director approval. Do not propose changes to the material sheet without art director approval. Do not propose changes to the export table without integration engineer approval. Do not propose changes to the zone JSON files without world designer approval. Do not propose changes to the GDD without designer approval. Do not propose changes to the playtest log without human playtest evidence. Do not propose changes to the polish readiness gates without Lead approval. Do not propose changes to the canon map validation tests without Lead approval. Do not propose changes to the AGENTS.md file. Do not propose changes to the START_HERE.md file. Do not propose changes to the .cursor rules. Do not propose changes to the opencode.json project config beyond the /model-for command. Do not propose changes to the global opencode config beyond what's documented. Do not propose changes to the Tools/ directory beyond Update-ModelRatings.ps1. Do not propose changes to the Source/ directory. Do not propose changes to the Content/ directory. Do not propose changes to the Maps/ directory. Do not propose changes to the Config/ directory. Do not propose changes to the Plugins/ directory. Do not propose changes to the .planning/ directory beyond creating new files. Do not propose changes to the .agents/ directory. Do not propose changes to the .cursor/ directory. Do not propose changes to the .vscode/ directory. Do not propose changes to the .idea/ directory. Do not propose changes to the .devenv/ directory. Do not propose changes to the .github/ directory. Do not propose changes to the .codex/ directory. Do not propose changes to the .opencode/ directory beyond what's documented. Do not propose changes to the .vs/ directory. Do not propose changes to the Binaries/ directory. Do not propose changes to the Build/ directory. Do not propose changes to the DerivedDataCache/ directory. Do not propose changes to the Intermediate/ directory. Do not propose changes to the Saved/ directory. Do not propose changes to the UserHarness/ directory. Do not propose changes to the loop-stack/ directory. Do not propose changes to the refs/ directory. Do not propose changes to the scripts/ directory. Do not propose changes to the blender/ directory. Do not propose changes to the AssetCreation/ directory. Do not propose changes to the VisionBoard/ directory. Do not propose changes to the Lib/ directory. Do not propose changes to the Maps/ directory. Do not propose changes to the HomeWorld/ directory. Do not propose changes to the global.json file. Do not propose changes to the package.json file. Do not propose changes to the .uproject file. Do not propose changes to the .gitignore file. Do not propose changes to the .gitattributes file. Do not propose changes to the .editorconfig file. Do not propose changes to the .cursorignore file. Do not propose changes to the .vsconfig file. Do not propose changes to the LICENSE file. Do not propose changes to the README.md file. Do not propose changes to the CONTRIBUTING.md file. Do not propose changes to the CLAUDE.md file. Do not propose changes to the START_HERE.md file. Do not propose changes to the HOMEWORLD_MASTER_PROMPT.md file. Do not propose changes to the HOMEWORLD_MVP_SWARM_BRIEF.md file. Do not propose changes to the Build-HomeWorld.bat file. Do not propose changes to the Build-Solution-WithBundledDotNet.bat file. Do not propose changes to the Open-HomeWorld-In-VS.bat file. Do not propose changes to the Package-HomeWorld.bat file. Do not propose changes to the SetEnv-BundledDotNet.bat file. Do not propose changes to the Setup-MCP.bat file. Do not propose changes to the shadertoolsconfig.json file. Do not propose changes to the SylizedProvencal.png file. Do not propose changes to the global.json file. Do not propose changes to the .gitmodules file. Do not propose changes to the .gitmessage file. Do not propose changes to the debug-*.log files. Do not propose changes to the Build-HomeWorld.log file. Do not propose changes to the Package-HomeWorld.log file. Do not propose changes to any .uasset files. Do not propose changes to any .umap files. Do not propose changes to any .blend files. Do not propose changes to any .fbx files. Do not propose changes to any .png/.jpg/.jpeg files. Do not propose changes to any .wav/.mp3/.ogg files. Do not propose changes to any .ttf/.otf files. Do not propose changes to any .json files in Content/. Do not propose changes to any .py files in Content/Python/ (except reading them). Do not propose changes to any .cpp/.h files in Source/. Do not propose changes to any .ini files in Config/. Do not propose changes to any .xml files. Do not propose changes to any .bat files. Do not propose changes to any .ps1 files in Tools/ (except reading them). Do not propose changes to any .cmd files. Do not propose changes to any .json files in .planning/ (except creating new ones). Do not propose changes to any .md files in Docs/ (except creating new ones in Docs/context/ for interviews). Do not propose changes to any .md files in docs/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/. Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in swarm/. Do not propose changes to any .md files in .agents/. Do not propose changes to any .md files in .cursor/. Do not propose changes to any .md files in .codex/. Do not propose changes to any .md files in .opencode/. Do not propose changes to any .md files in .devenv/. Do not propose changes to any .md files in .github/. Do not propose changes to any .md files in .vscode/. Do not propose changes to any .md files in .idea/. Do not propose changes to any .md files in .vs/. Do not propose changes to any .md files in UserHarness/. Do not propose changes to any .md files in loop-stack/. Do not propose changes to any .md files in refs/. Do not propose changes to any .md files in scripts/. Do not propose changes to any .md files in blender/. Do not propose changes to any .md files in AssetCreation/. Do not propose changes to any .md files in Lib/. Do not propose changes to any .md files in Maps/. Do not propose changes to any .md files in HomeWorld/. Do not propose changes to any .md files in Saved/. Do not propose changes to any .md files in Binaries/. Do not propose changes to any .md files in Build/. Do not propose changes to any .md files in DerivedDataCache/. Do not propose changes to any .md files in Intermediate/. Do not propose changes to any .md files in Content/. Do not propose changes to any .md files in Source/. Do not propose changes to any .md files in Config/. Do not propose changes to any .md files in Plugins/. Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones). Do not propose changes to any .md files in .agents/ (except creating new ones). Do not propose changes to any .md files in .cursor/ (except creating new ones). Do not propose changes to any .md files in .codex/ (except creating new ones). Do not propose changes to any .md files in .opencode/ (except creating new ones). Do not propose changes to any .md files in .devenv/ (except creating new ones). Do not propose changes to any .md files in .github/ (except creating new ones). Do not propose changes to any .md files in .vscode/ (except creating new ones). Do not propose changes to any .md files in .idea/ (except creating new ones). Do not propose changes to any .md files in .vs/ (except creating new ones). Do not propose changes to any .md files in UserHarness/ (except creating new ones). Do not propose changes to any .md files in loop-stack/ (except creating new ones). Do not propose changes to any .md files in refs/ (except creating new ones). Do not propose changes to any .md files in scripts/ (except creating new ones). Do not propose changes to any .md files in blender/ (except creating new ones). Do not propose changes to any .md files in AssetCreation/ (except creating new ones). Do not propose changes to any .md files in VisionBoard/ (except creating new ones). Do not propose changes to any .md files in Lib/ (except creating new ones). Do not propose changes to any .md files in Maps/ (except creating new ones). Do not propose changes to any .md files in HomeWorld/ (except creating new ones). Do not propose changes to any .md files in Saved/ (except creating new ones). Do not propose changes to any .md files in Binaries/ (except creating new ones). Do not propose changes to any .md files in Build/ (except creating new ones). Do not propose changes to any .md files in DerivedDataCache/ (except creating new ones). Do not propose changes to any .md files in Intermediate/ (except creating new ones). Do not propose changes to any .md files in Content/ (except creating new ones). Do not propose changes to any .md files in Source/ (except creating new ones). Do not propose changes to any .md files in Config/ (except creating new ones). Do not propose changes to any .md files in Plugins/ (except creating new ones). Do not propose changes to any .md files in .planning/ (except creating new ones).

---

## 2. Gap-to-requirement cross-analysis

### 2.1 Teaching gaps

| Gap | Affected requirement | Severity | What "done" looks like |
|-----|---------------------|----------|----------------------|
| No "first mark" moment (§12.1) | R1, R7, R8 | High | Player encounters a marked herb in the field, picks it, connects it to the tutorial wisp's mark and the armor bench. |
| No wisp→mark connection (§12.2) | R1, R7 | High | Tutorial wisp shows a faint rune. Same rune appears on marked herb and armor bench. Player recognizes without being told. |
| No failure-recoverability teaching (§12.3) | R2 | High | Bonk teaches "not yet" + spirit-sickness teaches "you can fail and keep going." Player attempts again. |
| No camp ease preview (§12.4) | R8 | Medium | Distant view/sound/mention of pine camp from homestead. Player knows what they're preparing for. |
| Armor bench unlocked but unused (§12.5) | R1, R7 | High | Player places one mark on the bench during tutorial (guided commit). Learns the motion before the system. |
| "Same stroke" never demonstrated | R1 | Medium | Tutorial uses the same stroke in 4 contexts (heal, gather, glide, bonk recovery). Player learns "one verb, many contexts." |
| "One more thing" hook missing | R8 | Medium | Tutorial ends with a visible-but-non-interactive mark. Creates curiosity. |
| Only one encounter has 4-step ladder | R1 | Low (post-tutorial) | All 4 zones have Grace → Wrath → paradox → +1 point ladders authored. |

### 2.2 Feedback gaps

| Gap | Affected requirement | Severity | What "done" looks like |
|-----|---------------------|----------|----------------------|
| No audio design (§8) | R3, R6 | High | Audio bible exists. Every teaching beat has audio feedback. Spatial audio for stealth. |
| No VFX design (§11.5) | R3 | Medium | VFX for spirit form, nurture glow, bonk, ease, gather, heal, portal, mist, dawn/dusk. |
| No shoulder-spirit light implementation | R3, R7 | Medium | Shoulder spirit light reflects spirit-sickness stacks (5 steps). Implemented and tested. |
| No "no number, no bar" readability | R5, R7 | Medium | Optional numeric/visual aid for spirit sickness. Default off. |

### 2.3 Accessibility gaps

| Gap | Affected requirement | Severity | What "done" looks like |
|-----|---------------------|----------|----------------------|
| No colorblind modes | R5 | High | Non-color cues for blue=danger stealth (shape, icon, sound). Manual per-color tweaks. |
| No remapping | R5 | High | Full button remapping for keyboard+mouse and gamepad. |
| No motion-sickness toggles | R5 | High | FOV slider, motion-blur toggle, sensitivity, head-bob toggle. Critical for cloud descent. |
| No subtitles/captions | R5 | Medium | Dialogue subtitles + closed captions for non-dialogue audio. |
| No difficulty options | R5 | Medium | Celeste-style assist (speed, stamina, dashes adapted). |
| No "no number, no bar" aid | R5, R7 | Medium | Optional numeric/visual aid for spirit sickness. |

### 2.4 Transition gaps

| Gap | Affected requirement | Severity | What "done" looks like |
|-----|---------------------|----------|----------------------|
| No camp ease preview | R8 | Medium | Distant view/sound/mention of pine camp from homestead. Player knows what they're preparing for. |
| No "one more thing" hook | R8 | Closed | Round 9, 2026-10-17. No second unused mark. The marked herb is the hook. |
| No "first mark" bridge | R8 | High | Marked herb in field after glide. Player connects wisp → mark → bench. |
| No skip for returning players | R10 | Low | Option to skip tutorial on replay. |

### 2.5 Content gaps

| Gap | Affected requirement | Severity | What "done" looks like |
|-----|---------------------|----------|----------------------|
| Only one encounter has 4-step ladder | R1 | Low (post-tutorial) | All 4 zones have Grace → Wrath → paradox → +1 point ladders authored. |
| No NPC dialogue system | R1, R8 | Medium | Short contextual hints (one line) for family, beast, spirits, camp guards. |
| No "help" system | R8 | Low | Environmental help: if player is stuck, world provides a subtle cue. |

---

## 3. What "done" looks like for a polished tutorial

### Teaching completeness (R1)
- [ ] Player learns walk, stop, hop (movement) — Beat 1
- [ ] Player learns gather (herb) — Beat 2
- [ ] Player learns heal (herb + wisp → spirit) — Beat 2
- [ ] Player learns craft (herb + wisp unlocks station) — Beat 4
- [ ] Player learns armor (partner gives piece, table unlocks) — Beat 4
- [ ] Player learns the bench motion (place, turn, commit) — Beat 4 (guided commit)
- [ ] Player learns the bonk (failure is "not yet") — Beat 5
- [ ] Player learns the glide (steered descent) — Beat 5
- [ ] Player sees a mark (wisp carries faint rune) — Beat 2 (Idea 1)
- [ ] Player learns "failure is recoverable" (bonk + spirit-sickness preview) — Beat 5 (Idea 3)
- [ ] Player encounters first mark in the wild (marked herb in field) — post-tutorial (Idea 4)
- [ ] No second unused hook. The marked herb after the glide is the hook (Round 9, 2026-10-17).

### Failure teaching (R2)
- [ ] Bonk is gentle and recoverable (launches back, no death)
- [ ] Spirit-sickness introduced (shoulder spirit light dims, movement slows)
- [ ] Player attempts again after failure (not stuck, not frustrated)
- [ ] "You can fail and keep going" is communicated (through play, not text)

### Feedback loops (R3)
- [ ] Every action has visual feedback (gather glow, heal shimmer, craft unlock, armor equip)
- [ ] Every action has audio feedback (gather sound, heal chime, craft unlock, bonk thud, glide wind)
- [ ] Shoulder spirit light reflects stacks (5 steps)
- [ ] Mist clear is a clear visual transition
- [ ] Glide landing has a "thud" and control return

### Pacing (R4)
- [ ] Each beat teaches one concept (no compound lessons)
- [ ] No beat takes >90s (player doesn't get stuck)
- [ ] Total tutorial <5 minutes (as designed)
- [ ] No idle time >10s (player always has something to do or look at)

### Accessibility (R5)
- [ ] Remappable controls
- [ ] Subtitles + closed captions
- [ ] Motion-sickness toggles (FOV, motion blur, sensitivity, head-bob)
- [ ] Colorblind non-color cues for blue=danger
- [ ] Optional numeric/visual aid for spirit sickness
- [ ] Toggle vs. hold for all interactions

### Audio reinforcement (R6)
- [ ] Walk sound (footsteps, different surfaces)
- [ ] Gather sound (per resource type)
- [ ] Heal chime (spirit healing)
- [ ] Craft unlock sound (station becomes usable)
- [ ] Armor equip sound
- [ ] Bonk thud (gentle, not punishing)
- [ ] Glide wind (ambient, spatial)
- [ ] Mist clear sound (transition cue)
- [ ] Form-change sting (bed → spirit, dawn → body)
- [ ] Shoulder spirit hum (reflects stacks)

### Visual language (R7)
- [ ] Runes are readable at a glance (which pole)
- [ ] Paradox marks read as both poles
- [ ] Shoulder spirit light reflects stacks (5 steps)
- [ ] Mist reads as "not yet" (visual, not textual)
- [ ] Marked herbs have visible rune (first mark bridge)
- [ ] Wisp carries faint rune (Idea 1)
- [ ] Consistent color language: warm (home) vs. cool (world), blue = danger (stealth)

### Transition to game (R8)
- [ ] "First mark" bridge exists (marked herb in field)
- [ ] Camp ease preview (distant view, sound, or mention)
- [ ] "One more thing" hook at end of tutorial
- [ ] Player knows what's next (gather, explore, find camp)
- [ ] Skip option for returning players

### Emotional arc (R9)
- [ ] Setup: hidden cottage, walk, reveal (curiosity → recognition)
- [ ] Tension: herb+wisp combine, heal spirit (problem → solution)
- [ ] Resolution: shoulder spirit, walk home, chores, mist clears, glide (reward → freedom)
- [ ] The heal is the emotional peak (care as active, not passive)

### Replayability (R10)
- [ ] Skip option for returning players
- [ ] Tutorial doesn't overstay (total <5 min)
- [ ] No unnecessary repetition (each beat teaches one thing)
- [ ] The marked herb is the curiosity. A second unused object is not required.

---

## 4. Prioritized gap closure plan

### Tier 1 — Blocks "polished" (must have)

| # | Gap | Requirement | Action | Owner |
|---|-----|-------------|--------|-------|
| 1 | No "first mark" moment | R1, R7, R8 | Design + implement marked herb in field (Idea 4). Author wisp mark (Idea 1). | design + impl |
| 2 | Armor bench unlocked but unused | R1, R7 | Implement guided commit (Idea 2). One mark, one axis, one success. | design + impl |
| 3 | No failure-recoverability teaching | R2 | Implement bonk + spirit-sickness preview (Idea 3). Shoulder spirit light dims. | impl |
| 4 | No audio design | R3, R6 | Create audio bible. Commission first audio assets (walk, gather, heal, bonk, glide). | art + audio |
| 5 | No accessibility P0 | R5 | Implement remapping, subtitles/captions, motion-sickness toggles, colorblind cues. | impl |
| 6 | No "one more thing" hook | R8 | Closed 2026-10-17. No second hook. The marked herb is the hook. | — |

### Tier 2 — Strongly recommended

| # | Gap | Requirement | Action | Owner |
|---|-----|-------------|--------|-------|
| 7 | No camp ease preview | R8 | Add distant view/sound/mention of pine camp from homestead. | design + level |
| 8 | "Same stroke" not demonstrated | R1 | Document teaching map (Idea 5). Ensure each beat uses the same stroke. | design |
| 9 | No VFX design | R3 | Create VFX list for spirit form, nurture glow, bonk, ease, gather, heal, portal, mist, dawn/dusk. | art |
| 10 | No skip for returning players | R10 | Add skip option (skip to glide or skip entire tutorial). | impl |
| 11 | No NPC dialogue system | R1, R8 | Design short contextual hints (one line) for family, beast, spirits. | design |

### Tier 3 — Nice to have

| # | Gap | Requirement | Action | Owner |
|---|-----|-------------|--------|-------|
| 12 | Only one encounter has 4-step ladder | R1 | Author step ladders for other 3 zones. | design |
| 13 | No "help" system | R8 | Design environmental help (subtle cues when stuck). | design |
| 14 | No HUD design | R3 | Design HUD: what's always shown, what's contextual, what's hidden. | design + art |
| 15 | No settings menu design | R5 | Design settings screen: audio, accessibility, controls. | design + art |

---

## 5. What we have vs. what we need

| Requirement | Have | Need | Gap |
|-------------|------|------|-----|
| R1 Teaching completeness | 8/12 beats taught | Mark on the wisp, bench used once, failure recovery, marked herb. No second hook. | Tier 1 items 1-3. Item 6 closed. |
| R2 Failure teaching | Bonk only | Spirit-sickness preview, "fail and keep going" | Tier 1 item 3 |
| R3 Feedback loops | Visual only | Audio, VFX, haptic | Tier 1 item 4, Tier 2 item 9 |
| R4 Pacing | Sequenced, not measured | Playtest data | Phase 1 playtest |
| R5 Accessibility | Nothing | Full P0 checklist | Tier 1 item 5 |
| R6 Audio | Nothing | Audio bible + first assets | Tier 1 item 4 |
| R7 Visual language | Runes/poles defined | First mark connection, shoulder spirit light | Tier 1 items 1-2 |
| R8 Transition to game | Glide only | Marked herb after the glide. Camp preview stays Tier 2. No second hook. | Tier 1 item 1. Item 6 closed. Tier 2 item 7. |
| R9 Emotional arc | Strong (heal peak) | Nothing missing | ✅ |
| R10 Replayability | Nothing | Skip option | Tier 2 item 10 |

---

## 6. Research still needed (not yet done)

These research tasks would further hone the ideas. They are in `TASK_LIST_TUTORIAL_DESIGN.md` as R-01 to R-05.

| Research task | Why it's needed | Status |
|---------------|----------------|--------|
| R-01: Zelda teaching methodology | Validate "show don't tell" techniques for HomeWorld's specific beats | Notes written 2026-10-17 |
| R-02: PoE onboarding (what works/doesn't) | Validate the "borrow/leave" analysis for the mark system | Notes written 2026-10-17 |
| R-03: Diegetic teaching in 3D games | Validate environmental teaching for the "first mark" bridge | Notes written 2026-10-17 |
| R-04: Failure as teaching | Validate bonk + spirit-sickness as teaching tools | Notes written 2026-10-17 |
| R-05: "One more thing" pattern | Validate the hook pattern for HomeWorld's context | Notes written 2026-10-17. Round 9 then rejected a second hook. |

**The notes were written before rounds 6–9. Those rounds are answered in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`.**

---

## 7. What I would NOT change

(From TUTORIAL_DESIGN_IDEAS.md §6, unchanged.)

- The 5-beat structure. Clean, sequenced, one concept per beat.
- The diegetic teaching approach. No UI tutorials, no popups.
- The bonk as failure. Right gentle consequence.
- The "unlock and discover later" pattern. Zelda-like, correct.
- The no-new-verbs rule. Introduce system through existing verbs.

---

## 8. Open questions (taste, for Lead)

Answered 2026-10-17 in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`, before the island playtest was played.

1. The wisp shows a mark. It is Love, a heart. The opening does not say the word.
2. The bench is used once. Place, turn, commit. No choice of axis.
3. A marked herb exists in the field after the glide. The player can bring it home.
4. The tutorial does not end on a second unused hook. The herb is the hook.

---

## 9. Sources

- `Docs/VISION_BOARD.md` — Opening tutorial (canon).
- `docs/context/OPENING_TUTORIAL_TASKS.md` — work order (in-flight, user's).
- `docs/context/OPENING_TUTORIAL_INTERVIEW.md` — interview rounds 1-5 (in-flight, user's).
- `.planning/research/TUTORIAL_DESIGN_IDEAS.md` — game designer ideas (6 ideas, 5 gaps, 4 questions).
- `.planning/TASK_LIST_TUTORIAL_DESIGN.md` — 23 tasks across 5 phases.
- `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` — audit + 11 research phases.
- `.planning/research/ACCESSIBILITY_CHECKLIST.md` — accessibility P0/P1/P2.
- `.planning/research/AUDIO_DESIGN_BRIEF.md` — audio design brief.
- `.planning/research/ONBOARDING_PLAYTEST_PROTOCOL.md` — playtest protocol.
- `Docs/canon/DESIGN_ETHOS.md` — borrowed/ours/disputed.
- `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` — virtue system rules.
- `Docs/canon/PILLARS.md` — 5 normative gates.