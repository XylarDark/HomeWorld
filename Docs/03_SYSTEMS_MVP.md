# Docs/03_SYSTEMS_MVP.md

## 1. Status: DONE (P5 / WAVE 4)

Date: 2026-09-16  
Owner: SYS  
Inputs (read-only): `Docs/00_CANON.md`, `Docs/01_GDD_MVP.md`  
Consumers: GP (verb spend checks), PROP (World/Stored meshes), CHA (beast/spirit state reads), later UE GameState

This file is the **data-table contract** for inventory-lite, gather/store counts, beast tame SM, heal, and nurture. No crafting tree. No combat. No seventh resource. No UE C++ in this slice — tables + Blender-demoable rules only.

---

## 2. Inventory-lite — exactly 6 slots

| Rule | Spec |
|---|---|
| Slots | Exactly **6** |
| Contents | At most one stack per `RES_ID` (six resources ⇒ one slot each when full set carried) |
| Stack max | **9** per `RES_ID` (tunable later; do not add a 7th resource) |
| Pickup fail | Gather fails if that `RES_ID` stack is at max **or** empty slots = 0 and `RES_ID` not already held |
| Spend | Tame / heal / nurture decrements stack; at 0 clear slot |
| Forbidden | Equipment grid, weapons, armor, crafting output slots, currency, trade, 7th slot |

**Slot schema (logical):**

| Field | Type | Notes |
|---|---|---|
| `slot_index` | int 0–5 | Fixed six |
| `res_id` | enum / null | One of six `RES_*` or empty |
| `count` | int 0–9 | 0 ⇒ clear `res_id` |

---

## 3. RES_* table (six only)

World = day gather on planet. Stored = homestead transfer. Spend sinks from GDD §5 / §8 / §10. **No crafting recipes.**

| ID | Display | Gather (World) | Store (Stored) | Spend sinks (MVP) | Stack max |
|---|---|---|---|---|---|
| `RES_WOOD` | Wood | Branch / choppable pine node → +1 | Firewood / plank pile | Visual store only | 9 |
| `RES_FIBER` | Fiber | Fern / vine / flax → +1 | Cord rack / basket | Visual store only | 9 |
| `RES_STONE` | Stone | Loose rock → +1 | Path-stone / tool-head pile | Visual store only | 9 |
| `RES_BERRY` | Forage fruit | Berry bush → +1 | Bowl / drying rack | **Tame offer** (V4) | 9 |
| `RES_HERB` | Herb | Herb cluster → +1 | Poultice shelf | **Heal** (V6); alternate **tame offer** | 9 |
| `RES_SEED` | Spirit seed | Faint day plant → +1 | Night crop planter | **Nurture crop** (V7); optional heal alternate | 9 |

**Gather rules:** One interact = +1 unit. Node cooldown or deplete until dawn. Prompt shows `RES_ID`. Fail if inventory cannot accept (§2). Day/body only.

**Store rules:** Homestead only. Transfer 1 unit inventory → Stored count on matching prop. Does not create new RES types.

---

## 4. Spend mapping (from GDD)

| Verb | Action | Consumes | On success |
|---|---|---|---|
| V4 Tame — Offer | Offer food to beast | 1× `RES_BERRY` **or** 1× `RES_HERB` | Progress toward `tamed` |
| V6 Heal (each of 3) | Heal one hurt spirit | 1× `RES_HERB` (default) **or** 1× `RES_SEED` (alternate) | Spirit `hurt` → `healed` |
| V7 N1 Crop | Nurture garden planter | 1× `RES_SEED` (or already planted waiting night nurture) | Target → `M_Nurtured` on |
| V7 N2 Stored | Nurture stored pile/rack | 1× matching RES in inventory **or** Stored count ≥ 1 already on rack (default pile: `RES_WOOD` Stored) | Prop → `M_Nurtured` on |

`RES_WOOD` / `RES_FIBER` / `RES_STONE` have **no** spend sink beyond visual store in MVP.

Wrong item for tame = soft reject, no damage, no state advance.

---

## 5. Beast states — wild / cautious / tamed / helper

