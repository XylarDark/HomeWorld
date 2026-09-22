# Docs/30 — Demo Spine (DS)

| Field | Value |
|-------|-------|
| **Status** | **DEMO-SPINE STRATEGY APPROVED** — Lead **`APPROVE DEMO-SPINE`**, 2026-09-21 ET; **DS-A IN PROGRESS** (this PR) |
| **Date** | 2026-09-22 |
| **Author** | Conductor (HomeWorld) |
| **Prior tracks** | [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) **CLOSED** (GC-B/C logs + placeholders) |
| **Prefix** | **DS** — do **not** reuse GC / CD / MV / SS gate strings |

---

## Gate

Lead **`APPROVE DEMO-SPINE`**, 2026-09-21 ET — **GRANTED** (chat). Unlocks **DS-A** (visible hearth path).

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal

Make **campfire → tent → cottage** **seeable in-world** on VS_MVP so a human can walk the demo progression without cheats as the only UX. GC-B/C **logs and volumes remain**; DS-A adds **engine-primitive visuals + labels** and reveals **`GP_Demo_Cottage`** after `PROGRESS:COTTAGE_UNLOCK`.

**KEEP-LOCAL:** Level `.umap` / mesh assignments may stay on the Windows Editor host; runtime C++ spawns primitives when saved content is absent.

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **DS STRATEGY** | Visible demo spine policy | Lead | **APPROVED** | Lead **`APPROVE DEMO-SPINE`**, 2026-09-21 ET |
| **DS-A** | Visible hearth + cottage blockout | CLOUD+DESKTOP | **IN PROGRESS** | Handoff [DS_A_VISIBLE_HEARTH.md](handoffs/DS_A_VISIBLE_HEARTH.md) |

**Out of scope (DS-A):** Full P0 Conductor prove on DESKTOP; functional kitchen cooking (P2 UT); spirit stealth polish; 7th RES; functional shop craft; combat; bulk `.uasset` import.

---

## Implementation map (DS-A)

| Surface | Role |
|---------|------|
| `AHomeWorldCraftStation` | Engine mesh + floating label per station kind (hub / campfire / tent) |
| `AHomeWorldGcPlaceholderVolume` | Room/shop floor marker + label (GC-C overlap logs unchanged) |
| `UHomeWorldCraftSubsystem::RevealDemoCottageShell` | Unhide or spawn `GP_Demo_Cottage` on `PROGRESS:COTTAGE_UNLOCK` |
| `place_vs_mvp_gc_craft.py` | Idempotent `GP_Craft_Hub` |
| `place_vs_mvp_gc_placeholders.py` | GC-C volumes + hidden cottage blockout |
| `vs_mvp_ds_visual_helpers.py` | KEEP-LOCAL cottage shell helper |

**Log tags (unchanged):** `CRAFT: CAMPFIRE`, `CRAFT: TENT`, `PROGRESS:COTTAGE_UNLOCK`, `PLACEHOLDER:COTTAGE_KITCHEN` — plus **`DS-A: cottage revealed`** / **`DS-A: cottage spawned`**.

---

## Cheats vs walk path

| Path | Use |
|------|-----|
| **Walk (primary UX)** | Day gather → `GP_Craft_Hub` interact → campfire → tent → cottage appears → walk into kitchen volume |
| **Cheats (prove only)** | `hw.Craft.GrantDemo`, `hw.Craft.Campfire`, `hw.Craft.Tent`, `hw.Craft.Status` |

---

## Next gates

**DS-B+** TBD (Lead) — e.g. art-dressed cottage prop rebind, P0 prove bundle. Do not open without Lead gate string prefixed **`DS`**.
