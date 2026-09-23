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

**Capture path:** Pilot camera + `AutomationLibrary.take_high_res_screenshot` (relative `Saved/ps_stills/`) + `HighResShot` fallback — same proven pattern as [vnp_night_tune_and_evidence.py](../../Content/Python/vnp_night_tune_and_evidence.py). **No MRQ** in PS-C (day/lit viewport; placement stills, not PA-E night stack). Black/dark PNG → **`soft_fail`** on that still, not **`closed_fail`** when Arrange gate was ready.

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
