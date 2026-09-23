# PS-B — Placement Stills camera / fixture Arrange

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE PS-B`**, 2026-09-22 ET (Luke Thompson) |
| **Track** | PS-B (Arrange) **CLOSED** · PS-C **OPEN** |
| **Scope** | Homestead **`L_VS_MVP_Markers`** only |
| **Host** | **DESKTOP** (spawn/aim) · CLOUD (script + handoff) |
| **Impl** | [arrange_ps_homestead.py](../../Content/Python/arrange_ps_homestead.py) |

---

## Lead gate

```text
APPROVE PS-B
```

**Stamped:** Lead **`APPROVE PS-B`**, 2026-09-22 ET — unlocks **PS-C** ([PS_C_METRICS.md](PS_C_METRICS.md)).

---

## DESKTOP prove (stamped)

`arrange_ps_homestead.py` on **`L_VS_MVP_Markers`**:

| Check | Result |
|-------|--------|
| `ready_for_ps_c` | **true** |
| `blocked_reasons` | **[]** |
| `DRESS_*` | **90** |
| `PA_D_*` | **16** |
| Required `PS_*` cameras | **Seven** spawned (N/E/S/W iso + Cliff + Path + Garden) |
| `CAM_Hero` / `CAM_CabinClose` | Relocated; **`PA_E_MRQ_shot1`/`shot2`** relocated when present |
| `ps_dress_bounds.json` | Written (**106** source actors in bounds pass) |
| Lead viewport eyeball | N iso + cliff underside + path corridor — **accepted** |

---

## Camera map (from PS-A §2)

| PS cam ID | PS-B action |
|-----------|-------------|
| `PS_N/E/S/W_HighIso` | **Spawn/update** under `VS_MVP/PS` — ring around dress AABB center |
| `PS_Cabin_ThreeQuarter` | **Relocate/aim** **`CAM_CabinClose`** (PA-E shot2 pose helpers) |
| `PS_Lookout_Hero` | **Relocate/aim** **`CAM_Hero`** (PA-E shot1 pose helpers) |
| `PS_Garden_Close` | **Spawn/update** `PS_Garden_Close` — closer garden stand-off |
| `PS_Cliff_Underside` | **Spawn/update** — low angle at `PA_D_SM_Cliff_*` (fallback dress min Z) |
| `PS_Path_Corridor` | **Spawn/update** — along `PA_D_SM_PathStone_*` midline |
| `PS_Shrine_Read` | **Optional** — `INCLUDE_PS_SHRINE_READ = False` by default in script |

**Reuse (do not delete):** all five JSON `CAM_*` from markers. **Optional relocate:** `PA_E_MRQ_shot1` / `PA_E_MRQ_shot2` when present (same loc/rot as shot1/2 Arrange).

**Forbidden alias actors:** `Shot1`, `Shot2`, `CAM_CabinGarden` — gate fails if present.

---

## Script entrypoints

| Step | Command |
|------|---------|
| 1 | `.\Tools\Safe-Build.ps1` (if C++ touched; optional for script-only) |
| 2 | Editor on **`L_VS_MVP_Markers`** |
| 3 | `execute_python_script("place_vs_mvp_markers.py")` |
| 4 | `execute_python_script("place_vs_mvp_dress.py")` |
| 5 | `execute_python_script("place_vs_mvp_pa_d.py")` |
| 6 | **`execute_python_script("arrange_ps_homestead.py")`** |

**Outputs (local `Saved/` only):**

- `ps_dress_bounds.json` — schema [PS_A_INVENTORY.md](PS_A_INVENTORY.md) §4
- `ps_arrange_gate.json` — world ok, counts, cam presence, `ready_for_ps_c`, `blocked_reasons`

---

## DONE-WHEN (PS-B)

- [x] DESKTOP: chain markers → dress → pa_d → **`arrange_ps_homestead.py`** on Markers world
- [x] `Saved/ps_arrange_gate.json` — `world_ok: true`, `ready_for_ps_c: true`, no `blocked_reasons`
- [x] `Saved/ps_dress_bounds.json` — non-placeholder `dress_aabb` from live `DRESS_*` (+ `PA_D_*`)
- [x] All six required `PS_*` cameras exist under **`VS_MVP/PS`**; `CAM_Hero` / `CAM_CabinClose` relocated (not deleted)
- [x] Lead viewport eyeball on N iso + cliff underside + path corridor (prototype framing)
- [x] Lead **`APPROVE PS-B`** → unlock **PS-C** metrics + still capture

---

## Next track

**PS-C** — [PS_C_METRICS.md](PS_C_METRICS.md) · **`execute_python_script("ps_placement_prove.py")`**

---

## References

- [PS_A_INVENTORY.md](PS_A_INVENTORY.md) · [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md)
- [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py) — `resolve_camera_transform`, `look_at_rotation`, dress bounds
- [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md)
