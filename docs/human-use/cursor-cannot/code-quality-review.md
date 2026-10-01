# Cursor cannot: Code Quality Review (PDF section 4)

**Label:** Cursor cannot. **Owner:** Agent, since 2026-10-01 (was: human Test).

The PDF wants objective metrics instead of reading the agent’s diff like junior
human code. Cursor will not run those metrics as gates. This template will not
add them on the GitHub Actions free tier.

Reviewing its own diff is now the agent's job, not a handoff to you. That is a
weaker position than the PDF's independent reviewer, and it is stated here so the
gap is visible rather than implied: the agent cannot act as a genuinely
independent reviewer of its own work. **Ship/no-ship remains a human Test
decision** ([OWNERSHIP.md](../OWNERSHIP.md#ownership-map)).

## What the PDF asked

- Map logic with **dynamic graphs**; reserve line-by-line reading for critical
  paths.
- **Cyclomatic complexity** bands (1–10 simple, 11–15 more tests, >15 split).
- **Test coverage** as a percentage — and then **mutation testing** so coverage
  has real assertions (kill ratio; surviving mutants must die).
- **Dependency structure** (high cohesion, low coupling; flag deep or cyclic
  graphs).
- **C.R.A.P.** (complexity vs coverage); result under 8. PDF points at a GitHub
  Action / skill pack. Not a free-tier gate here.

## What Cursor actually has

- The agent can **draw** mermaid or similar graphs when you ask. There is no
  always-on graph view of the last change.
- This repo reports complexity **on TypeScript files the agent touches** (glob
  rule: report >5, split >15). That is not a Cursor-wide metric UI.
- `npm test` is the suite. There is **no** coverage-percent gate and **no**
  Stryker/mutation job. Surviving mutants are not something CI will show you.
- No dependency-matrix tool ships in this template.
- CRAP is **judgment** on [review.md](../review.md), not an Action.

## What the agent does

Use [review.md](../review.md) for the shape:

- Draw graphs; validate ordering against architecture.
- Report complexity for the files it touched, and split or accept on that basis.
- Record the call in [AGENT_DECISIONS.md](../../decisions/AGENT_DECISIONS.md) when
  a boundary moves, naming the alternative it rejected.

Coverage % and CRAP remain optional notes, not a green check — the tooling does not
exist. Supplying them to the human as if they did would be the failure this file
exists to prevent.

Do not add a mutation-testing CI job, a CRAP Action, or `npx skills@latest add …`
to this repository to "complete" the PDF.
