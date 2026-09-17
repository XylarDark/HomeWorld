# Docs/08 — Audit sign-off (WAVE F)

| Field | Value |
|-------|-------|
| **Status** | **SIGNED OFF** — Lead Luke Thompson |
| **Board status** | Audit **COMPLETE** — WAVE F archive merged (PR #16) |
| **Date (ET)** | 2026-09-16 |
| **Date (UTC)** | 2026-09-17 |
| **Author** | Audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Delete authority** | [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) §8 |
| **Prior gate** | Lead **APPROVE WAVE E** (PR #15 merged) |

**Gate:** **CLOSED** — Lead Luke Thompson typed **`SIGN OFF AUDIT`** (2026-09-16 ET / 2026-09-17 UTC). Audit is **COMPLETE**.

---

## 1. Waves A–F status

| Wave | Deliverable | PR | Status |
|------|-------------|-----|--------|
| **A** | [08a_INVENTORY.md](08a_INVENTORY.md) | #11 | **COMPLETE** |
| **B** | [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) | #12 | **COMPLETE** |
| **C** | [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) | #13 | **COMPLETE** |
| **D** | [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) | #14 | **COMPLETE** |
| **E** | [08e_UPGRADE_PASS.md](08e_UPGRADE_PASS.md) | #15 | **COMPLETE** |
| **F** | **This document** + repo deletes | #16 | **COMPLETE** |

---

## 2. WAVE F — repo deletes (492 tracked paths)

Aggressive archive of quarantined harness, dual-canon fighters, and legacy Content per §8. **Kept:** `Safe-Build.ps1`, `Build-HomeWorld.bat`, WAVE E helpers (`batch_import_asset_creation.py`, `place_vs_mvp_markers.py`, `init_unreal.py`, `mcp_harness.py`, `pie_test_runner.py`), `Source/`, capital `Docs/00–08e`, `START_HERE`, `swarm/`, `Lib/`, `Maps/Preview_*`, `AssetCreation/` MVP exports, `MainMenu` map.

### Python — map builders, GUI automation, agent loop (38 paths)

| Path | Notes |
|------|-------|
| `Content/Python/create_demo_from_scratch.py` | DemoMap builder |
| `Content/Python/ensure_demo_map.py` | DemoMap ensure |
| `Content/Python/create_homestead_from_scratch.py` | Homestead builder |
| `Content/Python/ensure_homestead_map.py` | Homestead ensure |
| `Content/Python/place_homestead_placeholders.py` | Homestead placeholders |
| `Content/Python/place_homestead_spawn.py` | Homestead spawn |
| `Content/Python/place_mass_spawner_demomap.py` | Mass spawner on DemoMap |
| `Content/Python/create_mec_family_gatherer.py` | Mass entity config |
| `Content/Python/link_state_tree_to_mec.py` | State Tree link |
| `Content/Python/create_state_tree_family_gatherer.py` | State Tree asset |
| `Content/Python/setup_planetoid_pcg.py` | Planetoid PCG |
| `Content/Python/assemble_planetoid_from_config.py` | Planetoid assembly |
| `Content/Python/run_automation_cycle.py` | Agent-loop orchestrator |
| `Content/Python/gui_automation/` | **Entire tree** (25 files) — PyAutoGUI ref-image automation |

### Tools / root entrypoints (10 paths)

| Path |
|------|
| `Tools/RunAutomationLoop.ps1` |
| `Tools/Start-AllAgents.ps1` |
| `Tools/Start-AllAgents-InNewWindow.ps1` |
| `Tools/Watch-AutomationAndFix.ps1` |
| `Tools/Run-RefinerAgent.ps1` |
| `Tools/Run-GapSolverAgent.ps1` |
| `Start-AllAgents.bat` |
| `Run-DemoMapScript.bat` |
| `Run-PCGForestScript.bat` |
| `README-Automation.md` |

### Content — legacy maps (8 paths)

| Asset | Path |
|-------|------|
| DemoMap | `Content/HomeWorld/Maps/DemoMap.umap` |
| DemoMap HLOD | `DemoMap_HLODLayer_Instanced.uasset`, `DemoMap_HLODLayer_Merged.uasset` |
| Homestead | `Homestead.umap`, `Homestead_WP.umap`, `Homestead.ini` |
| Homestead HLOD | `Homestead_HLODLayer_Instanced.uasset`, `Homestead_HLODLayer_Merged.uasset` |

**Kept:** `MainMenu.umap`, `MainMenu_Homestead_HLODLayer_*` (not in §8).

### Content — PCG, Mass, combat placeholders, building (10 paths)

| Category | Paths |
|----------|-------|
| PCG graphs | `ForestIsland_PCG.uasset`, `Planetoid_POI_PCG.uasset` |
| Mass / AI | `MEC_FamilyGatherer.uasset`, `ST_FamilyGatherer.uasset` |
| Combat GAs | `GA_Dodge`, `GA_PrimaryAttack`, `GA_ProtectorAttack` |
| Agentic building | `BP_BuildOrder_Wall`, `SO_WallBuilder`, `DA_SO_WallBuilder_Behavior` |

### Content — sample packs + Milady (434 paths)

| Tree | Count |
|------|-------|
| `Content/StylizedProvencal/` | 357 tracked assets |
| `Content/Man/` | 76 tracked assets |
| `Content/HomeWorld/Milady/` | 1 tracked asset (`M_MiladyPastel.uasset`) |

### Docs — stubs (content replaced, paths kept)

| Path | Replacement |
|------|-------------|
| `VisionBoard/MVP/VERTICAL_SLICE_SIGNOFF.md` | Stub → **Docs/07** CLOSED |
| `docs/Automation/AGENT_COMPANY.md` | Stub → **swarm/SWARM_OPS** + this sign-off |

### Config / bootstrap updates (this PR)

| File | Change |
|------|--------|
| `Config/DefaultEngine.ini` | `EditorStartupMap` → **MainMenu** (DemoMap removed) |
| `Content/Python/bootstrap_project.py` | Removed legacy DemoMap/PCG path; VS_MVP slice only |
| `AGENTS.md` | Removed deleted loop entrypoints; VS_MVP primary |

---

## 3. Windows-local cleanup remaining (DESKTOP-21CT3H0)

Lead should verify on the **Windows dev machine** after pulling this PR. These are **not** in the repo delete set or are gitignored — remove manually if still present locally:

| Item | Why local |
|------|-----------|
| **`Saved/`** caches referencing DemoMap, Homestead, ForestIsland_PCG | Gitignored runtime state |
| **Untracked Milady / sample-pack duplicates** under `Content/` if copied outside git | May exist only on desktop |
| **`SylizedProvencal.png`** (repo root) | Quarantine ref image — **not** §8 delete; optional local discard |
| **LFS object cache** for deleted `.uasset`/`.umap` | `git lfs prune` after merge if disk reclaim needed |
| **Legacy automation logs** | `Saved/Logs/automation_*`, `agent_run_history.ndjson` — archive or delete |
| **`.cursor/worktrees/`** stale checkouts | Local copies only |
| **Orphaned Guardian/capture scripts** (`Tools/Guard-AutomationLoop.ps1`, `Run-AutomationWithCapture.ps1`, etc.) | **Kept in repo** for now; Lead may retire separately if unused |

**Verification status (DESKTOP-21CT3H0):**

| Check | When | Result |
|-------|------|--------|
| **Safe-Build** | Before WAVE F merge (WAVE E tip `9180850`) | **GREEN** |
| **WAVE F post-merge checks** (§3 list below) | After Windows pull of PR #16 | **PENDING** |

**Post-merge Windows checks** (pending pull):

1. `.\Tools\Safe-Build.ps1` — green compile
2. Open Editor — boots to **MainMenu** (no DemoMap missing-map prompt)
3. Run `bootstrap_project.py` — VS_MVP import + markers path
4. Run `pie_test_runner.py` — soft VS_MVP checks in `Saved/pie_test_results.json`

---

## 4. Hard rules (unchanged)

| Rule | Status |
|------|--------|
| **Docs/07 vertical slice sign-off** | **CLOSED** — do not reopen |
| **FALLBACK FLIGHT** | **ARMED** — CRUMB glide + portal both ways |
| **No new features during audit WAVEs** | Honored through WAVE F |
| **Single product canon** | **`Docs/`** + `Maps/Preview_*` / VS_MVP — no DemoMap/Homestead dual canon |

---

## 5. Gate — SIGN OFF AUDIT (CLOSED)

| | |
|---|---|
| **Gate** | Lead **`SIGN OFF AUDIT`** — **GRANTED** |
| **Signed by** | Lead Luke Thompson |
| **Signed (ET)** | 2026-09-16 |
| **Signed (UTC)** | 2026-09-17 |
| **WAVE F PR** | #16 merged to `main` |
| **Audit status** | **COMPLETE** — post-audit feature work per Lead roadmap |

---

## Board / Actions / Gate / Next

| | |
|---|---|
| **Board** | Audit **COMPLETE** — Waves A–F done (PR #11–#16); 492 quarantine paths removed; VS_MVP primary |
| **Verification** | Safe-Build green at WAVE E (`9180850`) on DESKTOP-21CT3H0; WAVE F post-merge checks pending Windows pull |
| **Gate** | **CLOSED** — Lead signed off |
| **Next** | Post-audit: VS_MVP dress in Editor, FALLBACK glide BP wiring, master material graphs — per Lead priority |
