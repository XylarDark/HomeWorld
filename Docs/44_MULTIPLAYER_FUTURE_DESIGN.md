# 44 - Future multiplayer design

**Status:** FUTURE — Lead idea 2026-10-21. Not in the vertical slice. Does not change current build order, MVP scope, or any APPROVED design doc until Lead answers and picks a stage gate.
**Origin:** Lead chat, 2026-10-21 (verbatim ideas in section 2).
**When to use:** Before any netcode, Steam session, cross-map visit, multiplayer zone, raid boss, trading, or leaderboard work. Read this file and the bridge rules in section 4 before proposing slice changes "for multiplayer later."

Mode: solo. State: decide. This file records a future direction and cheap readiness rules only.

Do not copy this into the vision board, the GDD, or the canon map body. The canon map keeps one pointer row.

## 1. Status and slice boundary

The vertical slice and T0 queue stay solo. [Docs/canon/MVP.md](canon/MVP.md) lists **Multiplayer netcode** under explicit out of scope. [Docs/canon/CONSTRAINTS.md](canon/CONSTRAINTS.md) says **No extra backend / multiplayer netcode unless Lead specifies.** [Docs/canon/DO_NOT.md](canon/DO_NOT.md) forbids **Co-op drop-in on hub (MVP)** because the homestead bible uses an NPC family instead. [Docs/canon/DECISIONS.md](canon/DECISIONS.md) records the homestead bible as **safe hub + NPC family (no co-op MVP).** [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) ranks **One playable client** and **Act 1 is a lone wanderer; co-op is later**, and skips inventing a consistency window for co-op until a real server quantum exists.

Nothing in this file authorizes networking work on the slice. Section 4 is documentation-only readiness unless Lead opens a stage in section 5.

## 2. Lead idea, restated faithfully

Up to **three human players**. Each player owns a **personal map instance**: the custom homestead island plus the generative field and forest progression that already match [Docs/39_ZONE_GENERATION_RESEARCH.md](39_ZONE_GENERATION_RESEARCH.md) and the seeded generator in [Source/HomeWorld/HomeWorldZoneGenerator.h](../Source/HomeWorld/HomeWorldZoneGenerator.h). On that map, **normal solo progression** runs to a **solo boss** at the end of that player's run.

**Visiting:** Players can **travel to another player's map** to **help** with that owner's progression, gather, or home tasks. Help is opt-in and respects the owner's world state; it is not a second solo campaign on the same save.

**Multiplayer-only zones:** Separate from the everyday map loop, there are **zones purpose-built for multiplayer**: co-op mechanics, a **dungeon or raid** cadence, and a **boss tuned for multiplayer**. These zones are where mechanics that only make sense with more than one player live. The solo map boss and the multiplayer raid boss are different beats.

