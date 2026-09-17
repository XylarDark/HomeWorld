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
6. **`place_vs_mvp_beast_tame.py`** — idempotent tame component on beast pad actor in VS_MVP markers level.
7. **Runbook** — PIE checklist in Docs/12d.

---

## Windows evidence (required post-merge)

| Step | Command | Expected |
|------|---------|----------|
| Safe-Build | `.\Tools\Safe-Build.ps1` | C++ compile PASS |
| Beast pad | `execute_python_script("place_vs_mvp_beast_tame.py")` | `TAME: placed component` log |
| Gather smoke | PIE + `hw.Goods` | RES_* slot counts |
| Tame smoke | PIE + berry/herb + E on pad | `TAME: bond complete -> tamed` |

Local `.umap` / component placement **not committed**.

---

## Out of scope (NP-E)

- Heal ×3, nurture ×2, dawn inventory persist
- Store transfer UI (optional stub deferred)
- NightMix smoke fix (unless trivial on Windows)

---

## Next gate

Lead **`APPROVE NP-D`** → unlock NP-E.
