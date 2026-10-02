# Harness bible — the source material

The two documents this project's harness was built from. Kept in the repo
because [`Docs/36_HARNESS_MAINTENANCE_CONTRACT.md`](../36_HARNESS_MAINTENANCE_CONTRACT.md)
cites them as authority, and a citation that cannot be opened is not a citation.

| File | Pages | Role |
|---|---|---|
| `Week 1 - Agentic Engineering.pdf` | 8 | Harness engineering, BDD over TDD, the feature lifecycle, complexity and mutation testing, sycophancy, context zones. **The primary.** |
| `Slides - Agentic Engineering in Unreal.pdf` | 11 | Input/output harness split, the AGENTS.md/architecture phase, GSD, and Loop Engineering vs Gauntlet. **The Unreal-specific deck.** |

**SHA-256** — verify with `Get-FileHash` (PowerShell) or `sha256sum` (sh):

```
09CEDDF2CA2C96083F2397E0035771936EB3CB94C56DEC858858BCEF947952C9  Week 1 - Agentic Engineering.pdf
B45EADEBD7FF6E54F019D2A43CF2245A4B12661110A2C78AC340AED26555BA6C  Slides - Agentic Engineering in Unreal.pdf
```

Verified byte-identical to the files supplied by the Lead on 2026-10-01. If a hash here
disagrees with `Docs/harness-bible/*.pdf` on disk, the PDFs were modified after they were
accepted as the harness bible and the change needs explaining before the contract is amended
against them.

## What we took from them, and what we did not

The harness refactor (§4 of Docs/36) deleted the layer these slides describe. That is not a
rejection of the material — see Docs/36 §6. The research answered *"do context files help
coding agents?"*; this project's question was *"does this help ship a C++ UE game with
several agents?"* Only the parts that answered **our** question survived.

| From the source | Kept | Why |
|---|---|---|
| Harness = instructions, tools, environment, state, verification | **all five** | the definition, used verbatim in `scripts/harness-fitness.js` |
| AGENTS.md as the single always-on surface | **kept** | highest-ROI step per p5 |
| BDD over TDD for agent output | **kept** | now 3 behaviour tests in `Source/` |
| "Stop agents declaring victory too early" | **kept** | the whole reason `verify` exists |
| Complexity gate, C.R.A.P. < 8 | **kept, JS-only** | C++ needs a build-integrated tool; not faked |
| Mutation testing | **partly** | `task-lift-control.js` is a positive control; full mutation tooling is not built |
| Cyclomatic > 5 reported on change | **deviated** | we gate at a higher number because the codebase is not written to that threshold; changing it is a trigger in Docs/36 §2 |
| Loop Engineering (deterministic stop, cost ceiling) | **kept** | applied to harness work itself |
| Gauntlet (subjective stop, unbounded state) | **rejected** | the deck names it as the failure mode, and 24 commits of harness work was exactly it |

**The three that are easy to forget:**

1. **Power is nothing without control** (p1, Pirelli 1995) — agents disengage you from *syntax*,
   not from architecture. That is why architecture stayed human-owned while code design moved
   to the agent on 2026-10-01.
2. **Context zones** (p8) — the smart zone ends and the dumb zone begins at ~60k tokens. The
   context-discipline rule in `AGENTS.md` is this, applied. The PDF also recommends requiring
   final output to an `.md` file, which is why session handoffs exist as files.
3. **Sycophancy is by design, disable it early** (p8) — `scripts/anti-sycophancy.js` and
   `Docs/decisions/DISAGREEMENTS.md`. The gate can only warn; judging the reasoning stays
   human.

## Provenance

Supplied by the Lead, 2026-10-01, as the reference for the harness's scope. `Week 1` is the
week-1 bootcamp material; the Unreal deck accompanies it. Neither is cited as a published
peer-reviewed source — they are internal training material, and Docs/36 §7 records the
harness's own separate research with its own confidence levels.