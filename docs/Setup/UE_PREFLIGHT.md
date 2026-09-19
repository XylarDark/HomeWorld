# UE preflight — fail loud before PIE (HR3-B)

**When to use this:** Before DESKTOP PIE / verb greps (VP-A class), before filing a DESKTOP handoff PR, or in CI to catch repo-side misconfiguration early.

**Problem solved:** VP-A ran verb greps and filed a hard-fail only after PIE — ABP skeleton missing, empty BP mesh. Preflight exits **non-zero** on those blocker classes **before** wasting a phase on empty `FORM:` greps.

**Related:** [DOCTOR_POLICY.md](DOCTOR_POLICY.md) (DevEnvTemplate host hygiene — separate concern), [WINDOWS_BRIDGE.md](WINDOWS_BRIDGE.md) (cloud → DESKTOP lane), [MCP_SETUP.md](MCP_SETUP.md) (port 55557).

---

## Commands

| Command | Host | What it checks |
|---------|------|----------------|
| `npm run preflight:ue` | **DESKTOP** (Editor open) | MCP **55557**, repo config, on-disk `.uasset`/`.umap`, optional `Saved/preflight_ue_editor.json` |
| `npm run preflight:ue -- --skip-mcp` | DESKTOP without MCP probe | Repo + disk assets + editor JSON |
| `npm run preflight:ue -- --require-editor` | DESKTOP before PIE | Above + **fail** if editor deep-check JSON missing or red |
| `npm run preflight:ue -- --assets-only` | **Cloud CI / Linux VM** | Repo scripts + `character_blueprint_config.json` paths only |
| `HW_PREFLIGHT_SKIP_MCP=1 npm run preflight:ue` | Cloud CI | Same as `--skip-mcp` (env alias) |
| `npm run preflight:ue:test` | Any | Unit tests for exit codes |

Config (machine-readable): [config/preflight-ue.json](../../config/preflight-ue.json).

---

## DESKTOP workflow (Conductor / Lead)

1. **`.\Tools\Safe-Build.ps1`** if C++ changed — [BUILD_POLICY.md](BUILD_POLICY.md).
2. Open **Unreal Editor** (`HomeWorld.uproject`); MCP green dot on port **55557**.
3. **Editor deep checks** (MCP):

   ```text
   execute_python_script("preflight_ue_editor.py")
   ```

   Writes `Saved/preflight_ue_editor.json` (ABP skeleton compile, BP mesh/anim_class, VS_MVP map load).

4. **Host preflight:**

   ```powershell
   npm run preflight:ue -- --require-editor
   ```

5. Only if exit **0** → run PIE / verb grep runbooks ([Docs/14 VP-A](../../Docs/14_VP_VERIFY_POLISH.md)).

---

## Cloud agent workflow

Cloud VMs have **no UE / MCP**. Run repo-side gate only:

```bash
npm run preflight:ue -- --skip-mcp --assets-only
npm run preflight:ue:test
```

CI runs the same in [validate.yml](../../.github/workflows/validate.yml). Full asset and ABP checks remain **DESKTOP-owned** per [WINDOWS_BRIDGE.md](WINDOWS_BRIDGE.md).

---

## Blocker classes (exit 1)

| Code | Meaning |
|------|---------|
| `MCP_UNREACHABLE` | Port 55557 closed — Editor not running or UnrealMCP not loaded |
| `CONFIG_MISSING` | Required repo file or invalid JSON |
| `CONFIG_EMPTY_PATH` | `character_blueprint_config.json` missing `skeletal_mesh` (`anim_blueprint` may be empty for VP-B mesh-only) |
| `ASSET_MISSING_ON_DISK` | Expected `.uasset`/`.umap` absent under `Content/` (`/Engine/...` paths skipped) |
| `MANNEQUINS_DIR_MISSING` | `Content/Characters/Mannequins` missing — HS-E KEEP-LOCAL local copy required (see Docs/17e) |
| `EDITOR_RESULTS_MISSING` | No `Saved/preflight_ue_editor.json` when `--require-editor` |
| `EDITOR_ABP_SKELETON` | ABP skeleton missing or AnimBP compile error (**VP-A root cause**) |
| `EDITOR_BP_MESH_EMPTY` | BP skeletal mesh unset (mesh-only: empty `anim_class` OK when config `anim_blueprint` empty) |
| `EDITOR_MAP_MISSING` | VS_MVP map missing or unloadable |

