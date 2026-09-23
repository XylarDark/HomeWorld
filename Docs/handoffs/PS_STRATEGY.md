# PS STRATEGY — Placement Stills (homestead placement confidence)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — pending Lead **`APPROVE PS STRATEGY`** |
| **Track** | PS-0 **OPEN** → PS-A locked until strategy gate |
| **Host** | CLOUD (strategy stamp) · DESKTOP (inventory + prove after PS-B) |
| **Impl doc** | [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) |
| **Scope locked** | **Homestead kit on `L_VS_MVP_Markers` only** — same footprint as closed PA ([32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md)) |
| **Close gate (PS-0)** | Lead **`APPROVE PS STRATEGY`** |

---

## Deliverable (PS-0)

| Item | Path |
|------|------|
| Strategy doc | [Docs/33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) |
| This handoff | [Docs/handoffs/PS_STRATEGY.md](PS_STRATEGY.md) |

**Not in this handoff:** `.uasset`, `.umap`, new MRQ sequences, gameplay C++.

---

## Lead gate (record)

Pending Lead chat stamp:

```text
APPROVE PS STRATEGY
```

Optional scope clarifier (if Lead repeats PA lock):

```text
APPROVE PS STRATEGY — homestead kit only
```

Unlocks **PS-A** (metrics + angle inventory on Markers level).

---

## Scope summary (locked)

**IN:** Multi-angle placement stills + automated env metrics for `DRESS_*` + `PA_D_*` on Markers; benchmark compare vs shotlist / key-art / kit plate / Lead-stamped stills (eyeball on PS-D).

**OUT:** Planetside dress; golden-image automation without SCOUT; character heroes.

**Quality:** Prototype placement confidence — grounded kit, no obvious floaters; full environment **matches benchmarks in intent** (not pixel ship-final).

---

## Next (PS-A)

1. Enumerate actors + anchors from `place_vs_mvp_dress.py` / `place_vs_mvp_pa_d.py`.
2. Map existing `CAM_*` labels vs proposed `PS_*` gaps ([pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py)).
3. Publish threshold table + `Saved/ps_placement_metrics.json` schema draft in handoff `PS_A_INVENTORY.md` (future PR).

---

## DESKTOP chain (after PS-B — reference only)

```text
.\Tools\Safe-Build.ps1
# Editor on L_VS_MVP_Markers:
execute_python_script("place_vs_mvp_markers.py")
execute_python_script("place_vs_mvp_dress.py")
execute_python_script("place_vs_mvp_pa_d.py")
# Future PS-C:
execute_python_script("ps_placement_prove.py")
```

Cloud agents: docs + scripts proposal only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist (PS-0)

- [x] Strategy doc [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md)
- [x] Handoff stub (this file)
- [ ] Lead **`APPROVE PS STRATEGY`**
- [ ] PS-A inventory handoff (separate PR after gate)
