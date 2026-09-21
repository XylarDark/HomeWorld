# CD-A — Combat/dream stubs (handoff)

| Field | Value |
|-------|-------|
| **Track** | CD-A |
| **Gate** | Lead **`APPROVE CD STRATEGY`** — **GRANTED** 2026-09-21 ET |
| **Close gate** | Lead **`APPROVE CD-A`** — **not stamped in PR** |
| **Impl doc** | [23_COMBAT_DREAM_IMPL.md](../23_COMBAT_DREAM_IMPL.md) |
| **Bible** | [COMBAT_DREAM_BIBLE.md](../COMBAT_DREAM_BIBLE.md) |

---

## Scope

- Planet / VS_MVP path only — **never homestead**
- Four minigame markers + one boss placeholder volume
- No weapons, kill win, trash AI, or second CMC

---

## DESKTOP chain

```text
.\Tools\Safe-Build.ps1
# Editor:
execute_python_script("place_vs_mvp_cd_stubs.py")
# PIE L_VS_MVP_Markers — log LogHomeWorld Log
```

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | Interact `GP_CD_Minigame_Heal` | `MINIGAME:HEAL` |
| 2 | Interact `GP_CD_Minigame_Possess` | `MINIGAME:POSSESS`, `MOVEMENT:POSSESS stub`, on-screen possess line |
| 3 | Walk into `GP_CD_BossPlaceholder` (day) | `BOSS:PHASE_DAY`; `hw.Boss.Status` → DayBoss=1 |
| 4 | `hw.TimeOfDay.Phase 2`, re-enter volume | `BOSS:PHASE_NIGHT` |
| 5 | Interact seal while flags active | `BOSS:SEAL` |

**Cheats (log-only prove):** `hw.Minigame.Heal` · `hw.Minigame.Nurture` · `hw.Minigame.Grow` · `hw.Minigame.Possess`

---

## Placement script

[place_vs_mvp_cd_stubs.py](../../Content/Python/place_vs_mvp_cd_stubs.py) — idempotent labels:

- `GP_CD_Minigame_Heal` / `_Nurture` / `_Grow` / `_Possess`
- `GP_CD_BossPlaceholder`

---

## Files touched (CD-A)

| Area | Files |
|------|-------|
| C++ | `HomeWorldCombatDreamTypes`, `HomeWorldMinigame*`, `HomeWorldBoss*`, `HomeWorldCharacter`, `HomeWorldInteractAbility`, `HomeWorldPlayerState`, `HomeWorld.cpp` |
| Python | `place_vs_mvp_cd_stubs.py` |
| Docs | `23_COMBAT_DREAM_IMPL.md`, `canon/DECISIONS.md` |

---

## Forbidden (recheck)

Homestead combat, kill win, aggro packs, full boss AI, reinventing Docs/21 as kill combat.
