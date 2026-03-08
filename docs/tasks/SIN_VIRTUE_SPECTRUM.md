# Sin/virtue spectrum (design)

**Purpose:** Design for the moral system per [VISION.md](../workflow/VISION.md) § Moral system: Seven Sins & Virtues. Skills, passives, and abilities are tied to the seven pairs; each axis is a spectrum from **-1** (sin) to **0** (neutral) to **+1** (virtue). **Implementation deferred; design only.**

**See also:** [PLANETOID_DESIGN.md](../PLANETOID_DESIGN.md) (sin-themed levels), [VISION.md](../workflow/VISION.md) § Moral system.

---

## 1. The seven axes

| Sin (-1) | Virtue (+1) |
|----------|-------------|
| Greed | Generosity |
| Gluttony | Abstinence |
| Sloth | Productivity |
| Wrath | Grace |
| Pride | Humility |
| Envy | Fulfillment |
| Lust | Love |

**0 (neutral)** is shared (e.g. Trade for Greed/Generosity). **-1** and **+1** are commitment. Environments and factions in the 7 levels are shaped by these aspects; player choices influence the player’s level on each axis.

---

## 2. Where we might read/display (future)

- **HUD stub:** Four lines on the in-game HUD (AHomeWorldHUD): **Pride: N**, **Greed: N**, **Wrath: N**, and **Envy: N** (sin/virtue stub), value stubs 0; each axis is -1 (sin)..0 (neutral)..+1 (virtue). Design only; no gameplay. See [VERTICAL_SLICE_CHECKLIST.md](../workflow/VERTICAL_SLICE_CHECKLIST.md) §3.1 (HUD metrics). Additional axes or a full panel are future work.
- **SaveGame key:** Persist per-axis values (e.g. `SinVirtuePride`, `SinVirtueGreed`, `SinVirtueWrath`, `SinVirtueEnvy`, …) in `UHomeWorldSaveGame` when we implement moral persistence.
- **Console:** The commands **`hw.SinVirtue.Pride`**, **`hw.SinVirtue.Greed`**, **`hw.SinVirtue.Wrath`**, and **`hw.SinVirtue.Envy`** are implemented as stubs: they log the current axis value (e.g. `Pride: 0`, `Greed: 0`, `Wrath: 0`, `Envy: 0`) to the Output Log. Use in PIE to read sin/virtue axes; documented in [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md). No gameplay implementation; design only.

---

## 3. Implementation status

**Design only.** No gameplay implementation in MVP. HUD shows four axes (Pride, Greed, Wrath, Envy) with stub values; console commands `hw.SinVirtue.Pride`, `hw.SinVirtue.Greed`, `hw.SinVirtue.Wrath`, and `hw.SinVirtue.Envy` log stub values (see CONSOLE_COMMANDS.md). When implementing gameplay: add stub getters (e.g. per-axis or aggregate) on a suitable subsystem or PlayerState; use in level theme, loot, or ability scaling per VISION.
