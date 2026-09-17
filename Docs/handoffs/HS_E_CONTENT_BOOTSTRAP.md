# Handoff — HS-E Content Bootstrap (KEEP-LOCAL) — Conductor parent DESKTOP

| Field | Value |
|-------|-------|
| **Phase** | HS-E |
| **Status** | **POLICY KEEP-LOCAL** stamped by Lead — DESKTOP verify **PENDING Conductor parent** |
| **Lead policy** | **`HS-E POLICY KEEP-LOCAL`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE HS-E`** — **not claimed** |
| **Spec** | [Docs/17e_HS_CONTENT_BOOTSTRAP.md](../17e_HS_CONTENT_BOOTSTRAP.md) |
| **Host (DESKTOP)** | **DESKTOP-21CT3H0** — Conductor **parent** only ([HR3_A_WINDOWS_EXEC.md](HR3_A_WINDOWS_EXEC.md)) |
| **Host (CLOUD)** | Linux — docs + preflight strengthen only; **no** Mannequins disk proof |
| **Policy meaning** | Keep PL-A `/Game/Characters/Mannequins/...` paths; copy Epic Mannequins **local-only**; never commit `.uasset`/`.umap` |
| **Evidence path** | This file — fill after parent verifies paths on DESKTOP |
| **Preflight** | `npm run preflight:ue` (DESKTOP); cloud: `--skip-mcp --assets-only` |
| **Prior** | [PL_A_CHARACTER.md](PL_A_CHARACTER.md) · [HR3_B_UE_PREFLIGHT.md](HR3_B_UE_PREFLIGHT.md) |

**Executor note:** Cursor Task / cloud agents **must not** claim DESKTOP Shell, MCP, or PIE. Steps below are for the **Conductor parent** session only. **Do not fake** path existence, preflight exit codes, or apply JSON.

---

## Expected paths (from `character_blueprint_config.json`)

| Key | Game path | Disk (after copy) |
|-----|-----------|-------------------|
| `skeletal_mesh` | `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` | `Content/Characters/Mannequins/Meshes/SKM_Manny_Simple.uasset` |
| `anim_blueprint` | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` | `Content/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.uasset` |
| Root dir | — | `Content/Characters/Mannequins/` |

---

## Conductor parent — DESKTOP checklist (do not fake)

Machine: **DESKTOP-21CT3H0** · `machineId` per [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

### A. Verify / copy Mannequins (local only)

**Source (Epic UE 5.7):**

```text
%UE_5.7%\Templates\TemplateResources\High\Characters\Content\Mannequins
```

**Destination:**

```text
<repo>\Content\Characters\Mannequins\
```

| Check | Pass? | Notes (real paths / times ET) |
|-------|-------|-------------------------------|
| `Content/Characters/Mannequins` exists | _pending parent_ | |
| `Meshes/SKM_Manny_Simple.uasset` exists | _pending parent_ | |
| `Anims/Unarmed/ABP_Unarmed.uasset` exists | _pending parent_ | |
| No Mannequins staged in `git status` | _pending parent_ | **Never** commit |

### B. Apply (MCP) — only if BP needs refresh

```text
execute_python_script("pl_a_apply_character.py")
```

| Check | Result |
|-------|--------|
| `Saved/PL_A_apply.json` `ok: true` | _pending parent_ |

### C. Preflight (fail-loud)

```powershell
# MCP: execute_python_script("preflight_ue_editor.py")
npm run preflight:ue -- --require-editor
```

| Check | Exit | Notes |
|-------|------|-------|
| No `MANNEQUINS_DIR_MISSING` | _pending_ | Dir missing = cold clone without copy |
| No `ASSET_MISSING_ON_DISK` for mesh/ABP | _pending_ | |
| `preflight:ue -- --require-editor` | _pending_ | Must be **0** before character PIE claims |

### D. Cold-clone failure mode (known — do not paper over)

Without the local copy: `git clone` succeeds; config still points at Mannequins; DESKTOP preflight **FAIL**s; apply **FAIL**s; PIE spawn breaks. Cloud `--assets-only` may still **PASS** — that is **not** proof.

Mitigation: complete § A–C on every new machine before character evidence.

---

## Pass/fail summary (fill after DESKTOP)

| Layer | Result | SHA / time (ET) |
|-------|--------|-----------------|
| Paths exist on DESKTOP | _pending parent_ | |
| Preflight `--require-editor` | _pending parent_ | |
| Lead **`APPROVE HS-E`** | **PENDING** | |

---

## Hard rules

- Docs/07 CLOSED — no reopen
- FALLBACK glide only — no free-flight / combat
- Exactly 10 masters — no invented product phases
- No `.uasset` / `.umap` commits
- No DESKTOP claims from Task executors or cloud VMs
- Do **not** claim **`APPROVE HS-E`** in this handoff
- Do **not** fake path verification

---

*HS-E handoff — KEEP-LOCAL setup for Conductor parent. Cloud filing is docs/preflight only.*
