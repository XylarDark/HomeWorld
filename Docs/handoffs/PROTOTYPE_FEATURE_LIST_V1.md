# PROTOTYPE_FEATURE_LIST_V1 — T0 first gameloop

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead stamped `APPROVE-PROTOTYPE-LIST` 2026-09-27 ET (HomeWorld Co) |
| **Host** | CLOUD (this doc) · Lead (taste + APPROVE) · **no DESKTOP Act from Design** |
| **Source EXIT** | Interview EXIT — SCOPE — `PROTOTYPE_T0_V1` (ACCEPTED + greenlit 2026-09-27 ET) |
| **Narrative bible** | Lead T0 narrative (`LEAD_NARRATIVE_Q2`) = vision; mechanics below = **T0 implemented floor** |
| **Supersedes** | Thin Spine candidate **A** as SCOPE target (historical Research lean only) |
| **Pins** | CAP/EA **DROPPED** · DET pin HOLD `0a27306` · map canon `Maps/VS_MVP` · no AGENTS/A–E rewrite |
| **Feel cites** | `GAME_DESIGN_MOVEMENT_ENV_CANON_V1` · `GAME_FEEL_CANON_V1` · `PROP_INVENTORY_V1` (T0_FEEL_PROP_FREEZE) — SCOPE feel overlay ACCEPTED; Bite B list amend HOLD |
| **Cite** | [HomeWorld Co ops](sand-workflow:homeworld-co-ops) · CAPTURE_REDUNDANCY · ONE_SHOT_BITES · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (canon blob `107a511`) — **stream/partition-ready** for bigger planetsides |

---

## Lead gate

```text
APPROVE-PROTOTYPE-LIST
```

**STAMPED** 2026-09-27 ET in HomeWorld Co (Lead). Unlocks Conductor to open **one** Implement bite: **gap inventory + walk-script** vs T0 MUST beats on existing `Maps/VS_MVP` actors. All other T0 mechanic implementation stays **DEFER** until that bite’s DONE-WHEN. Design does **not** declare this APPROVE.

---

## DONE-WHEN (this artifact)

Lead can stamp `APPROVE-PROTOTYPE-LIST` from **§ Scope table + § Inventory freeze + § First Implement bite** alone — no Implement wake required to approve the list.

---

## Non-goals (locked)

- No CAP / EA reopen
- No Content / Python / Source / `.uasset` / `.umap` in this Design packet
- No Design invent of beats outside EXIT SCOPE table
- No Research REC **A** defaults as SCOPE (T0 supersedes)
- No Implement feature PRs before Lead APPROVE + Conductor bite open
- No quarantined Homestead / DemoMap as primary playable surface
- No free-flight · no homestead combat · no player death as T0 law
- No pin bump · no AGENTS dump · no invent greps/cheats in this bite
- No DESKTOP MCP / PASS-FAIL from Design

---

## Pillars (Lead)

1. Homestead  
2. Movement to/from planetside  
3. Playable zone + day/night  

---

## Scope table (from EXIT ONLY)

| Feature / beat | Pillar | MUST/CUT/DEFER | Prove hint | Taste? |
|----------------|--------|----------------|------------|--------|
| Wake / start day (homestead) | 1 | **MUST** | Actor/log: day start on VS_MVP homestead | Later Lead polish |
| Kettle + herbs → tea → sprint (~half day) | 1 | **MUST** | Interact kettle/herbs → buff duration readable | Later |
| Plant given herb nearby outside | 1 | **MUST** | Plant interact + planted marker near homestead | Later |
| Equip backpack → inventory | 1 | **MUST** | Equip → inventory UI/state | Later |
| Glider interact → glide to open field | 2 | **MUST** | Seamless home↔planet feel; glider→field | Lead polish |
| Collect herb seeds in field | 3 | **MUST** | Gather nodes in field | Later |
| Rune unlock before bed→spirit | 3 | **MUST** | Unlock gate; bed→spirit blocked until rune | Later |
| Day camp: cartoon eject (launch→glider→home) | 3 | **MUST** | Eject-to-home; **not** lethal; convert-not-kill | Lead polish |
| Homeworld night w/o bed: no spirit; day abilities off | 3 | **MUST** | Night homeworld: spirit OFF + day abilities OFF | Later |
| Planetside night w/o bed path: glider boot home | 3 | **MUST** | Same eject path as day camp | Later |
| Bed → spirit (night planetside gate) | 1+3 | **MUST** | After rune; bed enables night planetside spirit | Later |
| Nurture planted herb (spirit) | 3 | **MUST** | Spirit nurture on planted herb | Later |
| Home portal → camp portal (spirit) | 2+3 | **MUST** | Spirit portal home→camp | Later |
| Camp night: avoid 1 guard; soothe 2 sleepers | 3 | **MUST** | Avoid + soothe (not kill) | Lead polish |
| Other plants nurture → daytime seed collect | 3 | **DEFER** | Loop extension; named in vision; not first bite | — |
| Player death | — | **CUT** | — | — |
| Quarantined Homestead/DemoMap as primary | — | **CUT** | — | — |
| CAP / EA reopen | — | **CUT** | — | — |

