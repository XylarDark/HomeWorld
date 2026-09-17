# Docs/17e — HS-E Character / Content Bootstrap Canon

| Field | Value |
|-------|-------|
| **Status** | **IN PROGRESS** — policy **KEEP-LOCAL** stamped by Lead; still **PENDING** Lead **`APPROVE HS-E`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (HomeWorld) — `gh` Contents API only |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | Lead **`APPROVE HS-D`**, 2026-09-17 ET (PR **#94**) — HS-E **UNLOCKED** |
| **Policy** | Lead **`HS-E POLICY KEEP-LOCAL`**, 2026-09-17 ET — Option A |
| **Debt** | Docs/17a ledger **#5** — Character assets local-only (`Content/Characters/Mannequins`) |
| **Baseline** | PL-A Manny + `ABP_Unarmed` ([PL_A_CHARACTER.md](handoffs/PL_A_CHARACTER.md), PRs #75–#77) · HR3-B preflight |
| **Hard rules honored** | Docs/07 CLOSED; FALLBACK glide only; no combat; **no `.uasset`/`.umap` commits** in this PR; exactly 10 masters; no invented product phases |

**Gate:** Lead typed **`HS-E POLICY KEEP-LOCAL`**. Next: Lead types **`APPROVE HS-E`**. This filing does **not** claim **`APPROVE HS-E`**.

**DESKTOP proofs:** Conductor-**parent** only (DESKTOP-21CT3H0). This cloud/executor filing documents checklists; it does **not** invent Shell/MCP/PIE results.

**Handoff:** [handoffs/HS_E_CONTENT_BOOTSTRAP.md](handoffs/HS_E_CONTENT_BOOTSTRAP.md) — Conductor-parent setup checklist (do not fake).

---

## Goal

One honest policy for Mannequins / Manny provenance + bootstrap / preflight expectations so **cold machines** do not silently break character spawn.

**Problem (debt #5):** PL-A powers spawn from **local** `Content/Characters/Mannequins` (~128 files / ~125 MB on DESKTOP). Those assets are **not in git**. A cold clone has config paths that point at missing project content → preflight `ASSET_MISSING_ON_DISK` / `MANNEQUINS_DIR_MISSING` and/or apply script `missing asset` → spawn breaks.

**Out of scope (this WAVE / this PR):** Silent `.uasset` dumps · AnimGraph / lookdev campaigns · inventing product phases · claiming DESKTOP proof from cloud · merging as approval stamp · claiming **`APPROVE HS-E`**.

---

## Policy stamp — KEEP-LOCAL (Lead, 2026-09-17 ET)

| Item | Spec |
|------|------|
| **Lead string** | **`HS-E POLICY KEEP-LOCAL`** |
| **Meaning** | Keep current PL-A paths (`/Game/Characters/Mannequins/...`). Mannequins stay **local-only** on each DESKTOP. Document copy + preflight. |
| **Config change** | **None** — `character_blueprint_config.json` already matches DESKTOP. |
| **Git** | Still **no** `.uasset`/`.umap` commits. |
| **Cold clone** | **Will fail loud** until § Complete DESKTOP setup runbook is followed. |
| **Options B/C** | Not chosen — Engine-only and binary strategy remain documented history only; do not implement without a new Lead policy string. |

---

## Current paths (cited from `main` via Contents API)

### Character config — `Content/Python/character_blueprint_config.json`

| Key | Value (PL-A / KEEP-LOCAL) |
|-----|----------------|
| `skeletal_mesh` | `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` |
| `anim_blueprint` | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` |
| Comments | Project path (**not** `/Engine/...`); DESKTOP must have local `Content/Characters/Mannequins` from Epic TP High Characters pack; no `.uasset` commits |

### Disk paths (expected after copy)

| Role | Project-relative path |
|------|------------------------|
| Mannequins root | `Content/Characters/Mannequins/` |
| Mesh uasset | `Content/Characters/Mannequins/Meshes/SKM_Manny_Simple.uasset` |
| Anim BP uasset | `Content/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.uasset` |

### Apply script — `Content/Python/pl_a_apply_character.py`

| Item | Value |
|------|-------|
| Target BP | `/Game/HomeWorld/Characters/BP_HomeWorldCharacter` |
| Reads | `Content/Python/character_blueprint_config.json` |
| Writes | `Saved/PL_A_apply.json` |
| Guards | Rejects config still on `/Engine/...`; fails if mesh/ABP `does_asset_exist` is false |
| Do **not** | Re-run legacy `vp_b_apply_character.py` after PL-A |

### Preflight — `config/preflight-ue.json` + `scripts/preflight-ue.js`

| Item | Value |
|------|-------|
| Character config path | `Content/Python/character_blueprint_config.json` |
| Required config keys | `skeletal_mesh` (required); `anim_blueprint` optional only for legacy VP-B mesh-only |
| Disk checks | Mesh + ABP from config; **plus** required local dir `Content/Characters/Mannequins` (KEEP-LOCAL) |
| Fail codes | `ASSET_MISSING_ON_DISK` · `MANNEQUINS_DIR_MISSING` |
| ABP path | Prefers config `anim_blueprint`; fallback `content.characterAnimBlueprint` = `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` |
| Character BP | `/Game/HomeWorld/Characters/BP_HomeWorldCharacter` |
| VS_MVP map | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| Engine paths | `/Engine/...` **skipped** for on-disk existence (treated as present) |
| Docs | [docs/Setup/UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) |

### Git / disk reality

| Path | In git? | Notes |
|------|---------|-------|
| `Content/Characters/Mannequins/` | **No** | Contents API: `Content/Characters` **does not exist** on `main` |
| `Content/Python/character_blueprint_config.json` | **Yes** | Paths assume local Mannequins |
| `Content/Python/pl_a_apply_character.py` | **Yes** | Apply via MCP on DESKTOP |
| Epic host source (PL-A handoff) | N/A (Engine install) | `UE_5.7\Templates\TemplateResources\High\Characters\Content\Mannequins` |

### PL-A evidence (already APPROVED — do not re-prove here)

See [PL_A_CHARACTER.md](handoffs/PL_A_CHARACTER.md): DESKTOP copy **PASS** (128 files); `pl_a_apply_character.py` `ok: true`; `preflight:ue -- --require-editor` exit **0**, `mesh_only: false`. Lead **`APPROVE PL-A`**, 2026-09-17 ET.

---

## Three policy options (Lead pick — **A chosen**)

### Option A — **KEEP-LOCAL** + documented setup runbook — **CHOSEN**

Lead string: **`HS-E POLICY KEEP-LOCAL`** (2026-09-17 ET). See § Policy stamp above and § Complete DESKTOP setup runbook below.

### Option B — **Engine-path-only** — **not chosen**

Would rewrite config to `/Engine/...`; PL-A apply rejects Engine mesh today; not proven viable. Lead string would have been `HS-E POLICY ENGINE-ONLY`.

### Option C — Lead-approved **binary strategy** — **not chosen**

Commit/distribute Mannequins via LFS or pack — **forbidden** in this PR (no silent `.uasset` dumps). Lead string would have been `HS-E POLICY BINARY`.

---

## Complete DESKTOP setup runbook (KEEP-LOCAL)

Host: **DESKTOP-21CT3H0**. Executor / cloud agents / Cursor Task **do not** run these steps — Conductor-**parent** only. Do **not** invent pass/fail from cloud.

### A.1 Prerequisites

1. UE **5.7** installed with **Third Person / TemplateResources High Characters** content available.
2. Repo cloned; `HomeWorld.uproject` opens.
3. Confirm git does **not** track `Content/Characters/Mannequins` (expected absent on cold clone).
4. Confirm config still PL-A KEEP-LOCAL paths (table above).

### A.2 Copy Mannequins (local only)

**Source (Epic install — PL-A citation):**

```text
%UE_5.7%\Templates\TemplateResources\High\Characters\Content\Mannequins
```

(Adjust drive/root to the machine’s UE 5.7 install. Example: `C:\Program Files\Epic Games\UE_5.7\Templates\TemplateResources\High\Characters\Content\Mannequins`.)

**Destination (project):**

```text
<repo>\Content\Characters\Mannequins\
```

**Rules:**

- Copy entire tree (PL-A evidence: ~128 files / ~125 MB).
- **Do not** `git add` any `.uasset` / `.umap`.
- After copy, these must exist on disk:
  - `Content/Characters/Mannequins/` (directory)
  - `Content/Characters/Mannequins/Meshes/SKM_Manny_Simple.uasset`
  - `Content/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.uasset`
- Optional sanity: `Meshes/SK_Mannequin.uasset` (or equivalent skeleton used by ABP).

### A.3 Apply character (MCP)

With Editor open + UnrealMCP on **55557**:

```text
execute_python_script("pl_a_apply_character.py")
```

Expect `Saved/PL_A_apply.json` with `"ok": true`, mesh `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple`, anim `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed`.

### A.4 Preflight (fail-loud if Mannequins missing)

```powershell
npm run preflight:ue -- --require-editor
```

Expect exit **0**. Disk checks must see:

- Directory `Content/Characters/Mannequins` (else **`MANNEQUINS_DIR_MISSING`**)
- Mesh + ABP under that tree (else **`ASSET_MISSING_ON_DISK`**)

Cloud `--assets-only` does **not** prove Mannequins on disk — DESKTOP-owned.

### A.5 Optional smoke

PIE spawn on VS_MVP / default map — Conductor parent only; paste real log excerpts into [HS_E_CONTENT_BOOTSTRAP.md](handoffs/HS_E_CONTENT_BOOTSTRAP.md). Do not invent greps.

### A.6 Never commit binaries

```powershell
git status
# Content/Characters/Mannequins must stay untracked / ignored — never staged
```

---

## Preflight check list (HS-E / debt #5 / KEEP-LOCAL)

| # | Check | Who | Pass criteria |
|---|-------|-----|---------------|
| 1 | `Content/Characters/Mannequins` exists on DESKTOP disk | DESKTOP parent | Folder present; key `.uasset` files present |
| 2 | Config paths still PL-A `/Game/Characters/Mannequins/...` | Any | Matches `character_blueprint_config.json` |
| 3 | `npm run preflight:ue -- --assets-only` | Cloud CI | Repo config keys non-empty (does **not** prove Mannequins on disk) |
| 4 | `npm run preflight:ue -- --skip-mcp` (or full) | DESKTOP | No `MANNEQUINS_DIR_MISSING` / `ASSET_MISSING_ON_DISK` for mesh/ABP |
| 5 | `npm run preflight:ue -- --require-editor` | DESKTOP | Exit 0; editor JSON green for BP mesh + ABP |
| 6 | `pl_a_apply_character.py` | DESKTOP MCP | `Saved/PL_A_apply.json` `ok: true` |
| 7 | No Mannequins in `git status` | DESKTOP | Local folder untracked / ignored — **never** staged |

---

## Cold-clone failure mode (document — do not paper over)

| Stage | What happens on cold machine without Mannequins copy |
|-------|------------------------------------------------------|
| `git clone` | Succeeds — Mannequins never in tree |
| Config | Still points at `/Game/Characters/Mannequins/...` |
| `preflight:ue` (DESKTOP, not assets-only) | **FAIL** — `MANNEQUINS_DIR_MISSING` and/or `ASSET_MISSING_ON_DISK` for `SKM_Manny_Simple` / `ABP_Unarmed` |
| `pl_a_apply_character.py` | **FAIL** — `missing asset: ...` |
| PIE spawn | Broken / mesh-empty / missing ABP depending on prior BP state |
| Cloud `--assets-only` | May still **PASS** (repo JSON only) — **false confidence**; disk proof is DESKTOP-owned |

**Mitigation under KEEP-LOCAL:** Run § Complete DESKTOP setup runbook before any character evidence or PIE claim on a new machine.

---

## Deliverables this PR

| Item | Path | Notes |
|------|------|-------|
| HS-E policy filing | [Docs/17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) | This doc — KEEP-LOCAL stamped; PENDING **`APPROVE HS-E`** |
| DESKTOP handoff | [handoffs/HS_E_CONTENT_BOOTSTRAP.md](handoffs/HS_E_CONTENT_BOOTSTRAP.md) | Conductor-parent checklist — do not fake |
| Board | [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) | HS-E **IN PROGRESS**; policy **KEEP-LOCAL** recorded |
| Preflight | `config/preflight-ue.json` + `scripts/preflight-ue.js` | Explicit Mannequins dir fail-loud |
| Preflight docs | [docs/Setup/UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) | KEEP-LOCAL / cold-clone section |

**Not in this PR:** `.uasset`/`.umap` · Engine-path config rewrite · LFS enablement · DESKTOP proof claims · product phase unlocks · **`APPROVE HS-E`** stamp.

---

## Next (after this filing)

1. ~~Lead types policy string~~ — **done:** **`HS-E POLICY KEEP-LOCAL`**.
2. Conductor parent runs DESKTOP setup checklist when needed ([HS_E_CONTENT_BOOTSTRAP.md](handoffs/HS_E_CONTENT_BOOTSTRAP.md)).
3. Lead types **`APPROVE HS-E`** when satisfied with KEEP-LOCAL + this filing (+ optional DESKTOP verify).
4. Then **HS-F** unlocks (sign-off & re-grade) per [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md).

---

## Gate

```
STOP — Lead approval required
Policy already chosen: HS-E POLICY KEEP-LOCAL
Type when ready:
  APPROVE HS-E
```

**Status:** character/bootstrap canon **COMPLETE as KEEP-LOCAL filing** — **PENDING** Lead **`APPROVE HS-E`**.

Until stamped: do not claim APPROVE HS-E; do not dump `.uasset`s; do not invent DESKTOP proofs; Docs/07 remains CLOSED; FALLBACK FLIGHT remains armed.

---

*PENDING APPROVE HS-E — Docs/17e. Policy **KEEP-LOCAL** recorded 2026-09-17 ET. Do not claim APPROVE in this PR.*

## Lead APPROVE HS-E

Lead **`APPROVE HS-E`** (Luke Thompson, 2026-09-17 ET) — character/bootstrap canon **APPROVED / CLOSED** (policy **KEEP-LOCAL**). **HS-F** (sign-off & re-grade) **UNLOCKED**.

---

*HS-E **APPROVED / CLOSED** — Lead **`APPROVE HS-E`**, 2026-09-17 ET.*