Dry-run a fail class (tests / docs):

```bash
npm run preflight:ue -- --assets-only --simulate-fail=EDITOR_ABP_SKELETON
```

---



## HS-E KEEP-LOCAL — Mannequins on DESKTOP (fail loud)

Lead policy **`HS-E POLICY KEEP-LOCAL`** (2026-09-17 ET): character mesh/ABP stay at project `/Game/Characters/Mannequins/...`. Those assets are **not in git**.

| Mode | Mannequins disk check? |
|------|-------------------------|
| `preflight:ue` / `--skip-mcp` / `--require-editor` (DESKTOP) | **Yes** — requires dir `Content/Characters/Mannequins` + mesh/ABP `.uasset` files |
| `--assets-only` (cloud CI) | **No** — repo JSON only; may PASS on cold clone (**false confidence**) |

**Fail codes when folder/assets missing (DESKTOP disk modes):**

| Code | Meaning |
|------|---------|
| `MANNEQUINS_DIR_MISSING` | `Content/Characters/Mannequins` directory absent — copy from Epic UE 5.8 `Templates\TemplateResources\High\Characters\Content\Mannequins` |
| `ASSET_MISSING_ON_DISK` | Config mesh/ABP `.uasset` not under `Content/` |

**Setup runbook:** [Docs/17e_HS_CONTENT_BOOTSTRAP.md](../../Docs/17e_HS_CONTENT_BOOTSTRAP.md) · DESKTOP checklist: [Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md](../../Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md).

**Never** `git add` Mannequins `.uasset`/`.umap` (excluded from [Docs/20 allowlist](../../Docs/20_UASSET_AI_POLICY.md)). Do not claim DESKTOP path proof from cloud agents.

Config key: `content.requiredLocalDirs` in [config/preflight-ue.json](../../config/preflight-ue.json).

### Docs/20 allowlisted assets (warn-only)

`npm run check:uasset-allowlist` — warns when required allowlisted VS_MVP / character assets are missing on disk. Use `--strict` to fail. See [Docs/20_UASSET_AI_POLICY.md](../../Docs/20_UASSET_AI_POLICY.md).

---

## Evidence capture (HS-D)

After DESKTOP PIE (or any real `Saved/Logs/*.log`), score canonical verb prefixes **without inventing greps**:

```powershell
npm run evidence:grep -- --log Saved/Logs/HomeWorld.log
npm run evidence:grep -- --log Saved/Logs/HomeWorld.log --json Saved/hs_d_evidence_grep.json
# Gate mode (exit 1 if any required prefix MISSING):
npm run evidence:grep -- --log Saved/Logs/HomeWorld.log --strict
```

Prefixes: `FORM:` `FALLBACK:` `HEAL:` `NURTURE:` `DAWN:` `TAME:` `GATHER:` `STORE:` `INVENTORY:` (PL-C dump via `hw.Inventory.Dump`).

Policy: [Docs/17d_HS_EVIDENCE.md](../../Docs/17d_HS_EVIDENCE.md) · DESKTOP checklist: [Docs/handoffs/HS_D_EVIDENCE.md](../../Docs/handoffs/HS_D_EVIDENCE.md) · re-verify: [SWARM_OPS.md](../../swarm/SWARM_OPS.md) §4c.

Cloud/CI may run `npm run evidence:grep:test` (fixture logs only — not a substitute for DESKTOP PIE).

## vs `doctor:ue`

| Tool | Purpose |
|------|---------|
| **`npm run doctor:ue`** | DevEnvTemplate health — accepted UE-host **declines** ([DOCTOR_POLICY.md](DOCTOR_POLICY.md)) |
| **`npm run preflight:ue`** | **Game harness** — MCP, slice assets, PIE prerequisites |

Do not extend doctor policy for PIE blockers; keep preflight separate (HR3-B).

---

## Handoff evidence

Implementation evidence and DESKTOP dry-run expectations: [Docs/handoffs/HR3_B_UE_PREFLIGHT.md](../../Docs/handoffs/HR3_B_UE_PREFLIGHT.md).

*HR3-B — harness screams before empty verb greps.*