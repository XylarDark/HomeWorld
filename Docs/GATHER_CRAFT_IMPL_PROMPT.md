# Gather & craft implementation prompt (agent / UE Copilot)

Source of truth: `Docs/GATHER_CRAFT_BIBLE.md`.

```
Implement HomeWorld gather/craft demo spine per Docs/GATHER_CRAFT_BIBLE.md NOW section only. Change only gather mapping, craft interact, placeable spawn, and progression flag files required. Do not implement shop functional craft, skill trees, weapon smithing, or a 7th RES.

LOCKED NOW (Lead A1/B1/C1/D1)
- Six RES only. A1 display: flint → RES_STONE, grass → RES_FIBER (flavor copy/UI — IDs unchanged).
- Day site→RES: trees→WOOD, rocks→STONE, flowers→FIBER and/or HERB rotate, berry→BERRY, seed pods→SEED. Den/camp/special stay Docs/21 — not primary miners.
- Named recipe costs (campfire station until cottage kitchen unlock):
  * Campfire: 1 WOOD + 1 STONE + 1 FIBER
  * Tent: 3 WOOD + 2 FIBER
  * Torch: 1 WOOD + 1 FIBER
  * Tame bait: 1 BERRY or 1 HERB
  * Heal salve: 1 HERB or 1 SEED
  * Fish gear: 1 FIBER + 1 BERRY
- Spend source: prefer Stored first, then inventory (NOTE Lead-swappable — log if inventory-only).
- Demo progression RES spend: campfire + tent recipes only; then PROGRESS:COTTAGE_UNLOCK at campfire (flag/log).
- C1 placeholders ONLY (props + enter volumes + logs, no RES spend): woodshop, textile shop, research shop; cottage kitchen/bedrooms/living room + cauldron prop.
- D1 craft UX: campfire early; cottage kitchen/stations after unlock (same recipe IDs, rebinding OK).
- Forbidden: crafting skill web, 7th RES, weapon smithing, functional shop craft NOW.

LATER (do not build): full upgrade-track buildings, functional magic/cooking/potion loops, shop craft economies.

DONE WHEN
- GATHER: RES_WOOD + RES_STONE + RES_FIBER from mapped day sites
- CRAFT: campfire stub succeeds (log + place or spawn stub)
- CRAFT: tent stub succeeds
- PROGRESS:COTTAGE_UNLOCK logged after demo conditions
- PLACEHOLDER:* enter logs from shop/room volumes
- No 7th RES; no weapon smithing
- PLAYTEST: day gather trio → craft campfire → gather → craft tent → unlock log → walk placeholder shop volume
```
