# Docs/09_FALLBACK_GLIDE.md

**Status:** FALLBACK V2 implementation runbook  
**Date:** 2026-09-17  
**Owner:** SYS/GPL  
**Canon:** [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) §5–§6, [Lib/08_Transit/GLIDE_SPLINE.md](../Lib/08_Transit/GLIDE_SPLINE.md)

---

## Hard rules (Lead locked)

| Rule | Detail |
|------|--------|
| **FALLBACK FLIGHT ARMED** | Scripted glide **only** along locked `CRUMB_*` order |
| **No free-flight** | No steering, no flight HUD, no energy meter |
| **Portal V5** | `SM_Shrine_Homestead` ↔ `SM_Shrine_Return` both ways (simple teleport OK) |
| **Docs/07** | CLOSED — do not reopen for free-flight features |

---

## C++ components

| Type | Role |
|------|------|
| `UHomeWorldFallbackGlideComponent` | On `AHomeWorldCharacter`; resolves crumbs, SmoothInterp traverse, `OnGlideCompleted` |
| `UHomeWorldShrinePortalComponent` | Box overlap → teleport to linked shrine label |
| `AHomeWorldShrinePortalTrigger` | Spawnable actor wrapping portal component (Editor / Python dress) |

### Locked crumb order (do not reorder)

1. `CRUMB_Depart_Lookout`
2. `CRUMB_Air_01`
3. `CRUMB_Islet_01`
4. `CRUMB_Air_02`
5. `CRUMB_Islet_02`
6. `CRUMB_Air_03`
7. `CRUMB_Islet_03`
8. `CRUMB_Approach`
9. `CRUMB_Landing`

Duration default **32 s** (clamp **25–40 s**). Logs prefixed **`FALLBACK:`** in Output Log.

### Input / interact

- **Interact (E)** via existing `GA_Interact` / `UHomeWorldInteractAbility`:
  1. If within **450 cm** of `GP_GlideStart` / `CRUMB_Depart_Lookout` / `GlideStart` tag → `StartGlide()`
  2. Else forward trace for shrine portal → `TryPortalTransit`
  3. Else existing harvest / POI interact chain

### Portal night gate (soft)

| Control | Default | Effect |
|---------|---------|--------|
| `bRequireNight` on portal component | `false` | PIE demo: portal works any phase |
| CVar `hw.Portal.RequireNight` | `-1` | `-1` = use component; `0` = day OK; `1` = night only |

---

## Level setup (VS_MVP)

### 1. Markers (one-time / idempotent)

```text
# Editor: Tools > Execute Python Script
Content/Python/place_vs_mvp_markers.py
Content/Python/place_fallback_glide_markers.py
```

`place_fallback_glide_markers.py` uses UE reflection names `DestinationLabel` / `bRequireNight` on portal components.

Creates:

- All `CRUMB_*` TargetPoints (from `AssetCreation/Exports/MVP_CRUMB_SPLINE.json`)
- `GP_GlideStart` at glider perch
- `GP_PortalA` (homestead → return), `GP_PortalB` (return → homestead)
- `ANCHOR_SM_Shrine_*` anchors (from JSON)

Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`

### 2. Build C++

On **Windows host DESKTOP-21CT3H0** (UE 5.7 — not available on cloud VM):

```powershell
.\Tools\Safe-Build.ps1
```

Cloud agents land C++ only; Lead verifies compile + PIE on Windows.

---

## PIE test checklist

1. Open `L_VS_MVP_Markers`, set GameMode default pawn `BP_HomeWorldCharacter` (or C++ with GAS interact).
2. Ensure phase is **Day** (`hw.SetPhase Day` or TimeOfDay subsystem).
3. Walk to **`GP_GlideStart`** / lookout perch → press **E**.
4. **Expect:** Output Log lines `FALLBACK: StartGlide`, segment logs, `Reached CRUMB_Landing`, walk restored (~25–40 s).
5. **Expect:** No WASD steering during glide; camera look still works.
6. Walk into **`GP_PortalA`** or **`GP_PortalB`** (or interact facing shrine trigger).
7. **Expect:** `FALLBACK: Portal transit ...` and pawn at opposite shrine.
8. **Reject:** Free-flight off crumbs, flight HUD, reordering crumbs without WLD sign-off.

---

## Cancel / debug

| Action | How |
|--------|-----|
| Cancel glide | Blueprint/C++ `CancelFallbackGlide()` on character |
| Portal cooldown | 2 s default (`TeleportCooldownSeconds`) |
| Force night portal | Console: `hw.Portal.RequireNight 1` then `SetPhase Night` |

---

## Related docs

- [03_GAMEPLAY_MVP.md](03_GAMEPLAY_MVP.md) — V2 glide + V5 portal contract
- [05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md) — FALLBACK note
- [docs/Maps/](../docs/Maps/) — UE engineering maps (lowercase `docs/`)
