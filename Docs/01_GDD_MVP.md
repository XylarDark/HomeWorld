# Docs/01_GDD_MVP.md

## 1. Status: IN PROGRESS (P1)

Date: 2026-09-16  
Owner: DES  
Inputs (read-only): `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`  
Consumers: GP (verbs / transit / day-night), SYS (gather / inventory / tame / heal / nurture)

This file is the executable design contract for WAVE 1 Track A. GP/SYS implement from tables below; do not open design questions mid-slice.

---

## 2. Player fantasy + tone (from canon)

**Fantasy:** You keep a warm floating homestead above a readable pine world. By day (body) you leave the lookout, take a constrained route down, gather six materials, meet one small beast, and come home. By night (spirit) you use shrine portals both ways, heal three wounded spirits, and nurture two homestead targets so home glows with care.

**Tone:** Warm, readable, handmade, hopeful. Not cutesy-infantile. Not grim. Not photoreal. Not sci-fi. (Canon §9.)

---

## 3. Day/body vs Night/spirit loop (canonical)

| Mode | Form | Where | Core verbs | Transit |
|---|---|---|---|---|
| Day | Body | Homestead walk + planet slice | Walk, Glide, Gather, Encounter/Tame, Return/dawn | Constrained glide island → planet (preferred); FALLBACK scripted spline |
| Night | Spirit | Homestead first, then planet via shrine | Portal both ways, Heal ×3, Nurture ×2, Return/dawn | Shrine portal homestead ↔ planet only. No night flight. |

**Cycle rules (implementable):**

1. **Dawn → Day/Body:** Player is body form on homestead. Spirit layer off / NightMix → 0. Gather nodes and beast pad active.
2. **Day departure:** From lookout / glider perch, start Verb 2 (glide or FALLBACK). Land at planet landing circle.
3. **Day slice:** Walk path 2–4 min; gather; encounter/tame one beast; optional return via Verb 8 (portal if night-armed) or hold until dusk.
4. **Dusk → Night/Spirit:** At homestead shrine (or on return), form swaps to spirit. NightMix → 1; spirit layer visible; gather/beast interactions idle or blocked.
5. **Night loop:** Portal homestead ↔ planet (Verb 5); heal three spirits at wound site(s); nurture two homestead targets; return / sleep → dawn (Verb 8).
6. **Homestead is hub.** Planet is the same world slice visible from lookout — not a second game.

**Lookout test (WLD gate, design requirement):** From lookout, player can point at landing, portal exit, first harvest, and way home.

---

## 4. Eight verbs (executable)

Each verb: trigger, player action, success, fail/idle, approx duration (seconds).

### V1 — Walk homestead

| Field | Spec |
|---|---|
| Trigger | Day or night; player on Hero Island navmesh / walk volumes |
| Player action | Move body or spirit on cabin / garden / path / pines / lookout / shrine / glider perch |
| Success | Reach named POI without leaving island bounds; camera readable per Shot 1–2 framing |
| Fail / idle | Off-nav → soft pushback or stop; no fall-to-void death loop in MVP |
| Duration | Continuous; cabin→lookout ~15–25 s; full island circuit ~45–90 s |

### V2 — Glide / fly island → planet (or scripted stand-in)

| Field | Spec |
|---|---|
| Trigger | Day/body only. Player enters lookout / glider perch interact volume + confirm |
| Player action | **Preferred:** constrained glide on air-current along visible islets toward landing circle (limited steering on rail/corridor; not free-flight). **FALLBACK:** scripted spline down (Conductor may arm without meeting) |
| Success | Touchdown on planet landing circle; control restored to walk |
| Fail / idle | Leave volume without confirm → idle. Abort mid-glide (if allowed) → soft reset to perch or last safe crumb. Night: verb unavailable |
| Duration | Preferred constrained ~20–40 s; FALLBACK scripted ~12–25 s |

### V3 — Gather 6 resources

