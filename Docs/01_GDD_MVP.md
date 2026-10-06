# Docs/01_GDD_MVP.md

## 1. Status: SIGNED slice + Docs/21 Reap & Sow extension

Date: 2026-09-16 (slice) · **RS-A canon stamp 2026-09-19**  
Owner: DES · Conductor (RS-A)  
Inputs (read-only): `Docs/00_CANON.md`, `Docs/00_SHOTLIST.md`, [21_REAP_SOW.md](21_REAP_SOW.md)  
Consumers: GP (verbs / transit / day-night), SYS (gather / inventory / tame / heal / nurture / recruit)

This file is the executable design contract for WAVE 1 Track A. GP/SYS implement from tables below; do not open design questions mid-slice. **Product day/night spine** for post-slice work is **Reap & Sow** ([21_REAP_SOW.md](21_REAP_SOW.md)) — day = reap, night = sow, astral = dream combat → heal/recruit.

---

## 2. Player fantasy + tone (from canon)

**Fantasy:** You live with your loved ones at a warm floating homestead above a readable pine world. **By day (body)** you gather and explore, then descend through clouds on the steered glide route. **By night**, sleep and the rune let you become spirit. You tend the world, ease suffering, and reach the loved one taken at the camp. Spirit encounters heal, calm, or convert; you do not kill. Items and bonuses from each half make you perform better on the other.

**Tone:** Warm, readable, handmade, hopeful. Not cutesy-infantile. Not grim. Not photoreal. Not sci-fi. (Canon §9.)

---

## 3. Day/body vs Night/spirit loop (canonical)

| Mode | Form | Where | Core verbs | Transit |
|---|---|---|---|---|
| Day | Body | Homestead walk + planet slice | Walk, steered cloud descent, **Reap** (Gather / Collect / Claim), Encounter/Tame, Return/dawn | Active steered descent to open field; scripted `FALLBACK` is separate |
| Night | Spirit, after both sleep and rune gates | Homestead and planetside via shrine | Portal both ways, **Sow** (Nurture / Influence), tend, heal/recruit, return/dawn | Shrine portal homestead ↔ planet. No night glide. |

**Cycle rules (implementable):**

1. **Dawn → Day/Body:** Player is body form on homestead. Spirit layer off / NightMix → 0. Gather nodes, material sites, den/camp day interacts, and beast pad active.
2. **Day departure:** From lookout / glider perch, start the steered cloud descent. Land in the open field. The scripted `FALLBACK` is a separate implementation path.
3. **Day slice:** Walk the field and forest path; **reap** at material / living sites; encounter/tame. The player remains in body form until both sleep and rune gates are met.
4. **Sleep + rune → Night/Spirit:** Both gates are required to become spirit. Without either gate, the player remains body. NightMix → 1 only after the form change; day reap interacts idle or blocked.
5. **Night loop:** Portal homestead ↔ planet (Verb 5); **sow** (nurture / influence); tend the camp and rescue the loved one; heal or recruit other dream encounters according to their current specification; return / sleep → dawn (Verb 8).
6. **Homestead is hub.** Planet is the same world slice visible from lookout — not a second game.

**Lookout test (WLD gate, design requirement):** From lookout, player can point at landing, portal exit, first harvest, and way home.

### 3.1 Planet site kit (Docs/21 — frozen)

Same dual pattern for materials and living sites. Special site cross-buffs the other half.

| Site | Day (body — reap) | Night (spirit — sow / dream) |
|------|-------------------|------------------------------|
| **Trees** | Gather wood / materials | Nurture / spirit-influence for next-day yield |
| **Rocks** | Mine / collect | Night influence for day reaping |
| **Flowers** | Gather herbs / fiber / related RES | Nurture / dream-tend for next-day yield or quality |
| **Animal den** | Collect from / claim helpers after recruitment | Dream-battle → heal → tame / recruit |
| **Humanoid camp** | Visit / collect from recruited | Dream-battle → heal → recruit |
| **Special site** | Bonus A (feeds **night**) | Bonus B (feeds **day**) — same landmark |

