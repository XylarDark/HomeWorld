# VERBS.md

**Status:** LOCKED allowlist  
**Rule:** If a verb is not listed here (or in the Docs/21 site actions below), **do not implement it**.

**Sources:** `Docs/00_CANON.md` §3; `Docs/01_GDD_MVP.md` §4; `Docs/21_REAP_SOW.md`

## Day / body only

| Verb ID | Name | Result (summary) |
|---|---|---|
| V1 | Walk homestead | Reach island POIs; soft pushback off-nav |
| V2 | Glide island → planet | FALLBACK scripted `CRUMB_*` → landing; ~12–40 s |
| V3 | Gather | Day Use on World node → +1 `RES_*`; ~1.5–3 s |
| V3b | Store transfer | Homestead: inventory → Stored count (1 unit) |
| V4 | Encounter / tame | Beast pad: offer food → `wild`→`cautious`→`tamed`(→`helper`) |
| RS-Reap | Collect / claim at sites | Trees/rocks/flowers/den/camp/special day bonuses (Docs/21) |

## Night / spirit only

| Verb ID | Name | Result (summary) |
|---|---|---|
| V5 | Portal A ↔ B | `SM_Shrine_Homestead` ↔ `SM_Shrine_Return`; ~3–6 s |
| V6 | Heal ×3 | Consume herb/seed; spirit `hurt`→`healed` |
| V7 | Nurture ×2 | Homestead N1 crop + N2 stored → `M_Nurtured` |
| RS-Sow | Nurture / influence sites | Night half of Docs/21 site kit |
| RS-Dream | Placeholder dream-convert | Den/camp: heal/recruit; **convert, not kill**; no homestead |

## Either / cycle

| Verb ID | Name | Result |
|---|---|---|
| V1 | Walk homestead | Same walk volumes; spirit has **no** flight |
| V8 | Return / dawn | Portal home and/or Rest → body; NightMix → 0 |

## Forbidden verb patterns

- Homestead combat / attack / aggro
- Free-flight / night glide
- Crafting tree / recipe craft
- Kill win-condition combat
- Any verb not in this file without Lead append to `DECISIONS.md`
