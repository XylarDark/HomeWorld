# PROP_INVENTORY_V1 — math-first prop inventory (CAP-INV-SCHEMA → T0_FEEL_PROP_FREEZE_V1)

**Bite id:** `T0_FEEL_PROP_FREEZE_V1` (extends prior `CAP-INV-SCHEMA` freeze; schema contract unchanged)  
**Parent EXIT feel SCOPE:** [`Docs/handoffs/research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md`](research/EXIT_INTERVIEW_SCOPE_PROTOTYPE_FEEL_V1.md)  
**Cite movement/env:** [`Docs/handoffs/GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md`](GAME_DESIGN_MOVEMENT_ENV_CANON_V1.md)  
**Feel DONE-WHEN templates (EXIT §6, cite by name):** `FEEL-TEA` · `FEEL-GLIDE` · `FEEL-PLANT` · `FEEL-NURTURE` · `FEEL-EJECT` · `FEEL-BED` · `FEEL-ENV-GREYBOX` (also `FEEL-NIGHT-HOME` · `FEEL-SOOTHE` · `FEEL-PORTAL` when later bites dress those).  
**GAME_FEEL_CANON:** may land on #238 soon — cite feel DONE-WHEN from EXIT §6 templates by name (`FEEL-*`); do not paste feel-library body here.  
**Schema:** `hw.prop_inventory/v1` → [`docs/Automation/schemas/prop_inventory.schema.json`](../../docs/Automation/schemas/prop_inventory.schema.json) (do not change schema)  
**Host this lap:** **CLOUD** docs-only · no DESKTOP Act · no Saved writers · no Python writers  
**CAP product:** **PARKED** · stills **confirm-only** · bright/day · **no night PASS**

---

## One unknown (closed by this bite)

Which greybox props occupy the ranked T0 MUST-ENV-GREYBOX envelopes so later Arrange can score presence without stills?

*(Prior CAP-INV-SCHEMA unknown — frozen fields for prop presence + pose without a still — remains closed; this bite freezes T0 envelope rows.)*

---

## Architecture (cite A–E only)

| Layer | Decision |
|-------|----------|
| **A** | Inventory schema is the Design→Test **contract quantum**; CAP product / stills stack stays **PARK** / **PARKED** until CAP-PROP-GATE. |
| **B** | One deep schema module (`prop_inventory`); no shallow per-track copy of golden transforms. |
| **C** | Golden transform + tol are **source**; stills (later) are **confirm-only** derived evidence. |
| **D** | Design owns inventory freeze; Implement codes later against schema; Test scores; Conductor alone DESKTOP Act when a later bite names it. |
| **E** | Labels ∉ inventory ∩ world → **block Act** (bounded degrade), not invent retry. |

---

## Rules (normative)

1. **Math-first.** Score presence/pose via inventory + golden transforms + AABB/overlap/ground (+ log greps). Do **not** use camera stills to discover placement.
2. **`prove_labels ⊆ inventory ∩ world`** before Act. Else **block Act**: `soft_fail`, `closed_fail: false`, `prove_loop_status: blocked` (same Arrange-block semantics as [`TEST_SCORE_PACKET_V1.md`](TEST_SCORE_PACKET_V1.md) / [`CAPTURE_REDUNDANCY.md`](../../docs/Automation/CAPTURE_REDUNDANCY.md)).
3. **Bright/day default.** `tod_light.phase` defaults to **`day`**. Night / lookdev = Lead taste later; bots must **not** PASS night mood.
4. **Stills confirm-only later.** Capture ID path is bite **`CAP-PROP-GATE`** (next Conductor paste after this Test PASS). Not this lap. CAP product remains **PARKED**.
5. **PROXY vs OBSERVED.** This card + schema = **PROXY**. World query / gate fields after a future Act = **OBSERVED**.

---

## Required keys per prop item

`label` · `class` · `mesh` · `golden_transform{location[3],rotation[3],scale[3],loc_tol_cm,rot_tol_deg}` · `aabb{extent_min_cm,envelope_id}` · `look_at{target}` · `tod_light{phase,preset_id,stack_verify[]}` · `overlap{forbid_labels[],allow_touch_cm}` · `ground{method,z_delta_max_cm}` · `prove_labels[]`

Root shape: either `{ "schema": "hw.prop_inventory/v1", "props": [ ... ] }` **or** a bare array of items (schema `oneOf`).

---

## Envelope → NODE_* → FEEL-* (MUST-ENV-GREYBOX)

