# GC-C — Placeholder shops + cottage room volumes

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE GC-C`**, 2026-09-21 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/22_GATHER_CRAFT_IMPL.md](../22_GATHER_CRAFT_IMPL.md) |
| **Prior** | GC-B **APPROVED / CLOSED** — Lead **`APPROVE GC-B`** 2026-09-21 ET |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Placeholder enum + log lines | `HomeWorldGcPlaceholderTypes.h/.cpp` |
| Overlap volume actor | `AHomeWorldGcPlaceholderVolume` — pawn overlap only |
| Placement | `Content/Python/place_vs_mvp_gc_placeholders.py` → `GP_PH_*` on `L_VS_MVP_Markers` |
| Cottage gate | Kitchen / bedroom / cauldron require `UHomeWorldCraftSubsystem::IsCottageUnlocked()` |

**Log idempotency:** One greppable line **per overlap visit**; `EndOverlap` clears `bLoggedThisOverlap` so walking out and back in logs again. Standing inside does **not** spam (no tick).

---

## Expected greps (Output Log)

```text
PLACEHOLDER:WOODSHOP enter
PLACEHOLDER:TEXTILE enter
PLACEHOLDER:RESEARCH enter
PLACEHOLDER:COTTAGE_KITCHEN
PLACEHOLDER:COTTAGE_BEDROOM
PLACEHOLDER:CAULDRON
```

**Before cottage unlock (kitchen only):**

```text
PLACEHOLDER:COTTAGE_KITCHEN locked
```

**Optional once after unlock (kitchen):**

```text
CRAFT: kitchen rebind TODO
```

**Grep commands (DESKTOP, saved log or live Output Log):**

```text
rg "PLACEHOLDER:(WOODSHOP enter|TEXTILE enter|RESEARCH enter|COTTAGE_KITCHEN|COTTAGE_BEDROOM|CAULDRON)" Saved/Logs/editor_output_filtered.txt
```

---

## DESKTOP runbook

```text
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("place_vs_mvp_gc_craft.py")
execute_python_script("place_vs_mvp_gc_placeholders.py")
# PIE — walk into each GP_PH_* volume near homestead
# Regression: GC-B still works
hw.Craft.GrantDemo
hw.Craft.Campfire
hw.Craft.Tent
rg "CRAFT: CAMPFIRE|CRAFT: TENT|PROGRESS:COTTAGE_UNLOCK" Saved/Logs/editor_output_filtered.txt
```

| Label | Kind |
|-------|------|
| `GP_PH_Woodshop` | Woodshop |
| `GP_PH_Textile` | Textile |
| `GP_PH_Research` | Research |
| `GP_PH_CottageKitchen` | Kitchen (gated) |
| `GP_PH_CottageBedroom` | Bedroom (gated) |
| `GP_PH_Cauldron` | Living / cauldron (gated) |

---

## Done criteria

- [x] All six `PLACEHOLDER:*` lines appear after walking volumes (cottage rooms after `PROGRESS:COTTAGE_UNLOCK` / `hw.Craft.Tent` path)
- [x] No shop menus, no RES spend in placeholders, no 7th `RES_*`
- [x] GC-B greps still pass (`CRAFT: CAMPFIRE`, `CRAFT: TENT`, `PROGRESS:COTTAGE_UNLOCK`)
- [x] Homestead remains non-combat
- [x] Lead **`APPROVE GC-C`**, 2026-09-21 ET — [Docs/22](../22_GATHER_CRAFT_IMPL.md) **CLOSED / COMPLETE**

---

## Gate

Lead **`APPROVE GC-C`**, 2026-09-21 ET — **GRANTED**. **GC** implementation track **CLOSED / COMPLETE** (merged main `7061e18` / PR #126). **Do not stamp phase gates in PR** — chat only.
