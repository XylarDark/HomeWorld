# SCHEMA.md

**Status:** LOCKED columns + ranges (pointer)  
**Source of truth tables:** `Docs/03_SYSTEMS_MVP.md`  
**Rule:** Schema before new data rows. Do not invent IDs outside these enums.

## Item / inventory

| Field | Type | Legal range |
|---|---|---|
| `slot_index` | int | 0–5 (exactly 6 slots) |
| `res_id` | enum \| null | `RES_WOOD` \| `RES_FIBER` \| `RES_STONE` \| `RES_BERRY` \| `RES_HERB` \| `RES_SEED` \| empty |
| `count` | int | 0–9; 0 clears `res_id` |

No 7th resource. No equipment/weapons/currency slots.

## Creature tame states

| Field | Legal values |
|---|---|
| `beast_id` | `SK_Beast_Small` only (MVP) |
| `state` | `wild` → `cautious` → `tamed` → `helper` |
| Offer cost | 1× `RES_BERRY` **or** 1× `RES_HERB` |
| Bond wait | ~3–5 s in calm radius |

## Spirit heal

| Field | Legal |
|---|---|
| Count | Exactly 3 (A/B/C) |
| State | `hurt` \| `healed` |
| Cost each | 1× `RES_HERB` (default) or 1× `RES_SEED` (alternate) |
| Form gate | Night / spirit only |

## Shrine / portal

| Field | Legal |
|---|---|
| Link | Homestead shrine ↔ planet return shrine **only** |
| Form | Night / spirit both ways |
| Channel+transit | ~3–6 s |
| Day | Locked (“at night”) |

## Nurture

| Target ID | Requires | Success |
|---|---|---|
| `N1_Crop` | 1× `RES_SEED` (or planted waiting nurture) | `M_Nurtured` on |
| `N2_Stored` | Matching RES or Stored ≥ 1 (default wood pile) | `M_Nurtured` on |

## Day / night clock

| Phase | NightMix intent | Form |
|---|---|---|
| Day | ~0.0 | Body |
| Dusk | 0 → 1 over ~4–8 s | Swap to spirit |
| Night | ~0.85–1.0 | Spirit |
| Dawn | 1 → 0 over ~4–8 s | Swap to body |

Console (existing): `hw.TimeOfDay.SetPhase N` — do not add a parallel clock without reading existing time/hub code.

## Docs/21 site IDs (stubs)

Legal site kinds: `trees` \| `rocks` \| `flowers` \| `animal_den` \| `humanoid_camp` \| `special`.  
Day/night bonus fields: TODO numeric magnitudes (proposed 1.1–1.5× next-half yield; rationale: readable but not snowball) — stamp in `DECISIONS.md` before hardcoding.
