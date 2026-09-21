# Docs/23 — Combat & Dream implementation (CD)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED / COMPLETE** — Lead **`APPROVE CD-A`**, 2026-09-21 ET (CD STRATEGY + CD-A approved; CD-B not required for this track) |
| **Date** | 2026-09-21 |
| **Author** | Conductor (HomeWorld) |
| **Bible** | [COMBAT_DREAM_BIBLE.md](COMBAT_DREAM_BIBLE.md) · [COMBAT_DREAM_IMPL_PROMPT.md](COMBAT_DREAM_IMPL_PROMPT.md) |
| **Parallel track** | [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) — **CLOSED / COMPLETE** on main (Lead **`APPROVE GC-C`**, PR #126); CD-A planet stubs are independent |
| **Prefix** | **CD** — do not reuse GC / RS gate strings |

---

## Gate

Lead **`APPROVE CD STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat). Unlocks **CD-A**.

**CD-A:** Lead **`APPROVE CD-A`**, 2026-09-21 ET — **GRANTED** (chat; DESKTOP greps deferred/accepted). Docs/23 Combat & Dream track **CLOSED / COMPLETE**. Implementation on main (`50faeab` / PR #128).

**Next gate:** None on CD — **MV-A** is a separate track TBD (Lead gate). **CD-B** remains locked bible scope only; no Lead track opened.

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

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **CD STRATEGY** | Bible + impl unlock | Lead | **APPROVED** | Lead **`APPROVE CD STRATEGY`**, 2026-09-21 ET |
| **CD-A** | Minigame stubs + boss phase volume | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE CD-A`**, 2026-09-21 ET — [CD_A_STUBS.md](handoffs/CD_A_STUBS.md) |

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

- [x] DESKTOP: `place_vs_mvp_cd_stubs.py` after Safe-Build (deferred/accepted with Lead **`APPROVE CD-A`**)
- [x] PIE: interact one minigame → `MINIGAME:*`
- [x] PIE: possess stub → `MINIGAME:POSSESS` (+ polish feedback)
- [x] PIE: walk boss volume day → `BOSS:PHASE_DAY`; night → `BOSS:PHASE_NIGHT`
- [x] Optional: interact seal → `BOSS:SEAL`
- [x] Homestead unchanged (no CD actors placed by script)
- [x] Lead **`APPROVE CD-A`**, 2026-09-21 ET → track **CLOSED / COMPLETE**

**Grep:** `MINIGAME:` · `BOSS:PHASE_` · `BOSS:SEAL` in Output Log / `Saved/Logs/HomeWorld.log`

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE CD STRATEGY`** | CD-A stubs — **DONE** 2026-09-21 ET |
| 1 | **`APPROVE CD-A`** | Docs/23 track complete — **DONE** 2026-09-21 ET |

```
Docs/22 Gather & Craft: CLOSED / COMPLETE — Lead APPROVE GC-C 2026-09-21 ET
Docs/23 Combat & Dream: CLOSED / COMPLETE — Lead APPROVE CD-A 2026-09-21 ET
```

**Next product track (separate):** MV-A (Movement impl) — TBD Lead gate.

---

## CD-B (locked — not on this track)

Full day+night boss siege, weak-point art, polished heal/nurture/grow kits, deep possess — **do not implement** without a new Lead track. CD-A DONE-WHEN satisfied playtest goals for NOW; CD-B is optional future scope, not required to close Docs/23.
