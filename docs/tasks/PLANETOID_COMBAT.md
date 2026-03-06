# Planetoid combat (away from home): combos and single-target

**Purpose:** Design for **planetoid (away from home)** combat style per [VISION.md](../workflow/VISION.md) § Combat variety. Planetoid combat uses **combos** and **single-target damage**. This doc describes the two styles and how they hook into packs/bosses on the planetoid. Implementation is **placeholder only** until a full vision board pass on combat.

**See also:** [NIGHT_ENCOUNTER.md](NIGHT_ENCOUNTER.md) (packs on planetoid, key-point bosses), [DEFEND_COMBAT.md](DEFEND_COMBAT.md) (defend = ranged/ground AOE), [VISION.md](../workflow/VISION.md) § Combat variety.

---

## 0. Vision summary

Per [VISION.md](../workflow/VISION.md) **Combat variety (defend vs planetoid):**

- **(1) Defend (waves at home)** — Ranged from defenses or ground AOE (see [DEFEND_COMBAT.md](DEFEND_COMBAT.md)).
- **(2) Planetoid (away from home)** — **Combos** and **single-target damage**. Variety lets you progress without building both at once; **end-game** = use either style in either situation.

This document covers **planetoid only**: combo chains vs single-target focus.

---

## 1. Combo style

- **Concept:** Player chains hits into **combo sequences** (e.g. light–light–heavy, or hit count scaling). Damage or effects scale with combo length.
- **Placeholder:** A style enum `PlanetoidCombatStyle = Combo` and a counter `ComboHitCount` (0–N) that can be incremented on hit and reset after a timeout or on miss. Future combo logic reads `ComboHitCount` to apply scaling or trigger finishers.
- **Hook:** When fighting packs or bosses on the planetoid, ability/combat code can read `GetPlanetoidCombatStyle()` and `GetComboHitCount()` to branch behavior. No full implementation; the stub exists so combo logic can be added later.

---

## 2. Single-target style

- **Concept:** Player focuses **single-target** damage on one foe (e.g. boss or priority pack member). No combo chain; direct, focused damage.
- **Placeholder:** A style enum `PlanetoidCombatStyle = SingleTarget` indicates the player is in single-target mode. Future abilities tagged for "planetoid single-target" can apply when this style is active.
- **Hook:** Same as combo — at night on planetoid (packs, key-point bosses), ability system reads the style to choose behavior. Placeholder only.

---

## 3. Stub: PlanetoidCombatStyle and ComboHitCount

- **Location:** `AHomeWorldPlayerState` (per-player for co-op; mirrors DefendCombatMode).
- **Enum:** `EPlanetoidCombatStyle::Combo` | `EPlanetoidCombatStyle::SingleTarget`.
- **API:**
  - `GetPlanetoidCombatStyle()`, `SetPlanetoidCombatStyle(EPlanetoidCombatStyle)`. Blueprint-callable.
  - `GetComboHitCount()` — current combo count (0 when not in combo or after reset).
  - `AddComboHit()` — increment combo (e.g. from a hit event); stub only, no scaling logic.
  - `ResetComboHitCount()` — clear combo (e.g. on timeout or miss); call from game code when combo breaks.
- **Default:** `SingleTarget` (or `Combo`; either is fine for stub). ComboHitCount default 0.
- **Use:** Future abilities or UI can branch on style and read ComboHitCount for combo scaling. No combat logic required for the stub; values are readable and writable, and documented here.

---

## 4. Validation

- **Doc:** This file exists and describes combo vs single-target and the stub.
- **Code:** Enum, getter/setter for style, and ComboHitCount getter/add/reset exist on PlayerState; no build or runtime errors.
- **Test:** In PIE, read `GetPlanetoidCombatStyle()` and `GetComboHitCount()`, set style to `Combo`, call `AddComboHit()` a few times, read count, then `ResetComboHitCount()`. Log or HUD can show current style and count for quick verification.

### 4.1. Testing in PIE

- **Read style and combo count:** In the game console (tilde during PIE), run **`hw.CombatStubs`**. The Output Log prints `PlanetoidCombatStyle=Combo` or `PlanetoidCombatStyle=SingleTarget` and `ComboHitCount=N`. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) "Key PIE-test usage".
- **Change style:** Select the local player's **PlayerState** in the World Outliner, then in **Details** under **HomeWorld|Planetoid** set **Planetoid Combat Style** to Combo or Single-target. Run `hw.CombatStubs` again to confirm.
- **ComboHitCount:** The count is updated by game code calling `AddComboHit()` or `ResetComboHitCount()` on the PlayerState (Blueprint or C++). To verify, use a Blueprint that calls these and then run `hw.CombatStubs` to see the new count.
- **Log on style change:** When the style is changed (via Details or Blueprint `SetPlanetoidCombatStyle`), the game logs to **LogHomeWorldPlayerState** (e.g. "PlanetoidCombatStyle set to Combo").

---

## 5. Implementation status

- **T2 (twenty-sixth list):** Design doc (this file) and minimal stub (`EPlanetoidCombatStyle` and `ComboHitCount` on `AHomeWorldPlayerState`). Placeholder only; no full combat implementation.
