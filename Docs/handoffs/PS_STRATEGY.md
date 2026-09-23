# PS STRATEGY — Placement Stills (homestead placement confidence)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — PS-0 **CLOSED** |
| **Lead stamp** | **`APPROVE PS STRATEGY — homestead kit only`**, 2026-09-22/23 ET (Luke Thompson) |
| **Track** | PS-0 **CLOSED** · PS-A **CLOSED** → **PS-B** **OPEN** (Arrange) |
| **Host** | CLOUD (strategy + inventory docs) · DESKTOP (live verify after PS-A) |
| **Impl doc** | [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) |
| **Scope locked** | **Homestead kit on `L_VS_MVP_Markers` only** — same footprint as closed PA ([32_PROTOTYPE_ASSETS.md](../32_PROTOTYPE_ASSETS.md)) |
| **Close gate (PS-0)** | Lead **`APPROVE PS STRATEGY`** — **GRANTED** |

---

## Deliverable (PS-0)

| Item | Path |
|------|------|
| Strategy doc | [Docs/33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md) |
| This handoff | [Docs/handoffs/PS_STRATEGY.md](PS_STRATEGY.md) |
| PS-A inventory | [Docs/handoffs/PS_A_INVENTORY.md](PS_A_INVENTORY.md) — **CLOSED** |
| PS-B Arrange | [Docs/handoffs/PS_B_ARRANGE.md](PS_B_ARRANGE.md) |

**Not in this handoff:** `.uasset`, `.umap`, new MRQ sequences, gameplay C++.

---

## Lead gate (record)

```text
APPROVE PS STRATEGY — homestead kit only
```

Unlocks **PS-A** (metrics + angle inventory on Markers level).

**Next gate:** **`APPROVE PS-B`** — see [PS_B_ARRANGE.md](PS_B_ARRANGE.md) (PS-A closed Lead **`APPROVE PS-A`**, 2026-09-22 ET).

---

## Scope summary (locked)

**IN:** Multi-angle placement stills + automated env metrics for `DRESS_*` + `PA_D_*` on Markers; benchmark compare vs shotlist / key-art / kit plate / Lead-stamped stills (eyeball on PS-D).

**OUT:** Planetside dress; golden-image automation without SCOUT; character heroes.

**Quality:** Prototype placement confidence — grounded kit, no obvious floaters; full environment **matches benchmarks in intent** (not pixel ship-final).

---

## Next (PS-B)

1. DESKTOP: markers → dress → pa_d → **`arrange_ps_homestead.py`** ([PS_B_ARRANGE.md](PS_B_ARRANGE.md))
2. Inspect `Saved/ps_arrange_gate.json` + viewport on key `PS_*` views
3. Lead **`APPROVE PS-B`** → PS-C metrics + stills

---

## DESKTOP chain

```text
.\Tools\Safe-Build.ps1
# Editor on L_VS_MVP_Markers:
execute_python_script("place_vs_mvp_markers.py")
execute_python_script("place_vs_mvp_dress.py")
execute_python_script("place_vs_mvp_pa_d.py")
execute_python_script("arrange_ps_homestead.py")
# Future PS-C:
execute_python_script("ps_placement_prove.py")
```

Cloud agents: docs + scripts proposal only — [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

---

## Checklist (PS-0)

- [x] Strategy doc [33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md)
- [x] Handoff stub (this file)
- [x] Lead **`APPROVE PS STRATEGY — homestead kit only`**
- [x] PS-A inventory handoff [PS_A_INVENTORY.md](PS_A_INVENTORY.md)
