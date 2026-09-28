# RESEARCH PROMPT — GAME_DESIGN_MOVEMENT_ENV_V1

**File protocol:** Lead pastes this file into an external LLM. Canonical path: `Docs/handoffs/research/PROMPT_GAME_DESIGN_MOVEMENT_ENV_V1.md`. Return EXIT as `Docs/handoffs/research/EXIT_GAME_DESIGN_MOVEMENT_ENV_V1.md`.

## ROLE
Advise Lead / Conductor on **industry game-design practices for movement + environment** that improve HomeWorld’s **harness** (how bots/Lead prove and iterate), **best-practice library** (pointer-only), and **vision/taste** for the T0 prototype — without inventing product features this turn.

## CONTEXT
- HomeWorld: UE 5.8 homestead ↔ planetside; day/night form; VS_MVP; T0 narrative = seed/nurture/cultivate seamless fantasy (Lead 2026-09-27).
- ACCEPTED SCOPE floor: Interview `PROTOTYPE_T0_V1` + `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` (MUST: wake/kettle-sprint, plant, backpack, glider↔field, gather, rune, eject-not-kill, bed→spirit, nurture, portals, avoid/soothe).
- Parallel Research: `PROMPT_GAME_FEEL_DESIGN_LIBRARY_V1` (draft HW #234) = **general feel/juice library**. This prompt is **narrower**: movement systems + environment layout/readability that make those verbs feel good.
- Parallel Interview amend: `PROMPT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1` (draft HW #235) — SCOPE overlay; do not duplicate SCOPE tables here.
- Caps: CAP product **PARKED**; greybox/low-poly OK; math-first prop arrange schemas on main (`f72d5d8`); bright/day for bot prove; night = Lead taste.
- Closed history to cite not reopen: Docs/24 MV-A traversal · Docs/30 DS-A · Movement bible LOCKED · FALLBACK FLIGHT armed.
- Pins: DET `0a27306` · OpenCode≡Cursor when usage capped.

## CANON
- HomeWorld Co ops — Research = external info; EXIT before Do; one unknown.
- `Docs/handoffs/READING_CANON_V1.md` — A–E KEEP; pointer-only libraries; no AGENTS dump.
- `Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md` — seven headings; Fitness A–D.
- `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` — T0 MUST beats / NODE_* inventory.
- CAPTURE_REDUNDANCY · ONE_SHOT_BITES · Architecture Trade-Offs A–E (cite only when EXIT invents harness boundaries).

## ASK
Return EXIT covering, ranked for a **small UE prototype** (not AAA production art):

1. **Movement design canon** — books/talks/studio essays on character control, traversal, glide/flight feel, camera-follow, input latency, “weight,” seamless zone transitions. KEEP/CANDIDATE/PARK + ≤2-line why for HomeWorld T0 (glider, eject-home, spirit portals).
2. **Environment design for verbs** — level/env practices that sell **seed/nurture/cultivate** + readable interactables in greybox: landmarking, affordance, pathing, day/night readability, camp/field/homestead envelopes. Same KEEP/CANDIDATE/PARK.
3. **Harness / prove practices** — how leading teams instrument movement+env iteration (metrics, playtest scripts, greybox gates, soft vs closed fails). Map to our CAPTURE_REDUNDANCY / gate JSON / files-only score style — **propose pointer rules**, not new CAP writers.
4. **Vision alignment** — 8–12 concrete “feel goals” for early testers tied to T0 MUST beats (e.g. “glide reads as intentional not floaty,” “homestead path invites plant-then-leave”). Mark Lead-only taste vs bot-proveable.
5. **Anti-patterns** — PARK/REJECT (over-authored polish before verbs; night mood as bot PASS; capture-first placement; lethal-combat defaults).
6. **Do bites (max 2)** — docs-only: e.g. `GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md` pointer table and/or one-line cites into READING_CANON / feel DONE-WHEN templates. Exclusive paths; forbidden: Source/Content/uasset/DESKTOP/CAP product/AGENTS body.
7. **Decision:** Go / Conditional / No-Go now vs wait for #234 EXIT first. Prefer **Conditional**: this EXIT may **cite** #234 rows but must stand alone if Lead runs them in either order.
8. **child Research?** — Y/N (prefer N unless a rights-blocked source blocks the table).

## NON-GOALS
- Implementing movement/env features, camera code, DESKTOP Acts, or `.uasset` this turn.
- Replacing T0 SCOPE; inventing new MUST beats; reopening CAP/EA; night bot PASS.
- Rewriting A–E; pin bump; marketplace; new seats; “implement now.”
- Duplicating the full general feel-library table from #234 (cross-link only).

## DONE-WHEN
EXIT includes: Diagnosis · Decision · KEEP/CANDIDATE/PARK tables (movement + env) · harness pointer rules · vision feel-goals · anti-patterns · Do bites ≤2 or PARK · eggbot · child Research Y/N · Accept checklist. Cite title+author or stable URL.

## child Research needed?
`Y` or `N` with one line. Prefer `N`.

**Accept checklist (Conductor):** seven headings · EXIT filed · no implement-now · pointer-only · T0 not voided · CAP PARKED · max 2 docs Do · coordinates with #234 without requiring merge order.
