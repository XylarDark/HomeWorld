# EXIT INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1

**Kind:** Interview EXIT — **SCOPE** (product scope amend), not Research external-info.

**File protocol:** Lead / Conductor paste. Canonical intended path: `Docs/handoffs/research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md`  
**Prompt:** `PROMPT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1`  
**Draft PR:** #235  
**Date:** 2026-09-27  
**Pins:** DET `0a27306` · map `Maps/VS_MVP` · CAP-PROP-GATE schemas on main `f72d5d8` · CAP product **PARKED**  
**Base SCOPE (stays ACCEPTED):** Interview EXIT `PROTOTYPE_T0_V1` + Design `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` (awaiting Lead list stamp — this EXIT does **not** stamp it).  
**Parallel:** #234 feel-library EXIT (this kit) · #237 movement-env canon Do.

---

## Diagnosis

T0 spine is already locked: homestead day loop, glider transit, field gather + rune gate, eject-not-kill, bed→spirit, nurture + portals, avoid 1 / soothe 2. The feature list is a **DRAFT waiting a Lead stamp**, not a hole in verbs.

What was thin in Co (2026-09-27 Lead taste): **feel priorities on that spine**. Early testers should feel *seamless cultivate/nurture fantasy* from movement + ability moments, with greybox env that *sells those notes*. Art polish and NightMix stay later. Without a SCOPE overlay, Design may dress the wrong envelopes, bots may treat night mood as PASS, or juice work may invent a second product track.

This EXIT is an **amend overlay**. It does not replace `PROTOTYPE_T0_V1`, does not invent beats outside the existing SCOPE table, and does not stamp the feature list.

**Unknown closed:** Which T0 rows stay MUST vs wait on a feel bar; north-star words; greybox/prop law; which envelopes to dress first; mechanic-feel rank; DONE-WHEN templates Design may cite; ≤2 docs bites after ACCEPT + Lead greenlight.

---

## Decision

| Option | Verdict |
|--------|---------|
| SCOPE amend overlay now | **Conditional Go** |
| Replace / void `PROTOTYPE_T0_V1` | **No-Go** |
| New MUST beats from feel talks | **No-Go** |
| CAP product / night bot PASS | **No-Go** |
| Feature work or DESKTOP this Interview | **No-Go** |

**Conditional:** Conductor may ACCEPT this EXIT as SCOPE words. Design bites below wait **Lead greenlight** after ACCEPT. List stamp remains a **separate Lead act** on `PROTOTYPE_FEATURE_LIST_V1.md`. #234 feel-library ACCEPT is parallel, not a blocker.

---

## 1. Relationship to T0 — amend overlay (delta only)

**Confirm:** overlay, not replacement. T0 MUST beats + NODE_* inventory freeze remain the floor.

### Stay MUST (no cell change)

All existing MUST rows stay MUST:

Wake · kettle+tea sprint · plant given herb · backpack · glider→field · field gather · rune-before-bed · day-camp eject · night-home-without-bed law · planetside-night eject · bed→spirit · spirit nurture · home↔camp portals · avoid 1 + soothe 2.

CUT stays CUT: player death · quarantined Homestead/DemoMap as primary · CAP/EA reopen.

Already-DEFER stays DEFER: other-plants nurture → daytime seed collect.

### Overlay cells (the only changes)

| Feature / beat | Overlay | Note |
|----------------|---------|------|
| Art-dress / NightMix / camera polish | **DEFER-FEEL-POLISH** (was already “Later Lead polish”) | Explicit: not early-tester bar; not bot PASS |
| Greybox env envelopes for ranked moments (§4) | **MUST-ENV-GREYBOX** | Silhouette / path / weenie only — still greybox/low-poly |
| Juice channels (particles, shake, fancy audio) | **DEFER** until verbs read in greybox | Cite #234 library after that EXIT ACCEPTs |
| Extra plant-nurture loop | **DEFER** (unchanged) | Vision, not first bite |
| Seamless home↔planet | **MUST** (unchanged) + feel bar | See DONE-WHEN templates |
| Stream / partition-ready | **MUST** (unchanged) | Cite A–E only; no new WP API |

No full T0 table reprint. No Research candidate **A** defaults slipped back in.

---

## 2. Feel north star (SCOPE words)

Lead may stamp these 7 lines as overlay language:

1. HomeWorld T0 *feels* like gently **seeding, nurturing, and cultivating** a home and a small world — not like clearing a camp.
2. Early-tester bar = **movement + ability moments read on the first walk** (tea sprint, plant, glide, eject, bed→spirit, nurture, soothe).
3. Art-polish bar is later. Greybox / low-poly props are in-law for T0 envelopes.
4. Seamless home↔planet is part of the fantasy, not a load beat.
5. Bots may prove: actor present, state on/off, labels ⊆ inventory ∩ world, buff readable in log/UI flag, eject lands home not dead, form flags, portal pair, 1 guard + 2 sleepers.
6. Lead-only taste: NightMix, camera romance, cartoon timing curves, “does this *feel* like care,” weight/sink beauty.
7. Convert-not-kill and eject-not-kill stay law. Juice must not teach a lethal verb.

