# Game design research interview

**Status:** Open — awaiting Lead answers.  
**Created:** 2026-10-17 by Beam (OpenCode plan model), from the game design audit and research schedule (`.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md`).  
**Owner:** Lead (taste/scope decisions). Agent cannot decide these.  
**Format:** Each question has a recommendation and numbered options. Pick one, edit, or dictate. Answer in the "Answer" line; the agent will fold answers into the relevant research deliverable and update the schedule.

This interview collects the decisions that research (phases 0–10, completed 2026-10-17) cannot make. Research findings and recommendations are in `.planning/research/`. This file only holds the decisions.

---

## Q1 — Island circuit contradiction (Phase 0, P0, blocks G-ENV)

**Context:** `Docs/37_POLISH_PASS_PROCESS.md` §6a. The island circuit window (45–90s) needs ~5.6 laps of a 48m perimeter at 6m/s walk. Three mutually exclusive readings.

**Limitation:** I cannot decide which number is wrong; this is a scope/feel ruling, not an engineering question.

**Recommend:** Reading 2 (window too long). Tighten to ~12–20s. Cheapest fix, most likely correct per the process doc's own analysis. Does not invalidate geometry.

**Need from you:**
1. (Recommended) Reading 2 — tighten the circuit window to ~12–20s in `Docs/canon/FEEL.md`.
2. Reading 1 — island is too small; grow it ~2.3× (invalidates spec, footprint data, all module placements, the `SM_Island_Hero` waiver).
3. Reading 3 — circuit includes a glide segment (even a 25s glide leaves 20s walking = 120m vs 48m lap; does not fully resolve).
4. Dictate your own reading.

**Answer:** 1 — Reading 2 (tighten window to ~12–20s). Applied to Docs/canon/FEEL.md 2026-10-17. Confirmed the same day: keep 12–20 s as a short inner loop. The island that loop is timed on is the L_SizeTest walk pad, where mechanics are introduced.

---

## Q2 — "Polish" stage rename (from polish readiness Q2)

**Context:** `Docs/qa/POLISH_READINESS.md` Q2. "Polish" implies alpha→beta transition; build is pre-production with no human playtest. Renaming touches gate row ids and four canon docs.

**Limitation:** Naming/vocabulary is a taste decision.

**Recommend:** Decide before the name does damage. If you want the rename, pick a name (e.g., "Pre-production readiness" or "Blockout readiness"). If not, keep "polish."

**Need from you:**
1. Keep "polish" (no change).
2. (Recommended) Rename — suggest a name: ___________
3. Skip / defer.

**Answer:** 1 — Keep "polish" (no change).

---

## Q3 — Onboarding priorities (Phase 1)

**Context:** Research found HomeWorld's hands-on/mixed onboarding aligns with best practice (Portal, God of War contextual tips). The 5-min opening is unplayed. The armor bench (place/turn/commit, no menu) is high cognitive load.

**Limitation:** I cannot decide which teaching beats to keep/cut without playtest data; I can only design the playtest protocol.

**Recommend:** Run the 5-tester think-aloud playtest first (protocol in `.planning/research/ONBOARDING_PLAYTEST_PROTOCOL.md`), then decide.

**Need from you:**
1. (Recommended) Approve the playtest protocol and schedule a playtest session before changing any onboarding.
2. Skip playtest; proceed to implement onboarding changes now (risk: unvalidated).
3. Dictate specific onboarding changes to make now.

**Answer:** 1 — Approve playtest protocol, schedule first.

---

## Q4 — Accessibility priorities (Phase 6)

**Context:** Research produced a P0/P1/P2 accessibility checklist (`.planning/research/ACCESSIBILITY_CHECKLIST.md`). P0 items: remapping, subtitles/captions, motion-sickness toggles (FOV, motion blur, sensitivity, head-bob), colorblind non-color cues for blue=danger stealth. P1: UI scaling, difficulty/assist options, "no number no bar" optional aid. P2: full WCAG audit.

**Limitation:** Which P0/P1 items ship in MVP vs. EA is a scope/taste decision.

**Recommend:** Adopt all P0 for MVP (low cost, high impact). Defer P1 to EA. Skip P2 unless funded.

**Need from you:**
1. (Recommended) P0 for MVP, P1 for EA, P2 deferred.
2. P0 + P1 for MVP (more scope).
3. P0 only, defer everything else.
4. Dictate your own priority.

**Answer:** 1 — P0 for MVP, P1 for EA, P2 deferred.

---

## Q5 — Audio direction (Phase 7)

**Context:** No audio bible exists. Research recommends: day vs night palette, spatial audio for stealth (blue light = sound), adaptive music for form/state, closed captions. Needs an art director + Lead decision.

**Limitation:** Audio direction is taste (art director territory).

**Recommend:** Commission an audio design brief (draft in `.planning/research/AUDIO_DESIGN_BRIEF.md`) and assign to the lighting/audio owner before any audio asset work.

**Need from you:**
1. (Recommended) Approve the brief as a starting point; assign to an owner.
2. Defer audio entirely until after the first playtest.
3. Dictate a different audio direction.

**Answer:** 1 — Approve brief as starting point, assign owner.

---

## Q6 — EA scope (Phase 5)

**Context:** Research: "EA launch is your launch" (7000 wishlists, full marketing, demo/Next Fest). HomeWorld's content is thin (1 beast, 1 camp, 6 resources, 3 spirits, 4 zones). Depth-per-encounter bet needs validation.

**Limitation:** EA scope and pricing are business decisions.

**Recommend:** Ship a "near-complete" vertical slice (homestead + field + pine camp + rescue) for EA rather than the full 4-zone chain. Validate depth-per-encounter via Phase 1 playtest first. Add a demo for Next Fest.

**Need from you:**
1. (Recommended) Vertical slice for EA (homestead + field + camp + rescue); defer 2nd forest/river/marsh/lair to post-EA updates.
2. Full 4-zone chain for EA (more scope, higher risk).
3. Dictate your own EA scope.

**Answer:** ___________

---

## Q7 — Camera tuning (Phase 2)

**Context:** Six FEEL.md tunables are TODO proposals with no chosen numbers: glide gravity scale, glide lateral influence, camera arm length, camera pitch bias, night length, gather node cooldown. None has been measured.

**Limitation:** I cannot pick tuning numbers without playtest data. I can only set up the measurement.

**Recommend:** Measure current values first (partially done via `POLISH_BASELINE.json` 6/6), then tune after Phase 1 playtest. Add motion-sickness mitigations (FOV slider, motion-blur toggle, sensitivity, head-bob off) as P0 accessibility.

**Need from you:**
1. (Recommended) Measure baselines now; tune after playtest; adopt motion-sickness toggles as P0.
2. Tune now without playtest (risk: unvalidated).
3. Dictate specific numbers.

**Answer:** ___________

---

## Q8 — "polish" stage rename (duplicate of Q2, for tracking)

See Q2.

---

## How to respond

Answer each question's "Answer" line (or say "skip" / "defer"). The agent will:
- Fold answers into the relevant research deliverable (`.planning/research/`).
- Update the research schedule (`GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md`) phase statuses.
- Create any follow-up interviews if an answer raises new questions.
- NOT make canon changes without a Lead decision recorded in `Docs/canon/DECISIONS.md`.

If you want to answer all at once, just list "Q1: 1, Q2: 1, Q3: 1, ..." etc.
