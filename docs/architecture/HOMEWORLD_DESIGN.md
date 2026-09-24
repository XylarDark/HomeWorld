# HomeWorld design complexity

Hard Parts already fixed the quanta in [HOMEWORLD_TRADEOFFS.md](HOMEWORLD_TRADEOFFS.md). This page is how code **inside** the game quantum stays cheap to change. The standing prompt is [design-complexity-brief.md](design-complexity-brief.md). Harness copy: [DevEnvTemplate/docs/architecture/design-complexity.md](../../DevEnvTemplate/docs/architecture/design-complexity.md).

Working code is not the goal. A design that stays obvious under change is the goal.

These choices follow [CONVENTIONS.md](../CONVENTIONS.md). Anything not in the table is **not decided**.

## Depth already chosen

| Module | Interface the caller sees | Knowledge kept inside |
|--------|---------------------------|------------------------|
| C++ gameplay type (character, ability, game mode) | A small set of calls and `UFUNCTION` entry points | Timing, attributes, combat and movement rules |
| GA_* Blueprint | Asset assignment on a C++ parent | No second copy of the rule |
| Python setup script | One idempotent entry | Editor steps, existing-asset checks |
| UnrealMCP | One bridge | Editor live control. No wrapper bridge |

Blueprint is a different abstraction from C++ (content, not control flow). A Blueprint graph that reimplements a C++ rule is a shallow copy, not a layer.

## Red flags in force

- A pass-through class or script whose signature matches the thing it calls and adds no abstraction.
- Two modules that both know the same gameplay invariant (a C++ ability and a Blueprint graph, or two scripts that must edit together).
- A public surface of knobs “just in case.” Defaults live on the C++ class.
- A one-off rule smeared into a reusable type. Today’s planetoid or homestead special case stays in the caller or in data.

Unreal `AActor` / `UGameplayAbility` inheritance stays. That is the engine. Do not add another subclass whose only job is to forward calls.

## Errors

“Already exists” on an idempotent setup script is success. A missing asset, a failed load, or lost player state is a real failure and stays visible. Do not invent a new exception taxonomy for GAS.

## Comments and names

A public C++ function whose signature omits units, order, null, or failure gets a short contract comment. Comments that restate the next line do not. Names follow the existing Unreal prefixes and Python style in the file being edited.

## Tests

High-value checks (PIE, log-driven validation, Python tests) protect behavior. Design the interface first. Tests-first are for reproducing a bug, not for inventing the API.

## Skipped

- Rewriting existing classes to satisfy a line-count or “one reason to change” rule.
- A comment-first pass over headers that are already obvious.
- Banning implementation inheritance the engine requires.
- A performance pass that is not measured.
- Filling the blank fields in [human-use/architecture.md](../human-use/architecture.md).

## Fitness

- New gameplay is a C++ class. The Blueprint child assigns assets.
- A new Python script checks for what it creates and hides the Editor steps. It does not only launch another script.
- If a reviewer cannot guess the call from the declaration plus its contract comment, the interface is not done.