### Night / combat law (EXIT)

- Day camp threat = **eject-to-home**, not lethal kill.  
- Night spirit = **avoid + soothe** (convert-not-kill preserved).  
- No homestead combat.  
- Bible lethal-kill amend: **not required**.

### Map / systems locks (EXIT)

| Lock | Value |
|------|-------|
| T0 playable surface | `Maps/VS_MVP` (+ markers) |
| Transition feel | Seamless home↔planet **MUST** |
| Scale | Systems **stream / world-partition-ready** for bigger planetsides **MUST** (future-proof; not “single umap forever”) |
| Host coding (temp) | OpenCode on DESKTOP ≡ Cursor until Cursor tokens restored |

### Cheats

Not locked this Interview. Default: no invent greps/cheats; use existing prove cheats only when a later bite’s DONE-WHEN names them (`Docs/30` cheat vs walk).

### Taste vs prove

Art-dress / NightMix feel / camera polish = **Lead final polish** (later). Team prove = readable actors + logs toward T0 beats.

---

## Architecture Trade-Offs cite (stream / partition — A–E, cite only)

**Decision recorded (SCOPE, not Implement API invent):** T0 proves on `Maps/VS_MVP`, but systems that own transit / planetside load must stay **partition- and stream-ready** so larger planetsides do not force a hub remesh.

| Layer | Application to T0 |
|-------|-------------------|
| **A — System** | Quantum: **playable world surface** (hub + transit + planetside slice) may grow planetside extent without splitting hub ownership. Do not invent a second deployable “stream service”; keep streaming/WP **inside** the world quantum. Name trade-off: seamless feel vs independent umap forever — **seamless wins**; WP/stream capability is the least-worst growth path. |
| **B — Module** | Deep modules hide load/unload and level-instance details behind simple transit / portal / glider interfaces. Callers (verbs, camp eject, spirit portal) must not know partition keys. |
| **C — Data** | When levels/instances are split or streamed: name **source vs derived** (authored VS_MVP markers vs runtime streamed cells), and keep save/progress keyed so a bigger planetside does not rewrite homestead identity. |
| **D — Team** | One stream-aligned Implement bite owns gap inventory first; later WP/stream work stays one team API (no parallel “map team” invent). |
| **E — Stability** | Integration points (load, portal, eject) need timeout/bounds/degrade: failed stream must not soft-lock player mid-transit (eject/home degrade path preferred over hang). |

**15-q gate (Design):** This handoff does **not** invent new module APIs or shared DB. Implement SCOUT for gap inventory must not invent WP contracts; if a later bite invents streaming APIs, load A–E + 15-q before PR.

---

## Inventory freeze (Arrange before Act)

Labels ⊆ this inventory ∩ `Maps/VS_MVP` world. Freeze look-at / AABB / TOD **before** any Act. Prove labels must subset this set.

### Spatial / beat markers

| Label | Meaning | Pillar | World intersection (T0) |
|-------|---------|--------|-------------------------|
| `NODE_WAKE` | Homestead day start | 1 | Homestead spawn / cabin |
| `NODE_KETTLE` | Tea / sprint craft | 1 | Homestead kitchen/interact |
| `NODE_PLANT_SLOT` | Given-herb plant site | 1 | Outside near homestead |
| `NODE_BACKPACK` | Equip → inventory | 1 | Homestead gear |
| `NODE_GLIDER` | Glider launch | 2 | Homestead perch / launch |
| `NODE_FIELD_GATHER` | Herb seed collect | 3 | Open field on VS_MVP |
| `NODE_RUNE` | Spirit unlock gate | 3 | Field / near path |
| `NODE_DAY_CAMP` | Day eject threat | 3 | Forest camp |
| `NODE_BED` | Bed → spirit gate | 1+3 | Homestead bed |
| `NODE_PORTAL_HOME` | Spirit home portal | 2+3 | Homestead night |
| `NODE_PORTAL_CAMP` | Spirit camp portal | 2+3 | Camp night |
| `NODE_GUARD` | Avoid target (1) | 3 | Camp night |
| `NODE_SLEEPER` | Soothe targets (2) | 3 | Camp night |

