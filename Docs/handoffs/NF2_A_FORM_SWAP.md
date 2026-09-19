# NF2-A — Soft form-swap feedback

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | NF2-A |
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE NF2-A`**, 2026-09-19 ET |
| **Track** | [Docs/27_NIGHT_FEEL_BUILD.md](../27_NIGHT_FEEL_BUILD.md) |

## What shipped

On body↔spirit form change (`ApplyFormForPhase`):

- Log `NF2: soft_feedback form=… phase=…`
- Soft **PointLight** pulse (~0.55s): warm amber (body) / cool moon (spirit)
- Optional `SoftFormSwapSound` + `SoftFormSwapParticles` on character defaults (NF2-D)

## Evidence

1. PIE on VS_MVP
2. `hw.TimeOfDay.SetPhase 1` then `3` (dusk→dawn)
3. Grep Output Log / `Saved/Logs` for `NF2: soft_feedback` and `FORM:`
4. Host: `py Content/Python/nf2_a_form_swap_evidence.py` → `Saved/nf2_a_form_swap_evidence.json`

## Gate

Lead **`APPROVE NF2-A`**, 2026-09-19 ET — unlocks NF2-B.
