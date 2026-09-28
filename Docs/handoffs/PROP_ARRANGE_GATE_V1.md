# PROP_ARRANGE_GATE_V1 — math-first Arrange readiness (CAP-PROP-GATE)

**Bite id:** `CAP-PROP-GATE`  
**Parent EXIT:** [`Docs/handoffs/research/EXIT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md`](research/EXIT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md)  
**Schema:** `hw.prop_arrange_gate/v1` → [`docs/Automation/schemas/prop_arrange_gate.schema.json`](../../docs/Automation/schemas/prop_arrange_gate.schema.json)  
**Inventory:** [`PROP_INVENTORY_V1.md`](PROP_INVENTORY_V1.md) · [`prop_inventory.schema.json`](../../docs/Automation/schemas/prop_inventory.schema.json)  
**Score bind:** [`TEST_SCORE_PACKET_V1.md`](TEST_SCORE_PACKET_V1.md) (`hw.test_score_packet/v1`)  
**Canon:** [`CAPTURE_REDUNDANCY.md`](../../docs/Automation/CAPTURE_REDUNDANCY.md) § Prop arrange (math-first)  
**Host this lap:** **CLOUD** docs-only · no DESKTOP Act · no Saved / Python writers

---

## One unknown (closed by this bite)

Gate schema + handoff so Test can score **Arrange readiness math-first** (bright/day) **without stills or Python**.

---

## Architecture (cite A–E only)

| Layer | Decision |
|-------|----------|
| **A** | Arrange gate is the pre-Act **contract quantum** between Design inventory and Test; CAP product stills stack stays **PARK**. |
| **B** | One deep gate schema (`prop_arrange_gate`); mirrors CAPTURE_REDUNDANCY Arrange shape — no second parallel gate dialect. |
| **C** | Inventory / transform / AABB math = **source**; stills (after `ready: true`) = confirm-only derived. |
| **D** | Design freezes inventory; Implement writers later; Test scores files/schema; Conductor DESKTOP Act only when a later bite names Saved emission. |
| **E** | `ready: false` → bounded block (`soft_fail`, `closed_fail: false`); no invent retry / stills-first ladder. |

---

## Rules (normative)

1. **Math-first.** Score via inventory ∩ world, golden transforms, AABB / overlap / ground, aim ray vs dress AABB — **not** camera still discovery.
2. **Shape.** Gate carries `ready`, `blocked_reasons[]`, `inventory`, `aim`, `lighting`, `tool_readiness`, plus `three_state` aligned with CAPTURE_REDUNDANCY Arrange + TEST_SCORE_PACKET.
3. **`ready: false` ≠ `closed_fail`.** Block Act → `soft_fail`, `closed_fail: false`, `prove_loop_status: blocked`.
4. **Exists-only ≠ PASS.** Stamps need `bytes` + `mtime` when `exists: true` (TEST_SCORE_PACKET bind).
5. **Bright / day default.** `lighting.phase` defaults to **`day`**. Night lookdev = Lead later; bots must **not** PASS night mood.
6. **Stills confirm-only after `ready: true`.** Do not start capture to find missing props.
7. **PARK CAP product.** No SC2D revive, stills-first loop, CAP-001/002 Do this lap (EXIT CAP_SWARM).

---

## PROXY example (minimal — Arrange blocked)

```json
{
  "schema": "hw.prop_arrange_gate/v1",
  "ready": false,
  "blocked_reasons": ["labels not ⊆ inventory ∩ world: PA_PROXY_CRATE_01"],
  "inventory": {
    "ok": false,
    "labels_required": ["PA_PROXY_CRATE_01"],
    "labels_present": [],
    "missing_labels": ["PA_PROXY_CRATE_01"],
    "prop_inventory_ref": "Docs/handoffs/PROP_INVENTORY_V1.md#PROXY",
    "transform_ok": false,
    "aabb_ok": false,
    "overlap_ok": true,
    "ground_ok": false
  },
  "aim": {
    "ok": false,
    "look_at_target": "CAM_PROP_READ_01",
    "forward_ray_hits_dress_aabb": null,
    "envelope_id": "ENV_HOMESTEAD_DRESS"
  },
  "lighting": {
    "ok": true,
    "phase": "day",
    "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
    "stack_verify": ["sky_visible", "key_lit"],
    "stack_ok": true
  },
  "tool_readiness": {
    "ok": true,
    "notes": ["docs-only bite — no MRQ/AL writer"],
    "mrq_status": "n/a"
  },
  "three_state": {
    "capture_outcome": "soft_fail",
    "ok": false,
    "closed_fail": false,
    "prove_loop_status": "blocked"
  },
  "stamps": []
}
```

---

## Seat ownership

| Seat | Owns |
|------|------|
| **Design** | Inventory freeze before Act; labels ⊆ world contract. |
| **Implement** | Later Saved writers matching this schema (not this lap). |
| **Test** | Files-only greps / schema bind this lap; runtime score when DESKTOP Act exists. |
| **Conductor** | DESKTOP Act only when a later bite names it — **not** CAP-PROP-GATE docs. |
| **Fix** | Defect-linked after scored closed_fail. |

---

## Greps (Conductor / Test)

```bash
grep -n 'ready:false\\|closed_fail: false\\|exists-only\\|bright\\|day\\|math-first\\|PARK' \
  Docs/handoffs/PROP_ARRANGE_GATE_V1.md \
  docs/Automation/schemas/prop_arrange_gate.schema.json \
  docs/Automation/CAPTURE_REDUNDANCY.md
grep -n 'hw.prop_arrange_gate/v1\\|blocked_reasons\\|tool_readiness\\|prove_loop_status' \
  docs/Automation/schemas/prop_arrange_gate.schema.json
```

---

## Forbidden this lap

Content/Python · MRQ/AL/SC2D writers · Saved emitters · `.uasset`/`.umap` · night bot PASS · DESKTOP Act · CAP-001/002 revive · ImageGrab · AGENTS dump · T0 Acts · TOOL SCOUT.

---

*Policy row: CAPTURE_REDUNDANCY § Prop arrange (math-first) — CAP-PROP-GATE.*
