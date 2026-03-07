# Day love/bond metric (design)

**Purpose:** Define how the player earns "love" (or bond) during the day and how that value scales night bonuses. Aligned with [VISION.md](../workflow/VISION.md) (goal of the day = build up love → bonuses at night) and [DAY_RESTORATION_LOOP.md](DAY_RESTORATION_LOOP.md).

**See also:** [PROTOTYPE_SCOPE.md](../workflow/PROTOTYPE_SCOPE.md) § Day/night and astral.

---

## 1. Design intent

- **Goal of the day:** Build up **love** through meals, care, building together, and (later) keeping the child safe. That love **gives bonuses used during the night** (stronger astral combat, better restoration, or other benefits).
- **Love is the bridge between day and night.** The existing "day restoration buff" (one meal → buff flag) is one narrow path; the **love** metric is the broader aggregate that can scale night bonuses by tier or multiplier.
- **Stub scope:** This doc defines the design; the code provides a **stub value** (e.g. `LoveLevel` or `BondPoints` on PlayerState) that can be read when applying night bonuses. Full implementation (all sources, persistence, UI) is deferred.

---

## 2. How love is earned

| Source | Description | Stub / future |
|--------|-------------|----------------|
| **Meals / food** | Cooking and having meals with family; consume meal restores and contributes to love. | Already: `ConsumeMealRestore` sets day restoration buff. Love: increment `LoveLevel` or add BondPoints when consuming a meal (and optionally when "meal with family" is true). |
| **Care** | Taking care of self and family (rest, comfort, healing). | Future: care actions add to love/bond. |
| **Building** | Building together (homestead, structures). | Future: completing build orders or placing structures adds to love. |
| **Child** | When a child NPC exists: keeping them safe, fed, and present. | Future: child-care actions add to love. |

**Aggregation (stub):** A single **LoveLevel** (integer 0–N) or **BondPoints** (integer) on PlayerState can represent the current day’s accumulated love. For the stub, one or more of the sources above can add to it (e.g. each meal +1, or each meal sets a tier). Exact formula is placeholder; the hook is that night bonus logic reads this value.

---

## 3. How love scales night bonuses

**How day love translates to night bonus (summary):** Meals, care, and building during the day increase **LoveLevel** (or bond); the day restoration buff (one meal) is one path. At night, that value is read when applying bonuses: stronger astral combat, more spiritual power per collectible, better restoration, or other benefits. Cause → effect: **day activities (meals, care, building) → LoveLevel / day buff → stronger at night.** See [VISION.md](../workflow/VISION.md) § Day and night (goal of the day = build up love → bonuses at night). **Automated check:** `pie_test_runner.py` includes day-buff and love-bonus checks (e.g. `hw.RestoreMeal` then `hw.TimeOfDay.Phase 2` and `hw.TestGrantSpiritualCollect` to verify bonus).

- **Night bonuses** are benefits during the astral phase: e.g. extra spiritual power per collectible, damage reduction, cooldown reduction, or regen. The existing **day restoration buff** gives a fixed bonus (e.g. +1 spiritual power per collectible); the **love** metric can scale that further.
- **Scaling (design):**
  - **Tier-based:** LoveLevel 0 = no bonus, 1 = small bonus, 2 = medium, 3+ = full bonus (e.g. multiplier on spiritual power gained, or extra effect duration).
  - **Linear:** Bonus = base + (LoveLevel * factor). Example: spiritual power per collectible = 1 + (HasDayBuff ? 1 : 0) + (LoveLevel * 0.5).
  - **Thresholds:** At certain LoveLevel thresholds, unlock or amplify specific night effects (e.g. stronger SpiritBurst, or conversion bonus).
- **Stub:** Code that applies night bonuses (e.g. `AHomeWorldSpiritualCollectible::OnCollectVolumeOverlap`, or a future "night bonus" subsystem) can call `PlayerState->GetLoveLevel()` and use it in a placeholder formula (e.g. extra power = LoveLevel, or tier lookup). No need to implement full scaling in the stub; the hook is that the value exists and is read.

---

## 4. Relation to existing systems

| System | Use |
|--------|-----|
| **HasDayRestorationBuff** | One meal (or one qualifying day activity) sets the flag; already used for +1 spiritual power per collectible at night. Love is broader: multiple activities can increase LoveLevel, which can scale that same bonus or others. |
| **AHomeWorldPlayerState** | Holds `LoveLevel` (or `BondPoints`) stub: `GetLoveLevel()`, `SetLoveLevel(int32)`, optional `AddLovePoints(int32)`. Cleared or decayed at dawn (same as day buff) so each day the player must earn it again. |
| **Dawn** | When advancing to dawn, clear or reset LoveLevel (e.g. set to 0) so the next day the player builds it again. |
| **Persistence (future)** | If we want to carry over a "bond" across days (e.g. long-term relationship meter), we can add `SavedLoveLevel` or `SavedBondPoints` to `UHomeWorldSaveGame` and restore on load. Stub does not require persistence. |

---

## 5. Success criteria (T1)

- This design doc exists and defines: how love is earned (meals, care, building, child), how it aggregates (LoveLevel or BondPoints), and how it scales night bonuses (tier or formula).
- PlayerState has a **stub value** (e.g. `GetLoveLevel()` / `SetLoveLevel(int32)`) that can be read when applying night bonuses; no full implementation required.
- Night bonus code (existing or future) can call the stub so the hook is code-ready; actual scaling formula can be placeholder (e.g. +0 for now, or +LoveLevel to spiritual power for testing).