**Astral / dream encounters (product):** Spirit encounters heal, calm, or convert; the player does not kill. Encounter-specific mechanics are defined by their current system specifications; the Vision Board does not define a broader combat system. Track: [21_REAP_SOW.md](21_REAP_SOW.md).

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
| Player action | Freely steer the glider through the cloud descent toward the open-field landing, without rail, corridor, or artificial steering limits. The existing scripted `FALLBACK` remains a separate route implementation. |
| Success | Touch down in the open field; control restored to walk |
| Fail / idle | Leave the perch volume without confirm → idle. Mid-route abort and recovery are unresolved for the current route. Night: verb unavailable. |
| Duration | 30 s from launch to landing (developer decision 2026-10-05). Route facts and placeholders are in [`HOMEWORLD_ROUTE.md`](context/HOMEWORLD_ROUTE.md). |

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
| Player action | Approach → offer food from inventory (prefer RES_BERRY or RES_HERB) → hold calm / Wait until state advances. A mount/helper may support field traversal; it does not restrict glider steering. |
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

**Gather rules:** One interact = one unit. Gathering a pile takes one from a pool of piles. There is no cooldown, and dawn alone does not bring a pile back; new piles come from spirit fertilizer (see [`HOMEWORLD_ROUTE.md`](context/HOMEWORLD_ROUTE.md)). Prompt shows RES_ID. Fail if no free inventory handling (§10).

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

### Active cloud descent (day/body)

1. Player begins at the lookout / glider perch.
2. Confirm → freely steer through the cloud descent. Steering has no rail, corridor, or artificial bounds.
3. Collect a cloud wisp; it stays with the player through landing.
4. Exit below the cloud layer and land in the existing field. Walk control returns on landing.
5. The route remains a glider descent; do not add a general flight HUD or energy meter. Duration is 30 s from launch to landing.

### Existing scripted `FALLBACK`

The fixed-crumb scripted glide remains a separate fallback implementation. Its route and timing do not define the active cloud descent.

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

Design teaches by framing + first successful verb — not tutorials with combat or a general-purpose flight model.

| Shot | Teach | Verb / system | Pass criteria |
|---|---|---|---|
| **1** Homestead night lookout | Hub fantasy: home above world; warm cabin vs cool moon; where planet / path / rooftops are | Orientation for V1, V5, V8 | Player (or camera) can point landing, portal exit, harvest zone, way home |
| **2** Cabin + garden close | Homestead care surfaces: warm windows, planters, path = nurture + store stage | Pre-teach V7 (N1 crop) + store props | Planters and path readable; windows glowing |
| **3** Glide departure | Freely steer the cloud descent; steering is never constrained | V2 active route | Cloud descent, wisp carry, field landing, and return to walk control |
| **4** Planet landing day | Arrival clearing; pine path continues; gather/beast space | V2 success → V3 / V4 setup | Open landing; no combat staging; same pine language |
| **5** Spirit portal arrival night | Night spirit transit = shrine portal; heal/nurture world | V5 → V6 (and return for V7) | Portal arrival soft spirit cue; handmade hopeful; no sci-fi gear |

**Suggested first-run order:** Shot1 read → dawn body → Shot3 V2 → Shot4 gather+tame → sleep + rune → spirit → camp rescue → portal home → tend → dawn.

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
- General-purpose free-flight model / flight HUD outside the steered cloud descent
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
| Walk, form swap body↔spirit, steered cloud descent, separate scripted FALLBACK, portal A↔B, day/night time float → NightMix + spirit visibility | GP | §§3, 4 V1 V2 V5 V8, §9 |
| 6-slot inventory, gather/store counts, tame state machine, heal hurt→healed, nurture flags → `M_Nurtured` | SYS | §§4 V3 V4 V6 V7, §§5–8, §10 |
| Cloud descent start, cloud/wisp placements, field landing, fallback crumbs, shrine links | WLD (not this file’s art) | Canon topology; this GDD defines the accepted traversal behavior |

## Appendix B — Duration budget (slice)

| Loop | Target play time |
|---|---|
| Homestead walk circuit | 45–90 s |
| Active cloud descent | 30 s from launch to landing (§9) |
| Gather all six once | 90–180 s |
| Tame one beast | 20–45 s |
| Night portal round trip | 6–12 s |
| Heal three | 15–40 s |
| Nurture two | 10–20 s |
| Dawn transition | 4–8 s |

End of GDD MVP (P1).
