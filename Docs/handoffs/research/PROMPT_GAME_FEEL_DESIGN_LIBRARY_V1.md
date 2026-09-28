# RESEARCH PROMPT — GAME_FEEL_DESIGN_LIBRARY_V1

**File protocol:** Lead pastes this file into an external LLM. Canonical path: `Docs/handoffs/research/PROMPT_GAME_FEEL_DESIGN_LIBRARY_V1.md`. Return EXIT as `Docs/handoffs/research/EXIT_GAME_FEEL_DESIGN_LIBRARY_V1.md`.

## ROLE
Advise Lead / Conductor on building a **thin, pointer-only development library** of **game design and game-feel** books, talks, and vendor resources so HomeWorld Co (and Lead asks) can be steered toward **industry-leading practices for making games feel good** — without dumping full texts into AGENTS, skills, or seat prompts.

## CONTEXT
- Project: HomeWorld (UE 5.8 homestead / day-night form prototype). Swarm: Conductor · Design · Implement · Test · Fix.
- Existing **architecture** reading canon (KEEP): `Docs/handoffs/READING_CANON_V1.md` — Layers A–E (Hard Parts, Ousterhout, DDIA, Team Topologies, Release It!) + harness CANDIDATE pointers. **Do not fork or rewrite A–E.**
- Product locks (2026-09-27): CAP product **PARKED**; math-first prop placement; bright/day for bot prop work; night/lookdev = Lead taste; stills confirm-only. T0 mechanics on VS_MVP.
- Research file protocol live: `Docs/handoffs/research/PROMPT_*` / `EXIT_*`.
- HW `main` tip after #231/#232 merges ≈ `234abe6`. DET pin `0a27306`.
- Goal: **library pointers** for feel / juice / feedback / verbs / camera / input / pacing — usable when Lead asks “make X feel good,” not a new product CAP track. CAP-PROP-GATE docs may land in parallel.

## CANON
- HomeWorld Co ops — EXIT before Do; one unknown; no invent tracks without Lead.
- `Docs/handoffs/READING_CANON_V1.md` — pointer-only; seats do not ingest full books; AGENTS ≤1 path pointer.
- `Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md` — seven headings; Fitness A–D.
- Architecture Trade-Offs A–E (blob `107a511`) — cite only; not a sixth architecture layer via feel books.
- Taste history Docs/28–29 — may **point**; do not reopen closed APPROVE tracks.

## ASK
Return EXIT covering, ranked:

1. **Core game-feel / juice canon** — top books, seminal talks, studio essays (e.g. Swink *Game Feel*, juice/polish talks, feedback/animation/input latency). For each: title, author/year, why it matters for a small UE prototype, **KEEP vs CANDIDATE vs PARK**, ≤2-line abstract.
2. **Broader game design that improves feel** — MDA, verbs, loops, difficulty/pacing, camera/character control. Same KEEP/CANDIDATE/PARK. Prefer sources that transfer to **3D UE** homestead / day-night / form-swap.
3. **How to use the library in Co** — propose **one** thin pointer doc (extend READING_CANON section **or** new `Docs/handoffs/GAME_FEEL_CANON_V1.md`). Surface rules: seats cite path only; no book lists in personas; no AGENTS body dump.
4. **Lead ask → practice map** — 8–12 common Lead asks (“tighter jump,” “camera less sick,” “night mood,” “verb reads,” “prop readability,” “hit feel,” …) → which 1–2 library rows to cite first. Mark which asks stay **Lead-only taste**.
5. **Anti-patterns** — PARK/REJECT (listicles, SEO blogs, juice tips without craft, duplicating A–E as feel sources).
6. **Do bites (max 2)** — docs-only ONE_SHOT; exclusive paths; DONE-WHEN greps; forbidden co-changes; child Research Y/N.
7. **Decision:** Go / Conditional on adding feel library now (parallel OK with CAP-PROP-GATE). Must not reopen CAP product.

## NON-GOALS
- Implementing juice/camera/feel features or DESKTOP Acts this turn.
- Rewriting A–E KEEP rows; DET pin bump; alwaysApply growth; new seats; marketplace.
- CAP product Do; night bot PASS; Lead APPROVE-* by bots; book chapters into skills/AGENTS.
- “Implement now” / open DESKTOP / trial-and-error ladders.

## DONE-WHEN
EXIT includes: Diagnosis · Decision table · ranked KEEP/CANDIDATE/PARK tables · Lead-ask map · Do bites or PARK · eggbot · child Research Y/N · Accept checklist. Do bites greppable under `Docs/handoffs/`. Cite title+author or stable URL.

## child Research needed?
`Y` or `N` with one line. Prefer `N` unless rights/edition blocks the pointer table.

**Accept checklist (Conductor):** seven headings · EXIT filed · no implement-now · pointer-only · A–E untouched · max 2 docs Do bites · CAP stays PARKED.
