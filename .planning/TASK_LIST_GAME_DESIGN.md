# HomeWorld — Game Design Task List (from audit + research)

**Source:** Game design audit (2026-10-17) + 11 research phases (R-0-1 to R-10-1) + interview answers (Q1–Q8).  
**Status:** Task list — not yet started. No project files modified by this document.  
**Owner key:** `agent` = can be done by an agent · `lead` = requires Lead decision · `human` = requires human labor (playtest, in-editor measurement) · `art` = art director.

---

## P0 — Blocks everything (do first)

### T-01: Resolve island circuit contradiction (Phase 0)
- **Owner:** lead
- **Decision made:** Reading 2 — tighten circuit window to ~12–20s (Q1 answered).
- **Action:** Update `Docs/canon/FEEL.md` (done: ~45–90s → ~12–20s). Update `Docs/qa/TRAVERSAL_BUDGET.md` to match. Record decision in `Docs/canon/DECISIONS.md`.
- **Acceptance:** FEEL.md and TRAVERSAL_BUDGET.md agree on the circuit window. G-ENV unblocked on this row.
- **Status:** Partially done. FEEL.md, TRAVERSAL_BUDGET, the polish-gate literal, and POLISH_BASELINE window agree on 12–20 s (2026-10-17). Confirmed the same day: that window is a short inner loop on the 180×100 m island, not one rim lap. DECISIONS.md entry still needed; that file is in another session's uncommitted set, so it was not edited.

### T-02: First human playtest of movement + opening
- **Owner:** human
- **Action:** Play the build (movement + opening tutorial) on desktop UE 5.8. Record in `Docs/canon/PLAYTEST.md`. One honest pass with notes.
- **Acceptance:** PLAYTEST.md updated with date, commit, what felt wrong. This is the single highest-leverage action.
- **Status:** Requirements written in `Docs/qa/TUTORIAL_ISLAND_PLAYTEST.md`. Not played.

### T-03: Place unbuilt NODE_* actors in levels
- **Owner:** agent (level placement) + human (verify in editor)
- **Action:** Place `NODE_KETTLE`, `NODE_BED`, `NODE_BACKPACK`, `NODE_PLANT_SLOT` in a playable map so the logic already written can be played. Gate fixed (interact gate admits all 14 NODE_* tags).
- **Acceptance:** All four node types placed in at least one `.umap`; `HomeWorld.T0` group still 19/19 passing against a real world.
- **Status:** Not started.

### T-04: Run polish readiness after island re-import
- **Owner:** agent
- **Action:** `py Content\Python\polish_readiness.py` and `py Content\Python\traversal_budget.py`. Record results.
- **Acceptance:** Gate states documented; any new blockers identified.
- **Status:** Not started.

---

## P1 — High leverage (do after P0)

### T-05: Onboarding playtest (Phase 1)
- **Owner:** human (test execution) + agent (protocol)
- **Action:** Run 5-tester think-aloud playtest per `ONBOARDING_PLAYTEST_PROTOCOL.md`. Record ranked list of teaching beats that fail.
- **Acceptance:** Playtest log with video timestamps + quotes; ranked failure list.
- **Status:** Protocol ready; playtest not scheduled.

### T-06: Measure 6 FEEL.md tunables (Phase 2)
- **Owner:** human (in-editor) + agent (record)
- **Action:** Extract current values of glide gravity, lateral influence, camera arm, pitch bias, night length, gather cooldown from `BP_HomeWorldCharacter` CDO. Write to `Docs/qa/POLISH_BASELINE.json`.
- **Acceptance:** All 6 tunables have measured values with source attribution.
- **Status:** Partially done (6/6 measured per polish readiness, but values are pre-tune snapshots; need current values after island re-import).

### T-07: Add motion-sickness toggles (Phase 2/6)
- **Owner:** agent (code) + lead (scope)
- **Action:** Implement FOV slider, motion-blur toggle (off default), camera sensitivity slider, head-bob toggle (off default). Per accessibility checklist P0.
- **Acceptance:** All four toggles functional in settings; default values match research recommendations.
- **Status:** Not started.

### T-08: Author step ladders for remaining zones (Phase 4)
- **Owner:** designer (agent role) + lead (review)
- **Action:** For each of the 4 zones, author the 4-step encounter ladder (Grace → Wrath → paradox → +1 visible point) per `VIRTUE_ATTRIBUTE_BIBLE.md` "Hardest form" section. Only camp ease has this today.
- **Acceptance:** Step ladder documented for all 4 zones; each has Grace-only, Wrath-only, paradox, and +1-rune variants.
- **Status:** Not started (camp ease only).

