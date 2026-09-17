# Docs/17e — HS-E Character / Content Bootstrap Canon

| Field | Value |
|-------|-------|
| **Status** | **PENDING** Lead policy pick + Lead **`APPROVE HS-E`** |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (HomeWorld) — `gh` Contents API only |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | Lead **`APPROVE HS-D`**, 2026-09-17 ET (PR **#94**) — HS-E **UNLOCKED** |
| **Debt** | Docs/17a ledger **#5** — Character assets local-only (`Content/Characters/Mannequins`) |
| **Baseline** | PL-A Manny + `ABP_Unarmed` ([PL_A_CHARACTER.md](handoffs/PL_A_CHARACTER.md), PRs #75–#77) · HR3-B preflight |
| **Hard rules honored** | Docs/07 CLOSED; FALLBACK glide only; no combat; **no `.uasset`/`.umap` commits** in this PR; exactly 10 masters; no invented product phases |

**Gate:** Lead picks policy (**A / B / C**), then types **`APPROVE HS-E`**. This filing does **not** claim **`APPROVE HS-E`**.

**DESKTOP proofs:** Conductor-**parent** only (DESKTOP-21CT3H0). This cloud/executor filing documents checklists; it does **not** invent Shell/MCP/PIE results.

---

## Goal

One honest policy for Mannequins / Manny provenance + bootstrap / preflight expectations so **cold machines** do not silently break character spawn.

**Problem (debt #5):** PL-A powers spawn from **local** `Content/Characters/Mannequins` (~128 files / ~125 MB on DESKTOP). Those assets are **not in git**. A cold clone has config paths that point at missing project content → preflight `ASSET_MISSING_ON_DISK` and/or apply script `missing asset` → spawn breaks.

**Out of scope (this WAVE / this PR):** Silent `.uasset` dumps · AnimGraph / lookdev campaigns · inventing product phases · claiming DESKTOP proof from cloud · merging as approval stamp.

---

## Current paths (cited from `main` via Contents API)

### Character config — `Content/Python/character_blueprint_config.json`

| Key | Value (PL-A) |
|-----|----------------|
| `skeletal_mesh` | `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` |
| `anim_blueprint` | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` |
| Comments | Project path (**not** `/Engine/...`); DESKTOP must have local `Content/Characters/Mannequins` from Epic TP High Characters pack; no `.uasset` commits |

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
| Disk checks | `content.skeletalMeshFromCharacterConfig: true` → checks config mesh on disk |
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

## Three policy options (Lead pick required)

### Option A — **KEEP-local** + documented setup runbook (**recommended default**)

| Item | Spec |
|------|------|
| **Meaning** | Keep current PL-A paths (`/Game/Characters/Mannequins/...`). Mannequins stay **local-only** on each DESKTOP. Document copy + preflight. |
| **Config change** | **None** required (already matches DESKTOP). |
| **Git** | Still **no** `.uasset`/`.umap` commits. |
| **Pros** | Lowest risk; matches live DESKTOP-21CT3H0; PL-A apply/preflight already green when folder present. |
| **Cons** | Cold clone / new machine **will** fail until setup runbook is followed. |
| **Lead string** | `HS-E POLICY KEEP-LOCAL` |

### Option B — **Engine-path-only**

| Item | Spec |
|------|------|
| **Meaning** | Point config at Engine-resident mannequin assets (no `Content/Characters` copy). |
| **Config change** | Would rewrite `skeletal_mesh` / `anim_blueprint` to `/Engine/...` (exact Engine mount paths **must** be verified on DESKTOP UE 5.7 before claiming viable). |
| **Preflight** | Today `scripts/preflight-ue.js` **skips** disk checks for `/Engine/...` — so cold-clone disk gate would go quiet, but Editor still must resolve Engine assets; PL-A apply **rejects** `/Engine/` mesh paths today (`pl_a_apply_character.py` guard). |
| **Pros** | No local 125 MB copy; no binary policy fight. |
| **Cons** | **Not proven viable** on this project: PL-A explicitly retired Engine DefaultSkeletalMesh mesh-only interim; apply script forbids Engine mesh; TemplateResources High Characters may not mount as `/Engine/...` the same way as project `/Game/...`. Requires Conductor-parent DESKTOP spike before accepting. |
| **Lead string** | `HS-E POLICY ENGINE-ONLY` |

### Option C — Lead-approved **binary strategy** (future)

| Item | Spec |
|------|------|
| **Meaning** | Commit or distribute Mannequins via **explicit** Lead-approved channel: Git LFS, Git large-file policy, or external content pack. |
| **This PR** | **Forbidden** — no silent `.uasset` dumps. |
| **Pros** | Cold clone can spawn without manual copy (if LFS/pack works). |
| **Cons** | Needs Lead binary policy, LFS quotas, license clarity for Epic template assets, CI bandwidth. Separate follow-on PR after policy. |
| **Lead string** | `HS-E POLICY BINARY` (then a later PR implements; not this filing) |

---

## Recommendation

**Recommend Option A (KEEP-local)** as default unless Lead confirms Engine-only is already viable on DESKTOP UE 5.7 with a green apply + preflight run.

**Why A:** Matches current DESKTOP state and PL-A APPROVED evidence; zero config churn; preserves hard rule against silent binaries; documents the known cold-clone failure mode instead of pretending git has the mesh.

**Do not pick B** without a Conductor-parent DESKTOP spike that: (1) finds real Engine asset paths, (2) updates config + relaxes/replaces the PL-A Engine reject guard, (3) proves `preflight:ue -- --require-editor` exit 0 and PIE spawn.

**Do not pick C** in this PR — policy acknowledgment only; implementation is a future Lead-gated PR.

---

## Option A — setup runbook skeleton (DESKTOP = Conductor parent)

Host: **DESKTOP-21CT3H0**. Executor / cloud agents **do not** run these steps.

### A.1 Prerequisites

1. UE **5.7** installed with **Third Person / TemplateResources High Characters** content available.
2. Repo cloned; `HomeWorld.uproject` opens.
3. Confirm git does **not** track `Content/Characters/Mannequins` (expected absent on cold clone).

### A.2 Copy Mannequins (local only)

**Source (Epic install — PL-A citation):**

```text
%UE_5.7%\Templates\TemplateResources\High\Characters\Content\Mannequins
```

(Adjust drive/root to the machine’s UE 5.7 install.)

**Destination (project):**

```text
<repo>\Content\Characters\Mannequins\
```

**Rules:**

- Copy entire tree (PL-A evidence: ~128 files / ~125 MB).
- **Do not** `git add` any `.uasset` / `.umap`.
- Key assets must exist after copy:
  - `Meshes/SKM_Manny_Simple.uasset`
  - `Meshes/SK_Mannequin.uasset` (or equivalent skeleton used by ABP)
  - `Anims/Unarmed/ABP_Unarmed.uasset`

### A.3 Apply character (MCP)

With Editor open + UnrealMCP on **55557**:

```text
execute_python_script("pl_a_apply_character.py")
```

Expect `Saved/PL_A_apply.json` with `"ok": true`, mesh `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple`, anim `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed`.

### A.4 Preflight

```powershell
npm run preflight:ue -- --require-editor
```

Expect exit **0**. Disk checks must see Mannequins under `Content/Characters/...` (not Engine skip).

### A.5 Optional smoke

PIE spawn on VS_MVP / default map — Conductor parent only; paste real log excerpts into handoffs. Do not invent greps.

---

## Preflight check list (HS-E / debt #5)

| # | Check | Who | Pass criteria |
|---|-------|-----|---------------|
| 1 | `Content/Characters/Mannequins` exists on DESKTOP disk | DESKTOP parent | Folder present; key `.uasset` files present |
| 2 | Config paths still PL-A `/Game/Characters/Mannequins/...` (if policy A) | Any | Matches `character_blueprint_config.json` |
| 3 | `npm run preflight:ue -- --assets-only` | Cloud CI | Repo config keys non-empty (does **not** prove Mannequins on disk) |
| 4 | `npm run preflight:ue -- --skip-mcp` (or full) | DESKTOP | No `ASSET_MISSING_ON_DISK` for mesh/ABP |
| 5 | `npm run preflight:ue -- --require-editor` | DESKTOP | Exit 0; editor JSON green for BP mesh + ABP |
| 6 | `pl_a_apply_character.py` | DESKTOP MCP | `Saved/PL_A_apply.json` `ok: true` |
| 7 | No Mannequins in `git status` | DESKTOP | Local folder untracked / ignored — **never** staged |

---

## Cold-clone failure mode (document — do not paper over)

| Stage | What happens on cold machine without Mannequins copy |
|-------|------------------------------------------------------|
| `git clone` | Succeeds — Mannequins never in tree |
| Config | Still points at `/Game/Characters/Mannequins/...` |
| `preflight:ue` (DESKTOP, not assets-only) | **FAIL** — `ASSET_MISSING_ON_DISK` for `SKM_Manny_Simple` and/or `ABP_Unarmed` |
| `pl_a_apply_character.py` | **FAIL** — `missing asset: ...` |
| PIE spawn | Broken / mesh-empty / missing ABP depending on prior BP state |
| Cloud `--assets-only` | May still **PASS** (repo JSON only) — **false confidence**; disk proof is DESKTOP-owned |

**Mitigation under Option A:** Run § Option A setup runbook before any character evidence or PIE claim on a new machine.

**Mitigation under Option B/C:** Only after Lead policy + follow-on config/binary PR — not claimed here.

---

## Deliverables this PR

| Item | Path | Notes |
|------|------|-------|
| HS-E policy filing | [Docs/17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) | This doc — PENDING Lead |
| Board | [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) | HS-E **IN PROGRESS**; HS-D stamped **APPROVED / CLOSED** |
| Config / scripts | — | **Unchanged** until Lead picks B or C |

**Not in this PR:** `.uasset`/`.umap` · Engine-path config rewrite · LFS enablement · DESKTOP proof claims · product phase unlocks · **`APPROVE HS-E`** stamp.

---

## Next (after Lead)

1. Lead types policy string: **`HS-E POLICY KEEP-LOCAL`** *or* **`HS-E POLICY ENGINE-ONLY`** *or* **`HS-E POLICY BINARY`**.
2. Lead types **`APPROVE HS-E`** when satisfied with the chosen policy + this filing.
3. If A: Conductor may add a short DESKTOP handoff pointer only; no binary commits. If B/C: separate implementation PR after policy.
4. Then **HS-F** unlocks (sign-off & re-grade) per [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md).

---

## Gate

```
STOP — Lead policy + approval required
1) Type one of:
     HS-E POLICY KEEP-LOCAL
     HS-E POLICY ENGINE-ONLY
     HS-E POLICY BINARY
2) Then type:
     APPROVE HS-E
```

**Status:** character/bootstrap canon **COMPLETE as DRAFT filing** — **PENDING** Lead policy + **`APPROVE HS-E`**.

Until stamped: do not claim APPROVE HS-E; do not dump `.uasset`s; do not invent DESKTOP proofs; Docs/07 remains CLOSED; FALLBACK FLIGHT remains armed.

---

*PENDING — Docs/17e HS-E Content Bootstrap. Awaiting Lead policy + **`APPROVE HS-E`**. Do not claim APPROVE in this PR. Recommendation: **A KEEP-local**.*
