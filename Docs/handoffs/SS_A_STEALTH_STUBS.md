# SS-A — Spirit stealth stubs (handoff)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE SS-A`**, 2026-09-21 ET |
| **Track** | SS-A |
| **Gate** | Lead **`APPROVE SS STRATEGY`** — **GRANTED** 2026-09-21 ET (chat **`SS-A`** unlock) |
| **Close gate** | Lead **`APPROVE SS-A`** — **GRANTED** 2026-09-21 ET (chat) |
| **Impl doc** | [25_SPIRIT_STEALTH_IMPL.md](../25_SPIRIT_STEALTH_IMPL.md) — **CLOSED / COMPLETE** |
| **Bible** | [SPIRIT_STEALTH_BIBLE.md](../SPIRIT_STEALTH_BIBLE.md) |
| **Main** | `7bc577f` / PR #133 |

---

## Scope

- Planet / VS_MVP path only — **never homestead**
- Spirit form only — **no crouch**, no kill-on-detect, no shrine kidnap on alert peak
- Three reveal volumes + one **body mundane** control (no spirit reveal)
- Does **not** change MV blink, CD minigames, or DAYNIGHT body darkness kidnap

---

## DESKTOP chain

```text
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("place_vs_mvp_ss_stealth.py")
# PIE L_VS_MVP_Markers — log LogHomeWorld Log
```

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | `hw.TimeOfDay.Phase 2` (spirit) | form sync (existing DAYNIGHT) |
| 2 | Walk into `GP_SS_Lit_Campfire` | `STEALTH: LIT enter (Campfire)` |
| 3 | Stay ~3s in volume | `STEALTH: ALERT` |
| 4 | Walk out | `STEALTH: CLEAR` |
| 5 | `hw.TimeOfDay.Phase 0`, re-enter campfire volume | **no** `STEALTH: LIT enter` |
| 6 | Spirit + `GP_SS_Lit_SpiritTorch` | `STEALTH: LIT enter (SpiritTorch)` |
| 7 | Interact minigame/heal while lit | `STEALTH: QUICK_WINDOW` (once) |

**Cheats:** `hw.Stealth.Status` · `hw.Stealth.ForceLit 1` (spirit) → `STEALTH: LIT enter (ForceLit)` then alert/clear flow

---

## Placement script

[place_vs_mvp_ss_stealth.py](../../Content/Python/place_vs_mvp_ss_stealth.py) — idempotent labels:

- `GP_SS_Lit_Campfire` · `GP_SS_Lit_NpcTorch` · `GP_SS_Lit_SpiritTorch` · `GP_SS_Lit_BodyMundane`

Base anchor: near `GP_RS_AnimalDen` / camp path (same pattern as CD-A).

---

## Files touched (SS-A)

| Area | Files |
|------|-------|
| Types | `HomeWorldSpiritStealthTypes.h/.cpp` |
| Volume | `HomeWorldSpiritLitVolume.h/.cpp` |
| Component | `HomeWorldSpiritStealthComponent.h/.cpp` |
| Character | `HomeWorldCharacter.h/.cpp` (component + interact haste hook) |
| Cheats | `HomeWorld.cpp` — `hw.Stealth.*` |
| Placement | `Content/Python/place_vs_mvp_ss_stealth.py` |
| Docs | `Docs/25_SPIRIT_STEALTH_IMPL.md`, this handoff, `Docs/canon/DECISIONS.md` |

---

## Close checklist

- [x] DESKTOP greps `STEALTH:` per table above (deferred/accepted with Lead **`APPROVE SS-A`**)
- [x] No crouch binding added
- [x] Lead **`APPROVE SS-A`** — Docs/25 SS-A **APPROVED / CLOSED** (2026-09-21 ET)

Lead **`APPROVE SS-A`** closes the SS-A track; **SS-B** remains locked bible LATER scope.
