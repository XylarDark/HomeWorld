# PA-D — Batch import + VS_MVP place

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead **`APPROVE PA-D`**, 2026-09-22 ET · DESKTOP import/place verified (KEEP-LOCAL map/mesh Content on DESKTOP; no `.uasset` in cloud PRs) · **awaiting formal Shot 1/2 for PA-E** (PA-D not CLOSED) |
| **Host** | **DESKTOP-21CT3H0** (Conductor parent — MCP / PIE) |
| **Track** | Whole **PA track not CLOSED** — **PA-E LOCKED** until Shot 1/2 evidence + Lead **`APPROVE PA-E`** |
| **Impl doc** | [32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md) |
| **Prior** | [PA_C_BLENDER.md](PA_C_BLENDER.md) · [PA_C_TRANCHE2.md](PA_C_TRANCHE2.md) — tranche-1/2 FBX on `main` |

**Do not** stamp **PA-D CLOSED**, **PA-E done**, or **whole PA track CLOSED** in a cloud PR — DESKTOP runs import/place and attaches evidence first.

---

## Lead gate (record)

Lead typed in chat (2026-09-22 ET):

```text
APPROVE PA-D
```

Unlocks DESKTOP **`batch_import_asset_creation.py`** + **`place_vs_mvp_dress.py`** on VS_MVP. Cloud agents: **docs stamp only** — no `.uasset` in this gate PR.

---

## FBX queue (import targets)

Homestead exports on `main` under `AssetCreation/Exports/Homestead/`:

| Mesh | Tranche |
|------|---------|
| `SM_Cliff_LookoutFace`, `SM_Cliff_CabinFace`, `SM_Cliff_Rear` | 1 |
| `SM_Pine_Homestead` | 1 |
| `SM_Cabin`, `SM_Glider_Perch` | 2 |
| `SM_PathStone_{A,B,C}`, `SM_Planter_{A,B,C}`, `SM_Garden_Fence_Seg` | 2 |

Manifest rows: [MVP_EXPORT_MANIFEST.md](../../AssetCreation/Exports/MVP_EXPORT_MANIFEST.md). Allowlist promote per [20_UASSET_AI_POLICY.md](../20_UASSET_AI_POLICY.md) + [AI_ASSET_LOG.md](../AI_ASSET_LOG.md) when AI-influenced.

---

## DESKTOP runbook

```text
.\Tools\Safe-Build.ps1
# Editor — VS_MVP markers level (prerequisite: place_vs_mvp_markers.py on level):
execute_python_script("batch_import_asset_creation.py")
execute_python_script("place_vs_mvp_dress.py")
```

Optional re-verify: `execute_python_script("place_vs_mvp_markers.py")` if level missing.

Cloud agents: no UE on Linux VM — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## UE placement note (cliffs + cabin)

Cliff assemblies export at **(0,0,0)** — place in VS_MVP at:

- LookoutFace: `(7.5, -5.5, -4.0)`
- CabinFace: `(-7.0, -4.5, -3.0)`
- Rear: `(0.0, 5.0, -2.5)`

Cabin portable kit origin `(0,0,0)` — place at `SOCKET_Cabin` (−6, 1, 0) per [PA_C_TRANCHE2.md](PA_C_TRANCHE2.md).

Dress script: [place_vs_mvp_dress.py](../../Content/Python/place_vs_mvp_dress.py) — idempotent `DRESS_*` actors from imported StaticMeshes.

---

## Evidence (PA-D — not claimed by docs stamp)

| Check | Expected |
|-------|----------|
| Import | Output Log: batch import success for Homestead FBX; meshes under `/Game/HomeWorld/Meshes/Homestead/` |
| Dress | `place_vs_mvp_dress:` lines; `DRESS_*` actors at graybox anchors |
| PIE spot | Shot 1 / Shot 2 homestead kit reads as low-poly dress (not engine primitives on locked list) |
| KEEP-LOCAL | Level save on DESKTOP after dress OK ([17e_HS_CONTENT_BOOTSTRAP.md](../17e_HS_CONTENT_BOOTSTRAP.md)) |

**PA-E** owns formal Shot 1 + Shot 2 captures per [00_SHOTLIST.md](../00_SHOTLIST.md).

---

## Checklist

- [x] Lead **`APPROVE PA-D`** stamped (2026-09-22 ET)
- [x] Tranche-1/2 FBX on `main`
- [x] DESKTOP: Safe-Build + batch import (done 2026-09-22 ET — Homestead meshes under `/Game/HomeWorld/Meshes/Homestead/` including SM_Cliff_*, SM_Planter_*, SM_Garden_Fence_Seg, SM_PathStone_*, cabin parts, pine family)
- [x] DESKTOP: `place_vs_mvp_pa_d.py` on `L_VS_MVP_Markers` (after save-before-dress fix in PR #149; evidence: 16× `PA_D_*` cliffs/planters/fence/path + refreshed `DRESS_*` cabin/pines/glider/island/lookout)
- [ ] Evidence appended (log excerpt / viewport capture) — **pending**
- [ ] PA-E Shot 1/2 + Lead close gate — **LOCKED**

---

## Blockers

- PA-E Shot 1/2 automation unreliable (Cmd HighResShot / host grab) — **Lead manual viewport capture**; see [DEFECT_PA_E_shot_capture_automation.md](../qa/DEFECT_PA_E_shot_capture_automation.md), [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) and [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) (2026-09-22 backfill). **2026-09-22 ET:** Conductor remote host ImageGrab under `C:\Users\User\Desktop\HomeWorld_PA_E\` produced chat/desktop/chrome captures — **not** shotlist PASS; **stop remote ImageGrab for PA-E**. **Not CLOSED** on this pointer alone.

---

## Gate

Lead **`APPROVE PA-D`** grants DESKTOP import/place work only. **PA-D CLOSED** requires DESKTOP evidence + Conductor stamp (or Lead **`APPROVE PA-E`** prep complete). **PA track** closes on **PA-E**, not PA-D.
