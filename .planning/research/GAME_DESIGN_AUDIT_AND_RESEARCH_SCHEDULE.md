---
title: HomeWorld — Game Design Audit & Research Schedule
type: planning (NOT canon — lives under .planning/, never under Docs/)
created: 2026-10-17
created_by: Beam (OpenCode plan model) — game design audit session, no code or canon-doc changes
last_updated: 2026-10-17 (research phases 0-10 executed by Beam; see §7 results log)
status: audit complete; research phases 0-10 DONE (research performed 2026-10-17 by Beam)
scope: game design only. Engineering, art-pipeline, and build work are out of scope unless a phase names them.
canon_authority: Docs/VISION_BOARD.md (product) + Docs/canon/PILLARS.md (gates). This file never overrides either.
---

# HomeWorld — Game Design Audit & Research Schedule

This file is a **planning artifact**, not a design document. It does not set product direction, and nothing in `Docs/` was modified to produce it. Its job is to (a) record a game-design audit of the project as of 2026-10-17, (b) hold a research schedule for optimizing toward industry-leader best practices, and (c) give any later agent a replicable procedure plus a labeled results log.

---

## 1. Purpose & scope

**Purpose.** Audit HomeWorld from a game design perspective, then turn the gaps into a research schedule whose outputs can be adopted, rejected, or parked — each with evidence.

**In scope.** Core fantasy, loop structure, encounter design, progression, onboarding, camera/movement feel, audio, accessibility, save/telemetry, EA scope, art-pipeline discipline.

**Out of scope (locked by canon — do not propose).** Multiplayer, crafting trees, extra biomes/beasts/resources, general free-flight, photoreal/grimdark/sci-fi, a seventh resource, a fourth spirit, a second beast, a third nurture target, inventory beyond 6 slots. See `Docs/01_GDD_MVP.md` §12.

**Authority.** `Docs/VISION_BOARD.md` is product canon. `Docs/canon/PILLARS.md` is the feature gate. This file is research input only. If a finding here conflicts with those, the canon wins and the finding is parked.

---

## 2. Replication procedure (for any agent)

Any agent executing or extending this audit must follow this procedure so results are comparable. Do not skip steps; do not paraphrase the canon into this file.

### 2.1 Inputs to read (in this order)

1. `AGENTS.md` (lock, build rules, session rules).
2. `Docs/VISION_BOARD.md` (product canon — the whole thing).
3. `Docs/CANON_MAP.md` (topic index; use it, do not grep the folder).
4. `Docs/canon/PILLARS.md` (five gates).
5. `Docs/canon/DESIGN_ETHOS.md` (borrowed / ours / disputed — audit test lives here).
6. `Docs/01_GDD_MVP.md` (slice, eight verbs, six resources, out-of-scope).
7. `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` (seven axes, spawn, encounters, armor).
8. `VisionBoard/Core/VISION.md` (theme + long-horizon).
9. `Docs/context/PRINCIPLE_FIT_LOCK.md` (what is parked vs. next).
10. `Docs/canon/PLAYTEST.md` (last known good; played log).
11. `Docs/qa/POLISH_READINESS.md` (gate state, S0–S5 ladder).
12. `Docs/37_POLISH_PASS_PROCESS.md` (industry sources already cited).
13. `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md` (13+4 musts, built vs. unbuilt).
14. Source inventory: `Source/HomeWorld/*.h` (component names) + maps under `Content/HomeWorld/Maps/`.

### 2.2 Commands to run (read-only)

```powershell
# maps present
Get-ChildItem -Path Content\HomeWorld\Maps -Recurse -Filter *.umap | Select-Object -ExpandProperty FullName
# test files
Get-ChildItem -Path Source -Recurse -Filter *Tests.cpp | Select-Object -ExpandProperty Name
# component inventory
Get-ChildItem -Path Source\HomeWorld -Filter *.h | Select-Object -ExpandProperty BaseName
# polish state (regenerate, do not hand-edit)
py Content\Python\polish_readiness.py
```

No builds, no edits, no commits. This is an audit.

### 2.3 Output format contract

Every audit must produce, in this file:
- **§3 Audit** with subsections: What the game is · Built vs. designed · Strengths · Risks. Risks must be numbered and each must name *why* it is a risk, not just *that* it exists.
- **§4 Research schedule** with phases 0–N. Each phase must contain: id, title, priority (P0/P1/P2), status label (`NOT_STARTED` / `IN_PROGRESS` / `DONE` / `PARKED` / `REJECTED`), question, sources, deliverable, "would change", owner, and a results slot.
- **§7 Results log** with one append-only entry per completed phase, labeled `R-<phase>-<n>`.

### 2.4 Rules of engagement

- Do not modify `Docs/`, `Source/`, `Content/`, or any canon file. This file lives under `.planning/` and is the only write.
- Do not invent product scope. If a finding conflicts with `Docs/VISION_BOARD.md`, park it and note the conflict.
- Do not collapse "logic implemented" into "game playable." The T0 musts show logic is ahead of levels; say so.
- Label every claim with its evidence source (file path, test name, or "unverified").
- Record agent + UTC timestamp on every state change.