| Field | Spec |
|---|---|
| Trigger | Day/body; interact prompt on World gather node when inventory has a free slot for that RES_ID (or stack rules in §10) |
| Player action | Hold / press Use on World node (branch/pine, fern/vine/flax, loose rock, berry bush, herb cluster, faint day seed plant) |
| Success | World node depletes or goes cool-down; +1 of matching RES_ID in inventory; Stored form available later via store interact at homestead |
| Fail / idle | Inventory full for that type → prompt “full”; night/spirit → gather disabled; already depleted → idle |
| Duration | Per gather ~1.5–3 s channel; full six-resource pass on slice ~90–180 s walk+gather |

### V4 — Encounter / tame 1 beast (no combat)

| Field | Spec |
|---|---|
| Trigger | Day/body; player enters beast pad proximity (one pad on planet slice) |
| Player action | Approach → offer food from inventory (prefer RES_BERRY or RES_HERB) → hold calm / Wait until state advances. Optional later: mount/helper for constrained glide assist if CHA provides saddle/glider socket — still not free-flight |
| Success | State reaches **tamed** (then optional **helper**). See §6 |
| Fail / idle | No food offered → stays wild/cautious and idles. Wrong item → soft reject, no damage. Combat inputs do not exist |
| Duration | Encounter read ~5–10 s; full tame chain ~20–45 s |

### V5 — Portal night island ↔ planet

| Field | Spec |
|---|---|
| Trigger | Night/spirit; interact at homestead shrine **or** planet return shrine |
| Player action | Use shrine → short portal transit to the linked shrine |
| Success | Arrive at opposite shrine; same two places only; spirit form retained |
| Fail / idle | Day/body → portal locked (or prompt “at night”). Mid-day shrine is landmark only |
| Duration | Channel + transit ~3–6 s each way |

### V6 — Heal 3 spirits

| Field | Spec |
|---|---|
| Trigger | Night/spirit; interact on hurt spirit / spirit-wound site (planet; one wound site hosts or spawns the three) |
| Player action | Approach hurt wisp → Use heal (consumes RES_HERB or RES_SEED per heal — SYS: 1 unit each). Repeat until three healed |
| Success | Each spirit: hurt → healed on `M_SpiritUnlit` state. All three healed = verb complete |
| Fail / idle | No required resource → prompt need. Day → spirits not interactable / layer off |
| Duration | Per heal ~2–4 s; three heals ~15–40 s including walk |

### V7 — Nurture 2 homestead targets

| Field | Spec |
|---|---|
| Trigger | Night/spirit; at homestead nurture volumes (garden crop + stored material rack/pile) |
| Player action | Use on target while holding required resource (see §8) |
| Success | Target gains nurtured state (`M_Nurtured` on); both targets done = verb complete |
| Fail / idle | Missing resource / day form → blocked. Already nurtured → idle success flash only |
| Duration | Per nurture ~2–4 s; both ~10–20 s |

### V8 — Return / dawn cycle

| Field | Spec |
|---|---|
| Trigger | (A) Night portal home after planet work, or (B) Interact sleep / dawn at cabin / shrine when night loop goals met or player elects rest |
| Player action | Portal home and/or confirm Rest → dawn |
| Success | Player on homestead in body form; NightMix → 0; spirit layer off; day gather/beast available again. Optional: persist tame + nurtured + inventory |
| Fail / idle | Rest mid-critical channel → cancel channel, no time skip |
| Duration | Portal return ~3–6 s; dawn transition ~4–8 s |

---

## 5. Six resources — interact table (gather / store)

World = gather on planet (day). Stored = place / convert at homestead storage prop. No crafting tree: gather → carry → store / spend. Inventory holds RES_IDs only (see §10).

| ID | Resource | Gather (World) | Store (Stored) | Spend sinks (MVP) |
|---|---|---|---|---|
| RES_WOOD | Wood | Day Use on branch / choppable pine node → +1 Wood | Homestead firewood / plank pile interact → World consumed from slot, Stored mesh count++ | Visual store only in MVP (no recipe web) |
| RES_FIBER | Fiber | Day Use on fern / vine / flax → +1 Fiber | Cord rack / basket → Stored cord | Visual store only |
| RES_STONE | Stone | Day Use on loose rock → +1 Stone | Path-stone / tool-head pile → Stored | Visual store only |
| RES_BERRY | Forage fruit | Day Use on berry bush → +1 Berry | Bowl / drying rack → Stored | **Tame offer** (V4); optional eat = no combat heal, flavor only if implemented |
| RES_HERB | Herb | Day Use on herb cluster → +1 Herb | Poultice bundle shelf → Stored | **Heal** (V6); alternate **tame offer** |
| RES_SEED | Spirit seed | Day Use on faint day plant (rare node) → +1 Seed | Night crop planter receives seed for nurture | **Nurture crop** (V7); optional **heal** alternate if SYS prefers seed over herb for one spirit |

