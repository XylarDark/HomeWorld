# HR2-C C++ CI Gate — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR2-C |
| **Status** | COMPLETE — await **`APPROVE HR2-C`** |
| **Lead gate** | **`APPROVE HR2-C`** closes HR2 track |
| **Spec** | [13c_HR2_C_CI_GATE.md](../13c_HR2_C_CI_GATE.md) |

## Summary

C++ PRs now **require** green `build-win64` (self-hosted Windows) unless Lead documents a waiver.

- **Path filters:** `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**`, `.github/workflows/ci.yml`
- **Docs-only:** `validate.yml` only — no Win64 build
- **Waiver:** PR body `Lead waiver: build-win64` or label `lead-waiver-build-win64`
- **Policy:** [docs/Setup/CI_POLICY.md](../../docs/Setup/CI_POLICY.md)
- **Branch protection:** [docs/Setup/CI_SETUP.md](../../docs/Setup/CI_SETUP.md) § Branch protection (Lead sets in GitHub)

## Prior stamp

Lead **`APPROVE HR2-B`** (Luke Thompson, 2026-09-17 ET) — HR2-B **APPROVED**; HR2-C unlocked.

## Next

Lead **`APPROVE HR2-C`** → HR2 track **CLOSED**. No HR2-D.
