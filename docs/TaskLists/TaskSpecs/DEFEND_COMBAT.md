# Defend combat (waves at home): ranged vs ground AOE

**Purpose:** Design for **defend (waves at home)** combat style per [VISION.md](../../../VisionBoard/Core/VISION.md) § Combat variety. Defend uses **defenses around your homestead**; the player can choose **ranged attacks from defenses** or **ground AOE**. This doc describes the two modes and how they hook into the existing night-encounter stub. Implementation is **placeholder only** until a full vision board pass on combat.

**See also:** [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (waves at home, spawn, defeat → convert), [CONVERSION_NOT_KILL.md](CONVERSION_NOT_KILL.md), [VISION.md](../../../VisionBoard/Core/VISION.md) § Combat variety.

---

## 0. Vision summary

Per [VISION.md](../../../VisionBoard/Core/VISION.md) **Combat variety (defend vs planetoid):**

- **(1) Defend (waves at home)** — You have **defenses around your homestead**. You can use **ranged attacks** from those defenses, or **go on the ground** and use **area-of-effect (AOE)** attacks.
- **(2) Planetoid (away from home)** — Combos and single-target damage (see [PLANETOID_COMBAT.md](PLANETOID_COMBAT.md) or NIGHT_ENCOUNTER for planetoid design).

This document covers **defend only**: ranged-from-defenses vs ground AOE.

---

## 1. Ranged from defenses

- **Concept:** Player fights from **defense positions** (turrets, walls, towers) around the homestead. Attacks are **ranged** (projectiles or hitscan from the defense).
- **Placeholder:** A flag or enum `DefendCombatMode = Ranged` indicates the player is in "ranged from defenses" mode. Future abilities tagged or keyed for "defend ranged" can apply when this mode is active.
- **Hook:** When at night and waves spawn, the game can read `DefendCombatMode` (e.g. on PlayerState) to decide which ability set or UI to show (ranged vs ground AOE). No full implementation; the stub exists so abilities can be classified later.
- **Defenses:** Actual defense positions (turrets, slots) are a separate concern; see [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) and future "defenses around homestead" design (e.g. DEFEND_DEFENSES.md).

---

## 2. Ground AOE

- **Concept:** Player **leaves the defense** and fights on the ground with **area-of-effect** attacks (splash, ground-target, cone, etc.).
- **Placeholder:** A flag or enum `DefendCombatMode = GroundAOE` indicates the player is in "ground AOE" mode. Future abilities tagged for "defend AOE" can apply when this mode is active.
- **Hook:** Same as ranged — at night, wave logic or ability system reads the mode to choose behavior. Placeholder only.

---

## 3. Stub: DefendCombatMode

- **Location:** `AHomeWorldPlayerState` (or GameMode if preferred; PlayerState keeps it per-player for co-op).
- **Enum:** `EDefendCombatMode::Ranged` | `EDefendCombatMode::GroundAOE`.
- **API:** `GetDefendCombatMode()`, `SetDefendCombatMode(EDefendCombatMode)`. Blueprint-callable so designers can toggle or bind to UI.
- **Default:** `Ranged` (or `GroundAOE`; either is fine for stub).
- **Use:** Future abilities or UI can branch on this value. No combat logic required for the stub; the value is readable and writable, and documented here.

---

## 4. Validation

- **Doc:** This file exists and describes ranged vs ground AOE and the stub.
- **Code:** Enum and getter/setter exist on PlayerState; default value is set; no build or runtime errors.
- **Test:** In PIE, read `GetDefendCombatMode()` (e.g. via Blueprint or console), set to `GroundAOE`, read again. Log or HUD can show current mode for quick verification.

### 4.1. Testing in PIE

- **Read current mode:** In the game console (tilde during PIE), run **`hw.CombatStubs`**. The Output Log prints `DefendCombatMode=Ranged` or `DefendCombatMode=GroundAOE` (and planetoid/combo values). See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) "Key PIE-test usage".
- **Change mode:** Select the local player's **PlayerState** in the World Outliner (e.g. "PlayerState_0"), then in the **Details** panel open **HomeWorld|Defend** and set **Defend Combat Mode** to Ranged or Ground AOE. Run `hw.CombatStubs` again to confirm.
- **Log on change:** When the mode is changed (via Details or Blueprint `SetDefendCombatMode`), the game logs to **LogHomeWorldPlayerState** (e.g. "DefendCombatMode set to GroundAOE").

---

## 5. Implementation status

- **T1 (twenty-sixth list):** Design doc (this file) and minimal stub (`EDefendCombatMode` on `AHomeWorldPlayerState`, getter/setter). Placeholder only; no full combat implementation.
