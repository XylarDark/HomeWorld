# Docs/SPIRIT_STEALTH_BIBLE.md

**Status:** LOCKED (Lead chat 2026-09-21 ET)  
**Pointers:** `Docs/DAYNIGHT_BIBLE.md`, `Docs/MOVEMENT_BIBLE.md`, `Docs/HOMESTEAD_BIBLE.md`, `Docs/COMBAT_DREAM_BIBLE.md`, `Docs/canon/VERBS.md`, `Docs/canon/DO_NOT.md`, `Docs/SPIRIT_STEALTH_IMPL_PROMPT.md`  
**Track:** **SS** (Spirit Stealth) — separate from **MV-A** (#130); SS-A impl gated later.

---

HOMEWORLD SPIRIT STEALTH BIBLE — HIDDEN BY DEFAULT, TORCH LIGHT REVEALS

## One-line lock

In **spirit form**, the player is **hidden by default** (stealth fantasy); **torch-class light** (NPC-carried torches, campfires, spirit torches) can **illuminate the spirit world** and **expose** the spirit player — found-out is **alert / pressure (A2)**, not crouch stealth, not kill-on-detect, and **not** the body **no-torch shrine kidnap**.

## Taste

- Night spirit play feels **unseen and intimate** until light catches you — pressure, not horror slasher.
- **No crouch** verb or “sneak mode” UI — visibility is **environment + light**, not a player stance toggle.
- Getting lit should read as **“they might notice”** — rise alert, finish the interact or **slip back to dark**, not instant fail-cutscene (except separate body darkness rules).
- **Body torch** = mundane warmth/safety for the **physical** world; **spirit torch** = same warmth **plus** reveals spirits — do not merge the two fantasies.

## Ownership (hard)

| Owner | Rule |
|---|---|
| **DAYNIGHT_BIBLE** | Sleep→spirit form, phase clock, **body** no-torch darkness → **soft shrine kidnap** stays **body-only** preparedness fail — **not** spirit found-out |
| **MOVEMENT_BIBLE** | Spirit **blink** and floatier walk remain; **no spirit flight**; stealth does not add a second mover |
| **HOMESTEAD_BIBLE** | **Never combat** — no homestead detection packs, no spirit alert combat loop on hub |
| **COMBAT_DREAM_BIBLE** | Planet **minigame / boss** content unchanged — spirit stealth is **orthogonal** to seal/banish boss and minigame stubs |
| **This bible** | Hidden-default spirit visibility, torch reveal sources, A2 alert meter, body vs spirit torch split, log tags, NOW stubs vs LATER polish |

---

## NOW (SS-A — future impl track)

### Default visibility (spirit form only)

| Piece | Spec |
|---|---|
| Default | Spirit player **hidden** / not shown to NPCs as “present” in unlit space (implementation: visibility + gameplay flag — exact rendering **TODO** art) |
| Body form | Stealth bible **does not apply** — body uses normal visibility; body torch is **mundane light only** (see below) |
| Crouch | **Forbidden** — not a stealth verb |

### Reveal sources (illuminate spirit world)

| Source | Spirit-world effect |
|---|---|
| **NPC-carried torch** | Overlap / light volume can set spirit **lit** state |
| **Campfire** | Same — authored overlap on hearth / campfire actors |
| **Spirit torch** | Light **and** **reveals / shows spirits** in volume (dual role) |

Use **thin overlap volumes** on these sources — not full AI vision cones unless a volume is the cone proxy.

### Found-out — **A2** alert / pressure

| Piece | Spec |
|---|---|
| Trigger | Spirit **lit** while in range of a reveal source (or stacked sources — **TODO** stacking rules) |
| Response | **Alert / pressure meter** rises — player **flees light** or **completes interact** before peak |
| Peak | **NOT** instant shrine kidnap; **NOT** kill-on-detect; **NOT** homestead combat |
| Clear | Leaving lit volumes → alert decays; log `STEALTH: CLEAR` |
| Haste window | In light, **interacts may need to complete quickly** before alert peaks (optional NOW hook) |

Minimum logs (impl): `STEALTH: LIT enter`, `STEALTH: ALERT`, `STEALTH: CLEAR` — see `SPIRIT_STEALTH_IMPL_PROMPT.md`.

### Two torch systems (do not merge)

| Torch kind | Body world | Spirit world |
|---|---|---|
| **Body / mundane torch** | Light, safety vs **body** darkness kidnap (`DAYNIGHT_BIBLE`) | **Does not** reveal spirits by default |
| **Spirit torch** | May still cast mundane light if equipped in body — **LATER** craft | **Light + reveal spirits** in volume |

---

## LATER (do not implement without Lead SS track)

- NPC torch **AI carry** paths and patrol-linked reveal  
- Full **alert UI** (meter, audio stingers, NPC bark stubs)  
- **Spirit torch** craft recipe + placement kit  
- Detection **VFX polish** (rim light, shimmer, NPC glance anims)  
- Stacking / line-of-sight refinement beyond overlap volumes  

---

## Explicit do-not

- **Crouch** or stance-based stealth  
- **Kill-on-detect** or combat aggro as spirit stealth resolution  
- **Homestead** spirit detection / combat loops  
- **Merging** body mundane torch with spirit reveal in one undifferentiated item  
- **Spirit flight** as escape from light (see `MOVEMENT_BIBLE`)  
- Using spirit found-out as **shrine kidnap** (body no-torch rule stays separate)  
- Full **AI vision cone** simulation in NOW unless represented as **thin overlap volumes**  

## Engine note (UE5)

Spirit-form flag from sleep (`DAYNIGHT_BIBLE`). Overlap volumes on campfire / NPC torch / spirit torch → spirit **lit** state. Alert stub subsystem or component — logs only in SS-A. Body torch continues to gate **body** darkness kidnap only. Read existing time-of-day + form owners before adding parallel stealth clocks.

## Done-when (playable test — SS-A)

After sleep→spirit on tutorial/planet slice: enter campfire overlap → `STEALTH: LIT enter`; hold in light → `STEALTH: ALERT` rises; exit → `STEALTH: CLEAR`. No crouch input. Body no-torch kidnap still only on **body** darkness. **MV-A (#130)** does **not** satisfy this test — **SS-A** track required.