---

## 3. Greybox / prop law

Lock:

- T0 envelope props = **greybox / low-poly OK**.
- Arrange = **math-first** via existing `prop_inventory.schema.json` + `PROP_INVENTORY_V1` + `prop_arrange_gate.schema.json` + `PROP_ARRANGE_GATE_V1`.
- CAP **product** stays **PARKED**. No capture writer, no stills-as-inventory.
- Bright / day default for bot prop work (`tod_light.phase: day`).
- Night = Lead taste. Bots must not PASS night mood.
- Stills = confirm-only after `ready: true`. Missing node ≠ take a picture.
- `prove_labels ⊆ inventory ∩ world` before any later Act. Labels ∉ set → block Act (soft), not invent.

---

## 4. Env-for-feel — prototype envelopes

Dress **greybox** so mechanics feel good. MUST-ENV = first freeze. DEFER-ENV = later dress, still not art-final.

| Envelope | NODE_* / moment | Env dress | Rank |
|----------|-----------------|-----------|------|
| Homestead run | `NODE_WAKE` `NODE_KETTLE` `NODE_BACKPACK` `NODE_BED` + stoop | Intimate interior; silhouette interactables; door = arrival | **MUST-ENV-GREYBOX** |
| Plant slot | `NODE_PLANT_SLOT` | Short walk from stoop; not in glide path | **MUST-ENV-GREYBOX** |
| Glide field | `NODE_GLIDER` → `NODE_FIELD_GATHER` | Perch height + field weenie; landing AABB readable | **MUST-ENV-GREYBOX** |
| Rune on path | `NODE_RUNE` | Landmark before bed; on gather path | **MUST-ENV-GREYBOX** |
| Camp approach | `NODE_DAY_CAMP` + `EJECT_HOME` | Edge + one threat volume; no kill metrics | **MUST-ENV-GREYBOX** |
| Bed / spirit threshold | `NODE_BED` + form flags | Readable interior; gate not a toggle | **MUST-ENV-GREYBOX** (geo only) |
| Nurture | same `NODE_PLANT_SLOT` at `TOD_NIGHT_SPIRIT` | Same slot identity; no second prop | **MUST-ENV-GREYBOX** (identity) |
| Night camp soothe | `NODE_GUARD` `NODE_SLEEPER` `NODE_PORTAL_*` | Same day-camp volume | **DEFER-ENV** dress / lighting (Lead) |
| Extra wild plants | DEFER T0 row | — | **DEFER-ENV** |