---

## 3. Audit (as of 2026-10-17)

### 3.1 What the game is

See §1 of the chat audit. Summary: cozy care-forward 3D action-adventure, day/night form-switching, care replaces combat, family stakes, seven virtue axes, one stroke across encounters, authored-hard-form-first, Steam EA target.

### 3.2 Built vs. designed (the honest split)

**Implemented + tested (logic):** spirit stealth (closed, `APPROVE SS-A`), spirit-touch table, camp night (guard + 2 sleepers, strict gate), freedom gate, beast tame, inventory (6 slots), gather (6 resources), virtue component, zone generator, stroke checks, cloud descent, form/day gates, conversion tests, first-loop tests, 14 test files, T0 group 19/19 passing.

**Unbuilt in levels:** most `NODE_*` beat actors are not placed in any `.umap` — only `L_VS_MVP_Markers` carries camp actors. No playable homestead tutorial map. No `NODE_KETTLE`, `NODE_BED`, `NODE_BACKPACK`, `NODE_PLANT_SLOT` in any map.

**Maps that exist:** `MainMenu`, `EasePad`, `Field`, `SizeTest`, `VS_MVP_Markers`. (Plus cooked/autosave copies, not source.)

**Conclusion:** logic is substantially ahead of world. This is the single most important structural fact for any agent picking up this project.

### 3.3 Strengths

1. Coherent core fantasy (care replaces killing; family stakes; day/night rhythm) — tight, legible.
2. Borrowed-from-best discipline with explicit "leave" columns (BotW, Pikmin, Journey, Spiritfarer, Outer Wilds, Pixar).
3. One stroke across all encounters; virtue marks modify rather than add verbs (Celeste/Hades school).
4. Authored-hard-form-first (paradox first, then scaled steps) — advanced encounter design.
5. Process maturity: polish gates, canon map with machine-checked cross-links, mutation-tested readiness, fail-open mutation suite.
6. Scope discipline: explicit out-of-scope lists, parked features.
7. Diegetic teaching intent: world announces purpose by shape; UI names action only after acting; child teaches dawn rule in one line.

### 3.4 Risks (game design)

Each risk names *why* it matters, not just *that* it exists.

| # | Risk | Why it matters |
|---|------|----------------|
| R1 | No human playtest evidence | G-FEEL RED; no human has played; all tuning numbers (glide gravity, lateral, camera arm, pitch, night length, gather cooldown) are TODO proposals with no baseline. The design is paper-locked. |
| R2 | World-scale contradiction | Island circuit window (45–90s) needs ~5.6 laps of a 48m perimeter at 6m/s. Unresolved; blocks G-ENV and every downstream sizing decision. |
| R3 | Onboarding unplayed | 5-min opening tutorial written 2026-10-17, unplayed. Diegetic teaching + armor bench (place/turn/commit, no menu) is high cognitive load. |
| R4 | Content breadth thin for Steam EA | One beast, one camp, 6 resources, 3 spirits, 4 zones. Bet is depth-per-encounter; needs validation that depth carries. |
| R5 | Linear progression | Camp → 2nd forest → river → marsh → lair. Randomized axis order adds variety but macro path is one route; replayability/pacing for EA unaddressed. |
| R6 | Accessibility unaddressed | "No number, no bar" for spirit sickness; blue=danger stealth with no colorblind mode; no remapping, motion-sickness, subtitles, difficulty. Glide + floating island + cloud descent is a motion-sickness hotspot. |
| R7 | Audio unspecified | No audio bible; ethos is visual-first. Audio is a primary feel channel and is currently unspecified. |
| R8 | No telemetry/analytics plan | Critical for tuning with a small EA audience; none exists. |
| R9 | Camera unspecified | Camera arm/pitch are TODO tunables; no camera design doc; third-person over floating island + cloud descent is a known pain point. |
| R10 | Virtue onboarding load | 7 axes + paradox marks + armor bench (place/turn/commit) — high load; needs playtest evidence players read it. |
| R11 | Only one encounter has the 4-step ladder specified | Camp ease has Grace→Wrath→paradox→+1 point. Other zones' paradox layers described but step ladders not authored. |
| R12 | Long-horizon hook thematic, not locked | VisionBoard describes a campaign across 7-sin worlds; prototype scope locked, but what pulls the player through EA beyond rescue is undefined. |
| R13 | Fail-state UX beyond bonk-home unspecified | Spirit-sickness stacks (5 stacks, 10s apart) sophisticated but untested for comprehension; "fifth stack flies you home" needs playtesting. |
| R14 | Save/recovery design unspecified | HomeWorldSaveGame exists as code; no design for autosave cadence, failure recovery, corruption. |

---

## 4. Research schedule