| Envelope (`envelope_id`) | NODE_* labels | FEEL-* templates (EXIT §6) |
|--------------------------|---------------|----------------------------|
| `ENV_T0_HOME` | `NODE_WAKE` · `NODE_KETTLE` · `NODE_BACKPACK` · `NODE_PLANT_SLOT` | `FEEL-TEA` · `FEEL-PLANT` · `FEEL-NURTURE` (same slot identity) · `FEEL-ENV-GREYBOX` |
| `ENV_T0_GLIDE` | `NODE_GLIDER` | `FEEL-GLIDE` · `FEEL-ENV-GREYBOX` |
| `ENV_T0_FIELD` | `NODE_FIELD_GATHER` · `NODE_RUNE` | `FEEL-GLIDE` (arrive AABB) · `FEEL-BED` (rune gate) · `FEEL-ENV-GREYBOX` |
| `ENV_T0_CAMP` | `NODE_DAY_CAMP` | `FEEL-EJECT` (`EJECT_HOME`) · `FEEL-ENV-GREYBOX` |
| `ENV_T0_BED` | `NODE_BED` | `FEEL-BED` · `FEEL-ENV-GREYBOX` |

Notes:

- **FEEL-NURTURE** identity: nurture target == same `NODE_PLANT_SLOT` as day plant — one inventory row; no second prop.
- Homestead run still greppable via `NODE_BED` even though bed row uses `envelope_id` `ENV_T0_BED`.
- `NODE_DAY_CAMP` prove_labels include `NODE_DAY_CAMP`; `EJECT_HOME` is named in `look_at.target` / `stack_verify` (no invented schema keys).

---

## T0 MUST-ENV-GREYBOX freeze (PROXY)

All `golden_transform` numbers below are **PROXY** (Design freeze for Arrange math-first scoring; not OBSERVED world query). Mesh paths are greybox **PROXY** assets. `tod_light.phase` is **`day`** · preset `TOD_DAY_BRIGHT_DEFAULT`. CAP product **PARKED**; stills **confirm-only**.

```json
{
  "schema": "hw.prop_inventory/v1",
  "props": [
    {
      "label": "NODE_WAKE",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyWakeMarker.SM_ProxyWakeMarker",
      "golden_transform": {
        "location": [0.0, 0.0, 0.0],
        "rotation": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 5.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [30.0, 30.0, 80.0],
        "envelope_id": "ENV_T0_HOME"
      },
      "look_at": {
        "target": "ENV_T0_HOME_CENTROID"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_KETTLE", "NODE_BED"],
        "allow_touch_cm": 2.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 5.0
      },
      "prove_labels": ["NODE_WAKE"]
    },
    {
      "label": "NODE_KETTLE",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyKettle.SM_ProxyKettle",
      "golden_transform": {
        "location": [80.0, -20.0, 90.0],
        "rotation": [0.0, 45.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 3.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [15.0, 15.0, 25.0],
        "envelope_id": "ENV_T0_HOME"
      },
      "look_at": {
        "target": "NODE_WAKE"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_WAKE", "NODE_BACKPACK"],
        "allow_touch_cm": 1.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 3.0
      },
      "prove_labels": ["NODE_KETTLE"]
    },
    {
      "label": "NODE_BACKPACK",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyBackpack.SM_ProxyBackpack",
      "golden_transform": {
        "location": [-60.0, 40.0, 20.0],
        "rotation": [0.0, -30.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 3.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [20.0, 12.0, 35.0],
        "envelope_id": "ENV_T0_HOME"
      },
      "look_at": {
        "target": "NODE_WAKE"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_KETTLE", "NODE_BED"],
        "allow_touch_cm": 1.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 3.0
      },
      "prove_labels": ["NODE_BACKPACK"]
    },
    {
      "label": "NODE_PLANT_SLOT",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyPlantSlot.SM_ProxyPlantSlot",
      "golden_transform": {
        "location": [200.0, 150.0, 0.0],
        "rotation": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 5.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [25.0, 25.0, 40.0],
        "envelope_id": "ENV_T0_HOME"
      },
      "look_at": {
        "target": "ENV_T0_HOME_STOOP"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_GLIDER"],
        "allow_touch_cm": 2.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 5.0
      },
      "prove_labels": ["NODE_PLANT_SLOT"]
    },
    {
      "label": "NODE_GLIDER",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyGliderPerch.SM_ProxyGliderPerch",
      "golden_transform": {
        "location": [350.0, -100.0, 400.0],
        "rotation": [0.0, 90.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 8.0,
        "rot_tol_deg": 3.0
      },
      "aabb": {
        "extent_min_cm": [60.0, 40.0, 20.0],
        "envelope_id": "ENV_T0_GLIDE"
      },
      "look_at": {
        "target": "NODE_FIELD_GATHER"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_PLANT_SLOT"],
        "allow_touch_cm": 2.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 8.0
      },
      "prove_labels": ["NODE_GLIDER"]
    },
    {
      "label": "NODE_FIELD_GATHER",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyFieldGather.SM_ProxyFieldGather",
      "golden_transform": {
        "location": [1200.0, 800.0, 0.0],
        "rotation": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 10.0,
        "rot_tol_deg": 3.0
      },
      "aabb": {
        "extent_min_cm": [80.0, 80.0, 30.0],
        "envelope_id": "ENV_T0_FIELD"
      },
      "look_at": {
        "target": "NODE_RUNE"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_DAY_CAMP"],
        "allow_touch_cm": 5.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 5.0
      },
      "prove_labels": ["NODE_FIELD_GATHER"]
    },
    {
      "label": "NODE_RUNE",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyRune.SM_ProxyRune",
      "golden_transform": {
        "location": [1400.0, 600.0, 50.0],
        "rotation": [0.0, -15.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 5.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [25.0, 25.0, 60.0],
        "envelope_id": "ENV_T0_FIELD"
      },
      "look_at": {
        "target": "NODE_FIELD_GATHER"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_BED"],
        "allow_touch_cm": 2.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 5.0
      },
      "prove_labels": ["NODE_RUNE"]
    },
    {
      "label": "NODE_DAY_CAMP",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyDayCamp.SM_ProxyDayCamp",
      "golden_transform": {
        "location": [1800.0, 400.0, 0.0],
        "rotation": [0.0, 180.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 10.0,
        "rot_tol_deg": 3.0
      },
      "aabb": {
        "extent_min_cm": [120.0, 120.0, 40.0],
        "envelope_id": "ENV_T0_CAMP"
      },
      "look_at": {
        "target": "EJECT_HOME"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit", "EJECT_HOME"]
      },
      "overlap": {
        "forbid_labels": ["NODE_FIELD_GATHER"],
        "allow_touch_cm": 5.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 5.0
      },
      "prove_labels": ["NODE_DAY_CAMP"]
    },
    {
      "label": "NODE_BED",
      "class": "/Script/Engine.StaticMeshActor",
      "mesh": "/Game/Props/Greybox/SM_ProxyBed.SM_ProxyBed",
      "golden_transform": {
        "location": [-40.0, -80.0, 0.0],
        "rotation": [0.0, 90.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "loc_tol_cm": 3.0,
        "rot_tol_deg": 2.0
      },
      "aabb": {
        "extent_min_cm": [50.0, 30.0, 25.0],
        "envelope_id": "ENV_T0_BED"
      },
      "look_at": {
        "target": "ENV_T0_BED_THRESHOLD"
      },
      "tod_light": {
        "phase": "day",
        "preset_id": "TOD_DAY_BRIGHT_DEFAULT",
        "stack_verify": ["sky_visible", "key_lit"]
      },
      "overlap": {
        "forbid_labels": ["NODE_WAKE", "NODE_KETTLE"],
        "allow_touch_cm": 1.0
      },
      "ground": {
        "method": "raycast_down",
        "z_delta_max_cm": 3.0
      },
      "prove_labels": ["NODE_BED"]
    }
  ]
}
```

