# Research prompt contract (ProveOps B)

**Owner:** Conductor writes paste-ready prompts to `Docs/handoffs/research/PROMPT_<ID>.md` and posts the **path** (optional ≤5-line digest) in HomeWorld Co. Lead runs the **file** through an external LLM and returns EXIT as `Docs/handoffs/research/EXIT_<ID>.md`. Conductor **ACCEPT**s EXIT → Lead greenlights Do. Chat is not the canonical prompt/EXIT body.

## File protocol (Lead lock 2026-09-27)

- Every Research **prompt** MUST exist as `Docs/handoffs/research/PROMPT_<ID>.md` before Co treats it as live.
- Every Research **EXIT** MUST exist as `Docs/handoffs/research/EXIT_<ID>.md` before `ACCEPT EXIT`.
- Interview EXIT SCOPE/IMPLEMENTATION prompts use the same `PROMPT_` / `EXIT_` naming under that folder.
- Fitness greps A–D run on those **files** (`$P` / `$E`), never a chat scrape.
- Folder README: `Docs/handoffs/research/README.md`.

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
- [ ] Run Fitness greps A–D (below) on the prompt + EXIT (and repo ALIGN after Do)

If any box fails → return to Lead for rewrite (do not ACCEPT).


## Fitness greps (before ACCEPT)

Conductor re-runs on every Research prompt (`$P`) and every EXIT (`$E`) before `ACCEPT EXIT`. Files-only. No DESKTOP. Do **not** invent a `RESEARCH_FITNESS` track. Seven heading **names** above stay the paste law.

### A. Prompt — seven exact heading names (FAIL if any missing)

```bash
# $P = Docs/handoffs/research/PROMPT_<ID>.md (canonical file)
for h in 'ROLE' 'CONTEXT' 'CANON' 'ASK' 'NON-GOALS' 'DONE-WHEN' 'child Research needed?'; do
  grep -E "^#{0,3}[[:space:]]*${h}" "$P" || echo "FAIL missing heading: $h"
done
```

Pass = all seven match as headings (leading `#` optional; name exact).

### B. EXIT — required sections + paste-ready (FAIL if any missing)

```bash
# $E = Docs/handoffs/research/EXIT_<ID>.md (full file, not chat slice)
for h in 'Diagnosis' 'Do bites' 'eggbot' 'child Research' 'Accept checklist'; do
  grep -E "$h" "$E" || echo "FAIL missing EXIT section: $h"
done
grep -E '^#+[[:space:]]*EXIT ' "$E" || echo "FAIL missing EXIT title"
```

### C. Four fail-strings (any hit in EXIT **Do bites / instruction** prose = FAIL ACCEPT)

Run on `$E` only. Do not run on the Research **prompt** (prompts legally name `#8`/`#9`/CAP in NON-GOALS). Judge intent on Do-bites lines; Diagnosis / Decision table / NON-GOALS / PARK / Forbidden lists are allowed.

```bash
grep -nEi 'implement now|start coding|land this PR now|do this now|merge this PR|open DESKTOP Act|run the prove' "$E" \
  && echo "FAIL: EXIT instructs immediate implement"

grep -nEi 'schedule #8|do MARKETPLACE_SCOUT|install marketplace|CAP-002 readiness as this bite|CAP product Do|APPROVE TOOL SCOUT' "$E" \
  && echo "FAIL: EXIT folds #8/#9/CAP product"

grep -nEi 'bump pin|alwaysApply|AGENTS.md body|Class S slim|rewrite A–E' "$E" \
  && echo "FAIL: EXIT grows locked surfaces"

grep -nE 'readiness `false`.{0,40}closed_fail|ready:false.{0,40}closed_fail|arrange-block.{0,20}closed FAIL' "$E" \
  && echo "FAIL: EXIT restates skill drift"
```

### D. Repo ALIGN greps (score-skill bar)

```bash
# Must be EMPTY (skill no longer equates readiness false with closed_fail)
grep -nE 'readiness `false`|readiness false' \
  .agents/skills-extras/testing-standards/SKILL.md \
  && echo "FAIL: testing-standards still binds readiness false to closed_fail"

grep -nE 'Arrange-block ≠ closed FAIL|ready:false|closed_fail: false|prove_loop_status' \
  Docs/handoffs/TEST_SCORE_PACKET_V1.md \
  docs/Automation/CAPTURE_REDUNDANCY.md

# ONE_SHOT ladder must not flip pre-Act arrange-block into closed_fail via "missing setup ⇒ closed_fail"
grep -nE 'missing setup.*closed_fail' docs/Automation/ONE_SHOT_BITES.md \
  && echo "FAIL: ONE_SHOT still flips arrange-block"
```

### Smallest bar (30s)

1. Prompt seven headings.
2. EXIT has Diagnosis + Do bites + child Research + no implement-now.
3. Repo: testing-standards does not contain `readiness false` next to `closed_fail`.

## AGENTS.md

At most **one pointer line** to this file. No paste of this contract body into `AGENTS.md`.