### TOD / form

| Label | Meaning |
|-------|---------|
| `TOD_DAY` | Body-work beats (wake→field→camp approach) |
| `TOD_NIGHT_HOME` | Homeworld night without bed: no spirit; day abilities off |
| `TOD_NIGHT_SPIRIT` | After bed (+ rune): spirit nurture / portals / camp soothe |
| `FORM_BODY` | Day player form |
| `FORM_SPIRIT` | Night spirit form (gated) |
| `EJECT_HOME` | Cartoon launch→glider→home (day camp or planetside night without bed) |

### Cam / AABB freeze (schema only — reuse existing cams where present)

| Cam ID | Intent | TOD | Look-at ⊆ inventory | AABB / framing |
|--------|--------|-----|---------------------|----------------|
| `CAM_T0_WAKE` | Homestead day start readable | `TOD_DAY` | `NODE_WAKE` | Cabin/garden mid |
| `CAM_T0_GLIDE` | Seamless transit read | `TOD_DAY` | `NODE_GLIDER` → field mass | Wide pastoral |
| `CAM_T0_FIELD` | Gather + rune | `TOD_DAY` | `NODE_FIELD_GATHER`, `NODE_RUNE` | Mid path |
| `CAM_T0_CAMP_DAY` | Eject threat readable | `TOD_DAY` | `NODE_DAY_CAMP` | Camp approach |
| `CAM_T0_BED` | Bed gate | dusk→`TOD_NIGHT_SPIRIT` | `NODE_BED` | Interior readable |
| `CAM_T0_CAMP_NIGHT` | Avoid + soothe | `TOD_NIGHT_SPIRIT` | `NODE_GUARD`, `NODE_SLEEPER` | Camp night mid |

**Reject:** free-fly cam as prove; lethal kill cam; Homestead/DemoMap quarantine as primary look-at.

---

## First Implement bite (exactly one — after APPROVE)

| Field | Value |
|-------|-------|
| **Name** | `T0_GAP_INVENTORY_WALK_V1` |
| **Do** | Gap inventory + walk-script checklist vs **T0 MUST** beats on **existing** `Maps/VS_MVP` actors |
| **Out** | Table: Beat \| Present? (Y/N/Partial) \| Actor/path \| Gap note \| Suggested prove label |
| **DONE-WHEN** | Table covers every **MUST** row in § Scope table; suitable for next Design/Implement mechanic bites — **not** full Lead polish |
| **HOLD** | All other T0 mechanic implementation **DEFER** until this bite’s DONE-WHEN |
| **Host** | OpenCode on DESKTOP ≡ Cursor (temp) or Cursor cloud when tokens restored |
| **Anti** | No feature invent beyond gap notes · no `.uasset` · no CAP/EA · no Design re-open of CUT rows |

---

## Do bites (routing)

| # | Owner | Bite | Blocked until |
|---|-------|------|---------------|
| 0 | **Lead** | `APPROVE-PROTOTYPE-LIST` | — (this doc) |
| 1 | Conductor → Implement | Open `T0_GAP_INVENTORY_WALK_V1` | Lead APPROVE |
| 2 | Design | Post-gap: mechanic inventories / DONE-WHEN per MUST (files-only) | Bite 1 DONE-WHEN |
| — | Impl/Test/Fix | Feature Acts | Design packets + Conductor open |

**eggbot:** N · **child Research:** N (unless gap inventory names a true external-info hole).

---

## Accept checklist (Lead)

- [ ] Scope table matches Interview EXIT T0 (no Research A defaults slipped in)
- [ ] CUT rows: death · quarantine maps · CAP/EA
- [ ] Stream/partition cite present; no invented WP API
- [ ] First Implement bite = gap inventory only
- [x] Stamp: `APPROVE-PROTOTYPE-LIST` (Lead, 2026-09-27 ET)