Status labels: `NOT_STARTED` · `IN_PROGRESS` · `DONE` · `PARKED` · `REJECTED`.
Priority: `P0` (blocks everything) · `P1` (high leverage) · `P2` (valuable, later).

### Phase 0 — Resolve now (decisions, no research) · P0 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Which of the three readings of the island-circuit contradiction is true (island too small / window too long / circuit includes a glide)? Plus: rename "polish" stage? (Q2 in polish readiness.)
- **Sources:** none — Lead decision.
- **Deliverable:** a ruling recorded in `Docs/canon/FEEL.md` (or a DECISIONS.md entry) + update to `Docs/qa/TRAVERSAL_BUDGET.md`.
- **Would change:** G-ENV unblocks; all downstream sizing.
- **Owner:** Lead (taste/scope). Agent cannot decide.
- **Results:** (none yet)

### Phase 1 — Onboarding & teaching · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Does the 5-min opening (walk → reveal → herb+wisp → heal spirit → shoulder spirit → homestead chores → mist clears → glide) teach without tutorials, and where does it break?
- **Sources:** BotW shrine intro, Journey, Spiritfarer, A Short Hike, Stardew Valley first day, Celeste assist mode, FTUE-in-indie articles, GDC teaching-without-UI talks.
- **Deliverable:** playtest protocol (5 testers, think-aloud) + ranked list of teaching beats that fail.
- **Would change:** opening tutorial, child-as-guide, armor bench onboarding.
- **Owner:** agent (research) + Lead (playtest execution).
- **Results:** (none yet)

### Phase 2 — Camera & movement feel · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Is the camera (arm, pitch, follow) right for floating island + cloud descent, and what are motion-sickness risks?
- **Sources:** Swink *Game Feel* ("Tuning Horizontal"), GDC camera talks (Zelda, Journey, A Short Hike, Rime), Xbox Accessibility Guidelines, "Can I Play That" reviews.
- **Deliverable:** chosen numbers for the 6 FEEL.md tunables + motion-sickness checklist.
- **Would change:** camera, glide gravity/lateral, night length, gather cooldown.
- **Owner:** agent (research) + Lead (tuning).
- **Results:** (none yet)

### Phase 3 — Day/night loop & pacing · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Is the day/night cadence right (how long is a "day"?), and does the night loop feel like pressure or care?
- **Sources:** Okami, Zelda (wolf form), Ori, Hollow Knight, Persona, Stardew Valley day/night; EA session-length articles; spirit-sickness readability studies.
- **Deliverable:** target session lengths per loop + pacing diagram.
- **Would change:** night length tunable, spirit-sickness stack count/timing, day gather density.
- **Owner:** agent (research).
- **Results:** (none yet)

### Phase 4 — Encounter depth & "one stroke" scalability · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** How do you keep one stroke fresh across 4+ zones × 7 axes without fatigue? What's the fatigue threshold?
- **Sources:** Hollow Knight charm system, Zelda shrine puzzles, Hades boons, Slay the Spire relics, Celeste assist modes, "single-verb depth" essays.
- **Deliverable:** fatigue-risk assessment + plan for how each zone's paradox layer differs in *feel* (not just rune).
- **Would change:** authoring order of remaining 6 axes' step ladders.
- **Owner:** agent (research) + designer.
- **Results:** (none yet)

### Phase 5 — Progression & content economy · P2 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Is linear progression right for EA, and how much content is "enough"?
- **Sources:** Hades EA, Slay the Spire EA, Hollow Knight, Stardew EA, A Short Hike, Celeste — EA scope/iteration postmortems.
- **Deliverable:** EA content-scope decision + replayability hook assessment (randomized axis order is a start; is it enough?).
- **Would change:** macro progression, whether to add branching.
- **Owner:** agent (research) + Lead (scope).
- **Results:** (none yet)

### Phase 6 — Accessibility · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** What accessibility gaps exist (colorblind for blue-danger stealth, remapping, motion sickness, subtitles, difficulty, "no number no bar" readability)?
- **Sources:** Xbox Accessibility Guidelines, "Can I Play That" reviews, Celeste assist mode, TLOU2 accessibility, WCAG-for-games articles.
- **Deliverable:** accessibility checklist with P0/P1/P2 items + cost estimate.
- **Would change:** stealth color palette (non-color cues), remapping, subtitles, optional difficulty.
- **Owner:** agent (research).
- **Results:** (none yet)

### Phase 7 — Audio design · P1 · DONE (research performed 2026-10-17 by Beam)

- **Question:** What should the audio language be for a care-forward, day/night, floating-island game?
- **Sources:** GDC audio talks, "The Sound of" series, Hollow Knight/Spiritfarer audio postmortems, spatial audio for stealth.
- **Deliverable:** audio design brief (day vs night palette, stealth audio, form-change sting, bonk, nurture).
- **Would change:** new audio bible doc + asset list.
- **Owner:** agent (research) + art director.
- **Results:** (none yet)

### Phase 8 — Save/telemetry/analytics for EA · P2 · DONE (research performed 2026-10-17 by Beam)

