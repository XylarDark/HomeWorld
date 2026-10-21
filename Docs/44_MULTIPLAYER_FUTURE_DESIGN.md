# 44 - Future multiplayer design

**Status:** FUTURE — Lead picks 2026-10-21, `1A 2A 3A 4A 5A 6A 7A 8A 9A 10A 11A 12A`, plus `MP-family A`. Not in the vertical slice. Does not change current build order, MVP scope, or any other canon file until a stage in section 5 opens.
**Origin:** Lead chat, 2026-10-21 (ideas below). Picks scribed the same day from the interview at `C:\dev\mp-interview.md`.
**When to use:** Before any netcode, Steam session, cross-map visit, multiplayer zone, raid boss, trading, or leaderboard work. Read this file and the bridge rules in section 4 before proposing slice changes "for multiplayer later."

Picks are closed. This file records the future direction and cheap readiness rules only.

Do not copy this into the vision board, the GDD, or the canon map body. The canon map keeps one pointer row.

This round writes the picks into section 2 and section 5 only. `MVP.md`, `DO_NOT.md`, `DECISIONS.md`, `HOMEWORLD_TRADEOFFS.md`, `VERBS.md`, and Doc 41 change when the stage that needs them opens. That stage-gate commit flips the `CANON_MAP` status row. This commit does not.

## 1. Status and slice boundary

The vertical slice and T0 queue stay solo. [Docs/canon/MVP.md](canon/MVP.md) lists **Multiplayer netcode** under explicit out of scope. [Docs/canon/CONSTRAINTS.md](canon/CONSTRAINTS.md) says **No extra backend / multiplayer netcode unless Lead specifies.** [Docs/canon/DO_NOT.md](canon/DO_NOT.md) forbids **Co-op drop-in on hub (MVP)** because the homestead bible uses an NPC family instead. [Docs/canon/DECISIONS.md](canon/DECISIONS.md) records the homestead bible as **safe hub + NPC family (no co-op MVP).** [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) ranks **One playable client** and **Act 1 is a lone wanderer; co-op is later**, and skips inventing a consistency window for co-op until a real server quantum exists.

Nothing in this file authorizes networking work on the slice. Section 4 is documentation-only readiness unless Lead opens a stage in section 5.

## 2. Lead idea and locked picks

Up to **three human players**. Each player owns a **personal map instance**: the custom homestead island plus the generative field and forest progression that already match [Docs/39_ZONE_GENERATION_RESEARCH.md](39_ZONE_GENERATION_RESEARCH.md) and the seeded generator in [Source/HomeWorld/HomeWorldZoneGenerator.h](../Source/HomeWorld/HomeWorldZoneGenerator.h). On that map, **normal solo progression** runs to a **solo boss** at the end of that player's run.

**Visiting:** Players can **travel to another player's map** to **help** with that owner's progression, gather, or home tasks. Help is opt-in and respects the owner's world state. It is help on their save, and it does not advance the helper's own seed.

**Multiplayer-only zones:** Separate from the everyday map loop, there are **zones purpose-built for multiplayer**: co-op mechanics, a **dungeon or raid** cadence, and a **boss tuned for multiplayer**. These zones are where mechanics that only make sense with more than one player live. The solo map boss and the multiplayer raid boss are different beats.