Movement-env canon (#237) already names these envelopes. This SCOPE *requires* the MUST-ENV set as product law; it does not invent new nodes.

---

## 5. Mechanic-feel priority order (top 5)

Early-tester “this is the game.” Movement/abilities first, aligned with seed/nurture/cultivate.

| Rank | T0 MUST beat | Why this is the game |
|------|----------------|----------------------|
| 1 | **Glider interact → field** | Seamless home↔planet fantasy. If transit is a load, the product is two maps. |
| 2 | **Kettle + herbs → tea → sprint** | First *ability moment*. Body-work reads as care-fuel, not combat buff. |
| 3 | **Plant given herb + later spirit nurture (same slot)** | Main draw: cultivate. Day plant / night care on one identity. |
| 4 | **Day camp cartoon eject (not lethal)** | Threat without teaching kill. Convert-not-kill starts here. |
| 5 | **Bed→spirit + avoid 1 / soothe 2** | Night form is a threshold + care verb, not a stealth-kill loadout. |

Wake, backpack, gather, rune, night-home law, portals stay MUST for completeness but are **supporting** on the first-tester pass.

---

## 6. Feel DONE-WHEN language (templates)

Design may cite these grep-friendly lines. They do **not** declare any Lead `APPROVE-*`.

```text
FEEL-TEA: tea interact sets sprint buff; buff on/off readable in log or UI flag
FEEL-GLIDE: left NODE_GLIDER, arrived field AABB, no load hang; fail degrades EJECT_HOME
FEEL-PLANT: NODE_PLANT_SLOT accepts day plant; planted marker present near homestead
FEEL-NURTURE: FORM_SPIRIT nurture target == same NODE_PLANT_SLOT as day plant
FEEL-EJECT: EJECT_HOME fired from NODE_DAY_CAMP; player at home; not dead
FEEL-NIGHT-HOME: TOD_NIGHT_HOME => spirit OFF and day abilities OFF
FEEL-BED: bed->spirit blocked until NODE_RUNE unlocked; after rune, bed enables FORM_SPIRIT
FEEL-SOOTHE: camp night proves 1 NODE_GUARD avoid + 2 NODE_SLEEPER soothe (no kill)
FEEL-PORTAL: NODE_PORTAL_HOME pairs with NODE_PORTAL_CAMP in FORM_SPIRIT
FEEL-ENV-GREYBOX: ranked envelopes have silhouette props in PROP_INVENTORY_V1; tod_light.phase=day
```

Bot-proveable = the tokens above. Lead-only = “feels like care,” NightMix, cartoon beat timing, camera romance.

Soft vs closed (existing law, restated not invented): unreadability / missing dress before Act = soft. MUST node marked Present then missing after Act, or eject with no home degrade = closed. Arrange `ready:false` is not a closed fail.

---

## 7. Do bites (max 2 after ACCEPT + Lead greenlight)

Files-only. Exclusive paths. No Python writer. No DESKTOP.

### Bite A — `T0_FEEL_PROP_FREEZE_V1` (prefer)

**Owner:** Design  
**Unknown (one):** Which greybox props occupy the ranked T0 envelopes so later Arrange can score presence without stills?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/PROP_INVENTORY_V1.md` — extend with T0 envelope rows (labels ⊆ existing NODE_* ∩ VS_MVP). Schema `hw.prop_inventory/v1` fields only. Bright/day. PROXY transforms OK.
- Optional sibling: a thin `Docs/handoffs/T0_FEEL_ENVELOPE_INDEX_V1.md` **only if** the inventory file would exceed a readable freeze — prefer **not** to open the sibling; fold envelope_id values into inventory (`ENV_T0_HOME`, `ENV_T0_GLIDE`, `ENV_T0_FIELD`, `ENV_T0_CAMP`, `ENV_T0_BED`).

**Forbidden co-changes:** `Source/**` · `Content/**` · `.uasset`/`.umap` · CAP product · night PASS · AGENTS · A–E · pin bump · feature list stamp · `#234` library body.

**DONE-WHEN:**

```bash
grep -E 'NODE_WAKE|NODE_KETTLE|NODE_PLANT_SLOT|NODE_GLIDER|NODE_FIELD_GATHER|NODE_RUNE|NODE_DAY_CAMP|NODE_BED' \
  Docs/handoffs/PROP_INVENTORY_V1.md
grep -E 'golden_transform|tod_light|phase.*day|envelope_id' \
  Docs/handoffs/PROP_INVENTORY_V1.md
grep -E 'CAP PARK|PARKED|confirm-only' Docs/handoffs/PROP_INVENTORY_V1.md
```

**Blocked until:** this EXIT ACCEPTED **and** Lead greenlight on Bite A. Does **not** require the feature-list stamp (gap-inventory Implement still does).

---

### Bite B — `T0_FEEL_POINTER_AMEND_V1` (optional)

**Owner:** Design  
**Unknown (one):** Can the feature list cite feel DONE-WHEN templates + feel/movement canons without changing MUST/CUT cells?

**Host:** CLOUD · artifact `docs`  
**Exclusive paths:**

- `Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md` — add a short **Feel overlay** subsection: north-star pointer, FEEL-* template names, cites to `GAME_FEEL_CANON_V1` (if #234 Bite 1 landed) and/or `GAME_DESIGN_MOVEMENT_ENV_CANON_V1`. **Do not** edit MUST/CUT/DEFER cells. **Do not** stamp the list.

**Forbidden co-changes:** MUST table rewrite · CAP · AGENTS · A–E · PROP schema fork · DESKTOP.

**DONE-WHEN:**

```bash
grep -E 'FEEL-TEA|FEEL-GLIDE|FEEL-NURTURE|FEEL-EJECT|FEEL-SOOTHE' \
  Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md
grep -E 'amend overlay|greybox|CAP PARK' \
  Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md
# MUST wake row still MUST
grep -E 'Wake / start day' Docs/handoffs/PROTOTYPE_FEATURE_LIST_V1.md
```

**Order:** Bite A first. Bite B only if Lead wants the list file to carry the overlay text. Either bite alone is a legal greenlight.

**Not opened:** Implement mechanic PRs · gap-inventory (that remains post-list-stamp) · night lookdev · Python.

---

## eggbot

N

---

## child Research needed?

**N** — SCOPE is Lead product. External refs live on parallel #234. No additional Research child.

---

## Accept checklist (Conductor)

- [ ] Seven Interview headings were on the prompt
- [ ] EXIT has Diagnosis · Decision · T0 amend table (delta only) · feel north star · greybox/env/mechanic priority · feel DONE-WHEN templates · Do bites ≤2 · eggbot · child Research · this checklist
- [ ] Title line `EXIT INTERVIEW_SCOPE_PROTOTYPE_FEEL`
- [ ] Amend-not-replace T0; no Research A defaults
- [ ] CAP stays PARKED; greybox + math-first explicit
- [ ] Max 2 docs Do; no feature work instruction; no list stamp declared
- [ ] Design owns post-ACCEPT inventory freeze (Bite A)
- [ ] Parallel note: Lead still owes #234 EXIT ACCEPT (if not already) and the separate feature-list stamp

### Fitness greps (EXIT)

```bash
grep -E 'Diagnosis|Do bites|eggbot|child Research|Accept checklist' \
  Docs/handoffs/research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md
grep -E '^#+[[:space:]]*EXIT ' \
  Docs/handoffs/research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md
grep -nEi 'implement now|open DESKTOP Act|run the prove|CAP product Do|APPROVE TOOL SCOUT' \
  Docs/handoffs/research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md && echo FAIL
```

*End EXIT INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1. Overlay only. CAP PARKED. List stamp remains Lead.*