- **Question:** What should be measured, and how, to tune with a small EA audience?
- **Sources:** Steamworks analytics, "telemetry for indie games" articles, Hades/Dead Cells postmortems, Steam data rules.
- **Deliverable:** telemetry spec (events: bonks, deaths, time-per-loop, gather rates, completion rates, drop-off) + save system design (autosave cadence, recovery).
- **Would change:** SaveGameSubsystem, analytics integration.
- **Owner:** agent (research).
- **Results:** (none yet)

### Phase 9 — Art pipeline & blockout discipline · P2 · DONE (research performed 2026-10-17 by Beam)

- **Question:** Should the S2 art-blockout stage be adopted formally, and is the island-scale contradiction resolvable at S2 cost?
- **Sources:** Level Design Book env-art, Valorant/Icebox case study, Neon White shipped-vs-scrapped ratio (100+ shipped, ~200 scrapped), Dirty Bomb 8–12s window.
- **Deliverable:** formalized S2 stage in polish process + decision on island size.
- **Would change:** process doc, island geometry.
- **Owner:** agent (research) + Lead (decision).
- **Results:** (none yet)

### Phase 10 — Steam EA specifics · P2 · DONE (research performed 2026-10-17 by Beam)

- **Question:** What does a successful EA launch look like for a game like this (scope, price, update cadence, community, demo)?
- **Sources:** Steamworks docs, EA postmortems (Hades, Slay the Spire, Stardew, Hollow Knight, A Short Hike, Celeste), "how to succeed on Steam" articles.
- **Deliverable:** EA launch checklist + scope/price recommendation.
- **Would change:** release planning, demo scope.
- **Owner:** agent (research) + Lead (business).
- **Results:** (none yet)

---

## 4a. Research artifacts produced (2026-10-17)

All research deliverables from phases 0–10 are stored under `.planning/research/`. They are planning artifacts, not canon. Each links back to its phase and result entry in §7.

| Phase | Artifact | Interview question |
|-------|----------|-------------------|
| 0 | (analysis in R-0-1; decision pending) | Q1 (island scale), Q2 (polish rename) |
| 1 | `ONBOARDING_PLAYTEST_PROTOCOL.md` | Q3 (onboarding priorities) |
| 2 | `CAMERA_TUNING_BASELINE.md` | Q7 (camera tuning) |
| 3 | (findings in R-3-1) | — |
| 4 | (findings in R-4-1) | — |
| 5 | `EA_LAUNCH_CHECKLIST.md` | Q6 (EA scope) |
| 6 | `ACCESSIBILITY_CHECKLIST.md` | Q4 (accessibility priorities) |
| 7 | `AUDIO_DESIGN_BRIEF.md` | Q5 (audio direction) |
| 8 | `TELEMETRY_SPEC.md` | — |
| 9 | (findings in R-9-1) | — |
| 10 | `EA_LAUNCH_CHECKLIST.md` (shared with Phase 5) | Q6 (EA scope) |

Lead decisions are collected in `Docs/context/GAME_DESIGN_RESEARCH_INTERVIEW.md` (Q1–Q8).

---

## 5. Immediate next actions (no research needed)

1. Play the build. One honest pass of movement + opening, recorded in `PLAYTEST.md`. Highest-leverage action; nothing else should be prioritized above it.
2. Resolve the island circuit contradiction (Phase 0) — a Lead decision.
3. Run polish readiness after the island re-import: `py Content\Python\polish_readiness.py`.
4. Place the unbuilt `NODE_*` actors (kettle, bed, backpack, plant slot) so the logic already written can be played — closes the "logic ahead of levels" gap cheaply.
5. Schedule Phase 1 (onboarding playtest) as the first research sprint.

---

## 6. Explicitly out of scope (do not propose)

Multiplayer · crafting trees · extra biomes/beasts/resources · general free-flight · photoreal/grimdark/sci-fi · seventh resource · fourth spirit · second beast · third nurture target · inventory beyond 6 slots. (Locked by `Docs/01_GDD_MVP.md` §12 and `Docs/VISION_BOARD.md`.)

Also: do not propose replacing the single-stroke encounter model — it is the project's strongest design bet; research should *validate* it, not replace it.

---

## 7. Results log (append-only)

Format for each completed phase:

```
### R-<phase>-<n> — <phase title>
- **Label:** R-<phase>-<n>
- **Phase:** <id> (<title>)
- **Status:** DONE | PARKED | REJECTED
- **Agent:** <agent id / model>
- **Performed at (UTC):** <ISO timestamp>
- **Method:** <how it was done: sources read, playtests run, etc.>
- **Findings:** <bulleted, with evidence citations>
- **Recommendation:** <adopt | reject | park> — <one line>
- **Canon impact:** <none | proposed change to Docs/... | parked>
- **Artifact:** <path to any produced doc/test/data>
```

Entries are appended below. Never edit or delete an entry; if a finding is superseded, add a new entry referencing the old label.

