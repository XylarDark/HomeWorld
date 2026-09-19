# Docs/20 — UASSET allowlist + AI asset provenance

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / COMPLETE** — Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET (PR #108) |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (cloud) |
| **Supersedes** | Blanket “never commit `.uasset`/`.umap`” hard rule (HS-E era) — see [17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) |
| **Machine config** | [config/uasset-allowlist.json](../config/uasset-allowlist.json) · [`.gitattributes`](../.gitattributes) |

**Gate:** Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET — **policy live**. Allowlist active per §2; default KEEP-LOCAL elsewhere. Extend only via §7 + **`APPROVE UASSET ALLOWLIST <id>`**.

---

## 1. Source of truth

| Layer | Role | Git |
|-------|------|-----|
| **DCC / refs** | Blender `Lib/`, PNG/WebP refs, AI drafts + sidecars | Text + refs under `Docs/refs/ai/`, `art/wip/` |
| **UE Content** | Runtime `.uasset` / `.umap` | **Allowlist only** (§2); everything else **KEEP-LOCAL** |

Authoritative paths for automation: [docs/CONTENT_LAYOUT.md](../docs/CONTENT_LAYOUT.md). This doc governs **which Content binaries may enter git**, not gameplay canon.

---

## 2. Allowlist (Lead-extended 2026-09-18)

**Default:** **KEEP-LOCAL** for all Content not listed here. No silent mass adds.

| Path (repo-relative) | Purpose |
|----------------------|---------|
| `Content/HomeWorld/Maps/VS_MVP/**` | VS_MVP slice maps, markers, shot cameras (`CAM_*` actors live in-map) |
| `Content/HomeWorld/Characters/BP_*.uasset` | Gameplay-critical character BPs |
| `Content/HomeWorld/Characters/ABP_HomeWorldCharacter.uasset` | Character AnimBP (gameplay-critical) |
| `Content/HomeWorld/Abilities/GA_Place.uasset` | Place / build verb |
| `Content/HomeWorld/Abilities/GA_Interact.uasset` | Interact / gather-store handoff |
| `Content/HomeWorld/Abilities/GA_Dodge.uasset` | Dodge verb (placeholder GA) |
| `Content/HomeWorld/Abilities/GA_PrimaryAttack.uasset` | Primary attack verb (placeholder GA) |
| `Content/HomeWorld/Meshes/**` | VS_MVP dress meshes (homestead / gatherables / forest / transit) |
| `Content/HomeWorld/Materials/**` | Master materials + MPC for VS_MVP |
| `Content/HomeWorld/Biomes/**` | Biome probe / import targets |
| `Content/HomeWorld/Harvestables/**` | Harvestable import targets |
| `Content/HomeWorld/Dungeon/**` | Dungeon volume markers / import targets |
| `Content/HomeWorld/Characters/khronos_box_scale_ref/**` | Scale reference mesh |

**Explicitly excluded** (never commit without a new Lead gate + allowlist extension):

- Marketplace kit dumps, bulk imports
- `Content/Characters/Mannequins/**` — **KEEP-LOCAL** per [17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md)
- AI WIP dumps under Content
- `Content/__ExternalActors__/**` legacy DemoMap shards (grandfathered in history only — do not expand)

**Grandfathered (already in git):** Pre-Docs/20 tracked paths (Input, MainMenu, legacy POI BPs, etc.) remain in history; **new** commits to those paths require allowlist extension (§7).

---

## 3. Git LFS

Allowlisted binaries **must** use **Git LFS**.

1. One-time per machine: `git lfs install`
2. Patterns: [`.gitattributes`](../.gitattributes) — scoped to allowlist + grandfather block (not whole-repo `*.uasset` wildcard)
3. After clone: `git lfs pull`

CI / cold-clone: [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) · [13b_HR2_B_COLD_CLONE.md](13b_HR2_B_COLD_CLONE.md).

---

## 4. AI asset rules

| Step | Rule |
|------|------|
| **Generate** | AI tools produce drafts only — not direct Content drops |
| **Store drafts** | `Docs/refs/ai/` or `art/wip/` — PNG/WebP + sidecar JSON (prompt, tool, date, license note) |
| **Promote** | Human or Lead promotes a draft → DESKTOP import → allowlisted path → log row in [AI_ASSET_LOG.md](AI_ASSET_LOG.md) |
| **Log** | Every promoted AI-influenced asset: one row in [AI_ASSET_LOG.md](AI_ASSET_LOG.md) |
| **License** | Record tool ToS + output rights in log **license note** column; no uncited third-party weights in shipped assets |
| **Forbidden** | Raw AI dump straight into `Content/` without promote + log |

---

## 5. Bot / agent rules

| Actor | May commit | Binary submit |
|-------|------------|-----------------|
| **Cloud agent** | Scripts, C++, docs, JSON | **No** — propose only |
| **Cloud agent** | Allowlisted `.uasset`/`.umap` | **Only** after Lead/Conductor explicit save+commit instruction **or** DESKTOP job with evidence |
| **DESKTOP (Conductor parent)** | Allowlisted binaries | Yes — with LFS + [AI_ASSET_LOG.md](AI_ASSET_LOG.md) when AI-assisted |
| **All agents** | Mass Content add | **Forbidden** — explicit paths only |

Cross-links: [swarm/CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) · [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md).

---

## 6. Cold clone / preflight

| Check | Command |
|-------|---------|
| Allowlisted assets on disk | `npm run check:uasset-allowlist` (warn) · `--strict` (fail) |
| Full UE preflight | `npm run preflight:ue` · [docs/Setup/UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) |
| Mannequins (KEEP-LOCAL) | Still required locally — `MANNEQUINS_DIR_MISSING` unchanged ([17e](17e_HS_CONTENT_BOOTSTRAP.md)) |

Missing allowlisted LFS objects → run `git lfs pull`; if still missing, DESKTOP bootstrap per [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md).

---

## 7. Extending the allowlist

1. File PR updating this doc §2 + [config/uasset-allowlist.json](../config/uasset-allowlist.json) + `.gitattributes`
2. Lead review — no drive-by expansions
3. Lead types **`APPROVE UASSET ALLOWLIST <id>`** (e.g. `APPROVE UASSET ALLOWLIST INPUT`) in PR or gate thread
4. Conductor stamps PHASE_BOARD + merges

---

## 8. Gate stamp

| Field | Value |
|-------|-------|
| **Lead string** | **`APPROVE UASSET POLICY`** |
| **Approved by** | Lead (2026-09-17 ET) |
| **Date (ET)** | 2026-09-17 |
| **PR / SHA** | PR **#108** (merge SHA on `main` after squash) |
