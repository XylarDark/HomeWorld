# Handoff — NP-D SYS V3–V4

| Field | Value |
|-------|-------|
| **Phase** | NP-D |
| **Status** | **COMPLETE — awaiting `APPROVE NP-D`** |
| **Lead stamp** | NP-C **APPROVED** (Luke Thompson, 2026-09-17 ET) |
| **Deliverable** | [12d_NP_D_SYS_V3_V4.md](../12d_NP_D_SYS_V3_V4.md) |

---

## What shipped

1. **`HomeWorldInventorySubsystem`** — six fixed slots, RES_* only, stack max 9, `TryAddResource` / `SpendTameFood`.
2. **`HomeWorldInventoryTypes`** — canonical RES_* IDs + legacy name normalization (Wood/Ore/Flowers).
3. **`AHomeWorldResourcePile::TryHarvest`** — +1 gather, deplete-until-dawn, inventory-full fail.
4. **`UHomeWorldBeastTameComponent`** — wild→cautious→tamed→helper; `TAME:` logs.
5. **`TryTameBeastInFront`** — wired in `UHomeWorldInteractAbility` (before harvest).
6. **`place_vs_mvp_beast_tame.py`** — idempotent `GP_BeastPad` spawn + tame component on `L_VS_MVP_Markers`.
7. **Runbook** — PIE checklist in Docs/12d.

---

## Windows evidence (DESKTOP-21CT3H0)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **HEAD (Safe-Build)** | `690a5e5` |
| **Capture** | UnrealMCP Editor run, 2026-09-17 ET |

| Step | Result | Notes |
|------|--------|-------|
| Safe-Build @ `690a5e5` | **PASS** | Editor closed per protocol, then relaunched |
| `place_vs_mvp_beast_tame.py` (initial) | **PARTIAL** | Script ran; **no beast pad actor** on level — `No beast pad actor found` |
| Beast pad fix | **SHIPPED** | Script now spawns idempotent `GP_BeastPad` TargetPoint (tags `BeastPad`, `SM_BeastPad_01`) near `CRUMB_Landing`, then attaches `UHomeWorldBeastTameComponent` |
| Re-run after fix | **PENDING** | Expect `Spawned TargetPoint GP_BeastPad` + `TAME: placed component` in Output Log |

Local `.umap` changes from placement scripts are **not committed** (project policy).

---

## Out of scope (NP-E)

- Heal ×3, nurture ×2, dawn inventory persist
- Store transfer UI (optional stub deferred)
- NightMix smoke fix (unless trivial on Windows)

---

## Next gate

Lead **`APPROVE NP-D`** → unlock NP-E.
