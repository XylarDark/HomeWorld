# HR2-B Cold-Clone — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR2-B |
| **Status** | COMPLETE — await **`APPROVE HR2-B`** |
| **Lead gate** | **`APPROVE HR2-B`** unlocks HR2-C |
| **Spec** | [13b_HR2_B_COLD_CLONE.md](../13b_HR2_B_COLD_CLONE.md) |

## Summary

Cold-clone onboarding is documented and CI-enforced:

- **Pin registry:** `config/devenv-template-pin.json` (`2efd756`)
- **Runbook:** clone → `git submodule update --init --recursive DevEnvTemplate` → `npm run doctor:build` → `npm run doctor:ue`
- **CI:** `scripts/verify-devenv-submodule.sh` in `validate.yml`

## Evidence (cloud, 2026-09-17)

Empty `DevEnvTemplate/` → verify script (init) → `doctor:build` exit 0 → `doctor:ue` exit 0.

## Next

Lead **`APPROVE HR2-B`** → HR2-C (C++ CI gate / build-win64 required).
