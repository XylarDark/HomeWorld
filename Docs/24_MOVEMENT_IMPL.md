# Docs/24 — Movement implementation (MV)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED / COMPLETE** — Lead **`APPROVE MV-A`**, 2026-09-21 ET (MV STRATEGY + MV-A approved; MV-B+ not required for this track) |
| **Date** | 2026-09-22 |
| **Bible** | [MOVEMENT_BIBLE.md](MOVEMENT_BIBLE.md) · [MOVEMENT_IMPL_PROMPT.md](MOVEMENT_IMPL_PROMPT.md) |
| **Parallel tracks** | [23_COMBAT_DREAM_IMPL.md](23_COMBAT_DREAM_IMPL.md) **CLOSED** · [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) **CLOSED** |
| **Prefix** | **MV** — do not reuse GC / CD / RS gate strings |

---

## Gate

Lead **`APPROVE MV STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat: Lead typed **`MV-A`** → strategy unlock + MV-A work).

**MV-A:** Lead **`APPROVE MV-A`**, 2026-09-21 ET — **GRANTED** (chat; DESKTOP greps deferred/accepted). Docs/24 Movement track **CLOSED / COMPLETE**. Implementation on main (`349d3e4` / PR #130).

**Spirit stealth:** [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md) (**SS-A**) is a **separate** track — bible locked PR #131; **not** part of MV-A close.

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal (MV-A NOW)

Traversal stubs on **one CMC** per locked bible: body sprint + parkour-lite mantle/vault, FALLBACK glide preserved, spirit blink (no flight), mount speed mode after tame.

| Deliverable | Log tags |
|-------------|----------|
| Hold sprint (Shift / IA_Dodge Started/Completed) | `MOVE: form_tune` · MaxWalkSpeed bump (no separate mover) |
| Mantle / vault (jump at ledge or `hw.Move.Mantle`) | `MOVE: MANTLE` · `MOVE: VAULT` |
| Spirit blink (spirit form + R / `hw.Move.Blink`) | `MOVE: SPIRIT_BLINK` or hook line if no anchor |
| Mount / companion boost after tame | `MOVE: mount_boost on` |
| Long fall | `MOVE: soft_reset fall` |
| FALLBACK glide | existing `FALLBACK:` logs; **dusk** blocks new start |

**PLAYTEST sentence:** day walk → sprint → vault/mantle → edge glide down; night sleep → spirit blink toward shrine anchor.

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **MV STRATEGY** | Bible + impl unlock | Lead | **APPROVED** | Lead **`APPROVE MV STRATEGY`** / **`MV-A`** unlock, 2026-09-21 ET |
| **MV-A** | NOW traversal stubs | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE MV-A`**, 2026-09-21 ET — [handoffs/MV_A_TRAVERSAL.md](handoffs/MV_A_TRAVERSAL.md) |

---

## Code map

| Piece | Path |
|-------|------|
| Traversal (MV-A) | `Source/HomeWorld/HomeWorldTraversalComponent.*` |
| Character wiring | `HomeWorldCharacter.*` (Jump → mantle, sprint, spirit blink) |
| FALLBACK dusk gate | `HomeWorldFallbackGlideComponent.cpp` |
| Mount hook | `HomeWorldBeastTameComponent.cpp` → `SetMountBoostActive` |
| Cheats | `hw.Move.Mantle`, `hw.Move.Blink` in `HomeWorld.cpp` |
| Handoff | [handoffs/MV_A_TRAVERSAL.md](handoffs/MV_A_TRAVERSAL.md) |

---

## DONE-WHEN (MV-A)

- [x] DESKTOP: `.\Tools\Safe-Build.ps1` compile C++ (deferred/accepted with Lead **`APPROVE MV-A`**)
- [x] PIE day: hold Shift sprint; jump or `hw.Move.Mantle` at ledge → `MOVE: MANTLE` or `MOVE: VAULT`
- [x] PIE day: interact glide start → `FALLBACK: StartGlide`; dusk (`hw.TimeOfDay.SetPhase 1`) blocks new start
- [x] PIE night: `hw.GoToBed` or bed → spirit form; R or `hw.Move.Blink` → `MOVE: SPIRIT_BLINK` (or hook log if no anchor)
- [x] After tame near player → `MOVE: mount_boost on`; walk speed uses same CMC
- [x] Lead **`APPROVE MV-A`**, 2026-09-21 ET → track **CLOSED / COMPLETE**

**Grep:** `MOVE:` · `FALLBACK:` in Output Log / `Saved/Logs/HomeWorld.log`

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE MV STRATEGY`** (or **`MV-A`** unlock chat) | MV-A stubs — **DONE** 2026-09-21 ET |
| 1 | **`APPROVE MV-A`** | Docs/24 track complete — **DONE** 2026-09-21 ET |

```
Docs/22 Gather & Craft: CLOSED / COMPLETE — Lead APPROVE GC-C 2026-09-21 ET
Docs/23 Combat & Dream: CLOSED / COMPLETE — Lead APPROVE CD-A 2026-09-21 ET
Docs/24 Movement: CLOSED / COMPLETE — Lead APPROVE MV-A 2026-09-21 ET
```

**Next product track (separate):** **SS-A** (spirit stealth impl) or Lead-named track — TBD Lead gate.

---

## MV-B+ (locked — not NOW)

PoE-scale procgen, spirit flight, full parkour kit, swim, second CMC, free-flight upgrade of FALLBACK — **do not implement** without a new Lead track.

**Future (not MV-A):** spirit stealth + spirit torches — locked in [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md) (**SS-A** later); MV-A does not implement torch detection, stealth meters, shadow volumes, or found-out fail loops.
