# DS-A — Visible hearth (campfire → tent → cottage)

| Field | Value |
|-------|-------|
| **Status** | **IN PROGRESS** — Lead **`APPROVE DEMO-SPINE`**, 2026-09-21 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/30_DEMO_SPINE.md](../30_DEMO_SPINE.md) |
| **Prior** | GC-B/C **CLOSED** — logs + placeholder volumes on main |

---

## Deliverable

| Item | Path / note |
|------|-------------|
| Craft visuals | `AHomeWorldCraftStation` — primitive mesh + label |
| Room visuals | `AHomeWorldGcPlaceholderVolume` — floor cube + label |
| Cottage reveal | `UHomeWorldCraftSubsystem::RevealDemoCottageShell` on `PROGRESS:COTTAGE_UNLOCK` |
| Level placement | `place_vs_mvp_gc_craft.py`, `place_vs_mvp_gc_placeholders.py`, `vs_mvp_ds_visual_helpers.py` |
| Cottage actor | Label **`GP_Demo_Cottage`**, tag **`DS_Demo_Cottage`** (hidden until unlock) |

---

## PLAYTEST sentence (no cheats)

**Day body:** gather **WOOD + STONE + FIBER** from VS day piles → homestead **`GP_Craft_Hub`** (floating **CRAFT HUB**) → Interact → **`GP_Craft_Campfire`** appears → Interact → **`GP_Craft_Tent`** → **`PROGRESS:COTTAGE_UNLOCK`** → **`GP_Demo_Cottage`** shell visible → walk into **`GP_PH_CottageKitchen`** volume → log **`PLACEHOLDER:COTTAGE_KITCHEN`**.

---

## DESKTOP runbook

```text
.\Tools\Safe-Build.ps1
# Editor (VS_MVP markers level):
execute_python_script("place_vs_mvp_gc_craft.py")
execute_python_script("place_vs_mvp_gc_placeholders.py")
# PIE — walk path (gather RES first) or cheat prove:
hw.Craft.GrantDemo
hw.Craft.Campfire
hw.Craft.Tent
hw.Craft.Status
```

**Expected greps (Output Log):**

```text
CRAFT: CAMPFIRE
CRAFT: TENT
PROGRESS:COTTAGE_UNLOCK
DS-A: cottage revealed
PLACEHOLDER:COTTAGE_KITCHEN
```

---

## KEEP-LOCAL

Saving `L_VS_MVP_Markers` after placement scripts persists hidden **`GP_Demo_Cottage`** on the DESKTOP host. Cloud PR ships **code + scripts** only; first Editor run applies the same layout idempotently.

---

## Done criteria (DS-A)

- [ ] Hub, campfire, and tent stubs visible in PIE with readable labels
- [ ] Cottage blockout appears after unlock (unhide or runtime spawn)
- [ ] Kitchen volume reachable on foot after unlock
- [ ] GC-B/C log greps still pass
- [ ] No 7th RES; no functional shop craft; no combat; no bulk uassets in PR

---

## Gate

Lead **`APPROVE DS-A`** in chat closes DS-A and unlocks any **DS-B** scope (TBD). **Do not stamp DS-A APPROVED in PR.**
