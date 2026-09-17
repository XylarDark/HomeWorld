# Handoff — NP-D SYS V3–V4

| Field | Value |
|-------|-------|
| **Phase** | NP-D |
| **Status** | **APPROVED** — Lead **`APPROVE NP-D`**, 2026-09-17 ET |
| **Lead stamp** | Luke Thompson, 2026-09-17 ET |
| **Deliverable** | [12d_NP_D_SYS_V3_V4.md](../12d_NP_D_SYS_V3_V4.md) |

---

## What shipped

1. **`HomeWorldInventorySubsystem`** — six fixed slots, RES_* only, stack max 9, `TryAddResource` / `SpendTameFood`.
2. **`HomeWorldInventoryTypes`** — canonical RES_* IDs + legacy name normalization (Wood/Ore/Flowers).
3. **`AHomeWorldResourcePile::TryHarvest`** — +1 gather, deplete-until-dawn, inventory-full fail.
4. **`UHomeWorldBeastTameComponent`** — wild→cautious→tamed→helper; `TAME:` logs.
5. **`TryTameBeastInFront`** — wired in `UHomeWorldInteractAbility` (before harvest).
6. **`AHomeWorldBeastPad`** + **`place_vs_mvp_beast_tame.py`** — C++ actor with tame component in constructor (replaces unreliable `add_component_by_class` on TargetPoint).
7. **Runbook** — PIE checklist in Docs/12d.

---

## Windows evidence (DESKTOP-21CT3H0)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **HEAD (Safe-Build)** | `690a5e5` / follow-up NP-E merge |
| **Capture** | UnrealMCP Editor run, 2026-09-17 ET |

| Step | Result | Notes |
|------|--------|-------|
| Safe-Build @ `690a5e5` | **PASS** | Editor closed per protocol |
| Beast pad (TargetPoint + add_component) | **FAILED** | `add_component_by_class` returned None |
| **`AHomeWorldBeastPad` fix** | **SHIPPED** (NP-E branch) | Spawn C++ actor; tame component in ctor |

---

## Next gate

Lead **`APPROVE NP-D`** — **DONE** (2026-09-17 ET). NP-E unlocked and delivered; await **`APPROVE NP-E`**.
