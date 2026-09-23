# PS-C — Placement metrics + still capture

| Field | Value |
|-------|-------|
| **Status** | **GATE READY** — pending Lead **`APPROVE PS-C`** after DESKTOP prove |
| **Track** | PS-C (metrics + stills) · PS-B **CLOSED** |
| **Scope** | Homestead **`L_VS_MVP_Markers`** only |
| **Host** | **DESKTOP** (prove) · CLOUD (script + handoff) |
| **Impl** | [ps_placement_prove.py](../../Content/Python/ps_placement_prove.py) |

---

## Lead gate

```text
APPROVE PS-C
```

Grant after DESKTOP runs prove, inspects `Saved/ps_placement_metrics.json` + `Saved/ps_stills/manifest.json`, and accepts `Saved/ps_c_prove_gate.json` with `ready_for_ps_d: true`. **Metric ≠ visual:** auto metrics gate **placement physics**; framing/mood vs benchmarks is **PS-D** Lead eyeball.

---

## Metrics catalog (thresholds)

From [PS_A_INVENTORY.md](PS_A_INVENTORY.md) §3 · [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md):

| Metric ID | Prototype threshold | Notes |
|-----------|---------------------|--------|
| `ground_z_delta_uu` | **8** UU | \|actor bottom Z − ground Z\| at bounds center XY |
| `float_gap_uu` | **4** kit / **12** cliff | Air gap under support (`PA_D_*Cliff*`) |
| `dress_aabb_inside` | margin **50** UU | From `Saved/ps_dress_bounds.json` |
| `pair_overlap_uu` | **> 2** UU flag | Sampled PA_D ↔ PA_D and PA_D ↔ core DRESS |
| `anchor_height_delta_uu` | skip | No sidecar table yet → `pass` + note |
| `facing_dot_look_at` | skip | Optional until sidecar exists |

**Sample policy:** All **`PA_D_*`** (16) + **core `DRESS_*`** whose labels match IslandTop, Cabin, Lookout, Shrine, landing, fence/planter/path substrings — **not** full 90+ DRESS sweep (timeout-safe).

Each metric → `pass` / `soft_fail` / `closed_fail`; aggregate **`placement_outcome`**.

---

## Still capture set

| Camera label | PS still / intent |
|--------------|-------------------|
| `PS_N_HighIso` | North iso overview |
| `PS_E_HighIso` | East iso (cliff face) |
| `PS_Cliff_Underside` | Underside float check |
| `PS_Path_Corridor` | Path continuity |
| `PS_Garden_Close` | Garden/planters |
| `CAM_Hero` | Shot1-compatible framing |
| `CAM_CabinClose` | Shot2-compatible framing |

**Output:** `Saved/ps_stills/<label>.png` + `Saved/ps_stills/manifest.json` (bytes, mean luminance when decodable).

**Capture path (hardened v2):** Pilot camera → [capture_viewport.py](../../Content/Python/capture_viewport.py) **absolute** `HighResShot filename="…/Saved/ps_stills/<label>.png"` (Epic doc order) + `AutomationLibrary.take_high_res_screenshot` with **absolute** path ([`_pl_d_capture_shot1.py`](../../Content/Python/_pl_d_capture_shot1.py) pattern). Relative `fname_only` **does not** write PNGs on DESKTOP (2026-09-23 prove). Optional copy fallback: newest `Saved/Screenshots/PA_E/*shot1|shot2*.png` for `CAM_Hero` / `CAM_CabinClose` after [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py) if viewport still empty. **No NirCmd.** Black/dark PNG → **`soft_fail`** on that still.

**Metrics path (hardened v2):** Multi-channel line trace (`line_trace_single_for_objects`, profile `BlockAll`, trace queries) — **no** `island_top_proxy_max_z` fallback. Trace miss → **`soft_fail` `no_ground`**. Skip ground metrics for `DRESS_SM_IslandTop` and `PA_D_*Cliff*`. Baseline caps over-threshold at **`soft_fail`** (pair overlap + float) until Lead tunes. Intentional planter↔cabin overlaps ignored.

### DESKTOP first-run note (2026-09-23 @ 71bb847)

Initial prove mass-**closed_fail** from island max-Z proxy and **0/7** stills (relative screenshot path). Re-run after harden merge; expect **`placement_outcome`** pass/soft_fail and **7** PNG paths when viewport capture succeeds. If stills still missing: run `capture_shotlist_mrq.py` once, then re-run prove (MRQ copy fallback for hero/cabin cams).

---

## Script entrypoints

| Step | Command |
|------|---------|
| 0 | PS-B chain complete — `Saved/ps_arrange_gate.json` with `ready_for_ps_c: true` (script re-runs [arrange_ps_homestead.py](../../Content/Python/arrange_ps_homestead.py) if missing) |
| 1 | Editor on **`L_VS_MVP_Markers`** |
| 2 | **`execute_python_script("ps_placement_prove.py")`** |

**Outputs (local `Saved/` only):**

- `ps_placement_metrics.json`
- `ps_stills/*.png` + `ps_stills/manifest.json`
- `ps_c_prove_gate.json` — `placement_outcome`, still counts, `ready_for_ps_d`, `blocked_reasons`

**Optional:** `prove_ps_placement(skip_stills=True)` from REPL for metrics-only dry run.

---

## DONE-WHEN (PS-C)

- [ ] DESKTOP: **`ps_placement_prove.py`** after PS-B Arrange chain
- [ ] `Saved/ps_c_prove_gate.json` — `ready_for_ps_d: true` (metrics written + required still files exist)
- [ ] `Saved/ps_placement_metrics.json` — sampled actors + `placement_outcome`
- [ ] `Saved/ps_stills/manifest.json` — seven camera entries with paths
- [ ] Honest tune note if thresholds or dark stills **soft_fail** on first run
- [ ] Lead **`APPROVE PS-C`** → unlock **PS-D** eyeball vs benchmarks

---

## DESKTOP prove checklist

1. Confirm **`L_VS_MVP_Markers`** loaded.
2. Verify `ps_arrange_gate.json` **`ready_for_ps_c: true`** (or let prove script run Arrange).
3. Run prove; tail Output Log for `PS Prove:` lines.
4. Open N/E iso + cliff underside stills — kit visible (dark still = soft_fail, fix lighting/viewmode before PS-D).
5. Scan metrics for **`closed_fail`** actors; tune thresholds in script constants only after baseline JSON saved locally.
6. Append gate path + one-line outcome to session log before **`APPROVE PS-C`**.

---

## PS-D pointer (not this PR)

Lead eyeball vs [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) benchmark table (key-art, kit plate, shotlist intent). No golden SCOUT / NirCmd.

---

## References

- [PS_B_ARRANGE.md](PS_B_ARRANGE.md) · [PS_A_INVENTORY.md](PS_A_INVENTORY.md)
- [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py) — bounds, luminance, three-state outcomes
- [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md)
