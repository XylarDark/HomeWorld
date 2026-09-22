# Docs/32 — Prototype Assets (PA — Homestead dress)

| Field | Value |
|-------|-------|
| **Track ID** | **PA** — Prototype Assets (Homestead dress) |
| **Status** | **PA STRATEGY APPROVED** · **PA-A CLOSED / COMPLETE** · **PA-C IN PROGRESS** (tranche-2 **DONE**; optional island rim only) · **PA-D IN PROGRESS** (DESKTOP batch import + place — Lead **`APPROVE PA-D`** **GRANTED** 2026-09-22 ET) · **PA-E LOCKED** · track **not CLOSED** |
| **Date** | 2026-09-22 |
| **Author** | Cloud agent (HomeWorld) |
| **Scope locked** | **Homestead kit only** — Lead **`APPROVE PA STRATEGY — homestead kit only`**, 2026-09-22 ET (planetside out) |
| **Prior tracks** | [30_DEMO_SPINE.md](30_DEMO_SPINE.md) **CLOSED** · [31_SPIRIT_STEALTH_FEEL.md](31_SPIRIT_STEALTH_FEEL.md) **IN PROGRESS** (orthogonal) |
| **Prefix** | **PA** — do **not** reuse DS / SS / GC gate strings |

---

## Gate

Lead **`APPROVE PA STRATEGY`** — **GRANTED** (chat, 2026-09-22 ET; Lead typed **`APPROVE PA STRATEGY — homestead kit only`**).

Lead **`APPROVE PA-A`** — **GRANTED** (chat, 2026-09-22 ET). Gap audit **accepted**; **PA-A CLOSED / COMPLETE**.

Lead **`APPROVE PA-C`** — **GRANTED** (chat, 2026-09-22 ET). **PA-C IN PROGRESS** — tranche-1 cliffs + pine **DONE**; tranche-2 cabin, path stones, planters, fence, glider perch **DONE** (FBX on `AssetCreation/Exports/Homestead/`).

Lead **`APPROVE PA-D`** — **GRANTED** (chat, 2026-09-22 ET). **PA-D IN PROGRESS** — DESKTOP **`batch_import_asset_creation.py`** + **`place_vs_mvp_dress.py`** on **DESKTOP-21CT3H0**; evidence pending. **Do not** stamp PA-D **CLOSED**, **PA-E done**, or **whole PA track CLOSED** until Lead **`APPROVE PA-E`** + Shot 1/2 evidence.

**Handoffs:** [handoffs/PA_STRATEGY.md](handoffs/PA_STRATEGY.md) — **APPROVED / CLOSED** (PA-0) · [handoffs/PA_A_GAP_AUDIT.md](handoffs/PA_A_GAP_AUDIT.md) — **APPROVED / CLOSED** (PA-A) · [handoffs/PA_C_BLENDER.md](handoffs/PA_C_BLENDER.md) · [handoffs/PA_C_TRANCHE1.md](handoffs/PA_C_TRANCHE1.md) · [handoffs/PA_C_TRANCHE2.md](handoffs/PA_C_TRANCHE2.md) · [handoffs/PA_D_IMPORT_PLACE.md](handoffs/PA_D_IMPORT_PLACE.md) — **APPROVED** (awaiting DESKTOP evidence).

**Kit plate (refs):** [refs/ai/homestead_kit_plate_labeled.jpg](refs/ai/homestead_kit_plate_labeled.jpg) · [../AssetCreation/RefImages/homestead_kit_plate_labeled.jpg](../AssetCreation/RefImages/homestead_kit_plate_labeled.jpg) · sidecar [refs/ai/homestead_kit_plate_labeled.sidecar.json](refs/ai/homestead_kit_plate_labeled.sidecar.json)

---

## Goal

Replace **engine-primitive / greybox** homestead kit meshes on VS_MVP with **demo-readable low-poly** dress (SMG-like per [AssetCreation/STYLE_GUIDE.md](../AssetCreation/STYLE_GUIDE.md)) so **Shot 1** (lookout key-art) and **Shot 2** (cabin / garden / path) read as intentional art in PIE — **not ship-final**, not Quixel photoreal.

---

## Quality bar

| In | Out |
|----|-----|
| Low-poly, flat-friendly, wholesome cartoon (SMG-like STYLE_GUIDE) | Engine box/cylinder **placeholders** for **locked homestead kit** listed below |
| Same `SM_*` names on upgrade-in-place | Hero Substance maps, new biomes, photoreal scans |
| Nanite on opaque statics; **UCX** collision per [MVP_EXPORT_MANIFEST.md](../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md) | Planetside camp dress, combat props, character hero meshes |

