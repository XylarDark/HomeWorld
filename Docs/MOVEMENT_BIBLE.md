# Docs/MOVEMENT_BIBLE.md

**Status:** LOCKED (Lead vision 2026-09-20 ET; Conductor scoped “bit of everything” NOW/LATER)  
**Pointers:** `Docs/CAMERA_BIBLE.md`, `Docs/DAYNIGHT_BIBLE.md`, `Docs/HOMESTEAD_BIBLE.md`, `Docs/SPIRIT_STEALTH_BIBLE.md`, `Docs/09_FALLBACK_GLIDE.md`, `Docs/canon/DO_NOT.md`

---

HOMEWORLD MOVEMENT BIBLE — TRAVERSAL IS THE ACTION

## One-line lock

Movement is the action layer on an immersive-scale fantasy planet: by day, efficient parkour-tinged routing and early mount/companion travel to hit interactions; by night, spirit mobility (blink/teleport now, flight later). Island-to-field transit is a freely steered glider descent through clouds. Keep the existing scripted `FALLBACK` separate. Never add a general-purpose free-flight model as the default body movement, invisible walls, or a second movement component.

## Taste

- Feel like **landing on a planet**, not a tiny diorama (WoW-esque scale ambition).
- Map fantasy borrows **Path of Exile preset/gen ideas** — **LATER** for real procgen; **NOW** = authored **tutorial planet** that teaches emerging mechanics.
- Prefer **action through movement + environment** over combat as the verb.
- Interactions should feel seamless, quick, slightly **mini-gamey** — a parkour tour, not a slog.

## Ownership (hard)

| Rule | Spec |
|---|---|
| One mover | Single CharacterMovement (or equivalent) — **no parallel CMC / second movement component** |
| Look ≠ control | Camera per `CAMERA_BIBLE`; move is camera-relative on foot |
| Bounds | No invisible walls as primary language (`HOMESTEAD_BIBLE`) |
| Read first | Existing character / FALLBACK glide / time gates before adding systems |

---

## NOW (MVP / tutorial planet)

### Body — ground

| Piece | Spec |
|---|---|
| Feel | Weightier readable third-person walk (Zelda-adjacent), not toddler-arcade |
| Sprint | Hold sprint — mild speed bump only |
| Jump | Small hop for ledges/path |
| Parkour lite | **1–2 verbs max:** mantle/vault onto ledges (combat-replacement seed). No full parkour kit yet |
| Fall | Soft reset to last safe ground on long falls — no void death loop |
| Swim | Out of scope NOW — TODO later |

### Body — mount / companion (early)

| Piece | Spec |
|---|---|
| Teach early | Tutorial planet establishes **tame → companion → mount-or-boost** for crossing space |
| Implementation | Speed/traversal **mode on the same CMC** (or attach that still uses one move pipeline). **No second movement component** |
| Helper | May follow on foot when not mounted |

### Transit — island ↔ planet

| Piece | Spec |
|---|---|
| Cloud descent | Freely steered glider descent from the island to the existing field landing |
| Edge start | Launch at the lookout glider perch (`GP_GlideStart`) when phase allows |
| Dusk | No **new** glide start |
| Steer in air | Unrestricted throughout the descent; no rail, corridor, or artificial steering bounds |
| Abort | Prefer ride-to-land; abort → soft reset perch/crumb if needed |

### Spirit — NOW

| Piece | Spec |
|---|---|
| Ground | Floatier / slightly faster horizontal than body — **still no free fly** |
| Blink | Short **teleport/blink** to linked shrine / marked spirit anchors (moonlight portals remain for longer hops) |
| Possess | Object/NPC possess = **stub/TODO** (log + one placeholder interact) — full kit LATER |
| Flight | **Not NOW** — see LATER |
| Stealth | **Hidden by default** in spirit form; torch light can expose — **no crouch**; alert/pressure **A2** per [`SPIRIT_STEALTH_BIBLE.md`](SPIRIT_STEALTH_BIBLE.md). **MV-A (#130)** does not implement SS-A |

### Day loop emphasis

Day movement centers on **reaching interactions efficiently** so night sow/heal/dream content is fed (Docs/21: **day = reap, night = sow** — keep).

### Tutorial planet

First planet is the **tutorial planet**: authored layout that eases players into gather, tame/mount, parkour lite, sleep/spirit, portals. Mechanics keep emerging later — don’t dump full kit on frame one.

---

## LATER (fantasy backlog — do not implement without Lead track)

- PoE-like **map generation** with gameplay presets at WoW scale  
- Fuller **parkour tour** verb set (slide, chain vaults, environment mini-games routes)  
- Rich **spirit flight** + deep **possession** gameplay  
- Multiple mount species / air mounts (still avoid duplicate CMC)  
- Swim / water traversal  
- General-purpose body flight outside the island-to-field glider descent

---

## Explicit do-not

- General-purpose free-flight body sim / flight HUD outside the glider descent  
- Second CharacterMovement / parallel controllers  
- Invisible walls as primary bounds  
- Spirit full flight in NOW without Lead amend  
- Crouch / stance stealth (use torch-light reveal per `SPIRIT_STEALTH_BIBLE`)  
- Combat as the primary action replacement for traversal depth  
- Procgen planet as NOW requirement  

## Engine note (UE5)

One CMC. Modes: Walk, Sprint, Mantle/Vault (lite), MountBoost, freely steered cloud descent, scripted `FALLBACK`, SpiritWalk, SpiritBlink. Day/body gates the descent start. Soft land recovery. Read existing `HomeWorldCharacter` + `HomeWorldFallbackGlideComponent` before extending.

## Done-when (playable test)

Walk tutorial path with sprint + one mantle/vault; freely steer the cloud descent from the glider perch, collect and retain a cloud wisp, land in the existing field, and regain walk control; spirit blink once after sleep; mount/companion speed mode once after tame. No second CMC. No invisible rim walls.
