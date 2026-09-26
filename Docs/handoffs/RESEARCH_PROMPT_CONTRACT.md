# Research prompt contract (ProveOps B)

**Owner:** Conductor posts paste-ready prompts in HomeWorld Co. Lead runs them through an external LLM and returns a Research EXIT. Conductor **ACCEPT**s EXIT → Lead greenlights Do.

Cite: Co skill `homeworld-co-ops` · EXIT `CO_BOTS_PROCESS_REFINE_V1`.

## Required paste block (seven fields)

Every Conductor Research prompt MUST include these headings (names exact):

1. **ROLE** — who the external LLM is advising (Lead / Fix root / harness, etc.)
2. **CONTEXT** — pins / SHAs / measured tip (HW `main`, DET pin, relevant soft_fail SHAs)
3. **CANON** — paths/skills that must not be contradicted
4. **ASK** — numbered questions; what the EXIT must contain
5. **NON-GOALS** — explicit bans (product CAP, AGENTS dump, new seats, …)
6. **DONE-WHEN** — greps/checks for any Do bites the EXIT may propose
7. **child Research needed?** — `Y` / `N` (and why)

Optional but preferred: **Accept checklist** the Conductor will run before `ACCEPT EXIT`.

## Conductor ACCEPT checklist (before ACCEPT EXIT)

- [ ] Diagnosis / decisions ranked; persona-tooling vs procedure split present when asked
- [ ] Seat KEEP set matches Co (no vanity add) when seats in scope
- [ ] Procedures / skills cite canon; no AGENTS.md body dump
- [ ] Do bites: one unknown each, DONE-WHEN greps, forbidden co-changes, child Research Y/N
- [ ] Non-goals include CAP product Do unless Lead asked for CAP Research
- [ ] 15-q Architecture Trade-Offs only for boundaries the EXIT invents
- [ ] EXIT is paste-ready and does **not** instruct immediate implement

If any box fails → return to Lead for rewrite (do not ACCEPT).

## AGENTS.md

At most **one pointer line** to this file. No paste of this contract body into `AGENTS.md`.
