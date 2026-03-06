# Defenses around homestead

**Purpose:** Design for **defense positions** (turrets, walls, placeholder slots) around the homestead per [VISION.md](../workflow/VISION.md) § Combat variety. Defend (waves at home) uses these positions so the player can fight **ranged from defenses** or **ground AOE**. This doc describes positions and how they hook into the existing night-encounter and Defend flow. Implementation is **placeholder only** until a full vision board pass.

**See also:** [DEFEND_COMBAT.md](DEFEND_COMBAT.md) (ranged vs ground AOE), [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (waves at home, spawn, DefendPosition), [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md), [VISION.md](../workflow/VISION.md) § Combat variety.

---

## 0. Vision summary

Per [VISION.md](../workflow/VISION.md) **Combat variety (defend vs planetoid):**

- **(1) Defend (waves at home)** — You have **defenses around your homestead**. You can use **ranged attacks** from those defenses, or **go on the ground** and use **area-of-effect (AOE)** attacks.
- Defenses = physical positions (turrets, walls, towers, or placeholder slots) where the player or family can stand to fight waves. "Ranged from defenses" assumes these positions exist and can host a ranged combat mode (see DEFEND_COMBAT.md).

This document covers **defense positions** only: what they are, how they are placed, and how they hook into the existing Defend flow.

---

## 1. Defense positions (design)

- **Concept:** Defense positions are **locations around the homestead** where the player or family can stand to defend during night waves. They can be:
  - **Turrets / towers** — future: interactable or manned structures that grant ranged attacks.
  - **Walls / barricades** — future: cover or chokepoints.
  - **Placeholder slots** — for now: simple positions (actors or spawn points) that define "around home" so ranged-from-defenses and family Defend have a hook.
- **Home reference:** "Homestead" or "home" is the defend anchor (e.g. player location when night starts, or a tagged Home actor). Defense positions are defined **relative to home** (offsets) or as **level-placed actors** with tag `DefendPosition`.
- **Existing hook:** The game already discovers actors with tag **`DefendPosition`** at night and logs their count/locations; family can be teleported to those positions (see [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) §4, [DAY12_ROLE_PROTECTOR.md](DAY12_ROLE_PROTECTOR.md)). So level designers can place actors (empty actors, volumes, or visible placeholders) and tag them `DefendPosition` to define defense slots.
- **Configurable offsets (stub):** When no level-placed `DefendPosition` actors exist, the game can use a **configurable list of defense offsets** (relative to home) to **spawn** placeholder defense-position actors at night. That gives a minimal testable stub: set offsets in Blueprint/Editor (e.g. `DefensePositionOffsets` on GameMode), and at night the game spawns one placeholder per offset at (home + offset), tagged `DefendPosition`, so existing Defend logic (log, family move) sees them.

---

## 2. Stub: configurable offsets and optional spawn

- **Location:** `AHomeWorldGameMode` (Category `HomeWorld|Defend` or `HomeWorld|DefensePositions`).
- **Config:** `DefensePositionOffsets` — `TArray<FVector>` of world-space offsets from "home" (player location when night starts). Editable in Blueprint/Editor. Empty = no auto-spawn; use level-placed `DefendPosition` actors only.
- **Behavior:** When night is triggered (same tick as `TryTriggerNightEncounter`):
  - If `DefensePositionOffsets.Num() > 0` and we have not yet spawned defense placeholders this night, for each offset spawn one placeholder actor at (home + offset), add tag `DefendPosition`, so `TryLogDefendPositions` and `TryMoveFamilyToDefendPositions` see them.
  - Reset "spawned this night" when phase leaves night (with other night state).
- **Home:** Use first player pawn location (same as night encounter wave spawn) as "home" for offset math.
- **Placeholder:** Spawn a simple visible actor (e.g. `AStaticMeshActor` with a small mesh such as Cylinder) so positions are observable in PIE; tag `DefendPosition`.
- **No conflict:** Level-placed `DefendPosition` actors are always used when present. The stub adds **spawned** positions when offsets are set, so both level design and config-driven positions are supported.

---

## 3. Validation

- **Doc:** This file exists and describes defense positions and the stub (offsets, optional spawn, tag `DefendPosition`).
- **Code:** `DefensePositionOffsets` on GameMode; when at night and offsets non-empty, spawn placeholders at home + offset, tag `DefendPosition`; reset when leaving night.
- **Test:** In PIE, set `hw.TimeOfDay.Phase 2`, ensure at least one offset in GameMode (e.g. (300,0,0)); observe spawned defense position(s) and log "Defend positions (T3): N actor(s)" from existing `TryLogDefendPositions`.

---

## 4. Implementation status

- **T8 (twenty-sixth list):** Design doc (this file) and minimal stub: `DefensePositionOffsets` on GameMode, spawn defense placeholders at night when offsets are set, tag `DefendPosition`; once-per-night flag reset when leaving night. Placeholder only; no turret/wall behavior.