**Identity:** One `SK_Beast_Small` on one planet beast pad. Material family `M_BeastStylized`. No HP, no weapons, no aggro.

| State | Enter when | Player-facing | Exit |
|---|---|---|---|
| `wild` | Spawn / dawn reset if never offered | Idle on pad; no follow | Approach into caution ring → `cautious` |
| `cautious` | Enter pad radius / approach | Idle anim; wait for offer | Offer food → bond wait; leave before offer → may return `wild` if Step 1 never done |
| `tamed` | Offer succeeded + calm Wait ~3–5 s | Tame-mark readable; stays near pad | Optional Call → `helper` |
| `helper` | Player Call / Befriend while `tamed` (day) | May follow planet path or enable constrained glide assist if mesh ready | Dawn may persist; never combat |

**State machine steps (GDD §6):**

| Step | Condition | Action | Result |
|---|---|---|---|
| 0 Encounter | Enter pad radius | Approach slowly | → `cautious` |
| 1 Offer | Has `RES_BERRY` or `RES_HERB` | Use Offer | Consume 1 food; progress |
| 2 Bond | Offer succeeded | Hold Wait in calm radius ~3–5 s | → `tamed` |
| 3 Helper (optional) | Already `tamed`; day | Use Call once | → `helper` |

**Hard rules:** Leaving pad mid-bond after Step 1 → reset to `cautious` (not `wild`). Combat inputs do not exist.

---

## 6. Heal — hurt → healed (×3)

**Identity:** Three spirit wisps at / around one planet `SM_SpiritWound`. Night/spirit only. Material `M_SpiritUnlit`.

| Field | Spec |
|---|---|
| Count | Exactly **3** (Spirit A/B/C) |
| Initial | All `hurt` at night arm |
| Input | Night Use + consume 1× `RES_HERB` (or `RES_SEED`) per spirit |
| Success | Per spirit: `hurt` → `healed`; soft emissive on `M_SpiritUnlit` |
| Complete | A+B+C all `healed` ⇒ V6 done |
| Fail | No resource / day form / already healed → idle or prompt |
| Order | Any order; 2–4 s channel each |
| Forbidden | Fourth spirit, combat, capture minigame, day heal |

---

## 7. Nurture — 2 targets → `M_Nurtured`

Homestead only. Night/spirit. Apply `M_Nurtured` (or Nurtured on).

| Target ID | Location | Requires | Success |
|---|---|---|---|
| `N1_Crop` | Raised garden planter | 1× `RES_SEED` (or planted seed waiting nurture) | Planter → `M_Nurtured` on |
| `N2_Stored` | Stored pile/rack (default `RES_WOOD` Stored) | 1× matching RES **or** Stored ≥ 1 on rack | Prop → `M_Nurtured` on |

Both complete ⇒ V7 done. Day: visible, nurture blocked. Already nurtured → idle success flash only.

---

## 8. Day / night interaction gates (SYS side)

| Mode | Gather | Beast tame | Heal | Nurture | Store transfer |
|---|---|---|---|---|---|
| Day / body | On | On | Off | Off | On |
| Night / spirit | Off | Off (idle) | On | On | Off (optional read-only) |

Form / NightMix ownership is **GP**; SYS only gates spends and state writes by form flag from GP.

---

## 9. Explicit out-of-scope

- Crafting tree / recipe web
- Combat, HP, weapons, aggro
- Extra resources beyond the six `RES_*`
- Extra beasts, fourth spirit, third nurture target
- Inventory beyond 6 slots
- Flight / glide / portal movement (GP)
- Art / meshes (PROP, CHA, ENV)
- UE C++ this wave
- Editing `PHASE_BOARD` or starting WAVE 5

---

## Appendix — Ownership

| System | Owner | This file section |
|---|---|---|
| 6-slot inventory, RES_*, gather/store counts | SYS | §§2–4 |
| Beast SM wild→helper | SYS | §5 |
| Heal hurt→healed ×3 | SYS | §6 |
| Nurture flags → `M_Nurtured` | SYS | §7 |
| Walk, form, glide, portal, time→NightMix | GP | `Docs/03_GAMEPLAY_MVP.md` |

End of SYSTEMS MVP (P5).
