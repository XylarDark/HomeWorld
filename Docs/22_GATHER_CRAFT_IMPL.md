# Docs/22 — Gather & Craft implementation (GC)

| Field | Value |
|-------|-------|
| **Status** | **GC STRATEGY APPROVED**; **GC-A APPROVED / CLOSED**; **GC-B IN PROGRESS** (this PR); GC-C locked |
| **Date** | 2026-09-21 |
| **Author** | Conductor (HomeWorld) |
| **Bible** | [GATHER_CRAFT_BIBLE.md](GATHER_CRAFT_BIBLE.md) · [GATHER_CRAFT_IMPL_PROMPT.md](GATHER_CRAFT_IMPL_PROMPT.md) |
| **Prior track** | [21_REAP_SOW.md](21_REAP_SOW.md) **CLOSED** — den/camp/special not primary RES miners |
| **Prefix** | **GC** — do **not** reuse RS / VP2 / D19 gate strings |

---

## Gate

Lead **`APPROVE GC STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat: “approve GC strategy”). Unlocks **GC-A**.

**GC-A:** Lead **`APPROVE GC-A`**, 2026-09-21 ET — **GRANTED** (DESKTOP greps deferred/accepted). **CLOSED** on main. Unlocks **GC-B**.

**GC-B:** Lead **`APPROVE GC-B`** — unlocks **GC-C** (placeholder shop/room volumes).

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal

Ship the **Gather & Craft** demo spine from the locked bible: six `RES_*` only; planet day gather → store → named hearth recipes. This track splits implementation so craft/placeholders do not land before site mapping is proven.

```mermaid
flowchart LR
  subgraph gca [GC-A_NOW]
    Sites[Planet_site_kinds]
    RES[Six_RES_map]
    Flavor[Flint_grass_logs]
  end
  subgraph gcb [GC-B_locked]
    Craft[Campfire_tent_recipes]
    Prog[PROGRESS_COTTAGE_UNLOCK]
  end
  subgraph gcc [GC-C_locked]
    Place[Shop_room_placeholders]
  end
  Sites --> RES --> Flavor
  Flavor --> Craft
  Craft --> Prog
  Prog --> Place
```

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **GC STRATEGY** | Bible + impl unlock | Lead | **APPROVED** | Lead **`APPROVE GC STRATEGY`**, 2026-09-21 ET |
| **GC-A** | Site→RES + flint/grass flavor | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE GC-A`**, 2026-09-21 ET |
| **GC-B** | Campfire + tent + cottage unlock | CLOUD+DESKTOP | **IN PROGRESS** (this PR) | Lead **`APPROVE GC-B`** |
| **GC-C** | Placeholder shop/room volumes | CLOUD+DESKTOP | **LOCKED** | Lead **`APPROVE GC-C`** |

---

### GC-A — Site→RES map + display flavor

**Goal:** Day/body gather on VS_MVP piles uses canonical site kinds; logs remain greppable `GATHER: RES_WOOD` / `RES_STONE` / `RES_FIBER` with optional `(flint)` / `(grass)` flavor lines.

| Site kind | Yield | Flavor (UI/log only) |
|-----------|-------|----------------------|
| `trees` | `RES_WOOD` | Wood |
| `rocks` | `RES_STONE` | **Flint** |
| `flowers` | `RES_FIBER`, alternate harvest `RES_HERB` | **Grass** (fiber) |
| berry nodes | `RES_BERRY` | Berry |
| seed pods | `RES_SEED` | Spirit seed |
| den / camp / special | [Docs/21](21_REAP_SOW.md) | Not primary six-RES miners |

| Item | Spec |
|------|------|
| **Code** | `EHomeWorldGatherSiteKind`, `AHomeWorldResourcePile::GatherSiteKind`, `homeworld_gc_site_setup.py` |
| **Placement** | `place_vs_mvp_rs_material_sites.py`, `place_vs_mvp_resource_piles.py` |
| **Handoff** | [handoffs/GC_A_SITE_RES.md](handoffs/GC_A_SITE_RES.md) |

**Done criteria (GC-A):**

- [x] C++ maps site kinds to six `RES_*` (no 7th id)
- [x] `GATHER: RES_WOOD` + `RES_STONE` + `RES_FIBER` from mapped day sites (DESKTOP PIE or scripted harvest)
- [x] Optional `GATHER: RES_STONE (flint)` / `GATHER: RES_FIBER (grass)` flavor lines
- [x] Lead **`APPROVE GC-A`**, 2026-09-21 ET — GC-B unlocked

---

### GC-B — Campfire + tent + cottage unlock (this PR)

**Goal:** Named recipe costs at campfire / hub bootstrap; `PROGRESS:COTTAGE_UNLOCK` log/flag after demo loop. Handoff: [handoffs/GC_B_CRAFT_SPINE.md](handoffs/GC_B_CRAFT_SPINE.md).

**Done criteria (GC-B):**

- [ ] `CRAFT: CAMPFIRE` after 1 WOOD + 1 STONE + 1 FIBER (Stored-first)
- [ ] `CRAFT: TENT` after 3 WOOD + 2 FIBER
- [ ] `PROGRESS:COTTAGE_UNLOCK` once
- [ ] Lead **`APPROVE GC-B`** (chat) to unlock GC-C — **not stamped in PR**

---

### GC-C — Placeholder shops/rooms (locked)

**Goal:** Enter volumes → `PLACEHOLDER:*` logs only; no functional shop craft. **Out of scope for GC-A PR.**

---

## Non-goals (GC-A PR)

| Out | Why |
|-----|-----|
| Craft recipes / campfire / tent | GC-B |
| Cottage unlock / placeholder shops | GC-B / GC-C |
| Combat, movement mantle | Other tracks |
| Bulk new `.uasset` / `.umap` | Docs/20 allowlist |

---

## Hard rules

| Rule | Source |
|------|--------|
| Exactly six `RES_*` | `Docs/canon/SCHEMA.md` |
| Flint/grass = display only | `GATHER_CRAFT_BIBLE` A1 |
| Extend harvest path — no parallel inventory | `HomeWorldResourcePile` / `NormalizeResourceId` |
| Den/camp/special stay Docs/21 | Not primary miners |
