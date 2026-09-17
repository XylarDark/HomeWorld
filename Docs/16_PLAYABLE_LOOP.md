# Docs/16 — Playable Loop (PL) Strategy

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / ACTIVE** — Lead Luke Thompson, **`APPROVE PL STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Baseline** | Main post–VP — Docs/14 Verify & Polish **CLOSED / COMPLETE** (`635bbaa`) |
| **Author** | Conductor (HomeWorld) |
| **Prior tracks** | Product NP (Docs/11) **CLOSED**; HR2 **CLOSED**; HR3 **CLOSED** (C **DEFERRED**); VP (Docs/14) **CLOSED** |

---

## Gate

Lead **`APPROVE PL STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET).

**Next gate:** Lead **`APPROVE PL-B`** before PL-C.

**PL-A CLOSED** — Lead **`APPROVE PL-A`**, 2026-09-17 ET. **PL-B OPEN**. PL-C/D **LOCKED**.

---

## Why PL (not NP-F or HR4)

NP shipped SYS/GP verbs; VP polished runbooks and thin UX around an **Engine `DefaultSkeletalMesh`** interim and a **WAIVED** verb PIE pass. The signed VS_MVP slice is not a credible playable demo until:

1. A **real** character mesh + compiling anim path exists on DESKTOP
2. Human Alt+P PIE produces real `FORM:` / `FALLBACK:` / … greps (close the WAIVE debt)
3. Thin leftover loop UX (store-transfer) lands without new masters

| Option | Verdict |
|--------|---------|
| HR4 harness | Low ROI — harness ~A; branch protection is Lead Settings, not a track |
| New SYS verbs / combat | Out of [AGENTS.md](../AGENTS.md) / Docs/07 |
| New biome / content expansion | Premature until VS_MVP plays |
| Store-transfer alone | Too thin for a full track |

**ROI order:** PL-A → PL-B → PL-C → PL-D. Polish on a broken pawn is theater.

---

## Board status

| Track | Status |
|-------|--------|
| Product NP (Docs/11) | **CLOSED** |
| HR2 / HR3 | **CLOSED** (HR3-C **DEFERRED**) |
| Docs/14 / VP | **CLOSED / COMPLETE** |
| **Docs/16 / PL strategy** | **APPROVED** — Lead **`APPROVE PL STRATEGY`**, 2026-09-17 ET |
| **PL-A** | **APPROVED / CLOSED** — Lead **`APPROVE PL-A`**, 2026-09-17 ET |
| **PL-B** | **OPEN / IN PROGRESS** |
| **PL-C** | **LOCKED** |
| **PL-D** | **LOCKED** |

---

## PL plan (Lead gates each phase)

Naming: **PL-A … PL-D** (Playable Loop). Do **not** reuse NP-* / HR-* / VP-* ids.

### PL-A — Character realization

**Goal:** Replace mesh-only interim with a spawnable character that has a real skeletal mesh and a compiling AnimBP (or documented minimal walk).

| Item | Spec |
|------|------|
| **Root cause** | `/Game/Man/Mesh/Full/SK_Man_Full_01` missing on disk; `ABP_HomeWorldCharacter` skeleton compile fail (PA-03 deferred accept in VP-B) |
| **Deliverables** | Import or substitute Man mesh + skeleton into Content; update `character_blueprint_config.json`; ABP compiles **or** documented minimal anim; preflight aligns with real paths |
| **Evidence** | [handoffs/PL_A_CHARACTER.md](handoffs/PL_A_CHARACTER.md) |
| **Gate** | Lead **`APPROVE PL-A`** before PL-B |
| **Host** | CLOUD (scripts/config) + DESKTOP (import / Safe-Build / apply) |

**Done criteria:**

- [ ] Character BP uses non-Engine project mesh (or Lead-accepted substitute path)
- [ ] ABP compiles **or** mesh-only explicitly retired with Lead note
- [ ] `npm run preflight:ue -- --require-editor` exit **0** on DESKTOP without relying on mesh-only skip as the primary path
- [ ] Safe-Build green if C++ touched


