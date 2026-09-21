# Docs/COMBAT_DREAM_BIBLE.md

**Status:** LOCKED (Lead locks 2026-09-21 ET — A1/B/C/D)  
**Pointers:** `Docs/MOVEMENT_BIBLE.md`, `Docs/DAYNIGHT_BIBLE.md`, `Docs/HOMESTEAD_BIBLE.md`, `Docs/21_REAP_SOW.md`, `Docs/canon/VERBS.md`, `Docs/canon/DO_NOT.md`

---

HOMEWORLD COMBAT & DREAM BIBLE — SEAL EVIL, NURTURE DREAMS

## One-line lock

Combat is **rare boss-only** vs great/terrible evil (**win = seal / banish / end the evil**, never murder fantasy); all other encounters are **non-combat minigames** (heal / nurture / grow / possess); the **model boss** is one huge foe spanning **day + night** with distinct phase verbs.

## Taste

- **Wholesome family fantasy** — convert and heal the evil’s dream, not slaughter.
- Bosses feel **monumental** (many times larger than the player); day phase reads as **siege / traversal**; night phase reads as **spirit dream-work** (blink, possess, heal-strip).
- Minigames feel **nurture / grow / possess**, not DPS meters or weapon loops.
- No grimdark kill cam, no trash-mob aggro packs, no homestead violence.

## Ownership (hard)

| Owner | Rule |
|---|---|
| **HOMESTEAD_BIBLE** | **Never combat** on homestead — no boss volumes, no minigames, no damage |
| **Docs/21** | Den/camp **dream-convert** remains the non-boss **night** path (heal/recruit; convert not kill) |
| **MOVEMENT_BIBLE** | Boss **day phase** reuses **parkour lite + world interacts / siege objects** — no second mover, no combat CMC |
| **DAYNIGHT_BIBLE** | **DayBoss / NightBoss** phase flags follow current day/night when entering placeholder volume |
| **CAMERA_BIBLE** | Unchanged — no combat camera kit |
| **This bible** | Names boss + minigame verb IDs, log tags, NOW stubs vs LATER full fight |

---

## NOW (MVP / tutorial planet or VS path)

### Non-boss — four minigame families (stubs)

| Family | Verb ID (canon) | Log tag (minimum) | NOW spec |
|---|---|---|---|
| Heal | `MinigameHeal` | `MINIGAME:HEAL` | Named interact stub; one-shot log on use |
| Nurture | `MinigameNurture` | `MINIGAME:NURTURE` | Named interact stub; one-shot log on use |
| Grow | `MinigameGrow` | `MINIGAME:GROW` | Named interact stub; one-shot log on use |
| Possess | `MinigamePossess` | `MINIGAME:POSSESS` | **Polish-first** (see NOTE below); bridges Docs/21 dream-convert + MOVEMENT possess stub |

**NOTE (Lead-swappable):** Default **polish-first = Possess** (spirit/object hook + clearer feedback). Lead may swap to heal / nurture / grow first — others stay stubs until chosen.

| Piece | Spec |
|---|---|
| Scope | Planet / tutorial slice only — **not homestead** |
| UX | No HP bars as primary trash UX; no weapons; no aggro wander packs |
| GAS | **Do not** invent a full ability kit NOW — interact + logs only |

### Model boss — bible lock (design NOW, fight LATER)

| Piece | Spec |
|---|---|
| Fantasy | **One** huge evil spanning **both** day and night; player must use **both** phases to **seal / banish** |
| Scale | Boss silhouette **≫ player** (monumental; exact mesh LATER) |
| Day phase (B) | **Traversal / parkour** + **weak-point interacts** + **siege objects** on the world (reuse MOVEMENT mantle/vault + interact volumes) |
| Night phase (B) | **Spirit blink**, **possess**, **heal-strip** on the **dream** of the evil — not DPS |
| Win (A1) | **`BOSS:SEAL`** (or equivalent) — **seal / banish / end evil** — **not** kill / murder win |

### Placeholder boss volume (NOW implementation target)

| Piece | Spec |
|---|---|
| Placement | **Tutorial planet** or **VS_MVP** path — volume name TBD on DESKTOP (`BP_BossPlaceholderVolume` or trigger volume) |
| Enter | On overlap: set phase flag **`DayBoss`** or **`NightBoss`** from **current day/night** (DAYNIGHT owner) |
| Logs | `BOSS:PHASE_DAY` \| `BOSS:PHASE_NIGHT` on enter; optional `BOSS:SEAL` stub on interact (no full AI) |
| Exit | Leave volume without spawning trash combat or weapon systems |
| Content | If binaries not in repo, **DESKTOP/Content step** per `COMBAT_DREAM_IMPL_PROMPT.md` |

### Explicit NOW exclusions

- Full tutorial-planet **multi-hour** boss siege
- Boss weak-point art, siege prop kit, trash combat loops
- Weapons, ammo, HP-primary HUD for “mobs”
- Homestead combat path of any kind

---

## LATER (do not implement without Lead track)

- Full **tutorial-planet model boss** fight (multi-hour day + night siege, weak points, siege object art)
- Polished **heal / nurture / grow** minigame kits (beyond one-line logs)
- **Deep possess** gameplay (multi-target, puzzles, dream layers)
- Boss cinematic beats, phase transitions, full AI
- Replacing Docs/21 dream-convert with kill combat

---

## Explicit do-not

- **Homestead combat** (any phase)
- **Kill win-condition** or murder fantasy payoff (including bosses)
- **Trash combat loops** — aggro packs, weapon-first kits, DPS races
- **Second CharacterMovement** / parallel combat controller
- **Reinvent Docs/21** as kill combat; dream-convert stays convert/heal/recruit
- **Free-flight** or night flight as boss crutch (MOVEMENT / DAYNIGHT locks stand)

## Engine note (UE5)

Stub layer only NOW: overlap volumes, interact components or existing interact ability hooks, `UE_LOG` / project log category with tags above. Read `HomeWorldCharacter`, day/night phase queries, and MOVEMENT possess stub before extending. No new weapon GAS templates without Lead track.

## Done-when (playable test)

1. Trigger **one** minigame stub log (`MINIGAME:*`) from a planet interact.
2. Trigger **possess** polished-or-stub path once (`MINIGAME:POSSESS` or MOVEMENT possess stub log).
3. Enter **boss placeholder volume** by **day** → see `BOSS:PHASE_DAY`; by **night** → see `BOSS:PHASE_NIGHT`.
4. Optional: fire **`BOSS:SEAL`** stub interact without full fight AI.
5. Confirm **no homestead combat** path (hub volumes unchanged).
