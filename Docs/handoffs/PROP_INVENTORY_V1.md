# PROP_INVENTORY_V1 — math-first prop inventory (CAP-INV-SCHEMA)

**Bite id:** `CAP-INV-SCHEMA`  
**Parent EXIT:** [`Docs/handoffs/research/EXIT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md`](research/EXIT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md) (filed on HW #231)  
**Schema:** `hw.prop_inventory/v1` → [`docs/Automation/schemas/prop_inventory.schema.json`](../../docs/Automation/schemas/prop_inventory.schema.json)  
**Host this lap:** **CLOUD** docs-only · no DESKTOP Act · no Saved writers

---

## One unknown (closed by this bite)

What **frozen fields** Design must emit so Implement/Test can score **prop presence + pose without a still**.

---

## Architecture (cite A–E only)

| Layer | Decision |
|-------|----------|
| **A** | Inventory schema is the Design→Test **contract quantum**; CAP product / stills stack stays **PARK** until CAP-PROP-GATE. |
| **B** | One deep schema module (`prop_inventory`); no shallow per-track copy of golden transforms. |
| **C** | Golden transform + tol are **source**; stills (later) are confirm-only derived evidence. |
| **D** | Design owns inventory freeze; Implement codes later against schema; Test scores; Conductor alone DESKTOP Act when a later bite names it. |
| **E** | Labels ∉ inventory ∩ world → **block Act** (bounded degrade), not invent retry. |

---

## Rules (normative)

1. **Math-first.** Score presence/pose via inventory + golden transforms + AABB/overlap/ground (+ log greps). Do **not** use camera stills to discover placement.
2. **`prove_labels ⊆ inventory ∩ world`** before Act. Else **block Act**: `soft_fail`, `closed_fail: false`, `prove_loop_status: blocked` (same Arrange-block semantics as [`TEST_SCORE_PACKET_V1.md`](TEST_SCORE_PACKET_V1.md) / [`CAPTURE_REDUNDANCY.md`](../../docs/Automation/CAPTURE_REDUNDANCY.md)).
3. **Bright/day default.** `tod_light.phase` defaults to **`day`**. Night / lookdev = Lead taste later; bots must **not** PASS night mood.
4. **Stills confirm-only later.** Capture ID path is bite **`CAP-PROP-GATE`** (next Conductor paste after this Test PASS). Not this lap.
5. **PROXY vs OBSERVED.** This card + schema = **PROXY**. World query / gate fields after a future Act = **OBSERVED**.

---

## Required keys per prop item

`label` · `class` · `mesh` · `golden_transform{location[3],rotation[3],scale[3],loc_tol_cm,rot_tol_deg}` · `aabb{extent_min_cm[3],envelope_id}` · `look_at{target}` · `tod_light{phase,preset_id,stack_verify[]}` · `overlap{forbid_labels[],allow_touch_cm}` · `ground{method,z_delta_max_cm}` · `prove_labels[]`

Root shape: either `{ "schema": "hw.prop_inventory/v1", "props": [ ... ] }` **or** a bare array of items (schema `oneOf`).

---

## PROXY example (minimal)

```json
{
  "schema": "hw.prop_inventory/v1",
  "props": [
    {
      "label": "PA_PROXY_CRATE_01",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/SM_ProxyCrate.SM_ProxyCrate",
      "golden_transform": {
        "location": [120.0, -40.0, 0.0],
        "rotation": [0.0, 90.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 2.0,
        "rot_tol_deg": 1.0
      },
      "aabb": {
        "extent_min_cm": [20.0, 20.0, 20.0],
        "envelope_id": "ENV_HOMESTEAD_DRESS"
      },
      "look_at": {
        "target": "CAM_PROP_READ_01"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["PA_PROXY_CRATE_02"],
        "allow_touch_cm": 1.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 3.0
      },
      "prove_labels": ["PA_PROXY_CRATE_01"]
    }
  ]
}
```

---

## Seat ownership

| Seat | Owns |
|------|------|
| **Design** | Freeze inventory JSON matching this schema (look-at / AABB / TOD before Act). |
| **Implement** | Later writers/scorers against schema (not this lap). |
| **Test** | Greps + schema bind; scores math signals when gate bite lands. |
| **Conductor** | DESKTOP Act **only** when a later bite names it — **not** CAP-INV-SCHEMA. |
| **Fix** | Defect-linked only after a scored Act fail. |

---

## Greps (Conductor / Test)

```bash
grep -n 'prove_labels\|golden_transform\|loc_tol_cm\|soft_fail\|closed_fail: false\|day' \
  Docs/handoffs/PROP_INVENTORY_V1.md \
  docs/Automation/schemas/prop_inventory.schema.json
grep -n 'CAP-INV-SCHEMA\|prop_inventory\|PROP_INVENTORY_V1' \
  docs/Automation/ONE_SHOT_BITES.md
```

---

## Forbidden this lap

Content/Python · MRQ/AL/SC2D · `.uasset`/`.umap` · Saved writers · CAP product revive · CAP-PROP-GATE · night bot PASS · DESKTOP Act · AGENTS dump.

---

*Pointer from [`docs/Automation/ONE_SHOT_BITES.md`](../../docs/Automation/ONE_SHOT_BITES.md) § Prop inventory (math-first).*