**Lead substitute (2026-09-17 ET):** UE 5.7 TemplateResources **High Characters Mannequins** → DESKTOP `Content/Characters/Mannequins` (local). Config: `/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple` + `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed`. Legacy `/Game/Man/...` deferred.

**Status:** **APPROVED / CLOSED** — Lead **`APPROVE PL-A`**, 2026-09-17 ET.

**Out of scope:** Full AnimGraph automation spike; Milady; combat idle sets.

---

### PL-B — Human PIE verb pass

**Goal:** Close VP-A **WAIVE** debt with real Output Log greps after PL-A.

| Item | Spec |
|------|------|
| **Runbooks** | Docs/12c–12e (same prefixes as VP-A) |
| **Map** | `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers` |
| **Evidence** | [handoffs/PL_B_PIE.md](handoffs/PL_B_PIE.md) — keep [VP_A_PIE.md](handoffs/VP_A_PIE.md) WAIVE record intact |
| **Gate** | Lead **`APPROVE PL-B`** before PL-C |
| **Host** | DESKTOP — Conductor **parent** (human Alt+P or proven PIE path) |

**Done criteria:**

- [ ] All six primary prefixes + supporting `GATHER:` have PASS or documented fail with log excerpt
- [ ] Character spawn confirmed in PIE (controlled pawn)

---

### PL-C — Thin loop UX

**Goal:** PA-07 store-transfer + lightweight inventory readout.

| Item | Spec |
|------|------|
| **PA-07** | World ↔ Stored gatherables per [GATHERABLES_WORLD_STORED.md](../Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md) |
| **Inventory readout** | Minimal on-screen or log-backed slot display — no new masters |
| **Evidence** | [handoffs/PL_C_LOOP_UX.md](handoffs/PL_C_LOOP_UX.md) |
| **Gate** | Lead **`APPROVE PL-C`** before PL-D |
| **Host** | CLOUD + DESKTOP smoke |

**Out of scope:** New masters (stay at **10**); full RPG UI; combat.

---

### PL-D — Optional presentation

**Goal:** Shot 1 camera path / stills from **existing** markers only.

| Item | Spec |
|------|------|
| **Cameras** | Existing CAM_* / TargetPoints — no new biome |
| **Evidence** | [handoffs/PL_D_PRESENTATION.md](handoffs/PL_D_PRESENTATION.md) |
| **Gate** | Lead **`APPROVE PL-D`** closes PL track |
| **Host** | DESKTOP |

---

## Hard rules (every PL phase)

| Rule | Source |
|------|--------|
| **Docs/07 CLOSED** | Do not reopen vertical-slice sign-off |
| **FALLBACK FLIGHT armed** | Scripted glide + portal only |
| **No free-flight / flight HUD** | Lead locked |
| **No combat** | AGENTS.md placeholder boundary |
| **No `.uasset` / `.umap` commits** | Local Windows Editor only |
| **Exactly 10 masters** | Docs/02 |
| **Lead APPROVE each PL-*** | This doc |
| **Windows Safe-Build** | After any C++ change |

---

## Explicit OUT

| Item | Reason |
|------|--------|
| Combat / foe waves | AGENTS.md |
| Free-flight / Docs/07 reopen | Lead CLOSED |
| New biomes / maps | Premature |
| HR4 harness redo | Low ROI |
| Nanite/Lumen beauty | Off-slice |
| Full AnimGraph automation | Spike deferred |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE PL STRATEGY`** | PL-A |
| 1 | **`APPROVE PL-A`** | PL-B |
| 2 | **`APPROVE PL-B`** | PL-C |
| 3 | **`APPROVE PL-C`** | PL-D |
| 4 | **`APPROVE PL-D`** | Close PL track |

```
Docs/16 / PL STRATEGY: APPROVED — Lead Luke Thompson, APPROVE PL STRATEGY, 2026-09-17 ET
PL-A: OPEN — PL-B/C/D: LOCKED
Prior: NP CLOSED — HR2/HR3 CLOSED — VP CLOSED
```

---

*Lead **`APPROVE PL STRATEGY`** locked 2026-09-17 ET. Next: **PL-A** character realization.*
