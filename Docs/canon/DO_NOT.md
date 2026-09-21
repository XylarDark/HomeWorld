# DO_NOT.md

Sacred systems and forbidden tropes. Prefer this over improvising mid-code.

**Sources:** `Docs/00_CANON.md` §7; `Docs/01_GDD_MVP.md` §12; `Docs/21_REAP_SOW.md`; Lead 2026-09-20 combat framing A (amended 2026-09-21 — [COMBAT_DREAM_BIBLE.md](../COMBAT_DREAM_BIBLE.md)); [HOMESTEAD_BIBLE.md](../HOMESTEAD_BIBLE.md); [GATHER_CRAFT_BIBLE.md](../GATHER_CRAFT_BIBLE.md) (Lead 2026-09-21)

## Sacred (do not break / replace silently)

- Homestead as **safe hub** (no combat there)
- FALLBACK glide along `CRUMB_*` (no free-flight controller)
- Day/body vs night/spirit **split verb sets** (`VERBS.md`)
- Six `RES_*` + 6-slot inventory (`SCHEMA.md`)
- One beast pad / three spirits / two nurture targets (MVP counts)
- Shrine portal link: homestead ↔ planet return **only**
- Docs/20 uasset allowlist + AI provenance log
- Existing movement / time / hub owners — read before extending

## Forbidden tropes / systems

| Forbidden | Why |
|---|---|
| Homestead combat | Pillar 1 |
| Kill/HP/weapons/aggro combat (general encounters) | Forbidden for **non-boss** planet content — minigames only (heal/nurture/grow/possess). No trash packs, no weapon-first UX |
| Kill win-condition (including bosses) | Boss win = **seal / banish / end evil** only — no murder fantasy payoff |
| Generic skill trees | Pillars beat systems |
| Free-flight sim / flight energy HUD | Canon + FALLBACK armed |
| Second CharacterMovement / parallel PlayerController | Harness |
| Crafting recipe webs | Gather → store → spend; homestead **named recipes only** at **campfire then cottage** — costs in `SCHEMA.md` / [GATHER_CRAFT_BIBLE.md](../GATHER_CRAFT_BIBLE.md) (demo: campfire/tent→cottage) |
| Invisible walls as primary bounds | HOMESTEAD_BIBLE — edge glide commit; rare immersive mid-map blockers only |
| Co-op drop-in on hub (MVP) | HOMESTEAD_BIBLE — NPC family instead |
| Extra biome / second beast / 7th resource | MVP lock |
| Night flight | Canon |
| Photoreal / grimdark / sci-fi kits | Tone |
| Silent refactors / deleting working files | Harness |
| Worker self-approving a phase | Swarm |
| Two agents writing the same file | Swarm |

## Allowed exception (do not confuse with kill combat)

- Night **placeholder dream-convert** at den/camp (Docs/21): heal/recruit; convert, not kill. **Never on homestead.**
- **Rare boss** vs great/terrible evil (tutorial planet / VS path): **day + night** phase model per [COMBAT_DREAM_BIBLE.md](../COMBAT_DREAM_BIBLE.md) — traversal/interacts by day, spirit blink/possess/heal-strip by night; win = **seal/banish**, not kill. NOW = placeholder volume + phase logs only.
- **Non-boss** planet encounters: four minigame stub families (`MinigameHeal` / `Nurture` / `Grow` / `Possess`) extending the Docs/21 convert path — not DPS combat.
