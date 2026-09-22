# SS-B — Spirit stealth feel (handoff)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE SS-B`**, 2026-09-21 ET |
| **Host** | CLOUD + DESKTOP |
| **Track** | [Docs/31_SPIRIT_STEALTH_FEEL.md](../31_SPIRIT_STEALTH_FEEL.md) — **CLOSED / COMPLETE** |
| **Prior** | SS-A **CLOSED** — [25_SPIRIT_STEALTH_IMPL.md](../25_SPIRIT_STEALTH_IMPL.md) |
| **Gate** | Lead **`APPROVE SS-B STRATEGY`** — **GRANTED** 2026-09-21 ET |
| **Close gate** | Lead **`APPROVE SS-B`** — **GRANTED** 2026-09-21 ET (Lead pre-authorized when SS-B impl merged) |
| **Main** | `a03940a` / PR #138 |

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

**Prove note:** DESKTOP PIE greps for the table above remain **deferred/accepted** with Lead **`APPROVE SS-B`** — not stamped PASS in cloud; no invented grep evidence.

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

- [x] DESKTOP greps `STEALTH: LIT` / `ALERT` / `CLEAR` per table (**deferred/accepted** with Lead **`APPROVE SS-B`**)
- [x] Hidden vs revealed readable in PIE (HUD + light) — impl on main
- [x] At least one NPC torch carrier on camp path — placement script on main
- [x] Lead **`APPROVE SS-B`** — Docs/31 **APPROVED / CLOSED** (2026-09-21 ET)

---

## Gate

Lead **`APPROVE SS-B`** closes SS-B and the Docs/31 track. **SS-C+** scope TBD (Lead). **Do not stamp SS-B APPROVED in PR** — Lead typed gate in chat.