**Collection share (Lead follow-up):** If you **set up a collection for another person**, the **owner keeps their progression on that collection**, and the **helper receives their own half-share copy** of the collection outcome (Lead's words: "your half of the collection"). That copy is **yours to keep**, and players may **trade items between players** subject to Lead picks in section 7.

This doc does not invent player counts beyond three, drop rates, raid timers, or backend topology until Lead answers.

**How the three layers fit together:** Layer one is **my map** (homestead plus seeded field and forest, solo boss at the end of my run). Layer two is **visiting your map** (I help you; your boss and quest flags stay yours unless Lead picks otherwise). Layer three is **multiplayer zones** (we enter a purpose-built instance for co-op verbs and a raid boss). Trading and half-share collections can span layers two and four once economy picks land.

## 3. What exists today that this builds on

### Canon and architecture

| Source | What it says for multiplayer / co-op |
|---|---|
| [Docs/canon/MVP.md](canon/MVP.md) | Multiplayer netcode is **out of scope**. |
| [Docs/canon/CONSTRAINTS.md](canon/CONSTRAINTS.md) | No extra backend / multiplayer netcode unless Lead specifies. |
| [Docs/canon/DO_NOT.md](canon/DO_NOT.md) | No co-op drop-in on the homestead hub in MVP. |
| [Docs/canon/DECISIONS.md](canon/DECISIONS.md) | Homestead bible: NPC family, **no co-op MVP**. |
| [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) | One client; lone wanderer first; co-op later; no invented co-op consistency window. |

**Plain conflicts with Lead's future idea:** Current canon is **single-player client** for Act 1 and the slice. **Live co-op on the hub** is explicitly forbidden for MVP. **Multiplayer netcode** is out of scope. The tradeoffs doc treats a **dedicated server quantum** as not decided and not a driver today. Lead's idea **does not** replace the NPC family on the slice; it adds **human visitors and separate multiplayer zones** later. Until Lead reverses MVP out-of-scope rows, implementation stays off the critical path.

### Per-player maps and zone bounds

[Docs/39_ZONE_GENERATION_RESEARCH.md](39_ZONE_GENERATION_RESEARCH.md) proposes PoE-style **seeded zones**: same seed yields the same layout, and a party can share one instance. [Source/HomeWorld/HomeWorldZoneGenerator.h](../Source/HomeWorld/HomeWorldZoneGenerator.h) implements **deterministic generation** from specs in `Lib/02_Zones`, **edge discovery boundaries** (`FHomeWorldDiscoveryBoundary`), and **camp placement only when the player crosses a pine_forest edge asset bounds** via `FHomeWorldZoneCrossing::DiscoverAt`. [Docs/handoffs/SESSION_HANDOFF_ZONE_GENERATION.md](handoffs/SESSION_HANDOFF_ZONE_GENERATION.md) records the field-first, discover-on-boundary loading model.

Future **one map per player** maps naturally onto **one field seed (and edge graph) per account**, with visit rules copying or streaming the **owner's seed and deltas**, not a global shared meadow.

### Transit: portal and cloud (solo today)

[Docs/canon/MVP.md](canon/MVP.md): day **glider descent through clouds** to the field; night **shrine portal** homestead ↔ planet only. [Docs/43_CLOUDS_WISPS_DESIGN.md](43_CLOUDS_WISPS_DESIGN.md) locks the cloud band, pass-through clouds, and **companions do not ride either glide**. Shrine portal work lives under `UHomeWorldShrinePortalComponent` and character portal helpers (see [Docs/handoffs/T0_M13_PORTAL_CAMP_GATE_PROVE.md](handoffs/T0_M13_PORTAL_CAMP_GATE_PROVE.md)).

Future **visit another player's homestead** can extend the **moonlight portal pattern** without making the slice hub a drop-in lobby.

### Companion party (NPC company, not net players)

[Docs/41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md): **one possessed pawn**; partner and child are **NPC followers** on day gather and travel only; **no second controller**; **co-op drop-in on hub stays forbidden**. Party state lives on [Source/HomeWorld/HomeWorldFamilySubsystem.h](../Source/HomeWorld/HomeWorldFamilySubsystem.h) (`bPartnerOut`, `bChildOut`, invite rules, save flags). [Source/HomeWorld/HomeWorldCharacter.cpp](../Source/HomeWorld/HomeWorldCharacter.cpp) **`TryPartyInviteInFront`** traces interact targets tagged `NPC_PARTNER` or `NPC_CHILD` and calls `ToggleMemberAtHome`.

**Mapping to future human co-op:** The same **GameInstance subsystem** pattern can hold **session party metadata** (who is visiting whom) without possessing NPC walkers. **Human visitors are not** the companion party flags; those flags stay NPC-only unless Lead merges the designs.

Invite flow today is **home-only, day, body form, after rescue** (`ToggleMemberAtHome` refuses night, spirit, and field invites). A future **friend visit invite** should reuse the same **refusal-first** pattern: failed rules leave state unchanged, and feedback uses the existing interact channel on `AHomeWorldCharacter`.

### Home loop and wisps (solo economies)

[Docs/42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) and [Docs/43_CLOUDS_WISPS_DESIGN.md](43_CLOUDS_WISPS_DESIGN.md) describe **solo** dawn/dusk home play and **cloud wisps** on night descent. Multiplayer collection-share and trading sit **on top of** existing `RES_*` and inventory subsystems ([Source/HomeWorld/HomeWorldInventorySubsystem.h](../Source/HomeWorld/HomeWorldInventorySubsystem.h)), not inside the opening tutorial kettle path.

### Boss and combat framing (solo vs raid)

[Docs/canon/DO_NOT.md](canon/DO_NOT.md) and [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md) lock **seal / banish** wins, not kill fantasy. The slice **solo boss** on a player's generative map and a **multiplayer raid boss** can share phase language (day traversal, night spirit tools) while using **different volumes and tuning**. Helpers on a visit should not skip the owner's boss gating unless Lead picks progress option B in section 7.

### Save and stream presence

`FHomeWorldZoneCrossing` tracks **stream presence** (`EHomeWorldStreamPresence`: homestead vs field) and generates the field before forest discovery. A future **MapOwnerId** on the save game should ride beside **FieldSeed** so visit code knows which generator inputs to run. [Source/HomeWorld/HomeWorldSaveGameSubsystem.h](../Source/HomeWorld/HomeWorldSaveGameSubsystem.h) already centralizes load and save; networking would attach to that subsystem first, not to level-placed globals.

## 4. Bridge from the vertical slice (multiplayer-ready, no netcode now)

Each rule is cheap documentation or naming discipline unless marked defer.

| Rule | Adopt now (cheap) or defer | Grounding |
|---|---|---|
| Keep **progression and inventory on GameInstance subsystems** (`UHomeWorldFamilySubsystem`, `UHomeWorldInventorySubsystem`, `UHomeWorldSaveGameSubsystem`) so a future host can own authoritative state per session. | **Adopt now (cheap)** | Existing subsystem layout in `Source/HomeWorld/`. |
| Treat **field seed, edge discoveries, and camp pin** as **per-save (per-owner) data**, not global level state. Visitors read the **owner id** when simulating that map. | **Adopt now (cheap)** | `FHomeWorldZoneCrossing`, `SeedForEdge`, save serialization path. |
| When adding new persistent state, **avoid static singletons** that assume one player in the universe; prefer subsystems keyed to save slot or future **PlayerId / MapOwnerId**. | **Adopt now (cheap)** | [docs/architecture/HOMEWORLD_TRADEOFFS.md](../docs/architecture/HOMEWORLD_TRADEOFFS.md) single-writer C++ rule. |
| **Do not** wire Steam, EOS, or listen-server in slice tasks. | **Adopt now (cheap)** | MVP out of scope + CONSTRAINTS. |
| **NPC party flags stay NPC-only.** Human co-op gets a **separate session record** when Lead opens stage 1. | **Adopt now (cheap)** | Docs/41 section 8; FamilySubsystem API. |
| Reuse **interact trace + feedback** pattern from `TryPartyInviteInFront` for future **invite / trade confirm** at range, not a global market UI. | **Adopt now (cheap)** | HomeWorldCharacter interact path. |
| **Multiplayer zones** as **separate level or streaming volumes** with their own spec id in `Lib/02_Zones`, not mixed into the solo field template. | **Adopt now (cheap)** | Zone spec + `HasCampContent` separation discipline. |
| **Owner-only boss progression** on the solo map; helpers get **loot / half-share / thank-you** per Lead pick, not silent dual campaign progress. | **Adopt now (cheap)** | Lead Q3 in section 7. |
| **Replication, prediction, and anti-cheat** for raids and trading. | **Defer** | No server quantum in tradeoffs doc. |
| **Global auction house, cross-player persistent structures without auth**, and **hub drop-in avatars**. | **Defer** | DO_NOT co-op hub; MVP scope. |
| Document **collection ids** on gather or collection setups so half-share copies can reference the same logical collection without sharing one inventory slot. | **Adopt now (cheap)** | Lead half-share idea; inventory is per-subsystem today. |
| Keep **homestead safe** (no combat) when visitors arrive; PvP and aggro stay in planet and multiplayer zones only. | **Adopt now (cheap)** | DO_NOT homestead combat; Docs/41 hub is home not a lobby. |

## 5. Staged path after the slice

No calendar dates. Each stage needs the prior stage's shippable proof plus Lead gate.

| Stage | Goal | Must exist first |
|---|---|---|
| **0 — Slice (solo)** | Shipped vertical slice: solo homestead, field, forest discovery, solo boss placeholder, NPC party optional. | Current queue; MVP canon unchanged. |
| **1 — Visit another player's map** | Authenticated visit to a friend's **homestead + their seeded field**; help actions; owner authority on quests and boss flags. | Stage 0; online identity; map owner id on save; visit transport pick (Q7); no hub drop-in (DO_NOT). |
| **2 — Multiplayer zones** | Instanced **co-op zones** with mechanics that require multiple players; matchmaking or invite into zone only. | Stage 1 networking; separate zone specs; zone placement pick (Q8). |
| **3 — Raid boss** | Dungeon/raid loop and **multiplayer boss** with seal/banish win per [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md). | Stage 2; combat dream boss phase model; party size pick (Q1, Q9). |
| **4 — Social extras** | **Trading**, **friends leaderboards**, **async help** (structures/signs), collection-share economy tuned. | Stage 3 loot rules; item sources/sinks design; picks Q2, Q4, Q5, Q6. |

**Dependency sketch (not a schedule):** Stage 1 needs identity and owner authority only. Stage 2 needs instancing and co-op verb prototypes that do not break solo `VERBS.md` counts on the slice. Stage 3 needs raid loot tables that stay non-rivalrous unless Lead picks collection option B. Stage 4 needs economy sinks before any global trading surface.

## 6. Research notes (external)

Industry notes only; not canon.

- **Party size:** Remnant: From the Ashes moved from four players to three because four made combat frantic or enemies felt like damage sponges; three stayed deliberate and still scaled to solo ([Gunfire interview via Fextralife](https://fextralife.com/remnant-from-the-ashes-developer-interview-with-gunfire-games/)).
- **Four-player games:** Grounded and Sea of Thieves chose four for distinct character roles and conversation distance ([Polygon on four-player design](https://www.polygon.com/22722365/four-multiplayer-developer-explanation-grounded-sea-of-thieves-minecraft-dungeons/)).
- **Co-op loot:** Non-rivalrous drops (instanced loot, auto-split, carve/chest rules) reduce friction ([gamedesign.gg co-op article](https://gamedesign.gg/articles/co-op-game-design/); [Nightingale multiplayer overview](https://playnightingale.com/news/multiplayer-overview)).
- **Trading:** Open player trading needs **sources and sinks** or economies inflate, hoard, and attract bots ([Lost Garden prosocial economics](https://lostgarden.com/2020/01/11/prosocial-economics-for-game-design/)).
- **Leaderboards:** Friends-only with **weekly resets** often beat global all-time for co-op indies (same co-op design literature; aligns with small friend groups in a three-player design).
- **Async help:** Death Stranding-style **structures and signs** left in another player's world, with likes, gives help without live scheduling (industry reference point for Q6 option A).
- **More than three players:** Remnant's move to three supports Lead's default cap; four-player games that succeed often hinge on **fixed roles** (Grounded, Sea of Thieves) rather than open roles on a care-game homestead. HomeWorld's slice already fills the "company" role with **NPC family** ([Docs/41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md)), so human slots above three risk crowding gather and stroke readability without a dedicated raid ruleset.

## 7. Pending Lead answers

Fold answers into section 2 and section 5 when Lead replies.

1. **Party size:** **A (Recommended).** Three players, raid tuned for three and scaling down to solo. **B.** Four players. **C.** Three by default plus a separate four-player raid.
2. **Collection share:** **A (Recommended).** Owner keeps 100% and the helper gets their own extra half-share copy (non-rivalrous). **B.** A literal 50/50 split of one pile. **C.** Every helper gets a full copy.
3. **Progress while helping:** **A (Recommended).** Only the map owner's progression and boss advance, and the helper gets loot plus a thank-you mark. **B.** Both players' progress advances.
4. **Trading:** **A (Recommended).** Direct friend-to-friend trades and gifts, in person on the same map, no market. **B.** A trade window for any item, from anywhere. **C.** A global market.
5. **Leaderboards:** **A (Recommended).** Friends-only, weekly reset (raid clear time, collections helped). **B.** Global all-time. **C.** None.
6. **Async help:** **A (Recommended).** Death Stranding-style structures and signs left on a friend's map, with likes. **B.** Live co-op only.
7. **How players reach each other's maps:** **A (Recommended).** Shrine or moonlight **portal** from your homestead to a friend's homestead (extends MVP portal pattern in [Docs/canon/MVP.md](canon/MVP.md) and shrine prove docs); visiting their field uses **their** cloud descent from their island ([Docs/43_CLOUDS_WISPS_DESIGN.md](43_CLOUDS_WISPS_DESIGN.md)). **B.** **Menu** travel only, no in-world portal. **C.** **Cloud** glide straight into another player's field without a homestead portal handshake.
8. **Where multiplayer zones live:** **A (Recommended).** Attached to the **host's map** via a gate or shrine invite (instance spins from the owner). **B.** A **shared hub** everyone meets in first. **C.** Menu-only raid finder with no map tie.
9. **Raid size:** **A (Recommended).** Scales **1–3** players with mechanics that stay fair alone and richer at three. **B.** Exactly three players required; solo uses separate content.

## 8. Related canon pointers (do not duplicate here)

- Opening tutorial and play queue: [Docs/context/PRINCIPLE_FIT_LOCK.md](context/PRINCIPLE_FIT_LOCK.md), [Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md](qa/TUTORIAL_PLAYTEST_QUEUE.md).
- Zone machine-readable specs: `Lib/02_Zones/**/*.json` (CANON_MAP row).
- Spirit and night solo rules: [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md), [DAYNIGHT_BIBLE.md](DAYNIGHT_BIBLE.md).

## 9. Out of scope for this document

- Engine plugin choice, Steam lobby API, or dedicated server hosting.
- Changing companion party to mean human players on the slice.
- Committing `.uasset` / `.umap` or Source for networking.
- Replacing the NPC family with online avatars on the homestead hub during MVP.
