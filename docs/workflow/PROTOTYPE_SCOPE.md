# HomeWorld – Prototype scope (vertical slice)

Scoping document for the 30-day demonstrable prototype. Update when you lock the "beautiful corner" (e.g. after Day 10) and when you choose the one moment for the vertical slice. See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice) and [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md).

**As of 2026-03-02 (run 4 of 4 toward polished MVP):** Chosen **moment** = Claim homestead; chosen **corner** = Homestead compound (see High-level below).

---

## High-level

- **Gameplay loop:** Explore → fight → build (solo, 2–3h). Context: family taken; lone wanderer secures a base for the rescue.
- **Creative pillars:** Love as Epic Quest; combat + bonds; roles (casual vs hardcore).
- **Chosen moment:** **Locked: Claim homestead** — player places first home asset (P) after exploring/harvesting. (Alternatives for future: First harvest, Dungeon approach, Planetoid POI. See [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).)
- **Chosen corner:** **Locked: Homestead compound** — DemoMap/Homestead with placed buildings + resource nodes + PCG. (Alternatives: Forest approach, Planetoid POI cluster, Dungeon entrance. See [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).)
- **As of:** 2026-03-02 (run 4 of 4 toward polished MVP). Moment and corner locked as above.

---

## Week 1 playtest (vision gate)

Per [VISION.md](VISION.md): **Week 1 playtest goal — Survive 3 missions: crash → scout → boss → claim home.**

| Beat | How to verify |
|------|----------------|
| **(1) Crash** | Start from crash/landing state: open DemoMap or Homestead; PIE starts with character spawned. Sign-off: character present, level loaded. |
| **(2) Scout** | Explore the map: move, harvest (E on BP_HarvestableTree), optional portal to planetoid. Sign-off: harvest works; explore loop playable. |
| **(3) Boss** | Reach or trigger a boss encounter (e.g. dungeon entrance, key-point boss at night with `hw.TimeOfDay.Phase 2` and KeyPoint-tagged actor or `KeyPointBossSpawnDistance` > 0). Sign-off: boss placeholder or encounter triggerable. |
| **(4) Claim home** | Place first home asset (P) after exploring/harvesting; building spawns. Sign-off: GA_Place / TryPlaceAtCursor works; "claim homestead" moment complete. |

See [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 for pre-demo run sequence and [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) for playtest sign-off.

---

## Day/night and astral (MVP scope)

Aligned with [VISION.md](VISION.md) **Day and night: physical and spiritual worlds**:

- **Day (physical):** **Daytime mechanics (vision):** (1) **Support/healer/caretaker** — cooking and having meals; (2) **Explorer/builder** — collecting resources, building, exploring the planetoid; (3) **Later game** — child NPC to take care of and keep an eye on. **Goal:** Build up **love** (meals, care, building, child care) → **bonuses used during the night**. Building, cooking, resources, socializing; horses and tools; physical goods. **No death mechanics during the day** — the day is safe. **Restoration:** Health and other losses from astral combat are **not** restored at dawn; they are restored **during the day** through food, care, and wholesome living. Day activities grant **buffs and love-based bonuses** for the next night. See [VISION.md](VISION.md) § Day and night.
- **Night (spiritual/astral):** Astral bodies defend the land; spirit abilities, flight, combat vs spirits/monsters; spiritual artefacts and power. **Astral death:** if we die in astral form we return to our body and wake up in the morning — no permanent death from night combat. How you spent the day (food, care, bonds) affects restoration and buffs available for the night.
- **Combat:** **Placeholder only** until a full vision board pass on combat mechanics. Placeholder abilities, UI, and spawn stubs are fine; avoid deep combat system work until the vision board.
- **Planetoid and homestead (vision):** When on a planetoid, the **homestead lands and appears** on it; you **venture out** from there. When you **complete a planetoid** you move on to another (homestead travels to the next). See [VISION.md](VISION.md) § Campaign summary.
- **Vanquishing (vision):** Combat **does not kill** — it **strips foes of their sin** and **converts them to their "loved" version**. Converted monsters can become **vendors**, **helpers**, **quest givers**, or **join the homestead as pets or workers**. See [VISION.md](VISION.md) § Day and night.
- **Night encounters (vision):** Two parts — (1) **waves at home** (defend and convert), (2) **packs across the planetoid** (explore to convert) plus **bigger monsters and bosses** at key points. Goal: limited time per night; balance defend vs explore; progress until you can clear a full planetoid in one night (all foes converted). See [VISION.md](VISION.md) § Day and night.
- **Combat variety (vision):** **Defend (waves at home):** Defenses around homestead; **ranged attacks** from defenses or **ground AOE** attacks. **Planetoid (away from home):** **Combos** and **single-target damage**. Variety lets you progress without building both at once; **end-game** = use AOE or single-target in either situation. See [VISION.md](VISION.md) § Combat variety.
- **Astral-by-day:** Per [VISION.md](VISION.md) § MVP full scope, the ability to **enter the astral during the day** is **in MVP scope** (progression unlock or stub).

---

## Asset list by type (to-do for the slice)

| Type | Needed for prototype | Notes |
|------|----------------------|--------|
| Player | 1 character, movement, GAS | FAB / Primitive / Polygon; see STACK_PLAN Free assets. |
| Enemies | 1+ types for scout/boss | Placeholder or free pack. |
| Allies (family) | Protector, Healer, Child | Primitive Characters or Polygon; Days 11–15. |
| Buildings | Homestead compound, outbuildings | Medieval Village or Polygon; Days 6–10. |
| Environment | Forest biome, homestead area | Quixel + one env pack; PCG + placed. |
| Items / resources | Resource nodes, harvestables | BP_WoodPile etc.; see AGENTIC_BUILDING. |
| Boss | 1 boss for "claim home" beat | Days 24–25. |

Update this table as you lock assets (e.g. "Quixel: forest; Medieval Village: homestead").

---

**See also:** [STACK_PLAN.md](../STACK_PLAN.md) (Free assets for prototype), [VISION.md](VISION.md), [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md).
