# HR3-B UE Preflight — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR3-B |
| **Status** | **EVIDENCE FILED — AWAITING APPROVE HR3-B** |
| **Lead gate** | **`APPROVE HR3-B`** — after evidence review |
| **Spec** | [15_HR3_A_PLUS.md](../15_HR3_A_PLUS.md) § HR3-B |
| **Policy** | [docs/Setup/UE_PREFLIGHT.md](../../docs/Setup/UE_PREFLIGHT.md) |

---

## Goal

`npm run preflight:ue` exits **non-zero** when VP-A-class blockers are present (MCP down, missing slice assets, ABP skeleton / empty BP mesh) **before** verb PIE greps.

---

## Deliverables

| # | Item | Path |
|---|------|------|
| 1 | Host preflight script | `scripts/preflight-ue.js` |
| 2 | Blocker config | `config/preflight-ue.json` |
| 3 | npm scripts | `package.json` → `preflight:ue`, `preflight:ue:test` |
| 4 | Editor deep checks | `Content/Python/preflight_ue_editor.py` |
| 5 | Policy doc | [docs/Setup/UE_PREFLIGHT.md](../../docs/Setup/UE_PREFLIGHT.md) |
| 6 | CI (cloud) | `.github/workflows/validate.yml` — `--assets-only` + unit tests |

**Not in scope:** `.uasset` commits, gameplay C++, AnimGraph spike, doctor:ue policy changes.

---

## Exit code contract

| Exit | Meaning |
|------|---------|
| **0** | No blockers in the active mode |
| **1** | One or more blockers — fix before PIE / handoff |
| **2** | Misconfiguration (missing config, bad CLI) |

### Blocker classes (minimum set)

1. **MCP_UNREACHABLE** — port 55557 (skip: `--skip-mcp` or `HW_PREFLIGHT_SKIP_MCP=1`)
2. **CONFIG_*** — repo scripts + character config paths
3. **ASSET_MISSING_ON_DISK** — VS_MVP map, BP, ABP, config skeletal mesh on disk (full mode)
4. **EDITOR_ABP_SKELETON** — ABP skeleton / compile (editor script)
5. **EDITOR_BP_MESH_EMPTY** — empty skeletal mesh or anim_class on BP (editor script)
6. **EDITOR_MAP_MISSING** — VS_MVP map unloadable (editor script)

---

## Cloud evidence (this PR)

Host: Linux cloud agent VM, Node 22, no UE/MCP.

```bash
npm run preflight:ue -- --skip-mcp --assets-only
# preflight:ue exit: 0 (PASS)

npm run preflight:ue -- --assets-only --simulate-fail=EDITOR_ABP_SKELETON
# preflight:ue exit: 1 — [EDITOR_ABP_SKELETON] … VP-A class failure

npm run preflight:ue:test
# node:test — assets-only pass, simulate-fail pass, full skip-mcp smoke
```

CI: `validate` job runs assets-only preflight + unit tests on every PR.

---

## DESKTOP dry-run (Lead / Conductor)

After merge, on **DESKTOP-21CT3H0**:

### Pass path (expected after VP-B fixes)

```powershell
# Editor open, MCP green
execute_python_script("preflight_ue_editor.py")   # via MCP
npm run preflight:ue -- --require-editor           # exit 0
```

### Fail paths (reproduce VP-A class — before VP-B fix)

| Step | Command | Expected |
|------|---------|----------|
| MCP down | Close Editor → `npm run preflight:ue` | exit **1**, `MCP_UNREACHABLE` |
| ABP skeleton | With broken ABP → run editor script → `npm run preflight:ue -- --skip-mcp --require-editor` | exit **1**, `EDITOR_ABP_SKELETON` |
| Simulated | `npm run preflight:ue -- --simulate-fail=EDITOR_ABP_SKELETON` | exit **1** (any host) |

**VP-A counterfactual:** If preflight had run with `--require-editor` before verb greps, `EDITOR_ABP_SKELETON` would have blocked PIE with a clear exit **1** instead of empty `FORM:` / `HEAL:` greps.

---

## Cross-links

- [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md) — cloud cannot run editor script; DESKTOP owns deep checks
- [DOCTOR_POLICY.md](../../docs/Setup/DOCTOR_POLICY.md) — doctor:ue remains host hygiene; preflight is game harness
- [VP_A_PIE.md](VP_A_PIE.md) — hard-fail evidence that motivated HR3-B

---

## Gate

_(Awaiting Lead **`APPROVE HR3-B`** — cloud evidence + DESKTOP dry-run table above.)_
