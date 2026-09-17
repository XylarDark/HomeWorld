# Docs/12e — NP-E SYS V6–V8 (Heal + Nurture + Dawn Persist)

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE NP-E`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent** | [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) |
| **Unlocked by** | Lead **`APPROVE NP-D`**, 2026-09-17 ET |
| **Canon** | [03_SYSTEMS_MVP.md](03_SYSTEMS_MVP.md) §6–7 |

---

## Deliverables

| Item | Path | Disposition |
|------|------|-------------|
| Heal ×3 (V6) | `HomeWorldSpiritHealComponent.*`, `HomeWorldSpiritWisp.*`, `HomeWorldHealAbility.*` | **PRESENT** — hurt→healed; RES_HERB/RES_SEED |
| Nurture ×2 (V7) | `HomeWorldNurtureComponent.*`, `HomeWorldNurtureTarget.*` | **PRESENT** — N1_Crop, N2_Stored; M_Nurtured flag |
| Dawn persist (V8) | `HomeWorldSaveGame.*`, `HomeWorldSaveGameSubsystem.*`, `HomeWorldTimeOfDaySubsystem` | **PRESENT** — inventory + tame + heal + nurture on Dawn |
| Beast pad residual | `HomeWorldBeastPad.*`, `place_vs_mvp_beast_tame.py` | **PRESENT** — C++ actor ctor (no add_component_by_class) |
| Spirit placement | `Content/Python/place_vs_mvp_spirit_heal.py` | **PRESENT** — idempotent GP_SpiritWisp_A/B/C |
| Nurture placement | `Content/Python/place_vs_mvp_nurture.py` | **PRESENT** — idempotent GP_N1_Crop, GP_N2_Stored |
| Handoff | [handoffs/NP_E_SYS_V6_V8.md](handoffs/NP_E_SYS_V6_V8.md) | **PRESENT** |

---

## V6 — Heal ×3

| Rule | Implementation |
|------|----------------|
| Three spirits at SM_SpiritWound | `AHomeWorldSpiritWisp` ×3 via placement script |
| Night/spirit only | `TryHeal` checks `GetIsSpiritForm` + spirit phase |
| RES_HERB default, RES_SEED alternate | `SpendHealResource()` on inventory subsystem |
| States hurt → healed | `EHomeWorldSpiritHealState`; log `HEAL:` |
| Soft fail | day/body, already healed, no resource |
| GA_Heal | `UHomeWorldHealAbility` → `TryHealSpiritInFront` |

**Console (PIE):**

```text
hw.Gather.Flowers 1     → RES_HERB +1
hw.TimeOfDay.Phase 2    → spirit form + NightMix 0.85
```

Interact (E) facing `GP_SpiritWisp_A` → `HEAL: success Spirit_A consumed RES_HERB`

---

## V7 — Nurture ×2

| Target | Requires | Success log |
|--------|----------|-------------|
| N1_Crop (`GP_N1_Crop`) | 1× RES_SEED | `NURTURE: success N1_Crop M_Nurtured=1` |
| N2_Stored (`GP_N2_Stored`) | 1× RES_WOOD | `NURTURE: success N2_Stored M_Nurtured=1` |

Homestead only (markers near `SM_Cabin` / `GP_PlayerStart`). Night/spirit only.

---

## V8 — Dawn persist

| Field | Saved on Dawn (`SetPhase(Dawn)`) | Restored on `hw.Load` |
|-------|-----------------------------------|------------------------|
| Six RES_* slots | `SavedInventorySlots` | `RestoreSlotsFrom` |
| Beast tame state | `SavedBeastTameState` | `ApplyPersistedState` on tame component |
| Spirit heal states | `SavedSpiritHealIds` + states | per wisp id |
| Nurture flags | `bSavedN1Nurtured`, `bSavedN2Nurtured` | `ApplyPersistedNurtured` |

**Log:** `DAWN: persisted inventory=N ...` on phase transition to Dawn.

**Form swap (NP-C verify):** `hw.TimeOfDay.Phase 3` → `FORM: body form`; NightMix 0.15.

---

## Windows Safe-Build (C++ changed)

After merge:

```powershell
.\Tools\Safe-Build.ps1
```

Then (Editor):

```text
execute_python_script("place_vs_mvp_beast_tame.py")
execute_python_script("place_vs_mvp_spirit_heal.py")
execute_python_script("place_vs_mvp_nurture.py")
```

Or `bootstrap_project.py` (includes NP-D/E placement chain).

Local `.umap` changes are **not committed**.

---

## PIE runbook — heal + nurture + dawn

**Prerequisites:** Safe-Build; placement scripts run; day start.

### V6 Heal (any order)

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | `hw.Gather.Flowers 1` (×3 for three heals) | `GATHER: RES_HERB +1` |
| 2 | Portal to planet (night) or night at homestead + portal | shrine transit OK |
| 3 | `hw.TimeOfDay.Phase 2` | `FORM: spirit form` |
| 4 | Interact each wisp A/B/C | `HEAL: success Spirit_*` |
| 5 | Repeat with no herb | `HEAL: soft fail — no RES_HERB or RES_SEED` |
| 6 | `hw.TimeOfDay.Phase 0` + Interact wisp | `HEAL: soft fail — day or body form` |

### V7 Nurture

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | `hw.Gather` seed + wood (console or piles) | RES_SEED, RES_WOOD in inventory |
| 2 | Night/spirit at homestead (`GP_N1_Crop`, `GP_N2_Stored`) | |
| 3 | Interact N1 then N2 | `NURTURE: success` ×2 |
| 4 | Interact again | `NURTURE: soft success — already nurtured` |

### V8 Dawn + form

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | After night verbs, `hw.TimeOfDay.Phase 3` | `FORM: body form`; `DAWN: persisted inventory=...` |
| 2 | `hw.Goods` | prior RES_* counts unchanged |
| 3 | `hw.Save` then restart PIE + `hw.Load` | inventory + verb states restored |

---

## Gate

Lead **`APPROVE NP-E`** → **product NP track complete** (final NP phase).

---

*NP-E delivered 2026-09-17 ET under Lead APPROVE NP-D.*
