# PS-B — Placement Stills camera / fixture Arrange

| Field | Value |
|-------|-------|
| **Status** | **GATE READY** — pending Lead **`APPROVE PS-B`** after DESKTOP Arrange prove + eyeball |
| **Track** | PS-B (Arrange) · PS-A **CLOSED** |
| **Scope** | Homestead **`L_VS_MVP_Markers`** only |
| **Host** | **DESKTOP** (spawn/aim) · CLOUD (script + handoff) |
| **Impl** | [arrange_ps_homestead.py](../../Content/Python/arrange_ps_homestead.py) |

---

## Lead gate

```text
APPROVE PS-B
```

Grant after DESKTOP runs Arrange, inspects viewport framing on key `PS_*` views, and accepts `Saved/ps_arrange_gate.json` with `ready_for_ps_c: true` (pose quality is still Lead eyeball — not auto-PASS).

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

**Optional flag:** Edit `INCLUDE_PS_SHRINE_READ = True` in script (or call `arrange_ps_homestead(include_shrine=True)` from REPL) before re-run.

---

## DONE-WHEN (PS-B)

- [ ] DESKTOP: chain markers → dress → pa_d → **`arrange_ps_homestead.py`** on Markers world
- [ ] `Saved/ps_arrange_gate.json` — `world_ok: true`, `ready_for_ps_c: true`, no `blocked_reasons`
- [ ] `Saved/ps_dress_bounds.json` — non-placeholder `dress_aabb` from live `DRESS_*` (+ `PA_D_*`)
- [ ] All six required `PS_*` cameras exist under **`VS_MVP/PS`**; `CAM_Hero` / `CAM_CabinClose` relocated (not deleted)
- [ ] Lead viewport eyeball on N iso + cliff underside + path corridor (prototype framing)
- [ ] Lead **`APPROVE PS-B`** → unlock **PS-C** metrics + still capture

---

## DESKTOP prove checklist

1. Confirm world token **`L_VS_MVP_Markers`** (script hard-fails otherwise).
2. Counts in gate JSON align with inventory baseline: **`DRESS_*` ≈ 90**, **`PA_D_*` = 16** (when optional PA-D meshes present).
3. Five JSON cams present; **`PA_E_MRQ_shot1`/`shot2`** noted in `relocate_cameras` if in level.
4. No **`Shot1`/`Shot2`/`CAM_CabinGarden`** actors.
5. Pilot **`PS_N_HighIso`**, **`PS_Cliff_Underside`**, **`PS_Path_Corridor`** — homestead kit framed, not void.
6. Append gate path + one-line framing note to session log before **`APPROVE PS-B`**.

---

## PS-C pointer (not this PR)

- New module sketch: `ps_placement_prove.py` — read `ps_arrange_gate.json`, assert metrics catalog, capture to `Saved/ps_stills/` via extended PA-E MRQ/viewport patterns.
- No golden SCOUT, no NirCmd in PS-B.

---

## References

- [PS_A_INVENTORY.md](PS_A_INVENTORY.md) · [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md)
- [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py) — `resolve_camera_transform`, `look_at_rotation`, dress bounds
- [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md)