**Collection share (Lead follow-up):** If you **set up a collection for another person**, the **owner keeps their progression on that collection**, and the **helper receives their own half-share copy** of the collection outcome (Lead's words: "your half of the collection"). That copy is **yours to keep**, and players may **trade items between players**.

**How the layers fit together:** Layer one is **my map** (homestead plus seeded field and forest, solo boss at the end of my run). Layer two is **visiting your map** (I help you; your boss and quest flags stay yours). Layer three is **multiplayer zones** (we enter a purpose-built instance on the host's map for a raid boss). Trading, half-share collections, async traces, and friends leaderboards sit on those layers. They add no currency.

Drop rates, raid timers, and backend topology stay undesigned. The player cap is locked.

### Locked 2026-10-21

1. **Party and raid size (1A).** Three humans at most, on every layer. The raid plays fair with one and is richer with three. There is no fourth human slot.
2. **Clock and form (2A).** The map owner's day and night are the only clock. Spirit form still comes only from a bed. On a visit the party shares that phase. A raid instance may move the whole party from its day phase to its night phase together. Spirit form waits until that night phase.
3. **Raid loop (3A).** One instance and one boss: day siege interacts, then night spirit work, then a shared seal. Extra hands make the richer version. One player can still finish it. A fail is a bonk back to the entrance. The owner's solo boss does not move. The raid can be run again. Rewards follow the collection rule.
4. **NPC family on a visit (4A).** A human visit sends the owner's partner and child to their home anchors. They stay visible: awake by day, asleep at night. They do not join the follow leash. A visitor does not bring their own family onto the friend's map. NPC flags stay NPC-only.
5. **Progress while helping (5A).** Only the map owner's progression and solo boss advance. The helper receives loot and a thank-you mark, and gains no campaign credit on their own seed.
6. **Reaching a map (6A).** A shrine portal from your homestead to their homestead. Their field is reached by their cloud descent, from their island.
7. **Where zones live (7A).** On the host's map, entered through a gate or shrine invite. The instance spins from that owner.
8. **Collection (8A).** A collection is a placed home set on that map (a plot, a station, or a chest line). It is not a `RES_*` gather node. The owner keeps the placed set and its progression. The helper receives a separate half-share copy in their own storage.
9. **Trading and sinks (9A).** Friends trade and gift in person, on the same map, through the same kind of confirm as an invite. There is no currency and no market. An item leaves play when it is spent on a named recipe, a collection setup, or a raid seal.
10. **Async help (10A).** You may leave structures and signs on a friend's map, and they can answer with a like. Those traces never advance a boss or a quest. If a structure would finish a collection, the half-share pays out only when the owner accepts it.
11. **Leaderboards (11A).** Friends only, reset weekly. Two rows: raid clear time, and collections helped.
12. **Canon edits (12A).** This round is Doc 44 only. The other canon files listed above change when the matching stage opens.
13. **Visitor assist roles (MP-family A).** Visiting players reuse the single-player partner and child assist roles: station help, holding a wave, and night spirit work. The NPC family goes to its home anchors per 4A. There are no separate multi-family mechanics.

## 3. What exists today that this builds on

### Canon and architecture

| Source | What it says for multiplayer / co-op |
|---|---|
| [Docs/canon/MVP.md](canon/MVP.md) | Multiplayer netcode is **out of scope**. |
| [Docs/canon/CONSTRAINTS.md](canon/CONSTRAINTS.md) | No extra backend / multiplayer netcode unless Lead specifies. |
| [Docs/canon/DO_NOT.md](canon/DO_NOT.md) | No co-op drop-in on the homestead hub in MVP. |
| [Docs/canon/DECISIONS.md](canon/DECISIONS.md) | Homestead bible: NPC family, **no co-op MVP**. |
| [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) | One client; lone wanderer first; co-op later; no invented co-op consistency window. |

**Plain conflicts with the future design:** Current canon is **single-player client** for Act 1 and the slice. **Live co-op on the hub** is explicitly forbidden for MVP. **Multiplayer netcode** is out of scope. The tradeoffs doc treats a **dedicated server quantum** as not decided and not a driver today. The future design does not replace the NPC family on the slice. It adds human visitors and separate multiplayer zones later. Until a stage in section 5 opens and Lead amends the MVP out-of-scope rows, implementation stays off the critical path.

### Per-player maps and zone bounds

[Docs/39_ZONE_GENERATION_RESEARCH.md](39_ZONE_GENERATION_RESEARCH.md) proposes PoE-style **seeded zones**: same seed yields the same layout, and a party can share one instance. [Source/HomeWorld/HomeWorldZoneGenerator.h](../Source/HomeWorld/HomeWorldZoneGenerator.h) implements **deterministic generation** from specs in `Lib/02_Zones`, **edge discovery boundaries** (`FHomeWorldDiscoveryBoundary`), and **camp placement only when the player crosses a pine_forest edge asset bounds** via `FHomeWorldZoneCrossing::DiscoverAt`. [Docs/handoffs/SESSION_HANDOFF_ZONE_GENERATION.md](handoffs/SESSION_HANDOFF_ZONE_GENERATION.md) records the field-first, discover-on-boundary loading model.

Future **one map per player** maps naturally onto **one field seed (and edge graph) per account**, with visit rules copying or streaming the **owner's seed and deltas**, not a global shared meadow.

### Transit: portal and cloud (solo today)

[Docs/canon/MVP.md](canon/MVP.md): day **glider descent through clouds** to the field; night **shrine portal** homestead ↔ planet only. [Docs/43_CLOUDS_WISPS_DESIGN.md](43_CLOUDS_WISPS_DESIGN.md) locks the cloud band, pass-through clouds, and **companions do not ride either glide**. Shrine portal work lives under `UHomeWorldShrinePortalComponent` and character portal helpers (see [Docs/handoffs/T0_M13_PORTAL_CAMP_GATE_PROVE.md](handoffs/T0_M13_PORTAL_CAMP_GATE_PROVE.md)).

The locked visit (6A) extends that pattern: a shrine portal from your homestead to their homestead, then their cloud descent into their field. The slice hub stays a home.

### Companion party (NPC company, not net players)

[Docs/41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md): **one possessed pawn**; partner and child are **NPC followers** on day gather and travel only; **no second controller**; **co-op drop-in on hub stays forbidden**. Party state lives on [Source/HomeWorld/HomeWorldFamilySubsystem.h](../Source/HomeWorld/HomeWorldFamilySubsystem.h) (`bPartnerOut`, `bChildOut`, invite rules, save flags). [Source/HomeWorld/HomeWorldCharacter.cpp](../Source/HomeWorld/HomeWorldCharacter.cpp) **`TryPartyInviteInFront`** traces interact targets tagged `NPC_PARTNER` or `NPC_CHILD` and calls `ToggleMemberAtHome`.

**Mapping to future human co-op:** The same **GameInstance subsystem** pattern can hold **session party metadata** (who is visiting whom) without possessing NPC walkers. Human visitors are not the companion party flags. Those flags stay NPC-only (4A). On a visit the owner's partner and child go to their home anchors and stay visible. They do not join the leash, and a visitor's family stays on the visitor's own map. The visitors themselves fill the partner and child assist roles (MP-family A): station help, holding a wave, and night spirit work. Doc 41 still owns the NPC family on the slice.

Invite flow today is **home-only, day, body form, after rescue** (`ToggleMemberAtHome` refuses night, spirit, and field invites). A future **friend visit invite** reuses the same **refusal-first** pattern: failed rules leave state unchanged, and feedback uses the existing interact channel on `AHomeWorldCharacter`. In-person trades use that same confirm (9A).

### Home loop and wisps (solo economies)

[Docs/42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) and [Docs/43_CLOUDS_WISPS_DESIGN.md](43_CLOUDS_WISPS_DESIGN.md) describe **solo** dawn/dusk home play and **cloud wisps** on night descent. A collection (8A) is a placed home set: a plot, a station, or a chest line. It sits **on top of** existing `RES_*` and inventory subsystems ([Source/HomeWorld/HomeWorldInventorySubsystem.h](../Source/HomeWorld/HomeWorldInventorySubsystem.h)), not inside the opening tutorial kettle path. The six `RES_*` ids stay the gather nodes. They are not the collection.

### Boss and combat framing (solo vs raid)

[Docs/canon/DO_NOT.md](canon/DO_NOT.md) and [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md) lock **seal / banish** wins, not kill fantasy. The slice **solo boss** on a player's generative map and the **raid boss** (3A) share that win and the day-then-night phase language, in different volumes. The raid scales from one to three. A fail there is a bonk back to the entrance. Help on a visit does not move the helper's solo boss (5A).

### Save and stream presence

`FHomeWorldZoneCrossing` tracks **stream presence** (`EHomeWorldStreamPresence`: homestead vs field) and generates the field before forest discovery. A future **MapOwnerId** on the save game should ride beside **FieldSeed** so visit code knows which generator inputs to run. The visited map uses the owner's clock (2A). [Source/HomeWorld/HomeWorldSaveGameSubsystem.h](../Source/HomeWorld/HomeWorldSaveGameSubsystem.h) already centralizes load and save; networking would attach to that subsystem first, not to level-placed globals.

## 4. Bridge from the vertical slice (multiplayer-ready, no netcode now)

Each rule is cheap documentation or naming discipline unless marked defer.

| Rule | Adopt now (cheap) or defer | Grounding |
|---|---|---|
| Keep **progression and inventory on GameInstance subsystems** (`UHomeWorldFamilySubsystem`, `UHomeWorldInventorySubsystem`, `UHomeWorldSaveGameSubsystem`) so a future host can own authoritative state per session. | **Adopt now (cheap)** | Existing subsystem layout in `Source/HomeWorld/`. |
| Treat **field seed, edge discoveries, and camp pin** as **per-save (per-owner) data**, not global level state. Visitors read the **owner id** when simulating that map. | **Adopt now (cheap)** | `FHomeWorldZoneCrossing`, `SeedForEdge`, save serialization path. |
| When adding new persistent state, **avoid static singletons** that assume one player in the universe; prefer subsystems keyed to save slot or future **PlayerId / MapOwnerId**. | **Adopt now (cheap)** | [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) single-writer C++ rule. |
| **Do not** wire Steam, EOS, or listen-server in slice tasks. | **Adopt now (cheap)** | MVP out of scope + CONSTRAINTS. |
| **NPC party flags stay NPC-only.** Human visitors use a separate session record at stage 1 and fill the existing partner and child assist roles. A visit clears the owner's leash to home anchors. | **Adopt now (cheap)** | 4A and MP-family A; Docs/41 section 8; FamilySubsystem API. |
| Reuse **interact trace + feedback** from `TryPartyInviteInFront` for a future **invite / trade confirm** at range. Trades are in person. There is no market UI. | **Adopt now (cheap)** | 9A; HomeWorldCharacter interact path. |
| **Multiplayer zones** as **separate level or streaming volumes** with their own spec id in `Lib/02_Zones`, entered from a gate on the host's map, not mixed into the solo field template. | **Adopt now (cheap)** | 7A; zone spec + `HasCampContent` separation discipline. |
| **Owner-only boss progression** on the solo map. Helpers get loot, a thank-you mark, and a half-share copy. They do not gain campaign credit. | **Adopt now (cheap)** | 5A and 8A. |
| **Replication, prediction, and anti-cheat** for raids and trading. | **Defer** | No server quantum in tradeoffs doc. |
| **Global auction house, cross-player persistent structures without auth**, and **hub drop-in avatars**. | **Defer** | 9A forbids a market; DO_NOT co-op hub; MVP scope. |
| Document **collection ids** on placed home sets (plot, station, chest line) so a half-share copy can reference the same logical collection without sharing one inventory slot. | **Adopt now (cheap)** | 8A; inventory is per-subsystem today. |
| Keep **homestead safe** (no combat) when visitors arrive. The owner's clock is the only clock on that map. | **Adopt now (cheap)** | 2A; DO_NOT homestead combat; Docs/41 hub is home not a lobby. |

## 5. Staged path after the slice

No calendar dates. Each stage needs the prior stage's shippable proof plus a Lead gate. The gate is what amends the other canon files.

| Stage | Goal | Must exist first |
|---|---|---|
| **0 — Slice (solo)** | Shipped vertical slice: solo homestead, field, forest discovery, solo boss placeholder, NPC party optional. | Current queue; MVP canon unchanged. |
| **1 — Visit another player's map** | Shrine portal from your homestead to theirs, then their cloud descent into their field. Owner's clock. Owner's quests and solo boss only. Helper gets loot and a thank-you mark. The visit sends partner and child to home anchors; they stay visible and off the leash. Visitors bring no family. Visitors fill the partner and child assists: station help, holding a wave, and night spirit work. | Stage 0; online identity; map owner id on save; no hub drop-in (DO_NOT). |
| **2 — Multiplayer zones** | An instance opened from a gate or shrine on the host's map. Separate zone spec. The party shares the owner's phase. | Stage 1 networking; a zone spec that is not the solo field template. |
| **3 — Raid boss** | One boss: day siege, then night spirit work, then a shared seal. Scales from one to three. The instance moves the whole party between those phases. A fail is a bonk to the entrance. The owner's solo boss does not move. The raid can be run again. | Stage 2; [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md) phase model. |
| **4 — Social extras** | Placed home-set collections with a half-share copy. In-person trades and gifts. Sinks are a named recipe, a collection setup, or a raid seal. Async structures and signs with likes; collection half-share pays when the owner accepts; bosses and quests do not. Friends-only weekly boards for raid clear time and collections helped. | Stage 3 rewards; no currency slot. |

**Dependency sketch (not a schedule):** Stage 1 needs identity and owner authority. Stage 2 needs instancing that does not break solo `VERBS.md` counts on the slice. Stage 3 needs non-rivalrous raid rewards under the half-share rule. Stage 4 spends items on recipes, collections, and seals, and it does not add a market.

## 6. Research notes (external)

Industry notes only; not canon. The picks in section 2 win where a note disagrees.

- **Party size:** Remnant: From the Ashes moved from four players to three because four made combat frantic or enemies felt like damage sponges; three stayed deliberate and still scaled to solo ([Gunfire interview via Fextralife](https://fextralife.com/remnant-from-the-ashes-developer-interview-with-gunfire-games/)).
- **Four-player games:** Grounded and Sea of Thieves chose four for distinct character roles and conversation distance ([Polygon on four-player design](https://www.polygon.com/22722365/four-multiplayer-developer-explanation-grounded-sea-of-thieves-minecraft-dungeons/)).
- **Co-op loot:** Non-rivalrous drops (instanced loot, auto-split, carve/chest rules) reduce friction ([gamedesign.gg co-op article](https://gamedesign.gg/articles/co-op-game-design/); [Nightingale multiplayer overview](https://playnightingale.com/news/multiplayer-overview)).
- **Trading:** Open player trading needs **sources and sinks** or economies inflate, hoard, and attract bots ([Lost Garden prosocial economics](https://lostgarden.com/2020/01/11/prosocial-economics-for-game-design/)).
- **Leaderboards:** Friends-only with **weekly resets** often beat global all-time for co-op indies (same co-op design literature; aligns with small friend groups in a three-player design).
- **Async help:** Death Stranding-style **structures and signs** left in another player's world, with likes, gives help without live scheduling. The lock adds owner acceptance before a collection half-share pays.
- **More than three players:** Remnant's move to three supports the locked cap. Four-player games that succeed often hinge on **fixed roles** (Grounded, Sea of Thieves). HomeWorld's slice already fills the company role with the **NPC family** ([Docs/41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md)).

## 7. Lead answers

Answered 2026-10-21. All recommended. Folded into section 2 and section 5 in this commit.

1. **1A.** Three humans. The raid scales from one to three.
2. **2A.** The owner's clock. Spirit form still comes from a bed. A raid moves the whole party from day to night together.
3. **3A.** Day siege, night spirit work, shared seal. A fail is a bonk to the entrance. Repeatable. The solo boss stays put.
4. **4A.** Partner and child stay visible at home and off the leash. Visitors bring no family.
5. **5A.** Only the owner's progression advances. The helper gets loot and a thank-you mark.
6. **6A.** Shrine portal to their homestead, then their cloud descent.
7. **7A.** The zone opens from a gate on the host's map.
8. **8A.** A collection is a placed home set. The owner keeps it. The helper gets a half-share copy.
9. **9A.** In-person trades and gifts. Sinks are a named recipe, a collection setup, or a raid seal.
10. **10A.** Structures and signs, with likes. A collection half-share waits for the owner to accept it.
11. **11A.** Friends-only weekly boards: raid clear time, and collections helped.
12. **12A.** Doc 44 only until a stage gate opens.
13. **MP-family A.** Visitors reuse the partner and child assists: station help, holding a wave, and night spirit work. The NPC family stays at its home anchors. No separate multi-family mechanics.

## 8. Related canon pointers (do not duplicate here)

- Opening tutorial and play queue: [Docs/context/PRINCIPLE_FIT_LOCK.md](context/PRINCIPLE_FIT_LOCK.md), [Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md](qa/TUTORIAL_PLAYTEST_QUEUE.md).
- Zone machine-readable specs: `Lib/02_Zones/**/*.json` (CANON_MAP row).
- Spirit and night solo rules: [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md), [DAYNIGHT_BIBLE.md](DAYNIGHT_BIBLE.md).

## 9. Out of scope for this document

- Engine plugin choice, Steam lobby API, or dedicated server hosting.
- Changing companion party to mean human players on the slice.
- Committing `.uasset` / `.umap` or Source for networking.
- Replacing the NPC family with online avatars on the homestead hub during MVP.
- A separate multi-family system. Visitors reuse the partner and child assist roles (MP-family A).
- Drop rates, raid timers, and backend topology.
