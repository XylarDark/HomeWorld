# Docs/23 — Combat & Dream implementation (CD)

| Field | Value |
|-------|-------|
| **Status** | **CD STRATEGY APPROVED**; **CD-A IN PROGRESS** (this PR); **CD-B** TBD only if DONE-WHEN needs a follow-on |
| **Date** | 2026-09-21 |
| **Author** | Conductor (HomeWorld) |
| **Bible** | [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md) · [COMBAT_DREAM_IMPL_PROMPT.md](COMBAT_DREAM_IMPL_PROMPT.md) |
| **Parallel track** | [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) — **CLOSED / COMPLETE** on main (Lead **`APPROVE GC-C`**, PR #126); CD-A planet stubs are independent |
| **Prefix** | **CD** — do not reuse GC / RS gate strings |

---

## Gate

Lead **`APPROVE CD STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat). Unlocks **CD-A**.

**CD-A:** Lead **`APPROVE CD-A`** in chat — **not stamped in this PR**. May close the CD track if DONE-WHEN is met on DESKTOP.

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal (CD-A NOW)

Planet-only **minigame interact stubs** + **boss placeholder volume** per locked bible: seal/banish win model; no weapons, HP trash UX, aggro, or homestead combat.

| Deliverable | Log tags |
|-------------|----------|
| Four minigame stubs | `MINIGAME:HEAL` · `MINIGAME:NURTURE` · `MINIGAME:GROW` · `MINIGAME:POSSESS` |
| Possess polish-first | Extra on-screen line + `MOVEMENT:POSSESS stub` (Docs/21 bridge) |
| Boss volume enter | `BOSS:PHASE_DAY` or `BOSS:PHASE_NIGHT` + PlayerState DayBoss/NightBoss flags |
| Optional seal interact | `BOSS:SEAL` |

---

## Code map

| Piece | Path |
|-------|------|
| Types | `Source/HomeWorld/HomeWorldCombatDreamTypes.*` |
| Minigame | `HomeWorldMinigameInteractComponent.*`, `HomeWorldMinigameStubMarker.*` |
| Boss | `HomeWorldBossPlaceholderVolume.*`, `HomeWorldBossSealComponent.*` |
| Interact chain | `HomeWorldInteractAbility`, `AHomeWorldCharacter::TryMinigameInFront` / `TryBossSealInFront` |
| Placement | [Content/Python/place_vs_mvp_cd_stubs.py](../Content/Python/place_vs_mvp_cd_stubs.py) |
| Cheats | `hw.Minigame.*`, `hw.Boss.Status` |
| Handoff | [handoffs/CD_A_STUBS.md](handoffs/CD_A_STUBS.md) |

---

## DONE-WHEN (CD-A)

- [ ] DESKTOP: `place_vs_mvp_cd_stubs.py` after Safe-Build
- [ ] PIE: interact one minigame → `MINIGAME:*`
- [ ] PIE: possess stub → `MINIGAME:POSSESS` (+ polish feedback)
- [ ] PIE: walk boss volume day → `BOSS:PHASE_DAY`; night → `BOSS:PHASE_NIGHT`
- [ ] Optional: interact seal → `BOSS:SEAL`
- [ ] Homestead unchanged (no CD actors placed by script)

**Grep:** `MINIGAME:` · `BOSS:PHASE_` · `BOSS:SEAL` in Output Log / `Saved/Logs/HomeWorld.log`

---

## CD-B (locked)

Full day+night boss siege, weak-point art, polished heal/nurture/grow kits, deep possess — **do not implement** without a new Lead track. Revisit only if CD-A DONE-WHEN is insufficient for playtest goals.
