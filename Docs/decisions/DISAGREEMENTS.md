# Substantive disagreements

**What this is.** One entry each time an agent proposes something and gets told it is
wrong — or the agent pushes back and is overruled. Both directions count.

**Why it exists.** "Week 1 — Agentic Engineering", under *Agent-specific Information
and Suggestions*:

> "Sycophancy — Agents are programmed to try to answer you anyhow first, and to be
> accurate as a secondary priority. Most LLM Agents will also try to flatter you to
> keep your attention. That's by design, so disable it as soon as possible!"

A document stating a virtue is not a mechanism. `npm run sycophancy` reads this file
and reports whether anything has been recorded recently.

**Format.** `## <what was proposed>` then the date, what was actually wrong with it,
and what was done instead.

**Rules that keep it honest:**

1. **Only substantive ones.** A wording preference is not a disagreement.
2. **Say what was actually wrong.** "I was wrong" without a reason is worthless.
3. **Struck entries are kept, not deleted.** A deleted disagreement is
   indistinguishable from one that never happened. Use `~~strike~~` if one turns out
   to have been wrong on review.
4. **Both directions.** Being overruled counts. So does agreeing after pushback.

**What this cannot do.** It cannot verify any entry is real, and it never fails the
build. Requiring a quota of disagreements per commit would produce manufactured ones,
which is worse than sycophancy because it is false *and* dressed as candour.

---

## Example — what a real entry looks like

- **2026-10-01 · Phase 1 deletions, proposed as safe in one pass.** Wrong because the
  first rebase attempt failed on a missing decision-log path, and I had not checked
  whether the log existed early in history. Split into per-surface commits instead.
  *Recorded after the fact; the warning came a day late.*