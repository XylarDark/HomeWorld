# Task List — Tutorial Design: Zelda + PoE Synthesis

**Source:** `.planning/research/TUTORIAL_DESIGN_IDEAS.md` (game designer ideas, 2026-10-17).  
**Status:** Task list — not yet started. No project files modified by this document.  
**Owner key:** `research` = online research task · `interview` = requires Lead input · `design` = design authoring (agent or designer) · `playtest` = human playtest · `impl` = code/level implementation · `art` = art decision.

---

## Phase 0 — Research (do first, informs everything)

These research tasks should be completed before any design or implementation. They exist to hone in on ideas not yet considered and to validate assumptions.

### R-01: Zelda teaching methodology research
- **Owner:** research
- **Action:** Research how Zelda (BotW, TotK, OoT, ALBW) teaches mechanics without tutorials. Focus on: (a) how each game introduces its first modifier/attribute system, (b) the "show don't tell" techniques used, (c) how failure is used as teaching, (d) the "one more thing" pattern at the end of early sequences.
- **Sources:** BotW great plateau analysis, TotK tutorial island, OoT Kokiri Forest, ALBW, GDC talks on Zelda design, "Designing Zelda" articles, Mark Brown (Game Maker's Toolkit) Zelda analyses.
- **Deliverable:** Research notes with 5-10 specific techniques applicable to HomeWorld's tutorial. Add to `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
- **Status:** Notes written 2026-10-17. OoT and ALBW were not in the retrieved sources.

### R-02: PoE onboarding research (what works, what doesn't)
- **Owner:** research
- **Action:** Research Path of Exile's onboarding: (a) what PoE does well (depth, modifier system, "one more run"), (b) what PoE does badly (hostile onboarding, information overload, no early teaching of modifiers), (c) how PoE2 or other ARPGs improved onboarding, (d) how other complex games (Hades, Slay the Spire, Hollow Knight, Stardew Valley) onboard players to deep systems.
- **Sources:** PoE new player experience articles, PoE2 onboarding changes, Hades tutorial design, Slay the Spire first-run experience, Hollow Knight Greenpath/Ancestral Mound, Stardew Valley first day, Celeste assist mode.
- **Deliverable:** Research notes with "borrow/leave" analysis (matching DESIGN_ETHOS.md format) for HomeWorld's tutorial. Add to `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
- **Status:** Notes written 2026-10-17. Stardew Valley’s first day was not in the retrieved sources.

### R-03: Diegetic teaching in 3D games research
- **Owner:** research
- **Action:** Research how 3D games teach without UI: (a) environmental storytelling as teaching, (b) "the world announces its purpose" (HomeWorld's pillar), (c) visual language for attributes/modifiers in games, (d) how games handle the transition from tutorial to open play.
- **Sources:** Journey (thatgamecompany), Outer Wilds, A Short Hike, Spiritfarer, Pikmin, BotW shrine design, "environmental storytelling" GDC talks, "show don't tell" game design articles.
- **Deliverable:** Research notes with applicable techniques. Add to `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
- **Status:** Notes written 2026-10-17. Journey, Pikmin, and Spiritfarer were left to DESIGN_ETHOS.md.

### R-04: "Failure as teaching" research
- **Owner:** research
- **Action:** Research how games use gentle, recoverable failure as a teaching tool: (a) Zelda's falling-off-cliff teaching, (b) Celeste's death-as-restart, (c) Dark Souls' "you died" (and why HomeWorld should NOT do this), (d) how HomeWorld's bonk can be tuned to teach "not yet" without frustration, (e) spirit-sickness as a readable failure cost.
- **Sources:** Celeste assist mode design, "failure in game design" articles, Dark Souls onboarding analysis, Zelda failure-as-teaching analysis, "gentle failure" game design essays.
- **Deliverable:** Research notes with failure-teaching principles applicable to HomeWorld's bonk and spirit-sickness. Add to `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
- **Status:** Notes written 2026-10-17. No primary Dark Souls study was retrieved.

### R-05: "One more thing" / hook pattern research
- **Owner:** research
- **Action:** Research the "one more thing" pattern in game onboarding: (a) how games end tutorials with a hook (not a clean stop), (b) Apple's "one more thing" as a design philosophy, (c) how to create curiosity without confusion, (d) the balance between "clean ending" and "hook."
- **Sources:** Game onboarding case studies, "curiosity gap" in game design, "the hook" in tutorial design articles, Journey's ending, A Short Hike's ending.
- **Deliverable:** Research notes with applicable patterns. Add to `.planning/research/TUTORIAL_RESEARCH_NOTES.md`.
- **Status:** Notes written 2026-10-17.

---

## Phase 1 — Interviews (rounds 6-9, per OPENING_TUTORIAL_INTERVIEW.md pattern)

These are taste questions that cannot be answered by research alone. They need the Lead's judgment, informed by the Phase 0 research.

### I-01: Round 6 — Should the tutorial wisp show a mark? (Idea 1)
- **Owner:** interview (Lead)
- **Question:** Should the wisp the child offers in Beat 2 carry a visible (but unnamed) rune shape?
  - Option A: Yes — the wisp shows a faint rune. Teaches the system earlier. (Recommended by game designer)
  - Option B: No — leave unmarked (current recommendation). Preserves "discover later."
  - Option C: Greybox only — show a shape but not a real rune. Safe middle ground.
- **Depends on:** R-01, R-02 (research on how early to introduce modifiers).
- **Status:** Answered 2026-10-17. Yes — a faint unnamed mark on the wisp the child offers. Recorded in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`. Not built.

### I-02: Round 7 — Should the armor bench be used in the tutorial? (Idea 2)
- **Owner:** interview (Lead)
- **Question:** Should the armor bench be used (one mark placement) in Beat 4, or just unlocked?
  - Option A: Used — one mark, one axis, one success. Teaches the motion. (Recommended by game designer)
  - Option B: Unlocked only — mystery preserved, player discovers later.
  - Option C: "Peek" — partner shows the bench, player watches, doesn't interact.
- **Depends on:** R-01, R-04 (research on teaching through doing vs. watching).
- **Status:** Answered 2026-10-17. Used once — place, turn, and commit one mark, with no axis choice. Recorded in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`. Not built.

### I-03: Round 8 — Should the "first mark" herb exist? (Idea 4)
- **Owner:** interview (Lead)
- **Question:** Should there be a marked herb in the field (after the glide) as the first real encounter with the virtue system?
  - Option A: Yes — bridges tutorial → first real challenge. (Recommended by game designer)
  - Option B: No — first mark encounter is the camp ease (preserves "author the hard form first").
  - Option C: Yes, but optional — visible, not required; player can skip.
- **Depends on:** R-01, R-02, R-03 (research on onboarding depth and teaching through discovery).
- **Status:** Answered 2026-10-17. Yes — a marked herb in the field after the glide, which can be brought home to the bench. Recorded in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`. Not built.

### I-04: Round 9 — Should the tutorial end with "one more thing"? (Idea 6)
- **Owner:** interview (Lead)
- **Question:** Should the tutorial end with a visible-but-non-interactive mark/wisp at the end, creating a hook?
  - Option A: Yes — creates curiosity and transition to game. (Recommended by game designer)
  - Option B: No — clean ending with the glide. Preserves simplicity.
  - Option C: Yes, but subtle — a faint visual, easily missed, rewards attention.
- **Depends on:** R-01, R-05 (research on "one more thing" pattern).
- **Status:** Answered 2026-10-17. No second hook. The marked herb is the hook. Recorded in `.planning/research/TUTORIAL_INTERVIEW_ROUNDS.md`.

---

## Phase 2 — Design (author the ideas)

These design tasks can only be done after the corresponding interview rounds are answered. They produce design specifications, not code.

### D-01: Author the wisp's visible mark (Idea 1)
- **Owner:** design (art + design)
- **Action:** If I-01 = Option A or C, design the visual rune shape for the tutorial wisp. Which rune? Grace? Love? Unmarked greybox? Needs an art decision (art bible owns the drawing). Document the choice and the visual spec.
- **Depends on:** I-01.
- **Status:** Choice recorded 2026-10-17. The mark is Love, a heart, and the opening does not say the word. The drawing is not authored.

### D-02: Author the guided commit (Idea 2)
- **Owner:** design
- **Action:** If I-02 = Option A, design the one-line partner dialogue and the single mark placement. Which mark? Which axis? What does the player do (place, turn, commit)? Document the exact interaction sequence.
- **Depends on:** I-02, D-01 (if the mark from D-01 is used).
- **Status:** Not started.

### D-03: Author the "first mark" herb (Idea 4)
- **Owner:** design + level design
- **Action:** If I-03 = Option A or C, design the marked herb encounter in the field. Where does it sit? How visible is it? What mark does it carry? What happens when the player picks it? Document placement, visibility, and interaction.
- **Depends on:** I-03.
- **Status:** Not started.

### D-04: Author the "one more thing" moment (Idea 6)
- **Owner:** design + art
- **Action:** If I-04 = Option A or C, design the visible-but-non-interactive mark/wisp at the end of the tutorial. What does it look like? Where does it appear? How subtle? Document the visual spec.
- **Depends on:** I-04.
- **Status:** Does not apply. Round 9 answered no.

### D-05: Document the "same stroke" teaching map (Idea 5)
- **Owner:** design
- **Action:** Create a teaching map showing how the same stroke is used in each tutorial beat: heal (stroke on spirit), gather (stroke on herb), glide (stroke through descent), bonk recovery (stroke to re-attempt). Show how the camp ease adds interference (the shove) to the same stroke. This is a design doc, not code.
- **Depends on:** R-01, R-04 (research on teaching through one verb).
- **Status:** Not started.

### D-06: Document the "first mark" bridge (Idea 4 + gap 5)
- **Owner:** design
- **Action:** Create a design doc for the bridge between tutorial and first real challenge. Include: (a) the marked herb encounter, (b) the optional armor bench placement, (c) how the player connects "wisp mark" → "herb mark" → "armor bench," (d) how this prepares the player for the camp ease.
- **Depends on:** D-01, D-02, D-03, D-04.
- **Status:** Not started.

---

## Phase 3 — Playtest

### P-01: Playtest the tutorial with marks (if any were added)
- **Owner:** human (playtest)
- **Action:** Play the tutorial with the mark-related changes (wisp mark, guided commit, first mark herb, "one more thing") and observe: (a) do players notice the wisp's mark? (b) do they understand the guided commit? (c) do they pick the marked herb? (d) do they understand the connection? (e) does the "one more thing" create curiosity or confusion?
- **Depends on:** D-01 through D-06 (design complete).
- **Status:** Not started.

### P-02: Playtest failure recoverability (Idea 3)
- **Owner:** human (playtest)
- **Action:** Playtest the bonk and observe: (a) do players understand "not yet"? (b) do they understand spirit-sickness (slower movement)? (c) do they attempt again? (d) is the failure recoverable without frustration?
- **Depends on:** Beat 5 playable in editor.
- **Status:** Not started (Beat 5 not yet built).

---

## Phase 4 — Implementation (code + level)

### I-01: Implement wisp mark visual (Idea 1)
- **Owner:** impl (art + code)
- **Action:** If D-01 is complete, implement the visible rune shape on the tutorial wisp. Art asset + code to display it.
- **Depends on:** D-01.
- **Status:** Not started.

### I-02: Implement guided commit (Idea 2)
- **Owner:** impl (code)
- **Action:** If D-02 is complete, implement the single mark placement on the armor bench. Partner dialogue line + one commit sequence.
- **Depends on:** D-02.
- **Status:** Not started.

### I-03: Implement "first mark" herb (Idea 4)
- **Owner:** impl (code + level)
- **Action:** If D-03 is complete, implement the marked herb in the field. Placement, visibility, gather interaction, marked item in inventory.
- **Depends on:** D-03.
- **Status:** Not started.

### I-04: Implement "one more thing" (Idea 6)
- **Owner:** impl (art + level)
- **Action:** If D-04 is complete, implement the visible-but-non-interactive mark/wisp at the end of the tutorial.
- **Depends on:** D-04.
- **Status:** Not started.

### I-05: NPC pathing, first case the partner and the door
- **Owner:** impl
- **Action:** Not now. Do not turn collision off and do not move the partner through the wall. NPCs use the same actions a player performs. First case, Luke 2026-10-17: the partner stops at the south door, uses the player’s interact to open it, plays the open animation, walks inside to the kettle on a real path, and the player follows. The pathing system is for the game, not only this door.
- **Depends on:** a door the player can already open, and a path that respects collision.
- **Status:** Scheduled. Not started.

---

## Phase 5 — Validation

### V-01: Full tutorial playtest with all ideas
- **Owner:** human (playtest)
- **Action:** Play the complete tutorial with all implemented ideas. Observe: (a) does the player understand the virtue system by the end? (b) does the "first mark" bridge work? (c) is the tutorial too long? (d) does the player want to continue?
- **Depends on:** I-01 through I-04.
- **Status:** Not started.

### V-02: Phase 1 onboarding playtest (from research schedule)
- **Owner:** human (playtest)
- **Action:** Run the 5-tester think-aloud playtest per `ONBOARDING_PLAYTEST_PROTOCOL.md`. Record ranked list of teaching beats that fail.
- **Depends on:** Tutorial playable in editor.
- **Status:** Not started.

---

## Open questions (from TUTORIAL_DESIGN_IDEAS.md §8)

These are taste questions for the Lead, informed by Phase 0 research:

| # | Question | Depends on research |
|---|----------|-------------------|
| 1 | Should the tutorial wisp show a mark? | R-01, R-02 |
| 2 | Should the armor bench be used in the tutorial? | R-01, R-04 |
| 3 | Should the "first mark" herb exist? | R-01, R-02, R-03 |
| 4 | Should the tutorial end with "one more thing"? | R-01, R-05 |

---

## What I would NOT change (from TUTORIAL_DESIGN_IDEAS.md §6)

- The 5-beat structure (clean, sequenced, one concept per beat).
- The diegetic teaching approach (no UI tutorials, no popups).
- The bonk as failure (right gentle consequence).
- The "unlock and discover later" pattern (Zelda-like, correct).
- The no-new-verbs rule (introduce system through existing verbs).

---

## Critical path

```
R-01..R-05 (research, parallel)
  → I-01..I-04 (interviews, sequential, Lead answers)
    → D-01..D-06 (design, sequential, depends on interviews)
      → I-01..I-04 (implementation, depends on design)
        → P-01, P-02 (playtest)
          → V-01, V-02 (validation)
```

Research (Phase 0) can start immediately. Interviews (Phase 1) can start as soon as research is done. Design (Phase 2) can start as soon as interviews are answered. Implementation (Phase 4) can start as soon as design is complete. Playtest (Phase 3/5) requires implementation.

**Do not start Phase 2+ without Phase 0 research and Phase 1 interviews. The ideas are speculative until validated by research and Lead judgment.**

---

## Sources

- `Docs/VISION_BOARD.md` — Opening tutorial (canon).
- `docs/context/OPENING_TUTORIAL_TASKS.md` — work order (in-flight, user's).
- `docs/context/OPENING_TUTORIAL_INTERVIEW.md` — interview rounds 1-5 (in-flight, user's).
- `.planning/research/TUTORIAL_DESIGN_IDEAS.md` — game designer ideas (this session).
- `.planning/research/GAME_DESIGN_AUDIT_AND_RESEARCH_SCHEDULE.md` — audit + research findings.
- `Docs/canon/DESIGN_ETHOS.md` — borrowed/ours/disputed (BotW, Pikmin, Journey, Spiritfarer, Outer Wilds, Pixar).
- `Docs/VIRTUE_ATTRIBUTE_BIBLE.md` — virtue system rules.
- `Docs/canon/PILLARS.md` — 5 normative gates.