**Gather rules:** One interact = one unit. Node cooldown or deplete until dawn. Prompt shows RES_ID. Fail if no free inventory handling (§10).

**Store rules:** Homestead-only. Transfer 1 unit inventory → Stored count. Does not create new RES types.

---

## 6. One beast — encounter + tame (no combat)

**Identity:** Single small quadruped `SK_Beast_Small` on **one** beast pad (planet slice). Material family `M_BeastStylized`. Optional glider/saddle socket for constrained assist only.

**States (SYS):** `wild` → `cautious` → `tamed` → `helper`

| Step | Condition | Player action | Result | Time |
|---|---|---|---|---|
| 0 Encounter | Enter pad radius | Approach slowly (move into caution ring) | Enter `cautious`; idle anim; no flee-to-combat | ~3–5 s |
| 1 Offer | Has RES_BERRY or RES_HERB in inventory | Use Offer on beast | Consume 1 food; progress meter or second beat | ~2–3 s |
| 2 Bond | Offer succeeded | Hold Wait / stay in calm radius ~3–5 s | → `tamed`; tame-mark slot readable | ~3–5 s |
| 3 Helper (optional) | Already `tamed`; day | Use Befriend / Call once | → `helper`; may follow on planet path or enable preferred glide assist if mesh ready | ~2 s |

**Hard rules:** No HP, no weapons, no aggro combat. Wrong item = reject VFX + stay state. Leaving pad mid-bond resets to `cautious` not `wild` if Step 1 done.

---

## 7. Three spirits — heal steps

**Identity:** Three spirit wisps (hurt / healed) using `M_SpiritUnlit`. Located at / around one planet **spirit-wound site** (`SM_SpiritWound` placeholder). Night/spirit only.

| Spirit | Hurt cue | Heal input | Success | Fail |
|---|---|---|---|---|
| Spirit A | Dim / cracked emissive at wound | Night Use + consume 1× RES_HERB (or RES_SEED) | → healed; soft emissive | No resource / day form |
| Spirit B | Same family, second spawn/slot | Same as A | → healed | Same |
| Spirit C | Same family, third spawn/slot | Same as A | → healed; V6 complete when A+B+C healed | Same |

**Sequence:** Any order. Per heal: trigger volume → confirm → 2–4 s channel → state flip hurt→healed. No combat, no capture minigame, no fourth spirit.

---

## 8. Two nurture targets (crop + stored material)

Homestead only. Night/spirit. Apply `M_Nurtured` (or Nurtured on).

| Target | Location | Requires | Player action | Success |
|---|---|---|---|---|
| **N1 — Crop** | Raised garden planter (Shot 2) | 1× RES_SEED in inventory (or already planted seed waiting night nurture) | Night Use on planter | Planter → nurtured glow / growth read |
| **N2 — Stored material** | Homestead stored pile/rack (wood firewood **or** fiber cord — pick one prop; default **RES_WOOD Stored** pile) | 1× matching RES in inventory **or** Stored count ≥ 1 already on rack | Night Use on stored prop | Stored prop → `M_Nurtured` on |

Both complete = V7 done. Day: targets visible but nurture blocked.

---

## 9. Transit

### Preferred — constrained glide (day/body)

1. Player at lookout / glider perch (Shot 3 departure).
2. Confirm → enter air-current corridor along 3–5 visible islet crumbs.
3. Limited lateral influence only; forward progress on route; no open sky free-flight, no flight HUD implying sim.
4. Exit: landing circle (Shot 4).

### FALLBACK — scripted spline

If preferred slips: Conductor arms **Flight fallback**. One-way scripted glide lookout → landing circle. No steering beyond camera follow. Still day-only.

