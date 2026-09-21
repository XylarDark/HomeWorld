# GC-B — Campfire + tent craft + cottage unlock

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE GC-B`** 2026-09-21 ET; GC-C unlocked |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/22_GATHER_CRAFT_IMPL.md](../22_GATHER_CRAFT_IMPL.md) |
| **Prior** | GC-A **APPROVED / CLOSED** — Lead **`APPROVE GC-A`** 2026-09-21 ET |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Craft subsystem | `UHomeWorldCraftSubsystem` — Stored-first spend, progression flags |
| Craft station actor | `AHomeWorldCraftStation` — hub / campfire / kitchen / tent stub |
| Interact | `AHomeWorldCharacter::TryCraftInFront` + `UHomeWorldInteractAbility` |
| Stored spend hook | `UHomeWorldStoreTransferComponent::SetStoredCountForCraft` |
| Hub placement | `Content/Python/place_vs_mvp_gc_craft.py` → `GP_Craft_Hub` |
| Cheats | `hw.Craft.*` in `HomeWorld.cpp` |

---

## Bootstrap path (no campfire in world)

1. Run `place_vs_mvp_gc_craft.py` on `L_VS_MVP_Markers` → **`GP_Craft_Hub`** (HubBootstrap).
2. Day/body: face hub within ~280 cm, **Interact (E)** → pays **1 WOOD + 1 STONE + 1 FIBER** → spawns **`GP_Craft_Campfire`** ahead of player + log **`CRAFT: CAMPFIRE`**.
3. Face campfire, Interact → **3 WOOD + 2 FIBER** → tent stub **`GP_Craft_Tent`** + **`CRAFT: TENT`** + **`PROGRESS:COTTAGE_UNLOCK`**.
4. Optional: second campfire interact before unlock also emits **`PROGRESS:COTTAGE_UNLOCK`** (tent already placed).

Spend order: **Stored props first** (`STORE:` homestead bins), then inventory; logs **`CRAFT: spend inventory-only for RES_*`** when stored empty.

---

## Done criteria

- [ ] **`CRAFT: CAMPFIRE`** after paying 1+1+1 (stored and/or inventory)
- [ ] **`CRAFT: TENT`** after 3 WOOD + 2 FIBER (requires campfire placed once)
- [ ] **`PROGRESS:COTTAGE_UNLOCK`** once per session/demo loop
- [ ] GC-A greps still pass: **`GATHER: RES_WOOD`**, **`RES_STONE`**, **`RES_FIBER`**
- [ ] No 7th `RES_*`; no GC-C placeholder shops in this PR

---

## DESKTOP runbook

```text
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("place_vs_mvp_gc_craft.py")
# PIE — cheat path:
hw.Craft.GrantDemo
hw.Craft.Campfire
hw.Craft.Tent
hw.Craft.Status
# Or interact at GP_Craft_Hub / GP_Craft_Campfire
```

**Expected greps (Output Log):**

```text
CRAFT: CAMPFIRE
CRAFT: TENT
PROGRESS:COTTAGE_UNLOCK
CRAFT: spend stored RES_WOOD
CRAFT: spend inventory-only for RES_FIBER
```

**Stub recipes (cheat only in GC-B):**

```text
hw.Craft.Torch
hw.Craft.TameBait
hw.Craft.HealSalve
hw.Craft.FishGear
```

---

## Gate

Lead **`APPROVE GC-B`** in chat unlocks **GC-C** (placeholder shop/room volumes). **Do not stamp GC-B APPROVED in PR.**
