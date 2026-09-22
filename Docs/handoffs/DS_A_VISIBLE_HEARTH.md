# DS-A — Visible hearth (campfire → tent → cottage)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE DS-A`**, 2026-09-21 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/30_DEMO_SPINE.md](../30_DEMO_SPINE.md) — **CLOSED / COMPLETE** |
| **Prior** | GC-B/C **CLOSED** — logs + placeholder volumes on main |
| **Close gate** | Lead **`APPROVE DS-A`** — **GRANTED** 2026-09-21 ET (chat; truncated **`APPROVE DS-`** → DS-A) |
| **Main** | `7d579f9` / PR #136 |

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

**Expected greps (Output Log)** — for optional DESKTOP verify; **not** claimed PASS by this docs close:

```text
CRAFT: CAMPFIRE
CRAFT: TENT
PROGRESS:COTTAGE_UNLOCK
DS-A: cottage revealed
PLACEHOLDER:COTTAGE_KITCHEN
```

**PROVE-BATCH** (full DESKTOP walk + grep bundle) remains **deferred** — placement-script crash / PIE MCP timeouts on host; Lead accepted close without invented PASS stamps.

---

## KEEP-LOCAL

Saving `L_VS_MVP_Markers` after placement scripts persists hidden **`GP_Demo_Cottage`** on the DESKTOP host. Cloud PR ships **code + scripts** only; first Editor run applies the same layout idempotently.

---

## Done criteria (DS-A)

- [x] Hub, campfire, and tent stubs visible in PIE with readable labels (impl on main; DESKTOP visual walk **deferred/accepted** with Lead **`APPROVE DS-A`**)
- [x] Cottage blockout appears after unlock (unhide or runtime spawn)
- [x] Kitchen volume reachable on foot after unlock (volume + logs on main)
- [x] GC-B/C log contract preserved (no 7th RES; no functional shop craft)
- [x] No combat; no bulk uassets in DS-A PR
- [x] Lead **`APPROVE DS-A`** — Docs/30 DS-A **APPROVED / CLOSED** (2026-09-21 ET)

---

## Gate

Lead **`APPROVE DS-A`** closes DS-A and the Docs/30 track. **DS-B+** scope TBD (Lead). **Do not stamp DS-A APPROVED in PR** — Lead typed gate in chat.