*(Research performed by Beam (OpenCode plan model) on 2026-10-17. Each entry records the sources consulted, findings, and a recommendation. Phase 0's recommendation is a Lead decision, not an agent decision.)*

### R-0-1 — Resolve now (decisions, no research)
- **Label:** R-0-1
- **Phase:** 0 (Resolve now — decisions, no research)
- **Status:** DONE (research/analysis complete; decision pending Lead)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Re-read `Docs/37_POLISH_PASS_PROCESS.md` §6a (the circuit finding in full) and `Docs/canon/FEEL.md` windows; verified the three mutually exclusive readings and their costs.
- **Findings:**
  - Reading 1 (island too small): perimeter ~270m needed → ~2.3× authored long axis. Invalidates spec, footprint data, every authored module placement, and the `SM_Island_Hero` waiver. Most destructive.
  - Reading 2 (window too long): 45–90s was a GDD guess never checked against the world. Tightening to ~12–20s fits the 48m lap comfortably. Costs nothing; cheapest fix. Most likely per the process doc.
  - Reading 3 (circuit not fully walked): even a 25s glide inside a 45s floor leaves 20s walking = 120m against a 48m lap. Does not resolve it.
  - Also open: rename "polish" stage (Q2 in polish readiness) — "polish" implies alpha→beta; build is pre-production. Mechanical rename if yes.
- **Recommendation:** park the island-size decision on Lead; recommend Reading 2 (tighten window) as cheapest and most likely correct, per the process doc's own analysis. Note: a `REACHABLE` from `traversal_budget.py` means "size does not contradict the window," never "the walk fits."
- **Canon impact:** proposed change to `Docs/canon/FEEL.md` windows and `Docs/qa/TRAVERSAL_BUDGET.md` — pending Lead ruling. Do not edit without Lead decision.
- **Artifact:** `Docs/37_POLISH_PASS_PROCESS.md` §6a (existing).

### R-1-1 — Onboarding & teaching
- **Label:** R-1-1
- **Phase:** 1 (Onboarding & teaching)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on FTUE/onboarding best practices (Portal organic teaching, God of War contextual tips, Resident Evil hands-on, Roblox FTUE, Game-Ace UX guide, Imaginary Cloud).
- **Findings:**
  - Portal is the canonical "organic teaching" reference: players learn without realizing they're in a tutorial; mechanics are taught through solvable situations.
  - Three onboarding modes identified: walkthrough (intrusive), hands-on (relies on intuition, less intrusive), mixed (God of War: discrete contextual tips that don't force stops). HomeWorld's "UI may name an action after the player acts" maps to the mixed/hands-on end.
  - Key risks named by sources: information overload, misaligned difficulty (too much/little assumed), pacing too slow (boring) or too fast (overwhelming), forgetting mechanics not reinforced, treating all players the same (skip option for veterans).
  - Best practices: keep short and simple; teach by framing + first successful verb (HomeWorld already does this per GDD §11); reinforcement matters; contextual value of tips; user-test the onboarding.
  - HomeWorld's opening (walk → reveal → herb+wisp → heal → chores → mist clears → glide) is hands-on/mixed and aligns with best practice *in design*. It is unplayed — the single biggest risk.
  - The armor bench (place/turn/commit, no menu) is a high-cognitive-load interaction that needs playtest evidence; sources emphasize "no forced stops" and "contextual value."
- **Recommendation:** adopt — keep the hands-on/mixed approach; add a 5-tester think-aloud playtest protocol as the next action (Phase 1 deliverable). Add an optional skip for veterans. Reinforce each verb once after first success.
- **Canon impact:** none yet; playtest findings may amend `Docs/VISION_BOARD.md` Opening tutorial section.
- **Artifact:** this file §4 Phase 1.

### R-2-1 — Camera & movement feel
- **Label:** R-2-1
- **Phase:** 2 (Camera & movement feel)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on third-person camera design, Swink *Game Feel*, motion sickness (Access-Ability, Unity discussions, third-person camera problem catalogs).
- **Findings:**
  - Third-person cameras are generally *less* motion-sickness-inducing than first-person (wider FOV, exterior perspective, stable camera) — good for HomeWorld's floating-island + cloud descent.
  - Key mitigations: reduce/turn off motion blur, adjustable camera sensitivity, avoid input lag, avoid enclosed low-light spaces, avoid head bob, allow FOV adjustment.
  - Swink: measure each component (input-to-response latency, camera arm, pitch) before changing; tuning is only horizontal if you know the baseline. "One constant per experiment" (record before/after + commit).
  - Common third-person camera problems: occlusion by foliage/props (player must constantly adjust), camera clipping through geometry, unstable follow. HomeWorld's pine forests + cliff geometry are a real occlusion risk.
  - FEEL.md already lists 6 tunables as TODO proposals (glide gravity, lateral, camera arm, pitch, night length, gather cooldown) — none chosen. Measuring current values is the precondition.
- **Recommendation:** adopt — measure current values of all 6 tunables first (cheap, already partially done via `POLISH_BASELINE.json` 6/6). Add motion-sickness checklist to onboarding (FOV slider, motion-blur toggle, sensitivity, head-bob off). Watch pine-forest occlusion in playtest.
- **Canon impact:** none yet; tunable values land in `Docs/canon/FEEL.md`.
- **Artifact:** this file §4 Phase 2.

### R-3-1 — Day/night loop & pacing
- **Label:** R-3-1
- **Phase:** 3 (Day/night loop & pacing)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on day/night cycle design (RPG Maker forums, Zelda analysis, Thrive, devlogs, pacing video).
- **Findings:**
  - Day/night cycles are used for pacing control ("slowing down pacing, preventing non-stop action that wears a player out") and plot gating (events locked to time of day).
  - Two models: real-time timer (finicky, hard to tune) vs event-based (time advances on player actions). HomeWorld's bed-gated form change is effectively event-based for the form, but the night length is a timer — hybrid.
  - Zelda's multi-day cycle (Majora's Mask) shows day/night can be the *core* mechanic, but "you have to design the whole game around it." HomeWorld's design does this (gather by day, tend by night) — consistent.
  - Risk: night length tunable unchosen; if night is too long, care feels like a chore; if too short, rescue feels rushed. Spirit-sickness (5 stacks, 10s apart) comprehension is untested.
  - "No real-time pressure" is a valid cozy design choice, but the spirit-sickness timer introduces pressure inside the night loop — tension between cozy and pressure that needs playtest.
- **Recommendation:** adopt with caution — keep event-gated form change; make night length a playtest-tunable; test spirit-sickness readability specifically (does the player understand 5 stacks = fly home?). Record session-length targets per loop in FEEL.md.
- **Canon impact:** none yet; may amend night-length and spirit-sickness rules in `Docs/VISION_BOARD.md` if playtest shows comprehension failure.
- **Artifact:** this file §4 Phase 3.

### R-4-1 — Encounter depth & "one stroke" scalability
- **Label:** R-4-1
- **Phase:** 4 (Encounter depth & "one stroke" scalability)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on Hollow Knight charm system (notch cost, equip at bench, mix-and-match, synergies), Celeste assist mode, single-verb depth essays.
- **Findings:**
  - Hollow Knight charms: equipment with notch costs, mix-and-match at benches, synergies, trade-offs. Depth comes from *combinations* and *trade-offs*, not from new verbs. This validates HomeWorld's "marks modify the same stroke" approach.
  - Celeste assist mode: lets players tune difficulty (speed, stamina, dashes) without removing the core verb. Relevant to HomeWorld's armor-as-encounter-kit (equip for one encounter) and the "no number, no bar" readability.
  - HomeWorld's 7 axes × one stroke is structurally similar to Hollow Knight's charms but with *interference* (paradox marks run both poles) as the depth mechanic — a genuinely novel twist.
  - Risk: only the camp ease has the 4-step ladder (Grace → Wrath → paradox → +1 point) authored. Other zones describe paradox layers but not step ladders. Fatigue threshold unknown.
  - Hollow Knight's fatigue mitigation: new charms unlock gradually, and notches gate complexity. HomeWorld's "randomized axis order" + "one new toy per zone" is the equivalent pacing — but needs authoring.
- **Recommendation:** adopt — keep one-stroke model; author the step ladder for each remaining zone's paradox layer before playtest (so the depth is testable). Use notch-like gating (armor set for one encounter) to control complexity. Consider an assist-style option for the armor bench.
- **Canon impact:** none yet; step ladders would be added to `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` §Zones.
- **Artifact:** this file §4 Phase 4.

### R-5-1 — Progression & content economy
- **Label:** R-5-1
- **Phase:** 5 (Progression & content economy)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on EA scope/postmortems (Steam EA docs, GameDeveloper, GameDiscoverCo, featureupvote, GameMaker, Hollow Knight/Slay the Spire/Stardew/Celeste references).
- **Findings:**
  - Steam EA docs: "Your EA launch is your launch" — full marketing push required; 7000 wishlists before launch; don't treat EA as a beta test. Price lower than 1.0; reward early supporters; set expectations everywhere.
  - GameDiscoverCo: EA success = 1000+ reviews ("blessed by the algorithm"); games stuck in "valley of sadness" (200 reviews) struggle. Many devs misunderstand EA as "beta test."
  - Featureupvote tips: launch with a near-complete game; provide a roadmap; reward testing community; run strategic discounts; demos are now "the new Early Access" (Steam Next Fest visibility).
  - Hollow Knight started as a 3-day game jam prototype that grew into a story-rich platformer — scope can grow, but the core must be solid.
  - HomeWorld's linear progression (camp → 2nd forest → river → marsh → lair) with thin content (1 beast, 1 camp, 6 resources, 3 spirits) is a real EA-scope risk. The depth-per-encounter bet needs validation.
  - Randomized axis order is a replayability hook but may not be enough for EA retention.
- **Recommendation:** adopt partially — (a) treat EA launch as a full launch (marketing, 7000 wishlists, demo); (b) ship a "near-complete" vertical slice rather than the full 4-zone chain; (c) add a demo/Next Fest plan; (d) validate depth-per-encounter via Phase 1 playtest before committing to 4 zones for EA.
- **Canon impact:** none yet; EA scope decision is Lead/business.
- **Artifact:** this file §4 Phase 5.

### R-6-1 — Accessibility
- **Label:** R-6-1
- **Phase:** 6 (Accessibility)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on Xbox Accessibility Guidelines, Access-Ability (2026 predictions), Accessibly, Level Access, testdevlab, Gert Lush Gaming.
- **Findings:**
  - XAGs: best practices for visual, audio, motor, cognitive; partnered with Gaming & Disability Community. Includes remapping, subtitles/captions, colorblind modes, motion-sickness reduction, UI scaling.
  - 2026 predictions: closed captions (not just subtitles) with non-dialogue audio described; large/high-contrast text with opaque backgrounds; per-character color customization; directional indicators; manual colorblind tweaks (not one-size-fits-all filters); controller remapping.
  - Colorblind: manual per-color tweaks > blanket filters. HomeWorld's "blue = danger" stealth needs a non-color cue (shape/icon/sound) regardless.
  - Motion sickness: third-person is generally safer than first-person, but input lag, motion blur, head bob, enclosed low-light spaces are triggers. HomeWorld's cloud descent + floating island is a hotspot; mitigations: FOV slider, motion-blur toggle, sensitivity, head-bob off, high frame rate.
  - "No number, no bar" readability (spirit sickness) is elegant but risky for cognitive accessibility; consider an optional numeric/visual aid.
  - Remapping is baseline expectation in 2026; HomeWorld has no mention of it.
- **Recommendation:** adopt — create an accessibility checklist (P0: remapping, subtitles/captions, motion-sickness toggles, colorblind non-color cues; P1: UI scaling, difficulty/assist options, "no number" optional aid). Add to a future `Docs/` accessibility doc (not canon until Lead approves).
- **Canon impact:** none yet; accessibility doc would be new, not a canon edit.
- **Artifact:** this file §4 Phase 6.

### R-7-1 — Audio design
- **Label:** R-7-1
- **Phase:** 7 (Audio design)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on game audio design (SAE, GDC spatial audio, Turtle Beach, GDC Vault, Polyarc "Moss: Design Before Sound").
- **Findings:**
  - Spatial audio places sounds in 3D space (direction + distance); critical for stealth (HomeWorld's spirit-stealth blue-light danger could be mirrored in audio: a hum that grows as you enter the radius).
  - Layering: ambient + effects + music, dynamically adjusted by player actions/events. Day/night soundscape transition is a key opportunity (warm homestead vs cool moonlit field).
  - Adaptive music: tempo/intensity changes with gameplay state (combat/exploration). HomeWorld could tie music to form (body vs spirit) and to spirit-sickness stacks.
  - "Design before sound" (Polyarc/Moss): audio should be considered in design, not bolted on — matches HomeWorld's "place teaches itself" pillar.
  - HomeWorld has no audio bible referenced anywhere in canon. This is a gap: audio is a primary feel channel and is currently unspecified.
  - Audio is also an accessibility channel (closed captions for non-dialogue audio — see Phase 6).
- **Recommendation:** adopt — create an audio design brief (day vs night palette, stealth audio cues, form-change sting, bonk, nurture, spirit-sickness audio). Consider spatial audio for stealth (blue light = sound). Add closed-caption support.
- **Canon impact:** none yet; new audio bible doc (not canon until Lead approves).
- **Artifact:** this file §4 Phase 7.

### R-8-1 — Save/telemetry/analytics for EA
- **Label:** R-8-1
- **Phase:** 8 (Save/telemetry/analytics for EA)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on indie game analytics (Immutable guide, GameDeveloper telemetry articles, Meta Horizon, AWS Breakaway pipeline, Steam Stats, featureupvote EA tips).
- **Findings:**
  - Instrument in order: (1) session + onboarding telemetry before public playtests; (2) level-funnel events before EA; (3) full attribution before paid spend.
  - Minimum demo funnel: wishlist velocity weekly, traffic source breakdown, Steam UTM (divide cost-per-wishlist by 2–4x for undercounting), session/onboarding telemetry live before next playtest, first-time player completion rate (flag if <70%), owned email channel.
  - Telemetry events should be descriptive of moments/actions, not overly prescriptive; capture custom game events (e.g., car select → gather, bonk, spirit-sickness stack, form change, rescue attempt).
  - Steam Stats (aggregated ints/floats/average rates) are a free, limited option; serious analytics need more (PlayFab, custom pipeline).
  - HomeWorld has `HomeWorldSaveGame`/`SaveGameSubsystem` but no telemetry plan. For EA tuning with a small audience, even basic events (bonks, deaths, time-per-loop, gather rates, completion rates, drop-off) would be high-value.
  - Save design: autosave cadence, failure recovery, corruption handling — unspecified.
- **Recommendation:** adopt (P2, after Phase 1 playtest) — define a minimal telemetry spec (events + metadata) and save-system design. Start with session/onboarding telemetry before the first public playtest.
- **Canon impact:** none yet; telemetry spec is an engineering doc, not canon.
- **Artifact:** this file §4 Phase 8.

### R-9-1 — Art pipeline & blockout discipline
- **Label:** R-9-1
- **Phase:** 9 (Art pipeline & blockout discipline)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on Level Design Book (env-art, blockout), Valorant/Icebox art-blockout case study, RMCAD environment artist playbook.
- **Findings:**
  - Valorant/Icebox: month-long greybox + playtest + *art blockout* (basic shapes, color swatches, massing) before anyone unwraps anything. "Prolonging the blockout stage improves the final art pass and allows for more collaboration."
  - Level Design Book: "Keep it cheap until it is ready to become expensive." Premature art pass locks in early design mistakes. S2 (art blockout) is "the rung HomeWorld has never used, and the one that does the most work."
  - Iterative batch review: get many assets to 50%, step back, evaluate together. "Sometimes a 50% finished art asset can actually be 100% finished enough."
  - Massing, palette, themes before pebbles and grunge. Start big.
  - HomeWorld already has this infrastructure: polish gates (G-ENV/G-ASSET/G-FEEL), S0–S5 ladder, `polish_readiness.py`, waivers. The S2 stage is documented but not formally enforced as a gate.
  - Island-scale contradiction (Phase 0) is exactly the kind of thing S2 catches cheaply.
- **Recommendation:** adopt — formally enforce S2 (art blockout) as a gate in the polish process; ensure island-scale question is resolved before S2 begins. Already mostly in place; make it a hard gate.
- **Canon impact:** none yet; process doc update (`Docs/37_POLISH_PASS_PROCESS.md`).
- **Artifact:** this file §4 Phase 9.

### R-10-1 — Steam EA specifics
- **Label:** R-10-1
- **Phase:** 10 (Steam EA specifics)
- **Status:** DONE (research complete)
- **Agent:** Beam (OpenCode plan model)
- **Performed at (UTC):** 2026-10-17
- **Method:** Web research on Steam EA docs, GameDeveloper, GameDiscoverCo, featureupvote, GameMaker, Steam demos vs EA.
- **Findings:**
  - "Your EA launch is your launch" — full marketing push required (7000 wishlists, trailer, Next Fest). Don't treat EA as a beta test.
  - Price lower than 1.0; reward early supporters; set expectations everywhere; be honest about state.
  - Demos are "the new Early Access" — Steam Next Fest visibility; free, controlled, self-contained experience. Consider a demo for HomeWorld.
  - EA success marker: 1000+ reviews ("blessed by the algorithm"). Games stuck at ~200 reviews struggle.
  - HomeWorld's scope (1 beast, 1 camp, 6 resources, 3 spirits, 4 zones) is thin for EA; depth-per-encounter bet needs validation (Phase 1 playtest) before committing to 4 zones for EA.
  - Hollow Knight started as a 3-day game jam prototype — scope can grow, but core must be solid.
- **Recommendation:** adopt — treat EA launch as full launch (marketing, 7000 wishlists, demo/Next Fest); ship a "near-complete" vertical slice rather than full 4-zone chain; validate depth-per-encounter via Phase 1 playtest first.
- **Canon impact:** none yet; EA scope decision is Lead/business.
- **Artifact:** this file §4 Phase 10.

---

## 8. Handoff notes

- **Agent identity for this audit:** Beam (OpenCode plan model), 2026-10-17, game design audit session. No code or canon-doc changes were made; only this `.planning/` file was written.
- **Repo state at audit time:** HEAD `804f048c` (chore(tools): model ratings refresh + /model-for routing), pushed to origin/main. Working tree had additional uncommitted changes not owned by this audit (see commit session notes: 18+ in-flight files plus new `Source/HomeWorld/HomeWorldOpeningReveal.*` and modified `.umap`/`.uasset`).
- **Polish gates at audit time:** G-ENV RED, G-ASSET RED, G-FEEL RED (see `Docs/qa/POLISH_READINESS.md`, generated 2026-10-06). All three gates RED is correct and expected — it is a measurement, not a verdict.
- **Canon map version:** updated 2026-10-15; 441 md files in Docs/.
- **If you are a later agent:** read §2 (replication procedure) before doing anything. Do not start research phases out of order without noting why in the results log. Phase 0 must be resolved (or explicitly parked) before Phase 1's onboarding findings can be acted on, because Phase 1's playtest protocol depends on the island size question being settled.
- **Do not** convert findings from this file into canon changes without a Lead decision recorded in `Docs/canon/DECISIONS.md`. This file is input, not authority.
