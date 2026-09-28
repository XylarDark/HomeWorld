# RESEARCH PROMPT — CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1

**File protocol:** Lead pastes this file into the external LLM. Conductor posts path in Co; full body lives here (not chat-only).

## ROLE
Advise Lead / Conductor whether (and how) Unreal **capture/still testing** should be part of a **bot-swarm** develop loop for HomeWorld, and what **industry/AI best practices** exist for placing environment props **without** relying on visual camera nudging. Goal: near-testable prop look + position **before** a human lighting pass.

## CONTEXT
- Project: HomeWorld (UE 5.8), map `Maps/VS_MVP` / `L_VS_MVP_Markers`. HW `main` ≈ `e3bc693` (T0_M9 merged). DET pin `0a27306`. DESKTOP prove host: `DESKTOP-21CT3H0`.
- Swarm seats: Conductor (DESKTOP parent MCP/PIE only) · Design · Implement · Test · Fix. Cursor cloud / OpenCode for code; Contents API for docs.
- Existing capture harness (canon): `docs/Automation/CAPTURE_REDUNDANCY.md` — Arrange before Act; inventory → aim AABB → lighting/TOD → capture; soft_fail vs closed_fail; MRQ primary for shotlist; SceneCapture SC2D→RT→PNG was historical CAP-002 EXIT then DROPPED; Lead reopened CAP interest then **reframed**.
- Lead locks (2026-09-27):
  - Capture protocol **defaults to bright/day** lighting so props are clearly visible for look + position work; human lighting/night lookdev later (bots must not PASS night taste).
  - Prefer **math / bounds / inventory / transforms** for positioning over visual/camera positioning.
  - Do **as much positioning as possible without camera captures**; use captures only for what they are good at.
  - CAP product Do is **folly** unless capture can **reliably identify / score** what bots need (object presence, framing, gross mis-place) — Research must stress **usage + limits**, not a stills-first implement plan.
- Prior soft_fail debt: CAP-001 STOP_AL `81798e8` (writer closed) — park unless EXIT says otherwise.
- Lead protocol (2026-09-27): all Research prompts (and returned EXITs) are **files** under `Docs/handoffs/research/` — not chat-only pastes.

## CANON
- HomeWorld Co ops (`homeworld-co-ops`) — Research EXIT before Do; one unknown; no invent tracks without Lead.
- `docs/Automation/CAPTURE_REDUNDANCY.md` · `docs/Automation/ONE_SHOT_BITES.md` · HomeWorld desktop prove.
- `Docs/handoffs/TEST_SCORE_PACKET_V1.md` · Architecture Trade-Offs A–E (cite only; 15-q if EXIT invents module boundaries).
- `Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md` — seven headings; Fitness greps A–D; EXIT as file.
- Do not contradict: Arrange `ready:false` ≠ closed_fail; parent-only DESKTOP Shell; no `.uasset` commits; no ImageGrab / desktop-grab as PASS.

## ASK
Return a Research **EXIT** as a markdown file (Lead will drop into `Docs/handoffs/research/EXIT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md`) that covers, ranked:

### A. Capture testing with a bot swarm — usage & limits
1. What capture/still evidence is **reliably automatable** today (file exists, luminance, AABB ray hit, actor inventory, log greps) vs what is **weak** (semantic “is this the right prop look?”, fine visual composition, night mood).
2. Where camera captures **add unique signal** vs where they are redundant with math/inventory/Arrange gates.
3. Failure modes bots hit: near-black, wrong aim, TOD mismatch, false PASS on tiny/black PNGs, MCP main-thread blocks — map each to soft_fail vs closed_fail practice.
4. Minimum bar for “successful identification” if CAP were revived (concrete metrics/schemas, not vibes). If bar is not met by industry practice → recommend **PARK CAP** and name the non-capture path.

### B. AI / automation best practices for environment prop setup
5. Proven patterns (UE Editor Python, Sequencer/MRQ, DataLayers, PCG, constraint/snap systems, golden transforms, CI diff of transforms JSON — cite public sources) for placing props with **math-first** transforms + bounds.
6. Recommended **default bright lighting / exposure** setup for prop readability during automation (without baking final lookdev).
7. Workflow split: **no-capture path** (inventory schema → place → verify transforms/AABB/overlap/log) vs **capture path** (only named checks captures are good for).
8. How Design inventories should freeze look-at/AABB/TOD **before** any Act; what prove labels ⊆ inventory ∩ world.

### C. Decision for HomeWorld
9. Go / No-Go / Conditional on CAP product Do now. If Conditional: exact preconditions.
10. At most **3** ONE_SHOT Do bites **only if** Go/Conditional — each one unknown, DONE-WHEN greps, forbidden co-changes. Prefer docs/schema/Arrange-hardening over new capture stacks. child Research Y/N per bite.
11. Explicit: what **not** to build (stills-first loops, night bot PASS, visual-nudge farms).

## NON-GOALS
- Implementing CAP, MRQ, or SceneCapture in this Research turn.
- EA/env-art; night lighting as bot PASS; Lead `APPROVE-*` by bots.
- T0 mechanic Acts (e.g. T0_M7) before this EXIT settles CAP vs math-first path.
- Marketplace installs, AGENTS.md dumps, new seats, `.uasset`/`.umap` commits.
- “Implement now” / open DESKTOP Act / trial-and-error ladders.

## DONE-WHEN
EXIT includes: Diagnosis · Decision table (Go/No-Go/Conditional + why) · Do bites (or PARK with non-capture alternative) · eggbot N/A or one line · child Research Y/N · Accept checklist. Any proposed Do bite has greppable DONE-WHEN (paths under `Docs/` / `docs/Automation/` / `Saved/*_gate.json` schema names). Sources cited for industry claims (links or paper/doc titles).

## child Research needed?
`Y` or `N` with one line. Use child Research only for a **specific** external API/doc hole (e.g. UE 5.8 SceneCapture readback limits), not as a substitute for this EXIT’s Go/No-Go.

**Accept checklist (Conductor):** seven prompt headings present · EXIT has Diagnosis + Do bites or explicit PARK · no implement-now · CAP only if Lead-asked Conditional met · Fitness greps A–D · bright-default + math-first reflected in Decision · EXIT filed under `Docs/handoffs/research/`.
