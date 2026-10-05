# Test contract (human-owned) — Test

You own what “done” means (scenarios, coverage, acceptance). The agent owns writing
the tests *from those scenarios* and the product code. Feature work is user-flow
(BDD). Classic red-green TDD is for critical or low-level pieces and escaped bugs.
See [OWNERSHIP.md](OWNERSHIP.md).

## Options the agent must offer

When no scenario is decided **for this task** (still stubs, and not a one-line skip).
Current accepted contract. Change this contract when the Lead replaces the behavior decision.

1. **Accept or edit the agent’s restatement** (recommended for a new behavior) —
   Given/When/Then taken from *my* request, not invented product goals.
2. **I'll fill `test-contract.md` myself** — agent waits.
3. **Dictate scenarios in chat** — agent restates them, I confirm, then it scribes.
4. **Bug fix** — I'll name the broken behavior in one sentence; agent writes that
   failing test first and does not implement until it fails.
5. **Existing suite is the contract** — no new scenarios; point at the tests to run.
6. **Skip this gate** — no new behavior. Agent records the skip.

## Task type

Gameplay traversal behavior: active steered cloud descent and cloud-wisp collection.

## Skill or human reference

Use [`Docs/context/HOMEWORLD_ROUTE.md`](../../Docs/context/HOMEWORLD_ROUTE.md) for
current route facts and [`Docs/VISION_BOARD.md`](../../Docs/VISION_BOARD.md) for
product direction. The scripted `FALLBACK` documents are not references for active
steering behavior. No human-written snippet in `references/` applies to this task.

## Granularity and coverage

End-to-end in-game traversal: day/body launch, unrestricted steering through the
cloud descent, cloud-wisp collection and retention, lower cloud exit, landing in
the existing field, and return of walk control. Do not add a travel-time target,
steering envelope, or new flight mode.

## Behavior scenarios

Accepted by the Lead on 2026-10-05, with unrestricted glider steering.

**Given** the player is at the glider perch in body form during day, **when**
they launch, freely steer through the cloud descent, collect a cloud wisp, and
continue to the lower cloud exit, **then** steering is not constrained by a
rail, corridor, or artificial bound, the wisp stays with the player, they land
in the existing field, and walk control returns.

## Bug-fix guard (if this cycle is a fix)

Not a bug-fix task.

## Acceptance

Human play check: confirm steering remains unrestricted throughout the cloud
descent, the collected wisp stays with the player, landing occurs in the existing
field, and walk control returns. Route duration and steering limits are not
acceptance criteria.