### T-09: Create audio design brief (Phase 7)
- **Owner:** art director (lead) + agent
- **Action:** Review `AUDIO_DESIGN_BRIEF.md`; assign an owner; commission audio assets. Day/night palette, spatial stealth audio, adaptive music, form-change sting, bonk, nurture, closed captions.
- **Acceptance:** Audio brief approved by Lead; owner assigned; asset list derived.
- **Status:** Brief drafted; awaiting owner assignment.

### T-10: Accessibility P0 implementation (Phase 6)
- **Owner:** agent (code) + lead (scope)
- **Action:** Implement P0 items from `ACCESSIBILITY_CHECKLIST.md`: remappable controls, subtitles+closed captions, motion-sickness toggles (overlaps T-07), colorblind non-color cues for blue=danger stealth, "no number no bar" optional aid.
- **Acceptance:** All P0 items functional; tested with colorblind simulation.
- **Status:** Not started.

### T-11: Adopt S2 art-blockout as formal gate (Phase 9)
- **Owner:** agent (process) + lead (approval)
- **Action:** Update `Docs/37_POLISH_PASS_PROCESS.md` to formally enforce S2 (art blockout) as a gate before S3 (asset production). Add S2 to `polish_readiness.py` gate ladder.
- **Acceptance:** S2 gate exists in polish readiness; G-ENV opens S2, G-ASSET depends on S2.
- **Status:** Not started (documented but not enforced).

---

## P2 — Valuable, later

### T-12: EA launch preparation (Phases 5/10)
- **Owner:** lead (business) + agent
- **Action:** Work through `EA_LAUNCH_CHECKLIST.md`: wishlist target (7000), marketing push, demo/Next Fest, store page, pricing, community. Scope: vertical slice (homestead + field + camp + rescue).
- **Acceptance:** EA launch checklist items checked off; scope decision recorded.
- **Status:** Not started.

### T-13: Telemetry spec implementation (Phase 8)
- **Owner:** agent (engineering)
- **Action:** Implement minimal telemetry (session + onboarding events) per `TELEMETRY_SPEC.md`. Start with session_start, form_change, bonk, gather, loop_complete, drop_off.
- **Acceptance:** Events fire and are recorded (local file for MVP; PlayFab/custom for EA).
- **Status:** Not started.

### T-14: Save system design (Phase 8)
- **Owner:** agent (engineering) + lead (design)
- **Action:** Define autosave cadence, failure recovery, corruption handling, slot count. Document in a save system design doc.
- **Acceptance:** Save system design documented; autosave on form change/rescue/zone transition.
- **Status:** Not started.

### T-15: P1 accessibility items (Phase 6)
- **Owner:** agent (code) + lead (scope)
- **Action:** Implement P1 from `ACCESSIBILITY_CHECKLIST.md`: UI scaling, difficulty/assist options (Celeste-style), toggle vs. hold inputs, invert axis + sensitivity sliders.
- **Acceptance:** All P1 items functional.
- **Status:** Not started.

### T-16: Audio asset production (Phase 7)
- **Owner:** art director + composer/contractor
- **Action:** Commission audio assets per `AUDIO_DESIGN_BRIEF.md`: day/night palette, spatial stealth audio, adaptive music, form-change sting, bonk, nurture, closed captions.
- **Acceptance:** Audio brief approved; asset list derived; first assets in-engine.
- **Status:** Brief drafted; awaiting owner assignment.

### T-17: P2 accessibility (Phase 6)
- **Owner:** agent (code) + lead (budget)
- **Action:** Full WCAG audit, screen reader support, one-switch/voice control, audio descriptions, cognitive accessibility review of virtue bench.
- **Acceptance:** P2 items implemented or explicitly deferred.
- **Status:** Not started.

---

## Summary

| Priority | Count | Key blocker |
|----------|-------|-------------|
| P0 | 4 tasks | Phase 1 playtest (T-02) — nothing else should be implemented before it |
| P1 | 7 tasks | T-05 (playtest) gates T-07, T-10; T-01 (island scale) gates G-ENV |
| P2 | 6 tasks | T-12 (EA scope) requires Lead/business decision |

**Critical path:** T-02 (playtest) → T-05 (onboarding playtest) → T-07/T-10 (accessibility) + T-06 (tuning) → T-08 (step ladders) → T-12 (EA scope decision).

**Do not start:** T-07, T-08, T-10, T-12 without playtest data. T-01 is a Lead decision (already made: Reading 2, applied to FEEL.md).

**Sources:** Game design audit (2026-10-17), research phases R-0-1 to R-10-1, interview answers Q1–Q8, `.planning/research/` deliverables.<|end|><|start|>write to=assistant<|channel|>analysis<|message|>Created file successfully: .planning/TASK_LIST_GAME_DESIGN.md