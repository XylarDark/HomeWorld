# Scope refinement

Reusable interview so the agent asks instead of guessing. The Lead decides. Use it when the next step would invent a product, scope, or architecture choice, and whenever a design change would move scope or a module boundary.

**Skill:** `scope-refinement`  
**Ask shape:** Cursor structured question picker · [OWNERSHIP.md](OWNERSHIP.md) · max **2** questions per turn ([taste-profile.md](taste-profile.md))  
**Queue:** same as [taste-gates.md](taste-gates.md) (`Docs/handoffs/TASTE_GATE_*.md`)

## Methods this protocol collects

| Method | What it already decides | What this protocol uses it for |
|--------|-------------------------|--------------------------------|
| [Taste Gates](taste-gates.md) | Detect, alert, queue, stop, scribe | The interview is a Taste Gate. No second queue. |
| [Taste Profiler](taste-profiler.md) | Read profile first; promote only after Lead confirm | Do not re-ask a locked row or a do-not. |
| [HOMEWORLD_TRADEOFFS.md](../architecture/HOMEWORLD_TRADEOFFS.md) | Quanta, data owner, skipped drivers | Hard Parts. Do not invent a service, saga, or store. |
| [HOMEWORLD_DESIGN.md](../architecture/HOMEWORLD_DESIGN.md) | Depth inside the client | Ousterhout. Do not add a special case “just in case.” |
| [VISION.md](../../VisionBoard/Core/VISION.md) vs [Docs/21](../../Docs/21_REAP_SOW.md) | Theme vs shipped slice | Name the conflict. Do not merge the texts yourself. |

Precedence stays: latest Lead chat / `APPROVE *` > taste profile > never invent.

## When to run

- The agent would have to guess to keep going.
- A design change would add, drop, or redraw scope, a quantum, or a module interface.
- Two or more canon texts describe different “what we are building,” and the profile does not already pick one.

Do not run for a typo, a one-file edit inside a settled boundary, or a fork the profile already locked.

## Question quality

This is the part to keep. A thin question (“Is this okay?”) is a failed round.

- One fork per question. The options are different things the project could be, drawn from the canon texts or from the Hard Parts / Ousterhout briefs.
- Put the recommended option first. The recommendation cites a file already in the repo. If nothing in the repo supports a recommendation, the recommendation is Skip.
- Every question includes Skip. Skip leaves the fork undecided and does not start the next round.
- The Lead can type a custom answer.
- At most two questions, then stop. The second question is the consequence of the first (what that choice refuses, which special cases stay out, what must not be built).
- Do not ask a question the profile already locked.

## Steps

1. List the conflicting sentences and the file each came from. One line each.
2. Strike any option that violates a locked decision or a do-not.
3. Stage `TP-CAND-SCOPE-R<N>` in `Saved/taste_profile_session.json` (`source`: `taste-gate`, `status`: `staged`) before asking. This is the Taste Profiler path. Do not write the durable profile yet.
4. Ask at most two questions through Cursor’s structured question picker (selectable options, not a markdown menu). Each question includes **Skip**. The Lead may also type a custom answer.
5. Stop. Do not build, do not open a Docs track, do not fill blank purpose fields.
6. When the Lead answers, promote that pick into the taste profile and set the candidate to `promoted`. Skip sets it to `rejected`. The fork stays undecided and the next round does not start. If they closed a “Skipped” architecture bullet, mark that bullet closed in one line. Leave every other bullet alone.
7. A later round starts only after the previous round was answered and not skipped.

## Current rounds

Rounds 1–3 below are **closed** (promoted 2026-09-23). Do not ask them again. They stay as the worked example of question depth. New forks get new questions in this shape.

Change this list when a round proves useless. Note the date and why in [Refinements](#refinements). Do not delete the old round; mark it retired.

**Round 1 — which text is the slice**

1. Which document is the scope of the next playable, when the Vision texts disagree?
   - A. Act 1 lone wanderer only (no family, no co-op).
   - B. The one-day tutorial that starts with a family and ends when they are taken.
   - C. Docs/21 reap/sow on the current VS_MVP slice only. Vision campaign text stays theme, not a build list.
2. When that choice collides with “placeholder combat” and “one client,” what is refused in this slice?
   - A. Family, child, and relationship systems.
   - B. Anything beyond a convert-stub encounter.
   - C. Saving, co-op, and any server. Session play only.

**Round 2 — only if Round 1 was not Skip**

3. Co-op: keep “later, no consistency window,” or name the first promise (local same-screen, Steam session, or still later)?
4. Persistence: keep “no second store,” or name what the one client must remember between sessions?

**Round 3 — special cases**

5. Which of these stay out of the slice until a later vision pass: child key-song, ancient ghost outside at night, partner resurrection, astral-during-day?
6. Is the slice one loop (day and night in one play), or day-only until night is approved?

**Round 4 — CLOSED 2026-09-24**

Mean luminance is one number. `analyze_png_luminance_content` in `Content/Python/pa_e_shotlist_common.py` already records center-crop, black fraction, and coverage. [Docs/33_PLACEMENT_STILLS.md](../../Docs/33_PLACEMENT_STILLS.md) keeps framing and mood on the Lead eyeball, and golden image diff behind `APPROVE TOOL SCOUT`.

7. What may automation decide about “looks proper”?
8. What does that choice refuse: golden pixel diff and a new Docs track, or screenshot-to-golden comparison now?

## Refinements

| Date | Change | Why |
|------|--------|-----|
| 2026-09-23 | Protocol created from Taste Gates, the profiler, Hard Parts, and Ousterhout. Rounds 1–3 added. | Vision texts disagree; architecture docs had left those forks skipped on purpose. |
| 2026-09-23 | Answers stage as `TP-CAND-SCOPE-R<N>` and promote only on Lead confirm. | Scope refinement is part of Taste Profiler, not a side file. |
| 2026-09-23 | Rounds are asked with Cursor’s structured question picker. | Lead process pref: GUI choices, not a markdown menu. |
| 2026-09-23 | The same question shape is required whenever the agent would guess, and whenever a design change moves scope or architecture. | Lead confirmed the depth and the picker. Thin yes/no questions are a failed round. |

When a question was already locked, or Skip was the wrong shape, add a row here and edit the round. Do not invent a new method beside this file.
