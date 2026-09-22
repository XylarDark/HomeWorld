# Docs/25 — Spirit Stealth implementation (SS)

| Field | Value |
|-------|-------|
| **Status** | **SS STRATEGY APPROVED** — Lead **`APPROVE SS STRATEGY`** (via **`SS-A`** chat unlock), 2026-09-21 ET · **SS-A IN PROGRESS** |
| **Date** | 2026-09-22 |
| **Author** | Conductor (HomeWorld) |
| **Bible** | [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md) · [SPIRIT_STEALTH_IMPL_PROMPT.md](SPIRIT_STEALTH_IMPL_PROMPT.md) |
| **Parallel tracks** | [24_MOVEMENT_IMPL.md](24_MOVEMENT_IMPL.md) (**CLOSED** — MV-A separate) · [23_COMBAT_DREAM_IMPL.md](23_COMBAT_DREAM_IMPL.md) (**CLOSED** — unchanged) |
| **Prefix** | **SS** — do not reuse MV / CD gate strings |

---

## Gate

Lead **`APPROVE SS STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat: Lead typed **`SS-A`** as strategy unlock). Unlocks **SS-A** implementation.

**SS-A:** **NOT APPROVED** — close with Lead **`APPROVE SS-A`** after DESKTOP greps `STEALTH:*`.

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal (SS-A NOW)

Spirit **hidden by default** (no crouch). **Overlap volumes** on campfire / NPC torch / spirit torch reveal spirit form only. Found-out = **A2 alert** (rise in light, clear in dark) — not shrine kidnap, not kill, not homestead combat. **Body torch** = mundane only (separate kind; no spirit reveal).

| Deliverable | Log tags |
|-------------|----------|
| Lit volume enter (spirit) | `STEALTH: LIT enter` (+ source name) |
| Alert peak stub | `STEALTH: ALERT` |
| Leave light | `STEALTH: CLEAR` |
| Optional interact haste | `STEALTH: QUICK_WINDOW` (once per lit session) |
| Debug | `STEALTH:STATUS` via `hw.Stealth.Status` |

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **SS STRATEGY** | Bible + impl unlock | Lead | **APPROVED** | Lead **`APPROVE SS STRATEGY`**, 2026-09-21 ET |
| **SS-A** | Lit volumes + alert stubs | CLOUD+DESKTOP | **IN PROGRESS** | Lead **`APPROVE SS-A`** — [handoffs/SS_A_STEALTH_STUBS.md](handoffs/SS_A_STEALTH_STUBS.md) |

---

## Code map

| Piece | Path |
|-------|------|
| Types | `Source/HomeWorld/HomeWorldSpiritStealthTypes.*` |
| Lit volume | `HomeWorldSpiritLitVolume.*` |
| Alert stub | `HomeWorldSpiritStealthComponent.*` on `AHomeWorldCharacter` |
| Placement | [Content/Python/place_vs_mvp_ss_stealth.py](../Content/Python/place_vs_mvp_ss_stealth.py) |
| Cheats | `hw.Stealth.Status`, `hw.Stealth.ForceLit` |
| Handoff | [handoffs/SS_A_STEALTH_STUBS.md](handoffs/SS_A_STEALTH_STUBS.md) |

---

## DONE-WHEN (SS-A)

- [ ] DESKTOP: `place_vs_mvp_ss_stealth.py` after Safe-Build
- [ ] PIE spirit (`hw.TimeOfDay.Phase 2`): enter `GP_SS_Lit_Campfire` → `STEALTH: LIT enter (Campfire)`
- [ ] Hold in volume ~3s → `STEALTH: ALERT`
- [ ] Exit volume → `STEALTH: CLEAR`
- [ ] Body form (`hw.TimeOfDay.Phase 0`): walk same volumes — **no** `STEALTH: LIT enter`
- [ ] `GP_SS_Lit_BodyMundane` — spirit **no** reveal; body unchanged (no stealth logs)
- [ ] Optional: interact while lit → `STEALTH: QUICK_WINDOW`
- [ ] MV blink / DAYNIGHT sleep unchanged
- [ ] Lead **`APPROVE SS-A`** → thin close (Docs/25 SS-A row **APPROVED / CLOSED**)

**Grep:** `STEALTH:` in Output Log / `Saved/Logs/HomeWorld.log`

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE SS STRATEGY`** | SS-A stubs — **DONE** 2026-09-21 ET |
| 1 | **`APPROVE SS-A`** | Docs/25 SS-A complete — **pending** |

```
Docs/24 Movement: CLOSED / COMPLETE — Lead APPROVE MV-A 2026-09-21 ET
Docs/25 Spirit Stealth: SS STRATEGY APPROVED — SS-A IN PROGRESS
```

**LATER (locked bible):** NPC torch AI carry, full alert UI, spirit torch craft, detection VFX — no Lead track opened.
