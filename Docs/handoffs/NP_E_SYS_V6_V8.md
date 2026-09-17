# Handoff — NP-E SYS V6–V8

| Field | Value |
|-------|-------|
| **Phase** | NP-E |
| **Status** | **COMPLETE — awaiting `APPROVE NP-E`** |
| **Lead stamp** | NP-D **APPROVED** (Luke Thompson, 2026-09-17 ET) |
| **Deliverable** | [12e_NP_E_SYS_V6_V8.md](../12e_NP_E_SYS_V6_V8.md) |

---

## What shipped

1. **V6 Heal ×3** — `UHomeWorldSpiritHealComponent` on `AHomeWorldSpiritWisp`; `HEAL:` logs; `UHomeWorldHealAbility` evolved; interact + GA_Heal path.
2. **V7 Nurture ×2** — `UHomeWorldNurtureComponent` on `AHomeWorldNurtureTarget`; N1_Crop (RES_SEED), N2_Stored (RES_WOOD); `NURTURE:` logs + `M_Nurtured` flag.
3. **V8 Dawn persist** — `UHomeWorldSaveGame` extended; `PersistDawnSnapshot` on `SetPhase(Dawn)`; `hw.Load` restores inventory + tame + heal + nurture.
4. **NP-D residual** — `AHomeWorldBeastPad` C++ actor (tame component in ctor); `place_vs_mvp_beast_tame.py` spawns actor class (no `add_component_by_class`).
5. **Placement** — `place_vs_mvp_spirit_heal.py`, `place_vs_mvp_nurture.py`; bootstrap chain extended.

---

## Windows evidence (DESKTOP-21CT3H0)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **Action** | **Safe-Build required** after merge (C++ changed) |
| **Scripts** | `place_vs_mvp_beast_tame.py`, `place_vs_mvp_spirit_heal.py`, `place_vs_mvp_nurture.py` |
| **PIE** | Runbook in Docs/12e — grep `HEAL:`, `NURTURE:`, `DAWN:`, `FORM:` |

Local `.umap` placement not committed (project policy).

---

## Out of scope

- Combat, seventh resource, store-transfer UI
- `.uasset`/`.umap` commits
- Product phases beyond NP-E

---

## Next gate

Lead **`APPROVE NP-E`** → product next-phase (NP-A…E) **complete**.