---

## PROXY example (minimal — CAP-INV-SCHEMA history)

Kept for schema contract continuity (crate proxy from CAP-INV-SCHEMA). Prefer T0 MUST-ENV-GREYBOX freeze above for Arrange.

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
| **Design** | Freeze inventory JSON matching this schema (look-at / AABB / TOD before Act). Bite A `T0_FEEL_PROP_FREEZE_V1`. |
| **Implement** | Later writers/scorers against schema (not this lap). |
| **Test** | Greps + schema bind; scores math signals when gate bite lands. |
| **Conductor** | DESKTOP Act **only** when a later bite names it — **not** this freeze. Ball after merge → HW Test / Conductor. |
| **Fix** | Defect-linked only after a scored Act fail. |

---

## Greps (Conductor / Test)

```bash
grep -E 'NODE_WAKE|NODE_KETTLE|NODE_PLANT_SLOT|NODE_GLIDER|NODE_FIELD_GATHER|NODE_RUNE|NODE_DAY_CAMP|NODE_BED' \
  Docs/handoffs/PROP_INVENTORY_V1.md
grep -E 'golden_transform|tod_light|phase.*day|envelope_id' \
  Docs/handoffs/PROP_INVENTORY_V1.md
grep -E 'CAP PARK|PARKED|confirm-only' Docs/handoffs/PROP_INVENTORY_V1.md
grep -n 'prove_labels\|golden_transform\|loc_tol_cm\|soft_fail\|closed_fail: false\|day' \
  Docs/handoffs/PROP_INVENTORY_V1.md \
  docs/Automation/schemas/prop_inventory.schema.json
grep -n 'CAP-INV-SCHEMA\|prop_inventory\|PROP_INVENTORY_V1\|T0_FEEL_PROP_FREEZE_V1' \
  docs/Automation/ONE_SHOT_BITES.md
```

---

## Forbidden this lap

`Source/**` · `Content/**` · `.uasset`/`.umap` · Saved writers · Python writers · CAP product Do / revive · CAP-PROP-GATE · night bot PASS · DESKTOP Act · AGENTS dump · A–E rewrite · pin bump · feature-list stamp · feel-library body paste · sibling `T0_FEEL_ENVELOPE_INDEX_V1.md` (fold `envelope_id` into props instead).

---

*Pointer from [`docs/Automation/ONE_SHOT_BITES.md`](../../docs/Automation/ONE_SHOT_BITES.md) § Prop inventory (math-first). Bite A `T0_FEEL_PROP_FREEZE_V1` · CAP PARKED · confirm-only · phase day.*