### Portal (night/spirit) — both ways

- Homestead shrine ↔ planet return shrine only.
- Both directions required in MVP (even under FALLBACK).
- No third map. No night flight.

---

## 10. Inventory-lite — 6 slots only

| Rule | Spec |
|---|---|
| Slots | Exactly **6** slots |
| Contents | At most one stack per RES_ID (six resources ⇒ one slot each when full set carried) |
| Stack size | MVP default stack max **9** per RES_ID (SYS may tune; do not add 7th resource) |
| Pickup | Gather fails if that RES_ID stack is at max **or** if empty slots = 0 and RES_ID not already held |
| No | Equipment grid, weapons, armor, crafting output slots, currency, multiplayer trade |

Spend (tame / heal / nurture) decrements stack; at 0 clear slot.

---

## 11. Teaching beats tied to shots 1–5

Design teaches by framing + first successful verb — not tutorials with combat or free-flight.

| Shot | Teach | Verb / system | Pass criteria |
|---|---|---|---|
| **1** Homestead night lookout | Hub fantasy: home above world; warm cabin vs cool moon; where planet / path / rooftops are | Orientation for V1, V5, V8 | Player (or camera) can point landing, portal exit, harvest zone, way home |
| **2** Cabin + garden close | Homestead care surfaces: warm windows, planters, path = nurture + store stage | Pre-teach V7 (N1 crop) + store props | Planters and path readable; windows glowing |
| **3** Glide departure | Leaving home is a **route**, not a flight sim | V2 preferred or FALLBACK | Trajectory + islets readable; no free-flight HUD |
| **4** Planet landing day | Arrival clearing; pine path continues; gather/beast space | V2 success → V3 / V4 setup | Open landing; no combat staging; same pine language |
| **5** Spirit portal arrival night | Night spirit transit = shrine portal; heal/nurture world | V5 → V6 (and return for V7) | Portal arrival soft spirit cue; handmade hopeful; no sci-fi gear |

**Suggested first-run order:** Shot1 read → dawn body → Shot3 V2 → Shot4 gather+tame → dusk spirit → Shot5 portal → heal×3 → portal home → nurture×2 → dawn (V8).

---

## 12. Explicit out-of-scope (matches canon hard rejects)

Do **not** design, implement, or schedule any of the following in MVP:

- Photoreal scans
- Grimdark tone / muddy horror staging
- Sci-fi kits / neon portal tech
- Pancake or cylinder islands
- Tiny white moons
- Dark cabin windows
- Extra biomes (desert, jungle canopy kits, alien flora, etc.)
- Extra beasts (only `SK_Beast_Small` / one pad)
- Combat (no HP combat, weapons, aggro loops)
- Free-flight sim / open flight model / flight HUD implying sim
- Crafting trees / recipe webs beyond gather→store→spend sinks above
- Multiplayer netcode
- Worker self-approving a phase
- Two agents writing the same file
- Art bible, material authoring docs, or graybox map files (other owners)
- Night flight
- Seventh resource, fourth spirit, second beast, third nurture target
- Inventory beyond 6 slots

---

## Appendix A — GP / SYS ownership split (no open questions)

| System | Owner | Source section |
|---|---|---|
| Walk, form swap body↔spirit, glide/FALLBACK spline follow, portal A↔B, day/night time float → NightMix + spirit visibility | GP | §§3, 4 V1 V2 V5 V8, §9 |
| 6-slot inventory, gather/store counts, tame state machine, heal hurt→healed, nurture flags → `M_Nurtured` | SYS | §§4 V3 V4 V6 V7, §§5–8, §10 |
| Volumes, spline crumbs, pads, shrine links | WLD (not this file’s art) | Canon topology; this GDD only for verb timing |

## Appendix B — Duration budget (slice)

| Loop | Target play time |
|---|---|
| Homestead walk circuit | 45–90 s |
| Glide / FALLBACK down | 12–40 s |
| Gather all six once | 90–180 s |
| Tame one beast | 20–45 s |
| Night portal round trip | 6–12 s |
| Heal three | 15–40 s |
| Nurture two | 10–20 s |
| Dawn transition | 4–8 s |

End of GDD MVP (P1).
