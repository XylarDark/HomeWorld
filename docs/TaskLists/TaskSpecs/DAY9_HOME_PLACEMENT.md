# Day 9 [1.4]: Home asset placement (player)

**Goal:** Player uses a place key + GetPlacementHit/GetPlacementTransform to place build orders (e.g. BP_BuildOrder_Wall) or props at the trace hit. Input: place key → trace → spawn at hit (or show hologram preview).

**Status:** Implemented (C++ ability + character helper; programmatic-by-default).

**See also:** [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md) Day 9, [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md), [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md).

---

## 1. Prerequisites

- **Day 8 done** — Resource collection loop (player harvest) complete; GA_Interact and inventory in place.
- **BuildPlacementSupport** — [Source/HomeWorld/BuildPlacementSupport.h](../../Source/HomeWorld/BuildPlacementSupport.h): `GetPlacementHit`, `GetPlacementTransform` exist from Day 3. Trace from local player camera; returns hit and optional placement transform (location = impact, rotation from surface normal).

---

## 2. Implementation outline

Placement is implemented in C++ with a data-only GA_Place Blueprint (programmatic-by-default, same pattern as Day 8).

1. **Place key (P)** — Bound to **IA_Place** in IMC_Default. Pressing P triggers **GA_Place** via `TryActivateAbilityByClass(PlaceAbilityClass)` in `AHomeWorldCharacter::OnPlaceTriggered`.
2. **C++ ability** — **UHomeWorldPlaceAbility** (GA_Place parent): `ActivateAbility` commits, calls `AHomeWorldCharacter::TryPlaceAtCursor()`, then ends with success/failure.
3. **TryPlaceAtCursor()** — Calls `UBuildPlacementSupport::GetPlacementTransform(World, MaxDistance, OutHit, OutTransform)` (e.g. MaxDistance 10000). If the trace hits, spawns **PlaceActorClass** at `OutTransform` via `UWorld::SpawnActor`. If `PlaceActorClass` is null, logs and returns false.
4. **BP_HomeWorldCharacter** — Holds `PlaceAbilityClass` (GA_Place), `PlaceAction` (IA_Place). **Place Actor Class** is set in Blueprint defaults: assign to **BP_BuildOrder_Wall** or a placeholder when available; if unset, placement logs "PlaceActorClass not set" and does nothing.
5. **Setup** — Run `Content/Python/setup_gas_abilities.py` (Editor or MCP) to create IA_Place, GA_Place, add P to IMC_Default, and set the 4th ability + input on the character. Do **not** set PlaceActorClass from script; assign in Editor or after creating BP_BuildOrder_Wall (see [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md)).

**References:**
- [DAY3_PLACEMENT_AND_PLAYTEST.md](DAY3_PLACEMENT_AND_PLAYTEST.md) — Placement API verification.
- [AGENTIC_BUILDING.md](AGENTIC_BUILDING.md) — Build-order flow, BP_BuildOrder_Wall, hologram, Smart Objects.

---

## 3. Validation

- **PIE:** Open DemoMap, start PIE.
- **Place key:** Press **P** while aiming at ground or surface.
- **If PlaceActorClass is set:** An actor of that class spawns at the hit; log: "HomeWorld: Place succeeded at ... (spawned ...)".
- **If PlaceActorClass is unset:** Log: "HomeWorld: Place failed - PlaceActorClass not set (assign BP_BuildOrder_Wall or placeholder in Blueprint)". No crash.
- **No hit:** Log: "HomeWorld: Place failed - no hit (aim at ground or surface)".

---

## 4. After Day 9

- Check off Day 9 in [30_DAY_SCHEDULE.md](../30_DAY_SCHEDULE.md).
- Update [DAILY_STATE.md](../../../VisionBoard/DAILY_STATE.md): Yesterday = Day 9 work; Today = Day 10; Current day = 10.
- Day 10 [1.5]: Optional agentic building (family agents fulfill build orders).
