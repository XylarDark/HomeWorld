# SS-B — Spirit stealth feel (handoff)

| Field | Value |
|-------|-------|
| **Status** | **IN PROGRESS** — Lead **`APPROVE SS-B STRATEGY`** granted; **SS-B not APPROVED** |
| **Track** | SS-B |
| **Gate** | Lead **`APPROVE SS-B STRATEGY`** — **GRANTED** 2026-09-21 ET |
| **Close gate** | Lead **`APPROVE SS-B`** — pending |
| **Impl doc** | [31_SPIRIT_STEALTH_FEEL.md](../31_SPIRIT_STEALTH_FEEL.md) |
| **Prior** | SS-A **CLOSED** — [25_SPIRIT_STEALTH_IMPL.md](../25_SPIRIT_STEALTH_IMPL.md) |

---

## Scope

- Planet / VS_MVP path only — **never homestead**
- Spirit form only — **no crouch**, no kill-on-detect, no shrine kidnap on alert peak
- SS-A overlap logs **unchanged**; SS-B adds feel + NPC torch carriers
- Does **not** add Mass AI patrol, full alert audio, or spirit torch craft

---

## DESKTOP chain

```text
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("place_vs_mvp_ss_b_feel.py")
# PIE L_VS_MVP_Markers — log LogHomeWorld Log
```

| Step | Action | Expected |
|------|--------|----------|
| 1 | `hw.TimeOfDay.Phase 2` (spirit) | HUD `Spirit: hidden` when unlit |
| 2 | Walk `GP_SS_Lit_Campfire` or `GP_SS_NpcTorch_CampPath` | `STEALTH: LIT enter (...)` + revealed HUD + screen edge |
| 3 | Stay ~3s in volume | Alert bar fills; `STEALTH: ALERT` |
| 4 | Walk out | `STEALTH: CLEAR`; hidden cue returns |
| 5 | Interact minigame/heal while lit | `STEALTH: QUICK_WINDOW` (once) |
| 6 | `hw.Stealth.Status` | `STEALTH:STATUS ... alert=0.xx feel=hidden\|revealed` |

**Cheats:** `hw.Stealth.Status` · `hw.Stealth.ForceLit 1`

---

## Placement

[place_vs_mvp_ss_b_feel.py](../../Content/Python/place_vs_mvp_ss_b_feel.py):

- Re-runs SS-A volume ensure via `place_vs_mvp_ss_stealth.py`
- `GP_SS_NpcTorch_CampPath` — patrol carrier (`NPC TORCH` label)
- `GP_SS_NpcTorch_DenSit` — static carrier near den path

Legacy SS-A labels unchanged: `GP_SS_Lit_*`.

---

## Files touched (SS-B)

| Area | Files |
|------|-------|
| Feel | `HomeWorldSpiritStealthComponent.h/.cpp` |
| NPC torch | `HomeWorldSpiritNpcTorchCarrier.h/.cpp` |
| HUD | `HomeWorldHUD.cpp` |
| Placement | `Content/Python/place_vs_mvp_ss_b_feel.py` |
| Docs | `Docs/31_SPIRIT_STEALTH_FEEL.md`, this handoff, `Docs/canon/DECISIONS.md` |

---

## Close checklist

- [ ] DESKTOP greps `STEALTH: LIT` / `ALERT` / `CLEAR` per table
- [ ] Hidden vs revealed readable in PIE (HUD + light)
- [ ] At least one NPC torch carrier on camp path
- [ ] Lead **`APPROVE SS-B`** — Docs/31 **APPROVED / CLOSED**