---

## Scope IN (homestead-only)

**Upgrade-in-place** (keep anchor labels / export names):

| Asset | Action |
|-------|--------|
| `SM_Cabin` | Upgrade modular cabin mesh |
| `SM_IslandTop` | Upgrade plateau top; **CREATE** cliff module kit under/overhang |
| `SM_Pine_Homestead` | Upgrade stylized pine (S/M/L family) |
| `SM_Lookout_Pad` | Upgrade lookout pad |
| `SM_Glider_Perch` | Upgrade glider perch |
| `SM_Shrine_Homestead` | Polish shrine (portal glow read) |

**CREATE (new meshes, homestead kit):**

| Asset | Action |
|-------|--------|
| Cliff modules | Torn-earth underside modules compositing with `SM_IslandTop` |
| Planters ×3 | Raised beds matching garden zone ([GRAYBOX_LAYOUT.md](../Lib/00_Core/GRAYBOX_LAYOUT.md)) |
| Fence segments | Post-and-rail along garden / path edges |
| Path dress | Stone slab path along `SM_Path_Homestead` corridor |
| Islet crumbs | Optional small floating islet dressing (transit read OK) |

**Silhouettes only:** family scale figures at lookout — no character hero work.

---

## Scope OUT

- Planetside camp dress, forest path hero kit, hamlet roofs (separate track)
- Characters beyond silhouettes
- Combat props, gatherable hero meshes (unless already on allowlist elsewhere)
- Quixel / Megascans photoreal
- New biomes, Marketplace kit dumps
- Substance hero material maps (masters only per art bible)

---

## Measured greybox reality (upgrade targets)

Scale-correct proxies already in export pipeline — **tri counts are baseline to replace**, not final budget:

| Mesh | ~Tris (measured greybox) | Notes |
|------|--------------------------|--------|
| `SM_Cabin` | ~252 | Modular parts + UCX in [SM_Cabin.fbx](../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md) |
| `SM_IslandTop` | ~60 | Plateau top; cliff modules add underside read |
| `SM_Lookout_Pad` | ~12 | Edge pad — upgrade for Shot 1 footing |
| `SM_Glider_Perch` | ~12 | Departure perch — Shot 3 helper |
| `SM_Pine_Homestead` | ~472 | S/M/L trunk/foliage family |

Anchors and volumes: [Lib/00_Core/GRAYBOX_LAYOUT.md](../Lib/00_Core/GRAYBOX_LAYOUT.md). Art direction: [02_ART_BIBLE.md](02_ART_BIBLE.md).

---

## Pipeline (defaults locked in strategy)

```
Kit plate (+ optional orthos)
  → optional Meshy/Tripo draft in AssetCreation/AI_Sources/
  → Blender MCP cleanup (STYLE_GUIDE)
  → export_to_asset_creation.py
  → batch_import_asset_creation.py (DESKTOP / MCP)
  → allowlisted Content/HomeWorld/Meshes/** + row in AI_ASSET_LOG on promote
```

| Default | Rule |
|---------|------|
| **Nanite** | On opaque static homestead meshes |
| **Collision** | UCX per export manifest |
| **Naming** | Upgrade **same** `SM_*` basenames; new pieces get manifest rows |
| **AI refs** | Grok Imagine **unavailable in bot** — plate + Lead manual / GenerateImage; store under `Docs/refs/ai/` + sidecar ([20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md)) |
| **Time rule** | **Blender-first**; AI mesh assist only when Blender cleanup would exceed ~30 min for a single asset |

Workflow index: [AssetCreation/README.md](../AssetCreation/README.md).

---

## Phases (Lead gates after strategy)

| Phase | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **PA-0** | Strategy + kit plate stamp | CLOUD | **APPROVED / CLOSED** | Lead **`APPROVE PA STRATEGY`**, 2026-09-22 ET |
| **PA-A** | Gap audit (mesh vs plate vs VS_MVP placement) | CLOUD+DESKTOP | **CLOSED / COMPLETE** | Lead **`APPROVE PA-A`**, 2026-09-22 ET |
| **PA-B** | Optional orthos / AI_Sources drafts | CLOUD+Lead | **OPTIONAL** | Parallel to PA-C if Lead requests |
| **PA-C** | Blender rebuild / upgrade | DESKTOP+Blender MCP | **IN PROGRESS** — tranche-2 **DONE**; optional island rim only | Lead **`APPROVE PA-C`**, 2026-09-22 ET |
| **PA-D** | Import + place + master material bind | DESKTOP | **IN PROGRESS** | Lead **`APPROVE PA-D`**, 2026-09-22 ET — [handoffs/PA_D_IMPORT_PLACE.md](handoffs/PA_D_IMPORT_PLACE.md) |
| **PA-E** | Shot 1 + Shot 2 evidence + close | DESKTOP+Lead | **LOCKED** | Lead **`APPROVE PA-E`** (TBD string) |

---

## PA-A accepted gap audit (2026-09-22 ET)

Lead **`APPROVE PA-A`** — verdicts **accepted** (chat, 2026-09-22 ET). Full handoff: [handoffs/PA_A_GAP_AUDIT.md](handoffs/PA_A_GAP_AUDIT.md).

| Piece | Verdict |
|-------|---------|
| Cabin | UPGRADE |
| IslandTop | KEEP (light rim later) |
| Cliff modules | CREATE (highest risk) |
| Pine S/M/L | UPGRADE (foliage collapsed) |
| Planters×3 | CREATE |
| Fence segs | CREATE |
| Path stones | CREATE |
| Lookout pad | KEEP |
| Glider perch | UPGRADE |
| Soft shrine | KEEP |
| Islets | KEEP optional |

### PA-C ordered queue (Blender — DESKTOP)

1. ~~Cliffs~~ **DONE** (tranche 1 — Lookout 864, Cabin 648, Rear 540 tris)
2. ~~Pines~~ **DONE** (tranche 1 — foliage Z-stack; 472 tris)
3. ~~Cabin~~ **DONE** (tranche 2 — 1680 tris; UCX 5.5×4.5×5.5)
4. ~~Path stones~~ **DONE** (tranche 2 — A/B/C 24/20/28 tris)
5. ~~Planters~~ **DONE** (tranche 2 — A/B/C 240/336/240 tris)
6. ~~Fence~~ **DONE** (tranche 2 — 100 tris)
7. ~~Glider perch~~ **DONE** (tranche 2 — 132 tris)
8. Optional island rim — **PENDING** (optional)

**UE cliff place (PA-D):** Lookout `(7.5, -5.5, -4)`, CabinFace `(-7, -4.5, -3)`, Rear `(0, 5, -2.5)` — portable origins at export `(0,0,0)`.

**KEEP (no PA-C mesh unless polish):** IslandTop (rim optional), Lookout pad, Soft shrine, Islets optional.

---

## DONE-WHEN (track close — PA-E)

- [ ] **Shot 1** and **Shot 2** readable in PIE without primitive homestead shapes (boxes/cylinders) on locked kit list
- [ ] Allowlisted mesh promote + [AI_ASSET_LOG.md](AI_ASSET_LOG.md) rows for AI-influenced assets
- [ ] Lead gate to close track (string TBD at PA STRATEGY approve)

**Evidence:** VS_MVP PIE captures / shot cameras per [00_SHOTLIST.md](00_SHOTLIST.md); DESKTOP owner per [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md).

---

## Citations

| Doc | Use |
|-----|-----|
| [02_ART_BIBLE.md](02_ART_BIBLE.md) | Palette, pine/cabin/shrine read |
| [Lib/00_Core/GRAYBOX_LAYOUT.md](../Lib/00_Core/GRAYBOX_LAYOUT.md) | Anchors, path, garden, lookout |
| [AssetCreation/README.md](../AssetCreation/README.md) | Export → import chain |
| [20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md) | Refs, sidecars, allowlist promote |
| [AssetCreation/Exports/MVP_EXPORT_MANIFEST.md](../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md) | Existing FBX names + UCX |

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE PA STRATEGY`** | PA-A gap audit — **DONE** 2026-09-22 ET |
| 1 | **`APPROVE PA-A`** (gap audit accepted) | PA-C Blender queue — **DONE** 2026-09-22 ET |
| 2 | **`APPROVE PA-C`** (2026-09-22 ET) + tranche-1/2 meshes | PA-C **IN PROGRESS** (rim optional); **PA-D OPEN** |
| 3 | **`APPROVE PA-D`** — **DONE** 2026-09-22 ET + DESKTOP import/place evidence | PA-E prep — **PA-D IN PROGRESS** |
| 4 | **PA-E** + Lead close gate | Whole PA track — **not CLOSED** |

---

*Docs/32 Prototype Assets — **PA-C IN PROGRESS** (tranche-2 **DONE**; optional rim) · **PA-D IN PROGRESS** (Lead **`APPROVE PA-D`** granted) — homestead kit only — track **not CLOSED** (2026-09-22 ET).*
